# 27_DISENO_DOMINIO_INVENTARIO.md

**Versión:** 1.0  
**Estado:** 📝 En Revisión (Fase 2: Diseño del Dominio)  
**Última actualización:** 2026-07-23  
**Documento:** Diseño del Dominio de Inventario  

---

# 1. ¿Qué problema del negocio resuelve Inventario?

El dominio de Inventario resuelve los siguientes problemas críticos del negocio en comercios minoristas y mayoristas (SaaS):
* **Fuga y pérdida hormiga de stock:** Controla la pérdida de mercancías registrando cronológicamente quién, cuándo y por qué retiró un producto.
* **Quiebres de stock (StockOUT):** Previene la pérdida de ventas al proveer información precisa sobre la disponibilidad de los artículos para la venta.
* **Capital de trabajo inmovilizado:** Proporciona visibilidad del stock real disponible para evitar compras excesivas (sobre-stock) y optimizar el flujo de efectivo.
* **Desviaciones en conteos físicos:** Permite auditar y corregir las discrepancias lógicas del sistema respecto a la realidad del almacén mediante procesos formales de conciliación.
* **Falta de trazabilidad histórica (Kardex):** Reconstruye el ciclo de vida operativo de un artículo, identificando si las existencias se redujeron por ventas, compras devueltas, mermas o ajustes manuales.

---

# 2. ¿Qué es un Movimiento de Inventario?

Un **Movimiento de Inventario** es un hecho comercial inmutable e histórico que documenta el flujo físico de entrada o salida de una cantidad determinada de un producto específico. 

Representa la transacción base del dominio. No es una simple edición del stock, sino una declaración formal del negocio que asocia:
1. El producto afectado.
2. El sentido del flujo (Adición/`ENTRADA` o Sustracción/`SALIDA`).
3. El motivo comercial que lo justifica (Concepto: compra, venta, merma, ajuste, devolución).
4. La cantidad física de unidades.
5. El documento o transacción de origen (compra, venta, arqueo) que originó la orden.

---

# 3. ¿Cuál es su responsabilidad exclusiva?

La responsabilidad exclusiva del dominio de Inventario es:
* **Gobernar de forma absoluta el balance físico de stock:** Ser el único punto de decisión autorizado para certificar cuántas existencias tiene una empresa.
* **Proteger la inmutabilidad física:** Garantizar que el historial de movimientos no sea modificado, alterado o eliminado retrospectivamente.
* **Validar las invariantes de consistencia física:** Decidir si una salida de inventario es legal basándose en los parámetros lógicos del producto (si permite o no stock negativo).

---

# 4. ¿Qué no pertenece al contexto Inventario?

Para mantener el contexto acotado limpio y evitar acoplamiento, quedan explícitamente fuera:
* **El Catálogo y Atributos Maestros del Producto:** El inventario no crea productos, no edita sus nombres, códigos de barra, códigos internos, categorías o marcas. Solo lee estas referencias lógicas.
* **Precios de Venta y Costos Financieros de Compra:** El inventario solo opera con unidades físicas (Cantidades). La valoración comercial de las ventas o las facturas de proveedores son responsabilidad de los módulos de **Ventas** y **Compras**.
* **El dinero y flujos de caja:** El inventario no valida si el cliente pagó en efectivo o tarjeta, ni gestiona el saldo monetario de la caja registradora.
* **La relación con los proveedores:** El inventario no maneja datos de contacto, contratos ni términos de pago de los proveedores.

---

# 5. ¿Qué hechos del negocio pueden generar un Movimiento de Inventario?

Los movimientos se dividen según su impacto físico:

### Entradas (Adición de stock)
* **Recepción de Compra (`COMPRA`):** Ingreso físico de productos adquiridos a un proveedor.
* **Reversión por Venta Anulada (`ANULACION_VENTA`):** Retorno físico de mercancía devuelta por el cliente debido a la cancelación de una venta.
* **Ajuste Físico Excedente (`AJUSTE_ENTRADA`):** Incremento correctivo tras una auditoría física donde se hallaron más unidades que las registradas.

### Salidas (Sustracción de stock)
* **Despacho por Venta Confirmada (`VENTA`):** Reducción de existencias entregadas al cliente en el mostrador.
* **Devolución a Proveedor (`DEVOLUCION_PROVEEDOR`):** Salida física de productos defectuosos o vencidos retornados al proveedor.
* **Registro de Merma (`MERMA`):** Descarte físico por rotura, daño, robo o vencimiento de la mercancía.
* **Ajuste Físico Faltante (`AJUSTE_SALIDA`):** Reducción correctiva tras una auditoría física donde se contaron menos unidades que las del sistema.

---

# 6. ¿Qué es una Existencia y cómo se relaciona con los Movimientos?

