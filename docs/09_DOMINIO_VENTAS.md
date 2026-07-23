# 09_DOMINIO_VENTAS.md

**Versión:** 2.0  
**Estado:** Listo para Revisión de Arquitectura  
**Última actualización:** 2026-07-23  
**Documento:** Especificación del Dominio de Ventas  

---

# Objetivo

Definir de manera formal y rigurosa el dominio del negocio para el módulo de **Ventas** (Sales) en CajaFácil, de acuerdo con los principios de Domain-Driven Design (DDD), garantizando el desacoplamiento de contextos y la inmutabilidad de los hechos históricos comerciales.

---

# 1. Definición del Dominio Ventas

## ¿Qué es una Venta dentro del dominio?
Una **Venta** representa el hecho comercial e inmutable mediante el cual el negocio transfiere de manera legal y física la propiedad de bienes o servicios a un cliente a cambio de una contraprestación económica (o un compromiso formal de pago al crédito). 

La Venta no es una transacción informática, ni el proceso de escaneo, ni el intento de cobro. Es un registro histórico inmutable que nace estrictamente en el instante en que el negocio acepta exitosamente el pago (en ventas de contado) o aprueba la obligación financiera del cliente (en ventas al crédito).

## Responsabilidad Exclusiva del Contexto
- **Registrar la transferencia de propiedad**: Mantener el detalle de qué artículos se vendieron, en qué cantidades, con qué precios unitarios pactados, qué descuentos se otorgaron y qué impuestos se aplicaron.
- **Mantener consistencia matemática comercial**: Garantizar que el subtotal, impuestos, descuentos y totales de la venta coincidan exactamente con la suma de sus partes y sean coherentes con las formas de pago registradas.
- **Vincular el hecho comercial**: Asociar de forma inmutable la venta con el Cliente (identificado o Consumidor Final), el Usuario (cajero) que autorizó la venta, la Caja donde se registró y la Empresa propietaria.
- **Publicar el hecho comercial**: Declarar eventos de dominio para que otros contextos reaccionen (Inventario, Caja, Cuentas por Cobrar, Costos).

