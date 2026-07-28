# 44_DISENO_ARQUITECTONICO_CONFIGURACION_TRIBUTARIA.md

**Versión:** 1.0  
**Estado:** Listo para Auditoría Arquitectónica  
**Última actualización:** 2026-07-24  
**Documento:** Diseño Arquitectónico del Módulo de Configuración Tributaria  

---

# Objetivo

Definir de forma rigurosa y exhaustiva la integración del dominio de la **Configuración Tributaria** dentro de la arquitectura modular de CajaFácil, garantizando el cumplimiento de **DDD**, **Clean Architecture** y las directrices de consistencia **Offline-First**, transaccionalidad e inmutabilidad histórica.

---

# 1. Organización del Módulo

El módulo se implementará de forma aislada y homóloga en el backend bajo la carpeta `backend/app/modules/tributacion/` (Tributación):

```text
backend/app/modules/tributacion/
├── domain/                      # Capa de Dominio (Pureza de Negocio)
│   ├── entities/                # ConfiguracionTributaria, TasaImpuesto, DesgloseImpuesto
│   ├── exceptions/              # Excepciones de negocio impositivas
│   ├── events/                  # ConfiguracionTributariaCreada, etc.
│   ├── services/                # MotorTributario (Servicio de Dominio)
│   └── repositories/            # ConfiguracionTributariaRepository (Interfaz)
├── application/                 # Capa de Aplicación (Casos de Uso)
│   ├── __init__.py
│   └── use_cases/               # CrearConfiguracion, ActivarConfiguracion, etc.
├── data/                        # Capa de Datos (SQLAlchemy e Infraestructura)
│   ├── models.py                # Tablas físicas de configuraciones y tasas
│   ├── mappers/                 # Traductores bidireccionales
│   └── repositories/            # ConfiguracionTributariaRepositoryImpl
└── presentation/                # Capa de Presentación (Enrutadores y DTOs)
    ├── routers/                 # Endpoints de administración fiscal
    ├── dto/                     # Pydantic schemas (Request/Response)
    └── dependencies/            # Inyección de dependencias
```

---

# 2. Responsabilidades por Capa

### Capa de Dominio (`domain/`)
* **Aggregate Root:** `ConfiguracionTributaria`.
* **Entidades Internas:** `TasaImpuesto`.
* **Value Objects:** `DesgloseImpuesto` (Calculado por el motor), `Porcentaje`, `TipoCalculoImpuesto`.
* **Servicio de Dominio (`MotorTributario`):** Algoritmo stateless que realiza el cálculo de impuestos cruzando precios y clasificaciones de productos.
* **Interfaz de Repositorio:** Contrato abstracto `ConfiguracionTributariaRepository`.

### Capa de Aplicación (`application/`)
* Orquesta casos de uso de administración fiscal (crear y activar configuraciones).
* Gobierna límites transaccionales mediante el patrón Unit of Work.
* Ofrece puertos de consulta y lectura para otros módulos (Ventas, Compras) sin acoplar persistencia.

### Capa de Datos (`data/`)
* Define los esquemas físicos relacionales para `configuracion_tributaria` y `tasa_impuesto`.
* Implementa la traducción bidireccional a entidades del dominio a través de un Mapper.
* Implementa `ConfiguracionTributariaRepositoryImpl` realizando flushes y delegando los commits a la aplicación.

### Capa de Presentación (`presentation/`)
* Expone endpoints para la creación, consulta y activación de políticas fiscales.
* Valida sintácticamente las peticiones utilizando esquemas Pydantic.

---

# 3. Contratos de Repositorio (Repository Port)