* **La Existencia (Stock):** Representa el saldo neto actual de unidades de un producto en un momento determinado.
* **Relación Matemática:** Es un dato puramente derivado y proyectado. No existe como variable de estado modificable en forma aislada. Se calcula exclusivamente como la sumatoria algebraica de todos los movimientos de entradas menos las salidas registradas desde el inicio de operaciones del producto:
  $$\text{Existencia} = \sum (\text{Movimientos Entrada}) - \sum (\text{Movimientos Salida})$$

> [!NOTE]
> Para optimizar el rendimiento de las búsquedas en la base de datos (CQRS / Read Model), se puede proyectar el stock actual en una tabla caché. Sin embargo, toda verificación y la verdad absoluta residen en la agregación de los movimientos físicos.

---

# 7. Elementos del Dominio (Entidades, Objetos de Valor y Agregados)

### Agregados (Aggregate Roots)
* **MovimientoInventario (Aggregate Root):**
  * Representa el hecho inmutable del cambio de stock.
  * Gobierna su propia consistencia e integridad.
  * Una vez guardado con estado `CONFIRMADO`, es inalterable.

### Entidades (Dentro del límite del Agregado o relacionadas)
* **Merma (Entidad):**
  * Detalla las razones de una salida por pérdida.
  * Atributos: `Motivo` (Rotura, Vencimiento, Robo), `Observaciones`, `EvidenciaFotoUrl` (opcional).
* **AjusteInventario (Entidad):**
  * Registra la auditoría física que motivó una corrección.
  * Atributos: `SupervisorId`, `CantidadFisica`, `CantidadSistema`, `Diferencia`, `Justificacion`.

### Objetos de Valor (Value Objects)
* **Cantidad:** Valor decimal no negativo (mayor que cero) con soporte para unidades enteras y decimales (gramos, litros).
* **ConceptoMovimiento:** Identificador del hecho comercial (Enum).
* **TipoMovimiento:** Sentido del flujo físico (Enum: `ENTRADA`, `SALIDA`).

---

# 8. Invariantes del Dominio (Reglas Indestructibles)

Las siguientes validaciones lógicas deben ser forzadas por el dominio antes de persistir cualquier cambio:

* **Invariante 1: Modificación Transaccional Exclusiva:** Las existencias lógicas de un producto nunca pueden variar sin la existencia de un `MovimientoInventario` asociado.
* **Invariante 2: Validación de Habilitación de Stock (`ManejaInventario`):** No se permite registrar ningún movimiento de inventario sobre un producto cuya especificación maestra declare `ManejaInventario = False`.
* **Invariante 3: Prevención de Stock Negativo (`PermiteStockNegativo`):** 
  * Si el producto tiene configurado `PermiteStockNegativo = False`, el dominio debe calcular el saldo acumulado actual. Si la cantidad solicitada en una `SALIDA` es mayor que la existencia calculada, la transacción debe ser rechazada inmediatamente arrojando `StockInsuficienteException`.
* **Invariante 4: Positividad del Flujo:** La cantidad de unidades de cualquier movimiento debe ser estrictamente mayor que cero ($> 0$).
* **Invariante 5: Inmutabilidad Histórica:** Ningún movimiento confirmado de inventario puede ser editado, actualizado o eliminado físicamente de la base de datos. Cualquier corrección requiere registrar un movimiento compensatorio.

---

# 9. Eventos de Dominio de Inventario

El dominio comunica sus hechos confirmados a través de los siguientes eventos:
* **`InventarioActualizado`:** Contiene `ProductId`, `CantidadCambio`, `NuevoBalanceCalculado`, `TipoMovimiento` y `Fecha`. (Utilizado por Reportes y alertas de Stock Mínimo).
* **`MermaRegistrada`:** Contiene `MermaId`, `ProductId`, `Cantidad`, `Motivo` y `Fecha`. (Utilizado por Auditoría Financiera).
* **`AjusteInventarioRegistrado`:** Contiene `AjusteId`, `ProductId`, `CantidadFisica`, `CantidadSistema`, `SupervisorId` y `Fecha`.

---

# 10. Matriz de Responsabilidades

| Responsabilidad | Producto (Catálogo) | Compras | Ventas | Inventario (Exclusivo) |
|---|:---:|:---:|:---:|:---:|
| Definir si el producto controla existencias | **Propietario** | No | No | No (Solo consulta) |
| Definir si permite stock menor a cero | **Propietario** | No | No | No (Solo consulta) |
| Validar suficiencia de stock para la venta | No | No | No | **Propietario** |
| Registrar y procesar el pago del cliente | No | No | **Propietario** | No |
| Autorizar y registrar factura del proveedor | No | **Propietario** | No | No |
| Registrar entrada física por compra recibida | No | No | No | **Propietario** |
| Registrar salida física por venta despachada | No | No | No | **Propietario** |
| Documentar mermas y ajustes de inventario | No | No | No | **Propietario** |
