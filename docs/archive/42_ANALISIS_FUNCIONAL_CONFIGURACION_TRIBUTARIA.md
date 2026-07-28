# 42_ANALISIS_FUNCIONAL_CONFIGURACION_TRIBUTARIA.md

**Versión:** 1.0  
**Estado:** 📝 En Revisión (Fase 1: Análisis Funcional)  
**Última actualización:** 2026-07-24  
**Documento:** Análisis Funcional de la Configuración Tributaria  

---

# 1. ¿Qué problema del negocio resuelve la Configuración Tributaria?

La **Configuración Tributaria** en CajaFácil resuelve los siguientes problemas de negocio:
* **Rigidez operativa para pequeños comercios:** Evita obligar a microempresas (bajo regímenes de monotributo o exención completa) a configurar esquemas impositivos complejos que ralentizan el checkout.
* **Inconsistencia y alteración contable histórica:** Resuelve el riesgo de que las facturas del pasado se recalculen o muestren valores erróneos cuando el Estado cambie una tasa tributaria (ej: incremento del ISV/IVA).
* **Bloqueo ante cambios legislativos:** Permite al negocio responder ágilmente a reformas tributarias, variaciones en los porcentajes de impuestos o categorización de la canasta básica sin requerir modificaciones en el código de la aplicación.
* **Incompatibilidad multi-régimen:** Facilita la operación de empresas con sucursales ubicadas en distintas jurisdicciones geográficas con normativas tributarias dispares.

---

# 2. ¿Por qué este concepto debe existir dentro de CajaFácil?

Como sistema de punto de venta (POS) y ERP enfocado en acompañar el crecimiento a largo plazo del comerciante, CajaFácil debe instrumentar el cumplimiento de las leyes estatales. Los impuestos no son detalles cosméticos en una factura; determinan el precio final al consumidor, el costo neto de adquisición de inventario, las ganancias reales del negocio y la validez legal ante las auditorías del Estado.

---

# 3. ¿Quién es el propietario de esta información?

El propietario absoluto de la Configuración Tributaria es la **Empresa (Company)**. Las obligaciones y tasas fiscales son dictadas por la naturaleza jurídica de la empresa, su régimen de tributación nacional y su ubicación física. No pertenecen de forma directa a un cliente, a un cajero ni a un terminal.

---

# 4. ¿La Configuración Tributaria pertenece a Empresa o a Ventas? Justificación.

Pertenece al contexto de la **Empresa** (dentro de su configuración de gobernanza global).
* **Justificación:**
  1. **Alcance Multimodular:** Las tasas e impuestos impactan tanto en la facturación de **Ventas** (recaudación) como en el ingreso de mercadería en **Compras** (crédito fiscal y costo neto del artículo). Si el concepto se confinara dentro de Ventas, el módulo de Compras o de Reportes dependería directamente de Ventas, violando el principio de bajo acoplamiento.
  2. **Ciclo de Vida:** Las ventas son transacciones dinámicas e inmutables que ocurren a cada minuto. Las configuraciones tributarias son políticas corporativas estables determinadas por periodos fiscales de mediano o largo plazo.

---

# 5. ¿Puede una empresa cambiar su configuración tributaria durante su vida?

**Sí.** Los comercios escalan: pasan de régimen simplificado a régimen general a medida que sus ventas anuales superan los límites del monotributo. Asimismo, el Estado puede promulgar reformas que alteren las tasas, eliminen incentivos o agreguen impuestos suntuarios especiales.

---

# 6. ¿Qué ocurre con las ventas históricas cuando cambia la configuración tributaria?

**Permanecen inalterables en su totalidad.**
* Las ventas consolidadas en el pasado representan hechos históricos consolidados.
* Si una transacción fue cobrada con un impuesto del 15% en el año 2024, el sistema debe garantizar que al consultar, reimprimir o auditar esa factura en el 2026, se refleje exactamente el 15% original, aun cuando la tasa vigente sea del 18% o la empresa se haya vuelto exenta.

---

# 7. ¿Debe existir historial de configuraciones tributarias? ¿Por qué?

**Sí.** Debe existir un histórico completo de versiones tributarias.
* **Justificación:**
  * **Conciliaciones retroactivas:** La empresa debe poder auditar, reconstruir y declarar balances correspondientes a periodos pasados aplicando las leyes vigentes en ese instante exacto del tiempo.
  * **Trazabilidad de cambios:** Permite saber con precisión qué configuración aplicó en qué rangos de fechas.

---

# 8. ¿Debe existir únicamente una configuración tributaria activa por empresa?

**Sí.** A nivel de vigencia en un instante $T$ de tiempo. Una empresa no puede cobrar y no cobrar impuestos simultáneamente para la misma transacción. No obstante, el sistema debe permitir preparar configuraciones tributarias futuras (ej: programar una nueva tasa para el inicio del mes) o mantener las inactivas del pasado.