```python
from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional
from app.modules.tributacion.domain.entities.configuracion import ConfiguracionTributaria

class ConfiguracionTributariaRepository(ABC):
    @abstractmethod
    def save(self, config: ConfiguracionTributaria) -> ConfiguracionTributaria:
        """
        Persiste una configuración y sus tasas en base de datos.
        No ejecuta commit.
        """
        pass

    @abstractmethod
    def get_by_id(self, config_id: UUID) -> Optional[ConfiguracionTributaria]:
        """
        Consulta una versión tributaria por su identificador.
        """
        pass

    @abstractmethod
    def get_active_by_company(self, company_id: UUID) -> Optional[ConfiguracionTributaria]:
        """
        Consulta la versión activa vigente para una empresa.
        """
        pass

    @abstractmethod
    def search(self, company_id: UUID, filters: dict) -> List[ConfiguracionTributaria]:
        """
        Listado histórico de versiones impositivas.
        """
        pass
```

---

# 4. Flujo del Servicio de Dominio: `MotorTributario`

El cálculo de desgloses de impuestos se centraliza en el Domain Service de forma desacoplada:

```text
       Capa de Aplicación de Ventas (ConfirmarVenta)
     ┌────────────────────────────────────────────────┐
     │ 1. Obtener ConfiguracionTributaria activa      │
     │ 2. Llamar MotorTributario.calcular(items, conf)│
     └───────────────────────┬────────────────────────┘
                             │
                             ▼ (Cálculo Stateless)
             ┌───────────────────────────────┐
             │       MotorTributario         │
             └───────────────┬───────────────┘
                             │
                             ▼ (Retorna)
             ┌───────────────────────────────┐
             │    list[DesgloseImpuesto]     │
             └───────────────────────────────┘
```

1. **Entradas del cálculo:**
   * Lista de ítems a cotizar: `list[ItemCotizacion]` (contiene identificador, precio neto y `CategoriaTributariaProducto`).
   * Instancia de `ConfiguracionTributaria` activa.
2. **Algoritmo:**
   * Itera sobre cada ítem.
   * Busca la `TasaImpuesto` correspondiente en la configuración utilizando el código que vincula la clasificación del producto.
   * Aplica la fórmula según el `calculation_type` (Incluido o Adicionado):
     * *Adicionado:*
       $$\text{Impuesto} = \text{Precio Neto} \times \text{Tasa}$$
     * *Incluido:*
       $$\text{Impuesto} = \text{Precio Final} - \left(\frac{\text{Precio Final}}{1 + \text{Tasa}}\right)$$
   * Acumula y agrupa los subtotales e impuestos calculados bajo el Value Object `DesgloseImpuesto`.
3. **Salida:** Retorna `list[DesgloseImpuesto]`.

---

# 5. Integración entre Bounded Contexts sin Acoplamiento

Para evitar acoplar la base de datos de Ventas/Compras con la de Tributación:

1. **Ventas define un Puerto de Lectura (Lookup Interface):**
   * `TaxConfigurationLookup`: Interfaz en la capa de aplicación de Ventas.
2. **Implementación del Puerto:**
   * La infraestructura de Ventas implementa este lookup consultando síncronamente al módulo de Tributación (en memoria o mediante servicio).
3. **Persistencia Transaccional Independiente:**
   * Una vez calculado el `list[DesgloseImpuesto]` por el `MotorTributario`, Ventas serializa y persiste este Value Object directamente en sus propias tablas (`venta_tax_breakdown` o similar), de forma plana.
   * La base de datos de Ventas almacena su propia copia física (snapshot) inmune a que en el futuro la configuración tributaria sea alterada o desactivada.

---

# 6. Estrategia Offline-First y Sincronización

* **Ejecución Local Síncrona:** Dado que SQLite local en la terminal posee una réplica de la `ConfiguracionTributaria` activa y las clasificaciones de productos, el POS ejecuta el `MotorTributario` síncronamente de forma local para facturar offline al instante.
* **Gobernanza Centralizada (Solo Lectura en Cliente):**
  * La creación y devaluación de configuraciones tributarias se realiza en la nube (servidor central).
  * Los terminales locales descargan las versiones mediante sincronización unidireccional y las marcan como solo lectura local. Esto anula la posibilidad de manipulación local fraudulenta de tasas impositivas.
* **Consistencia Histórica WAL:** SQLite garantiza la atomicidad de la grabación de la venta junto a su `DesgloseImpuesto` en la base de datos del cliente local.
