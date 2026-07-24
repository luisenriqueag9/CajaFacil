# 48_ANALISIS_FUNCIONAL_GESTION_EXISTENCIAS.md

**Versión:** 1.1  
**Estado:** 📜 Aprobado e Inmutable (Sprint 19)  
**Última actualización:** 2026-07-24  
**Documento:** Análisis Funcional de la Gestión de Existencias  

---

# 1. ¿Qué problema resuelve la Gestión de Existencias?

El módulo de **Gestión de Existencias** resuelve los siguientes problemas del negocio:
* **Sobreventa de mercancía (Venta de humo):** Evita que el cajero cobre artículos en el mostrador que no se encuentran físicamente en el local, previniendo devoluciones molestas y frustración en el comprador.
* **Pérdida de ventas por falsos agotados:** Impide que el sistema indique incorrectamente que no hay stock de un producto cuando sí hay unidades guardadas en bodega.
* **Fuga silenciosa de inventario (Robo hormiga):** Permite detectar discrepancias inmediatas entre lo que el sistema proyecta y lo que el conteo físico revela, identificando pérdidas de mercadería a tiempo.
* **Lentitud y cuellos de botella en el mostrador:** Resuelve la devaluación del tiempo del cliente en la facturación del POS al evitar que el sistema realice cálculos complejos sobre todo el historial antes de autorizar el cobro de cada producto.

---

# 2. Inviabilidad de Consultar el Kardex para el Stock Actual

El **Kardex** es el historial cronológico e inmutable de todos los movimientos de inventario. Consultarlo en tiempo real para conocer la existencia disponible es el mecanismo inadecuado por las siguientes razones:
* **Problema de Escala:** Un comercio registra miles de entradas y salidas de mercancía al mes. Para saber el stock de 50 productos en un ticket de venta, el sistema tendría que buscar, filtrar y sumar algebraicamente millones de filas de Kardex.
* **Latencia Inaceptable en Mostrador:** En un punto de venta (POS) offline, los recursos de hardware son limitados. Consultar el Kardex completo incrementa la latencia del checkout. **La consulta de existencias debe ser prácticamente inmediata para no ralentizar ni afectar el proceso de venta en el mostrador.**
* **Bloqueos Concurrentes:** Múltiples cajas vendiendo al mismo tiempo colapsarían el motor de base de datos local al competir por leer de forma repetida las mismas tablas históricas.

---

# 3. Diferencia entre Historial de Movimientos y Existencia Disponible

* **Historial de Movimientos (Kardex):**
  * Es una **bitácora cronológica inmutable**. Registra el detalle minucioso de cada transacción del pasado (ej: "Compra #123 de 10 unidades el 20 de mayo", "Venta #456 de 2 unidades el 21 de mayo").
  * Su responsabilidad es la **auditoría, trazabilidad y justificación legal** de los flujos físicos.
* **Existencia Disponible (Stock Actual):**
  * Es una **proyección de estado instantáneo**. Representa el saldo neto resultante disponible en el presente inmediato (un simple número decimal, ej: "8 unidades en estantería").
  * Su responsabilidad es la **toma de decisiones operativas inmediatas** (habilitar/denegar cobros en mostrador o emitir alertas de reposición). Es transitorio y mutable ante nuevos movimientos.

---

# 4. Propietario de la Existencia de un Producto

El propietario exclusivo de la existencia es el contexto de **Inventario**.
* Ventas altera el stock (lo disminuye) y Compras lo incrementa, pero solo Inventario custodia el saldo de unidades físicas y gobierna las reglas de ingreso, salida y mermas físicas de los almacenes del tenant.

---

# 5. Momentos Obligatorios de Actualización de Existencia

El stock disponible debe actualizarse de forma **inmediata** en el momento en que se confirma el hecho comercial que altera la realidad física:
* Al registrarse la confirmación de una Compra (entrada inmediata).
* Al procesarse el checkout final de una Venta en mostrador (salida inmediata).
* Al registrarse y firmarse un Ajuste de inventario físico (nivelación inmediata).
* Al registrarse una Merma autorizada por daño, robo o vencimiento (salida inmediata).

---

# 6. Operaciones que Modifican la Existencia

* **Compras (Entrada):** Incrementa el stock disponible tras el ingreso de mercancía del proveedor.
* **Ventas (Salida):** Disminuye el stock disponible al entregar el artículo al consumidor final.
* **Ajustes de Conteo (Entrada o Salida Correctiva):** Corrige el saldo disponible para alinear la verdad del sistema con la auditoría del conteo físico del almacén.
* **Mermas (Salida):** Disminuye el stock por descarte de productos defectuosos, vencidos o robados.
* **Devoluciones de Clientes (Entrada):** Incrementa el stock si el artículo devuelto está en condiciones aptas para venta.
* **Devoluciones a Proveedores (Salida):** Disminuye el stock al retornar mercancía defectuosa al distribuidor.