---

# 9. Tipología de Empresas y Variabilidad Tributaria

Diferentes giros comerciales tienen necesidades tributarias diversas:
* **Pulperías y Tiendas de Conveniencia Pequeñas:** Requieren omitir cálculos de impuestos (operan con importes netos directos) para priorizar la velocidad de cobro.
* **Farmacias:** Operan con productos exentos (medicinas de canasta básica impositiva) y productos gravados tasa general (artículos de aseo).
* **Ferreterías y Supermercados:** Operan bajo régimen general con múltiples tasas (exento 0%, tasa general 15%, y tasas suntuarias o especiales para licores y tabaco).
* **Restaurantes:** Suelen incorporar impuestos sobre ventas más recargos por concepto de servicio o propina reglamentaria.

CajaFácil debe resolver esta diversidad mediante parámetros lógicos flexibles y evitar reglas rígidas cableadas en el código.

---

# 10. Tipos de Configuraciones Tributarias a Soportar

* **Sin Impuestos (Exención Completa / Monotributo):** La tasa efectiva es cero. Las ventas no realizan desgloses fiscales.
* **Tasa Única General (IVA/ISV):** Una tasa estándar aplicable por igual a toda la mercadería.
* **Multitasa por Categorías:** Clasificaciones por producto (Exento, Gravado Tasa General, Gravado Tasa Especial).
* **Impuesto Incluido en el Precio:**
  $$\text{Precio Neto} = \frac{\text{Precio Final}}{1 + \text{Tasa}}$$
* **Impuesto Adicionado al Precio:**
  $$\text{Precio Final} = \text{Precio Neto} \times (1 + \text{Tasa})$$

---

# 11. Comportamiento en la Transición a Régimen Gravado

Cuando una empresa pasa de no cobrar impuestos a cobrarlos:
1. El administrador registra la nueva versión tributaria con su fecha de inicio de vigencia.
2. A partir de esa fecha, los productos de catálogo deben asociarse a sus tasas impositivas correspondientes.
3. El motor de checkout de Ventas y el ingreso de Compras computan y desglosan impuestos.
4. Los reportes separan limpiamente los ingresos históricos exentos de los gravados.

---

# 12. Flexibilidad ante Cambios de Leyes Estatales

CajaFácil evita cablear tasas directas en el código. La tasa impositiva se resuelve consultando el estado tributario del producto vinculado a la configuración de la empresa vigente a la fecha de la transacción.

---

# 13. Matriz de Módulos Afectados por la Configuración

* **Empresa:** Almacena el régimen fiscal activo, datos fiscales (RUC, RTN, etc.) y la vigencia.
* **Productos:** Asocia a cada artículo su clasificación fiscal (Exento, Gravado Tasa A, etc.).
* **Compras:** Calcula el impuesto pagado para deducir costos netos y registrar crédito fiscal.
* **Ventas:** Ejecuta el desglose de IVA/ISV en el subtotal en tiempo real durante el checkout.
* **Reportes:** Consolida reportes fiscales de ventas exentas, gravadas e impuestos devengados.
* **Facturación Electrónica (Futuro):** Requerirá el desglose exacto en formatos XML/JSON oficiales según el ente fiscal del país.

---

# 14. Módulos Desacoplados de la Lógica Tributaria

* **Inventario:** Solo controla existencias y movimientos físicos en unidades. Su labor es ajena a si el producto está gravado con 15% o 18%.
* **Caja (Cash):** Custodia y registra flujos físicos de dinero total recaudado en el mostrador. No divide el billete de pago por concepto de impuestos.
* **Clientes / Proveedores:** Gestionan datos de contacto, saldos de cuenta corriente y plazos, independientemente del régimen.

---

# 15. Información Requerida para Auditoría Histórica

Cada factura (Venta o Compra) confirmada debe guardar un **snapshot inmutable de la regla tributaria aplicada**:
* Tasa porcentual utilizada.
* Subtotal neto calculado.
* Impuesto exacto recaudado.
* Identificación de la versión de la configuración tributaria activa en ese momento.

Esto previene discrepancias si en el futuro se edita la ficha del producto o la tasa general de la empresa.

---

# 16. Riesgos de un Diseño Deficiente

* **Inconsistencia Fiscal:** Modificaciones que recalculen retroactivamente importes facturados en el pasado, exponiendo a la empresa a multas graves por evasión o declaraciones inconsistentes.
* **Pérdida de Velocidad de Venta:** Obligar a comercios de barrio a flujos de configuración tributaria complejos que entorpecen la operación del POS.
* **Falta de Portabilidad (SaaS):** Incapacidad de escalar el software a múltiples mercados internacionales al cablear las tasas de un único país.

---

# 17. Beneficios del Desacoplamiento de la Configuración Tributaria

