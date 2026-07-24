# 43_DISENO_DOMINIO_CONFIGURACION_TRIBUTARIA.md

**Versión:** 1.0  
**Estado:** 📝 En Revisión (Fase 2: Diseño del Dominio)  
**Última actualización:** 2026-07-24  
**Documento:** Diseño del Dominio de la Configuración Tributaria  

---

# 1. Modelo de Agregados y Entidades del Dominio

El dominio del contexto Configuración Tributaria se organiza bajo un único agregado principal para salvaguardar la consistencia de las reglas impositivas del negocio.

```text
                        ┌───────────────────────────────┐
                        │  ConfiguracionTributaria (AR) │
                        └──────────────┬────────────────┘
                                       │
                                       ▼ (1..N)
                        ┌───────────────────────────────┐
                        │      TasaImpuesto (Ent)       │
                        └───────────────────────────────┘
```

### Agregado Raíz (Aggregate Root)
* **`ConfiguracionTributaria` (Entidad principal):**
  * Representa una versión específica y fechada de las políticas fiscales aplicables a una empresa.
  * **Atributos:**
    * `id: UUID` (Identificador único de la configuración)
    * `company_id: UUID` (Tenant propietario)
    * `name: str` (Nombre descriptivo, ej: "Régimen General 2026", "Régimen Simplificado")
    * `is_active: bool` (Indicador de vigencia operativa actual)
    * `valid_from: datetime` (Fecha/Hora de inicio de vigencia de las tasas)
    * `valid_to: datetime | None` (Fecha/Hora de finalización de vigencia, nulo si sigue activa)
    * `calculation_type: TipoCalculoImpuesto` (Value Object: Impuesto Incluido o Adicionado)
    * `rates: list[TasaImpuesto]` (Colección de tasas impositivas válidas en esta configuración)

### Entidades Internas del Agregado
* **`TasaImpuesto` (Entidad interna):**
  * Representa un porcentaje tributario específico y su código clasificador aplicable en el mostrador.
  * **Atributos:**
    * `id: UUID`
    * `configuracion_id: UUID` (Enlace de integridad a la raíz)
    * `name: str` (Ej: "IVA Tasa General", "IVA Canasta Básica")
    * `code: str` (Identificador único de tasa en la versión, ej: `IVA_GENERAL`, `IVA_EXENTO`, `IVA_ESPECIAL`)
    * `rate_percentage: Porcentaje` (Monto porcentual, ej: 15.00%, 0.00%)

---

# 2. Objetos de Valor (Value Objects)

* **`Porcentaje`:** Representa un valor numérico decimal no negativo ($\ge 0$) que determina la carga impositiva.
* **`TipoCalculoImpuesto` (Enum):**
  * `INCLUIDO`: El precio de venta en catálogo ya contiene el impuesto.
  * `ADICIONADO`: El impuesto se calcula y se suma sobre el precio neto de catálogo.
* **`CategoriaTributariaProducto` (Enum):**
  * Define la etiqueta de clasificación impositiva que un `Producto` posee en su catálogo.
  * Valores válidos: `EXENTO`, `TASA_GENERAL`, `TASA_ESPECIAL`.

---

# 3. Invariantes del Dominio (Reglas Indestructibles)

* **Invariante 1: Exclusividad de Vigencia Temporal (No Solapamiento):**
  * No puede existir más de una `ConfiguracionTributaria` activa (`is_active = True`) simultáneamente para la misma empresa (`company_id`).
* **Invariante 2: Inmutabilidad de Versiones Expiradas:**
  * Si una `ConfiguracionTributaria` posee una fecha `valid_to` en el pasado, es completamente inmutable. No se permite alterar sus tasas ni tipo de cálculo, garantizando la integridad de auditorías históricas.
* **Invariante 3: Tasas Impositivas No Negativas:**
  * El `rate_percentage` de cualquier `TasaImpuesto` debe ser mayor o igual a cero ($\ge 0.00$).
* **Invariante 4: Unicidad de Códigos de Tasa:**
  * Los códigos de tasa (`code`) dentro de la misma `ConfiguracionTributaria` deben ser únicos.

---

# 4. Eventos de Dominio

* **`ConfiguracionTributariaCreada`:** Emite `configuracion_id`, `company_id` y `valid_from`.
* **`ConfiguracionTributariaActivada`:** Notifica que una versión impositiva ha entrado en vigencia operativa activa, forzando la devaluación de la versión previa.
* **`ConfiguracionTributariaDesactivada`:** Emite la desactivación e inactividad de una regla fiscal.

---

# 5. Análisis del Nuevo Concepto: Motor Tributario (MotorTributario)

Tras contrastar los principios de DDD y la necesidad del negocio, determinamos que el **Motor Tributario** corresponde a un **Servicio de Dominio (Domain Service)**.