## Lo que NO es responsabilidad de Ventas
- **Existencias físicas (Stock)**: El control de existencias corresponde al contexto de [Inventario](file:///c:/Users/User/Desktop/CajaFacil/docs/07_DOMINIO_INVENTARIO.md).
- **Control de efectivo físico**: El dinero físico en la gaveta y su cuadre corresponden al contexto de [Caja](file:///c:/Users/User/Desktop/CajaFacil/docs/10_DOMINIO_CAJA.md).
- **Procesamiento técnico de cobros**: Las integraciones con pasarelas de pago, datafonos, validación de tarjetas bancarias o transacciones externas pertenecen al proceso de cobro técnico, no al dominio comercial de la venta.
- **Administración del crédito y cobranza**: El control del límite de crédito de un cliente, sus estados de cuenta y la recepción de abonos corresponden al contexto de [Clientes y Créditos](file:///c:/Users/User/Desktop/CajaFacil/docs/11_DOMINIO_CLIENTES_CREDITO.md).
- **Costos de adquisición y valuación**: El cálculo del costo de venta (PEPS, Promedio Ponderado) y márgenes de ganancia pertenece al dominio de Inventario / Costos.

---

# 2. Modelo de Agregados del Dominio

## Aggregate Root: Venta
El agregado `Venta` encapsula todos los detalles de la venta y las formas de pago. Su consistencia interna y sus invariantes se protegen a través de este único punto de entrada.

### Entidades y Conceptos Internos
- **Venta** (Aggregate Root): Entidad transaccional inmutable una vez confirmada.
- **DetalleVenta** (Entidad interna): Línea de detalle que vincula un producto, su cantidad, precio unitario de venta, descuento e impuestos.
- **FormaPagoAceptada** (Entidad/Value Object interno): Registra la manera en que se liquidó el monto de la venta (Efectivo, Tarjeta, Crédito, etc.) y su valor parcial.

### Value Objects
- **PrecioVenta**: Monto monetario unitario pactado para la venta.
- **CantidadVenta**: Cantidad del producto vendido (soporta decimales para productos a granel).
- **DescuentoVenta**: Valor de descuento aplicado al producto o total de la venta.
- **ImpuestoVenta**: Tasa (porcentaje) e importe del impuesto aplicado al producto.
- **IdentificadorVenta**: UUID global de sincronización offline-first.

---

# 3. Decisiones sobre el Ciclo de Vida y Estados

## Estados de la Venta
El dominio de ventas de CajaFácil **no incluye** estados intermedios de proceso como `BORRADOR`, `ABIERTA` o `PENDIENTE`.

Los únicos estados comerciales válidos en el ciclo de vida del agregado son:
- **Confirmada**: Estado en el que nace el agregado en el dominio. Representa una venta exitosa e inmutable.
- **Anulada**: Estado que representa la reversión comercial de la venta, sin eliminar el registro histórico del sistema.

### Justificación de la Decisión
1. **Sesión de Venta vs. Venta**: Toda la lógica de "escaneado de productos", "modificación de cantidades", "aplicación provisional de descuentos" y "espera de confirmación de pago" pertenece a la **Sesión de Venta** (o Carrito de Compras), que reside en la capa de Aplicación/Interfaz. La Sesión de Venta es temporal, modificable y destruible.
2. **Nacimiento Tardío**: El agregado `Venta` se instancia en el dominio **únicamente cuando el pago es aceptado exitosamente** (o se aprueba formalmente el crédito). No hay necesidad de persistir borradores que nunca se concretaron o pagos que fallaron, manteniendo la base de datos libre de ruido e inconsistencias operativas.
3. **Inmutabilidad Absoluta**: Al nacer en estado `Confirmada`, garantizamos que toda venta persistida representa un hecho comercial verídico.
4. **Anulación en lugar de Eliminación**: Si se requiere deshacer una venta por motivos comerciales (error, devolución total), se realiza una operación de anulación. El estado pasa a `Anulada` registrando la auditoría del supervisor y la justificación. Esto publica el evento `VentaAnulada` para que Inventario reponga el stock y Caja o Crédito reversen los importes correspondientes. El registro original nunca se modifica ni elimina, cumpliendo con la regla global de inmutabilidad histórica.

---

# 4. Operaciones de Negocio del Agregado

Debido a su inmutabilidad, las operaciones disponibles sobre el agregado son:

- **Confirmar Venta (Creación/Factory Method)**: Instancia e inscribe la venta en el dominio, validando que todas las invariantes comerciales, matemáticas y financieras se cumplan simultáneamente. Dispara el evento `VentaConfirmada`.
- **Anular Venta**: Cambia el estado del agregado de `Confirmada` a `Anulada`. Requiere:
  - Identificación del Usuario que autoriza (con rol/permiso de supervisor).
  - Fecha y hora de la anulación.
  - Justificación o motivo comercial.
  Dispara el evento `VentaAnulada`.

---

# 5. Invariantes del Negocio (Reglas de Consistencia)

Para que el agregado `Venta` sea válido en el dominio, debe proteger y garantizar en todo momento las siguientes reglas:

1. **Invariante de Existencia Mínima**: Una venta debe contener obligatoriamente al menos una línea de `DetalleVenta`. No existen ventas vacías.
2. **Invariante de Cantidad Positiva**: La cantidad de producto en cada detalle debe ser estrictamente mayor que cero (`cantidad > 0`).
3. **Invariante de Importes Coherentes**: Los cálculos de subtotales, descuentos, impuestos y totales de cada línea y del encabezado deben coincidir de forma exacta según las fórmulas del negocio:
   $$\text{TotalLínea} = (\text{Cantidad} \times \text{PrecioUnitario}) - \text{Descuento} + \text{Impuesto}$$
   $$\text{TotalVenta} = \sum \text{TotalLínea}$$
4. **Invariante de Coherencia de Cobertura Total del Importe**: La suma de los montos de las `FormasPagoAceptadas` debe ser exactamente igual al `Total` de la venta. No se permiten cobros insuficientes o incompletos al crear la venta.
5. **Invariante de Cliente para Crédito**: Si alguna de las formas de pago es `Crédito`, el cliente **no puede ser** "Consumidor Final". Debe registrarse un Cliente identificado que posea cuenta de crédito activa y cupo disponible suficiente en el contexto de Créditos.
6. **Invariante de Caja Abierta**: La venta debe asociarse a una Caja cuya jornada laboral (AperturaCaja) se encuentre actualmente activa y abierta en el momento de la confirmación.
7. **Invariante de Inmutabilidad Histórica**: Ningún atributo comercial de una venta en estado `Confirmada` puede ser alterado (no se pueden editar precios, cambiar productos, remover líneas ni modificar totales).

---

# 6. Repositorio del Dominio

El dominio de ventas requiere la interfaz abstracta `VentaRepository` para interactuar con la persistencia. Sus responsabilidades son:

- **`guardar(Venta)`**: Persistir el agregado completo (Venta, Detalles, Formas de Pago) de forma atómica en una única transacción.
- **`obtenerPorId(VentaId)`**: Recuperar el agregado completo utilizando el identificador único UUID.
- **`obtenerPorComprobante(NumeroComprobante)`**: Buscar la venta utilizando el número de factura o código correlativo de comprobante.
- **`buscar(CriteriosBusqueda)`**: Permitir consultas sobre el historial (rango de fechas, cajero, cliente, estado de venta).

---

# 7. Excepciones del Dominio

Se definen las siguientes excepciones de negocio para evitar estados inconsistentes:

- **`VentaVaciaException`**: Se intenta confirmar una venta que no contiene productos.
- **`CantidadInvalidaException`**: La cantidad de un producto es cero o negativa.
- **`ImporteIncoherenteException`**: Los cálculos matemáticos de subtotales, impuestos, descuentos o totales de la venta no coinciden.
- **`PagoInsuficienteException`**: La suma de los pagos ingresados es menor al total que se debe cobrar.
- **`ClienteRequeridoParaCreditoException`**: Se intenta pagar con crédito a nombre de "Consumidor Final".
- **`VentaInmutableException`**: Intento de modificar o alterar datos de una venta confirmada.
- **`VentaYaAnuladaException`**: Intento de anular una venta que ya fue anulada previamente.
- **`UsuarioNoAutorizadoParaAnulacionException`**: El usuario provisto para autorizar la anulación no posee permisos de supervisión.
- **`CajaCerradaException`**: Se intenta confirmar una venta en una caja que no se encuentra abierta.

---

# 8. Eventos de Dominio Publicados

- **`VentaConfirmada`**: Publicado al momento de crearse exitosamente la venta en el dominio.
  - *Suscripciones y Reacciones*:
    - **Inventario**: Genera la salida física de mercadería a través de un `MovimientoInventario`.
    - **Caja**: Registra el `MovimientoCaja` de tipo "Ingreso por Venta" por la fracción de pago en efectivo.
    - **Cuentas por Cobrar**: Registra la cuenta por cobrar (`Crédito`) y asocia el saldo al cliente por la fracción pagada a crédito.
- **`VentaAnulada`**: Publicado al anularse comercialmente la venta.
  - *Suscripciones y Reacciones*:
    - **Inventario**: Genera una entrada física de retorno de mercadería mediante un `MovimientoInventario`.
    - **Caja**: Genera un egreso o contra-movimiento de caja para balancear el dinero en caso de devoluciones en efectivo.
    - **Cuentas por Cobrar**: Reversa o cancela el saldo adeudado del crédito asociado a esa venta.

---

# 9. Resolución de Preguntas de Negocio Adicionales

## A) ¿Qué ocurre cuando el pago falla?
*Escenario: El cliente selecciona sus productos, intenta pagar con tarjeta en la terminal bancaria y la transacción es rechazada.*

### Análisis y Decisión
**Únicamente existió una Sesión de Venta.** La venta como agregado del dominio **no existe ni existió**.

### Justificación Comercial
La Venta representa un hecho comercial y jurídico donde se transfiere la propiedad de los bienes a cambio de valor. Si el pago es rechazado, la contraprestación no se ha recibido, el comercio no entrega la mercadería y no hay mutación de propiedad. 

La falla en el pago es una contingencia de la capa transaccional del proceso de cobro (un evento técnico e interactivo). Mantener el estado en la "Sesión de Venta" en el frontend o la capa de aplicación evita:
1. Contaminar el historial de la base de datos con folios de venta inválidos o cancelados.
2. Complicar el flujo de sincronización offline-first con ventas nulas que nunca ocurrieron físicamente.
3. Consumir rangos de folios de comprobación fiscal (comprobantes de venta).

El cliente puede intentar pagar con otro medio (efectivo, otra tarjeta) dentro de la misma Sesión de Venta. Si finalmente desiste, la Sesión de Venta simplemente se descarta y no deja rastro en el dominio del negocio.

---

## B) ¿Qué ocurre con un pago parcial?
*Escenario: Venta por un total de L 1,000. El cliente entrega L 500 en efectivo y solicita llevarse los productos pagando los L 500 restantes después.*

### Alternativas de Modelado
1. **La venta no nace**: No es viable porque el cliente se lleva físicamente los productos. La mercadería sale del stock e ingresa efectivo a caja, por lo que legal y comercialmente la transferencia de propiedad ocurrió.
2. **La venta nace como contado, y la diferencia es una deuda informal**: Inaceptable en un ERP/POS profesional. Todo saldo pendiente debe tener trazabilidad financiera formal.
3. **La venta nace en el dominio de forma inmediata mediante Multi-pago (Efectivo + Crédito)**: La venta se confirma por L 1,000. Sus formas de pago asociadas son: `Efectivo = L 500` y `Crédito = L 500`.

### Decisión Comercial y Justificación
**La Venta NACE en ese instante, liquidándose mediante pagos parciales híbridos (Efectivo y Crédito).**

Esta es la única representación fiel de la realidad comercial del negocio:
1. **Venta total (L 1,000)**: Nace y se confirma de inmediato. Se emite el Comprobante por el total de la transacción comercial.
2. **Efectivo (L 500)**: Genera de forma inmediata un movimiento de ingreso en la Caja del día.
3. **Crédito (L 500)**: El sistema valida que el Cliente esté identificado (RN-601). Al confirmarse la venta, se publica el evento `VentaConfirmada` detallando la porción de crédito. El módulo de Cuentas por Cobrar recibe el evento y crea una cuenta de `Crédito` activa vinculada al cliente por L 500.

Esta decisión separa limpiamente las responsabilidades: la Venta registra el total de la compra e imputa las formas de pago iniciales; los módulos de Caja y Crédito manejan la repercusión financiera.

---

## C) Separación de Conceptos: VENTA vs COBRO (PAYMENT)

Es fundamental mantener los límites de diseño claros para no contaminar el dominio comercial con la volatilidad del flujo transaccional financiero.

| Característica / Concepto | Dominio Venta | Proceso de Cobro (Payment) |
|---|---|---|
| **Definición** | Hecho comercial e inmutable que registra la transacción de mercancía. | Proceso transaccional y técnico que recolecta el dinero. |
| **Responsabilidad** | - Validar consistencia de los productos.<br>- Calcular impuestos y descuentos aplicables.<br>- Emitir el Comprobante oficial.<br>- Registrar quién vendió y a quién. | - Comunicarse con pasarelas de pago y terminales.<br>- Administrar reintentos en tarjetas bancarias.<br>- Controlar el flujo de efectivo recibido y cambio (vuelto). |
| **Volatilidad** | Muy baja. Solo cambia si se anula la venta completa. | Alta. Puede haber múltiples intentos fallidos, cambios de tarjeta o renegociaciones de forma de pago en segundos. |
| **Ciclo de vida** | Lineal: Confirmada -> Anulada. | Dinámico: Esperando pago -> Procesando -> Rechazado / Aprobado. |

### Responsabilidades que nunca deben mezclarse
1. **El Agregado Venta no debe conocer de pasarelas ni terminales**: La venta solo recibe un Value Object con la confirmación de la forma de pago exitosa (ej. "Tarjeta de Crédito, Transacción #982312, L 500"). Toda la lógica de "conectar con el banco" se resuelve en la capa de aplicación o infraestructura antes de construir la Venta.
2. **El Cobro no calcula impuestos ni precios**: El cobro es ciego al detalle de los productos. Solo requiere saber el monto total a pagar (Monto Cobrado). No le importa si se vendió pan, licor o un servicio; solo le importan los fondos y el canal de pago.
3. **El estado de Caja es independiente del estado de Venta**: La Venta reporta el hecho comercial. Si el cajero ingresó mal el método de pago en la Sesión de Venta (ej. marcó efectivo pero era tarjeta), esto se resuelve mediante una auditoría o anulación comercial de la Venta, pero el saldo de Caja físico se cuadra a través de los arqueos y movimientos de caja específicos.

---

# 10. Reglas para Antigravity

- **No implementar flujos de Venta pendientes o borradores en base de datos**: Los borradores se guardan en almacenamiento local/temporal del cliente (ej. localStorage o memoria local del dispositivo) si se requiere persistir la Sesión de Venta para modo offline. La base de datos compartida o sincronizada solo almacena Ventas confirmadas.
- **Transaccionalidad obligatoria**: La confirmación de la venta en el repositorio debe ser atómica (se guardan cabecera, detalles y formas de pago al mismo tiempo, o no se guarda nada).
- **Desacoplamiento mediante Eventos**: No realizar inserciones directas en las tablas de inventario o saldos de caja desde el código de ventas. Todo debe fluir mediante los eventos de dominio (`VentaConfirmada` y `VentaAnulada`).

---

# 11. Reglas de Negocio Referenciadas

Este dominio se rige formalmente por las siguientes reglas definidas en [Reglas de Negocio](file:///c:/Users/User/Desktop/CajaFacil/docs/06_REGLAS_DE_NEGOCIO.md):
- **RN-001**: Pertenece a una Empresa.
- **RN-002**: Ejecutado por un Usuario autenticado.
- **RN-004**: No se elimina información histórica; se conserva mediante el estado `Anulada` y registros de auditoría.
- **RN-400**: Genera Movimientos de Inventario al confirmarse.
- **RN-401**: Genera Movimientos de Caja al confirmarse (por porciones en efectivo).
- **RN-402**: Los importes históricos de la venta son inmutables.
- **RN-403**: Las anulaciones conservan el registro original e intacto.
- **RN-404**: Uso del cliente genérico Consumidor Final si es contado y no se identifica al cliente.
- **RN-601**: Cliente identificado es obligatorio si se utiliza la forma de pago Crédito.