* **Independencia en Ventas:** El checkout permanece simple y rápido. El motor de impuestos calcula el desglose de forma desacoplada.
* **Coherencia Compras-Ventas:** Un único punto de gobernanza tributaria regula la venta (impuesto recaudado) y la compra (crédito fiscal).
* **Mantenimiento Simplificado:** Reformas fiscales se configuran de manera administrativa sin reescribir código core.

---

# 18. Habilitaciones Futuras de la Arquitectura

* Integración modular con servicios de facturación electrónica nacionales (SAR, DIAN, SAT, etc.).
* Gestión multirégimen por sucursales.
* Configuración de exenciones temporales o días sin IVA.

---

# 19. Configuración Tributaria de la Empresa vs. Clasificación Tributaria de un Producto

### ¿Representan el mismo concepto del negocio o responsabilidades diferentes?

Representan **conceptos y responsabilidades del negocio completamente independientes y desacopladas**, aunque actúan en estrecha colaboración para determinar la carga fiscal final de una transacción.

---

### Justificación desde la Perspectiva del Negocio (Escenarios de Análisis)

#### A. Una empresa cuyo régimen tributario cambia con el tiempo
* **El escenario:** Una pequeña *pulpería* inicia operaciones bajo el Régimen Simplificado (exento de cobrar impuestos). Años más tarde, debido al crecimiento de sus ventas, el Estado la obliga a transicionar al Régimen General (comenzando a cobrar impuestos).
* **Análisis de responsabilidades:** 
  * Si la tasa impositiva estuviera directamente en el producto, la pulpería tendría que editar individualmente todos los productos de su catálogo para cambiar la tasa de "0%" a "15%".
  * Al estar separados, el catálogo de productos ya posee la clasificación intrínseca del producto (ej: soda es "Tasa General", leche es "Exento"). Al cambiar el régimen de la Empresa, la configuración de la Empresa activa el porcentaje del 15% para el tipo "Tasa General". El catálogo de productos permanece intacto; el sistema simplemente aplica la nueva regla tributaria de la Empresa a la clasificación ya existente de los productos.

#### B. Venta simultánea de productos gravados y exentos (Farmacias y Supermercados)
* **El escenario:** Un *supermercado* o una *farmacia* vende leche (exenta por ley de canasta básica) y una botella de vino (gravada con tasa especial de licores).
* **Análisis de responsabilidades:**
  * El **Producto** es propietario de su **naturaleza impositiva** (Clasificación): declara si es un bien de consumo exento por ley o si es estándar.
  * La **Empresa** es propietaria de la **política de cálculo y porcentajes**: define cuánto equivale el impuesto para la categoría "Tasa General" (ej: 15%) y "Tasa Especial" (ej: 18%), y si el cobro se realiza adicionado o incluido.

#### C. Impuesto Incluido vs. Adicionado al precio (Ferreterías y Tiendas de Conveniencia)
* **El escenario:** Una ferretería vende un martillo a $100 netos. En un país se vende adicionando el impuesto (total cobrado $115), y en otro país o por política del comercio se vende con el impuesto incluido (total cobrado $100, con $86.96 de subtotal y $13.04 de impuesto).
* **Análisis de responsabilidades:**
  * El **Producto** tiene el mismo precio y código en ambos escenarios.
  * La **Empresa** posee la configuración que determina la fórmula matemática de desglose (adicionado o incluido).

---

### Responsabilidades Específicas de cada Concepto

* **Responsabilidad de la Empresa (Configuración Tributaria):**
  * Determina **CÓMO** y **CUÁNDO** se calculan los impuestos (Régimen, fórmulas de cálculo, vigencia de tasas).
  * Gobierna el porcentaje numérico activo para cada categoría (ej: General = 15%, Exento = 0%, Licores = 18%).
* **Responsabilidad del Producto (Clasificación Tributaria):**
  * Determina **QUÉ** categoría fiscal le corresponde por su naturaleza intrínseca (General, Exento, Especial).
  * Permanece inalterable ante cambios de régimen de la empresa o variaciones en los porcentajes de impuestos decretados por el Estado.

---

### Beneficios del Desacoplamiento para la Arquitectura y Evolución de CajaFácil

1. **Aislamiento SaaS y Multi-Tenant:** Permite que múltiples empresas (tenants) compartan o utilicen un catálogo maestro de productos idénticos (con sus clasificaciones de ley) pero calculen los impuestos de forma totalmente diferenciada según su propia configuración fiscal.
2. **Independencia ante Cambios del Estado:** Si el gobierno aumenta la tasa del 15% al 16%, el administrador del sistema actualiza un único registro en la Configuración Tributaria de la Empresa. Ningún producto en el catálogo necesita ser modificado.
3. **Optimización del POS Offline:** El POS en el mostrador recupera el catálogo y la regla tributaria por separado, aplicando los cálculos de forma instantánea según la versión fiscal activa, reduciendo la latencia de facturación.