### Justificación:
1. **Operación sin Estado (Stateless):** El motor no almacena registros en base de datos ni posee un ciclo de vida independiente. Recibe datos, ejecuta cálculos matemáticos puros y devuelve desgloses.
2. **Coordinación Multiorigen:** La regla para calcular el desglose impositivo de una Venta involucra interactuar con dos agregados independientes: la `ConfiguracionTributaria` activa (Empresa) y el `Producto` (con su `CategoriaTributariaProducto`).
3. **No pertenencia natural:** Colocar el algoritmo de cálculo de impuestos en el agregado `Venta` acoplaría la venta a la lógica fiscal cambiante. Colocarlo en `ConfiguracionTributaria` obligaría a este agregado a conocer el detalle de los ítems y precios de la venta.
4. El **Domain Service** encapsula limpiamente esta regla de cálculo pura, permitiendo que tanto Ventas como Compras la utilicen sin acoplamiento.

---

# 6. Integración Conceptual Desacoplada

La interacción entre módulos se instrumenta sin acoplamiento de persistencia mediante identificadores y Value Objects:

```text
                   ┌──────────────────────────────────────┐
                   │        Ventas (Caso de Uso)          │
                   └──────────────────┬───────────────────┘
                                      │ (Consulta tasas y solicita cálculo)
                                      ▼
┌──────────────────┐       ┌──────────────────────┐       ┌──────────────────┐
│   Configuración  │◄──────┤    MotorTributario   ├──────►│     Catálogo     │
│  Tributaria (AR) │       │   (Domain Service)   │       │  Productos (AR)  │
└──────────────────┘       └──────────────────────┘       └──────────────────┘
```

* **Empresa $\rightarrow$ Configuración Tributaria:** La empresa almacena su RUC/RTN y hace referencia al ID de la `ConfiguracionTributaria` activa.
* **Producto $\rightarrow$ Configuración Tributaria:** El producto en catálogo no almacena números de porcentaje (ej: 15%). Solo almacena el Value Object `CategoriaTributariaProducto` (ej: `TASA_GENERAL`).
* **Venta/Compra $\rightarrow$ Configuración Tributaria:**
  * Al confirmarse una venta, el caso de uso recupera la `ConfiguracionTributaria` activa del tenant.
  * Llama al `MotorTributario` (Domain Service) pasando los ítems de venta.
  * El motor evalúa la clasificación de cada ítem, busca la tasa correspondiente en la configuración (ej: `IVA_GENERAL` $\rightarrow$ 15%) y calcula el desglose.
  * La venta guarda el desglose calculado como un **snapshot inmutable** dentro del agregado `Venta`.

---

# 7. Modelado del Resultado del Motor: DesgloseImpuesto (Value Object)

### Análisis y Justificación del Concepto

1. **¿Representa un concepto del negocio?**  
   **Sí.** Representa el **Desglose Tributario (DesgloseImpuesto)**. Es el desglose financiero e impositivo oficial que certifica ante el Estado cuánto impuesto se cobró (Ventas) o pagó (Compras) por cada tipo impositivo en una transacción.
2. **¿Necesita identidad propia?**  
   **No.** No posee ciclo de vida independiente ni un identificador único persistente por fuera del documento transaccional que lo contiene. Dos desgloses con idénticos valores son plenamente equivalentes.
3. **¿Cambia después de confirmarse la transacción?**  
   **No.** Es estrictamente **inmutable**. Representa un hecho histórico congelado en el tiempo.
4. **¿Debe formar parte del historial inmutable de Venta/Compra?**  
   **Sí, obligatoriamente.** Es la base legal y fiscal para auditorías y declaraciones ante el ente tributario.
5. **¿Conviene modelarlo explícitamente como un Value Object?**  
   **Sí.** Por sus características de inmutabilidad, falta de identidad y dependencia de la transacción, es idóneo modelarlo como un **Value Object (Objeto de Valor)**.

---

### Composición del Value Object: `DesgloseImpuesto`

* **`rate_code` (str):** El código identificador de la tasa aplicada (ej: `IVA_GENERAL`, `IVA_ESPECIAL`).
* **`rate_percentage` (Porcentaje):** El valor de la tasa activa al momento del cálculo (ej: 15.00%).
* **`net_amount` (Decimal):** El subtotal neto del artículo o ítems que sufrieron la base gravada.
* **`tax_amount` (Decimal):** El importe monetario del impuesto calculado resultante.

---

### Beneficios de no reutilizar directamente el Agregado `ConfiguracionTributaria`

* **Aislamiento y Autonomía de Datos:** Reutilizar o enlazar directamente el agregado `ConfiguracionTributaria` en el registro histórico de la venta violaría los límites de Bounded Context. Si la configuración tributaria se modificara, desactivara o purgara, el historial de ventas del pasado podría corromperse o perder sus referencias físicas.
* **Fortalecimiento de la Inmutabilidad Histórica:** Al persistir el `DesgloseImpuesto` como una copia física plana (snapshot) dentro del agregado `Venta` o `Compra`, la factura se vuelve autocontenida. Se puede imprimir, auditar y declarar en el futuro sin realizar un `JOIN` a las tablas del módulo fiscal, asegurando inmunidad absoluta ante futuros cambios impositivos de la empresa.