---

# 7. Información Requerida por Rol de Negocio

### A. Para el Cajero (Punto de Venta)
* **Disponibilidad Inmediata:** Visualizar de forma inmediata si hay stock del producto al pasarlo por el lector.
* **Alertas de Stock Mínimo:** Aviso visual de que quedan pocas unidades en estantería para solicitar reposición.
* **Habilitación de Stock Negativo:** Saber si el sistema permite vender el producto aun sin existencia física registrada.

### B. Para el Administrador/Dueño (ERP Central)
* **Kardex Histórico:** Detalle de auditoría de los movimientos que explican el stock actual.
* **Alertas de Quiebre de Stock:** Listado de productos agotados o próximos a agotarse.
* **Reporte de Mermas y Ajustes:** Detalle de pérdidas de stock valorizadas en costo monetario.

---

# 8. Riesgos ante Discrepancias de Stock

* **Inconsistencias y pérdidas financieras:** Al no saber cuántas unidades físicas hay, se incrementan los robos hormiga y las mermas no detectadas.
* **Quiebre de stock no atendido:** Pérdida de ventas de artículos de alta rotación al no generarse la orden de compra a tiempo.
* **Pérdida de clientes:** Frustración de compradores por sobreventa o demoras en entregas debido a datos de stock erróneos.

---

# 9. Comportamiento en Modo Offline

* El terminal local POS opera consultando y mutando la **existencia disponible almacenada localmente en la base de datos SQLite**.
* Las ventas realizadas sin internet descuentan el stock local inmediatamente de forma transaccional. Esto garantiza que si se venden las últimas unidades offline, el POS bloquee la facturación de unidades inexistentes de inmediato en ese terminal.

---

# 10. Sincronización al Recuperar Conexión

1. Los movimientos de inventario offline se suben de forma ordenada al servidor central (nube).
2. El servidor procesa cronológicamente los movimientos recibidos y recalcula el saldo maestro de existencias.
3. Si múltiples terminales alteraron el stock del mismo producto, el servidor central consolida los balances netos.
4. El saldo maestro del servidor se descarga de vuelta a los terminales locales, sobrescribiendo el stock local y garantizando la aliniación de datos.

---

# 11. Existencia Física vs. Disponibilidad Comercial (Análisis Estratégico)

A nivel conceptual y en la planeación a largo plazo de un ERP, la **Existencia Física** y la **Disponibilidad Comercial** representan conceptos distintos del negocio:
* **Existencia Física:** Cantidad real y tangible de artículos que se custodian físicamente en los estantes y bodegas (ej: 10 unidades en el local).
* **Disponibilidad Comercial (Stock Neto Vendible):** Cantidad de artículos que son lícitamente elegibles para la venta inmediata. Difiere de la física por varios escenarios del negocio:
  * *Productos Reservados / Apartados:* Artículos físicamente presentes pero comprometidos para clientes (ej: layaways o pedidos pendientes).
  * *Productos Dañados / En Cuarentena:* Artículos físicamente presentes pero que no pueden venderse por estar defectuosos o vencidos.
  * *Pedidos Futuros / E-commerce:* Artículos que se han vendido por internet y están listos para despacho (descontados comercialmente pero presentes físicamente).
  * *Expansión Futura:* Venta de stock en tránsito o inventarios compartidos multicanal.

### Decisión de Negocio Aprobada para el MVP:
Para mantener el principio de **evitar sobreingeniería** y asegurar el máximo rendimiento offline en el punto de venta de mostrador, **para el MVP de CajaFácil ambos conceptos se considerarán equivalentes**. 
* Toda existencia registrada físicamente se considerará disponible comercialmente para venta rápida.
* Las mermas (daños) se registrarán inmediatamente como salidas físicas para mantener esta equivalencia al día.
* El soporte para productos reservados, apartados y ventas futuras queda diferido para fases avanzadas del ERP.

---

# 12. Beneficios de Disponer de Existencias Inmediatas

* **Checkout Prácticamente Inmediato:** Garantiza que la consulta de existencias no afecte en absoluto el ritmo de venta física en el mostrador.
* **Continuidad del Negocio:** Venta offline robusta con protección contra sobreventas.
* **Decisiones de Compra de Alta Precisión:** Compras basadas en stock real actualizado de forma ágil, optimizando el capital de trabajo de la empresa.
