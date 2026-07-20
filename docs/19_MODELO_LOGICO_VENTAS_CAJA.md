# 19_MODELO_LOGICO_VENTAS_CAJA.md

Versión: 1.0

Estado: Aprobado

Última actualización: 2026-07-20

Documento: Modelo Lógico de Datos

---

# Objetivo

Definir el modelo lógico del dominio Ventas y Caja.

Este documento establece las entidades encargadas del proceso de venta, control de efectivo y movimientos de caja.

No define tipos físicos de SQLite o PostgreSQL; define entidades, atributos, relaciones y restricciones del dominio.

---

# Alcance

Este documento comprende las siguientes entidades:

- Caja
- AperturaCaja
- CierreCaja
- MovimientoCaja
- Venta
- DetalleVenta

---

# Convenciones

## Tipos de entidades

### MASTER DATA

Información relativamente estable.

### TRANSACCIONAL

Información generada durante la operación del negocio.

---

# Dominio Caja

---

# Caja

## Descripción

Representa una caja registradora utilizada para realizar ventas y controlar el efectivo.

Cada computadora registrada en CajaFácil podrá asociarse a una Caja.

---

## Tipo de entidad

MASTER DATA

---

## Aggregate Root

Caja

---

## Atributos del negocio

| Campo | Tipo | Obligatorio |
|--------|------|-------------|
| EmpresaId | UUID | Sí |
| SucursalId | UUID | Sí |
| Nombre | Texto(100) | Sí |
| Codigo | Texto(30) | Sí |
| Activa | Boolean | Sí |

---

## Relaciones

- Sucursal 1 → N Cajas
- Caja 1 → N Aperturas
- Caja 1 → N Ventas
- Caja 1 → N MovimientosCaja

---

## Restricciones

- El código debe ser único por empresa.
- No puede eliminarse si posee historial.

---

# AperturaCaja

## Descripción

Representa el inicio de una jornada de trabajo de una caja.

---

## Tipo de entidad

TRANSACCIONAL

---

## Aggregate Root

Caja

---

## Atributos del negocio

| Campo | Tipo | Obligatorio |
|--------|------|-------------|
| CajaId | UUID | Sí |
| UsuarioId | UUID | Sí |
| FechaHora | DateTime | Sí |
| FondoInicial | Dinero | Sí |
| Observaciones | Texto(300) | No |

---

## Relaciones

- Caja 1 → N Aperturas

---

## Restricciones

- Solo puede existir una apertura activa por caja.

---

# CierreCaja

## Descripción

Representa el cierre de una jornada de trabajo.

---

## Tipo de entidad

TRANSACCIONAL

---

## Aggregate Root

Caja

---

## Atributos del negocio

| Campo | Tipo | Obligatorio |
|--------|------|-------------|
| AperturaCajaId | UUID | Sí |
| FechaHora | DateTime | Sí |
| TotalSistema | Dinero | Sí |
| TotalContado | Dinero | Sí |
| Diferencia | Dinero | Sí |
| Observaciones | Texto(300) | No |

---

## Relaciones

- AperturaCaja 1 → 1 CierreCaja

---

## Restricciones

- Una apertura solamente puede cerrarse una vez.

---

# MovimientoCaja

## Descripción

Representa cualquier movimiento de dinero realizado en la caja.

Ejemplos:

- Venta contado
- Retiro
- Ingreso
- Gasto
- Ajuste

---

## Tipo de entidad

TRANSACCIONAL

---

## Aggregate Root

MovimientoCaja

---

## Atributos del negocio

| Campo | Tipo | Obligatorio |
|--------|------|-------------|
| CajaId | UUID | Sí |
| UsuarioId | UUID | Sí |
| TipoMovimiento | Enum | Sí |
| Concepto | Texto(200) | Sí |
| Monto | Dinero | Sí |
| FechaHora | DateTime | Sí |

---

## Relaciones

- Caja 1 → N MovimientoCaja

---

## Restricciones

- Todo movimiento pertenece a una caja.
- El monto debe ser mayor que cero.
- No puede eliminarse.

---

# Dominio Ventas

---

# Venta

## Descripción

Representa una transacción realizada con un cliente.

Una venta puede ser de contado o a crédito.

---

## Tipo de entidad

TRANSACCIONAL

---

## Aggregate Root

Venta

---

## Atributos del negocio

| Campo | Tipo | Obligatorio |
|--------|------|-------------|
| EmpresaId | UUID | Sí |
| CajaId | UUID | Sí |
| UsuarioId | UUID | Sí |
| ClienteId | UUID | No |
| NumeroFactura | Texto(50) | No |
| FechaVenta | DateTime | Sí |
| TipoVenta | Enum | Sí |
| Subtotal | Dinero | Sí |
| Descuento | Dinero | No |
| Impuesto | Dinero | No |
| Total | Dinero | Sí |
| Estado | Enum | Sí |

---

## Relaciones

- Caja 1 → N Ventas
- Usuario 1 → N Ventas
- Cliente 1 → N Ventas
- Venta 1 → N DetalleVenta

---

## Restricciones

- Debe contener al menos un detalle.
- Toda venta pertenece a una caja abierta.
- Una venta confirmada no puede modificarse.

---

## Observaciones

Las ventas de contado generan automáticamente un ingreso en caja.

Las ventas a crédito generan el crédito correspondiente, pero no generan ingreso de efectivo.

---

# DetalleVenta

## Descripción

Representa cada producto vendido dentro de una venta.

---

## Tipo de entidad

TRANSACCIONAL

---

## Aggregate Root

Venta

---

## Atributos del negocio

| Campo | Tipo | Obligatorio |
|--------|------|-------------|
| VentaId | UUID | Sí |
| ProductoId | UUID | Sí |
| Cantidad | Decimal | Sí |
| PrecioUnitario | Dinero | Sí |
| Descuento | Dinero | No |
| Impuesto | Dinero | No |
| Subtotal | Dinero | Sí |
| Total | Dinero | Sí |

---

## Relaciones

- Venta 1 → N DetalleVenta
- Producto 1 → N DetalleVenta

---

## Restricciones

- La cantidad debe ser mayor que cero.
- El precio unitario debe ser mayor o igual a cero.
- No puede eliminarse un detalle de una venta confirmada.

---

## Observaciones

Cada detalle confirmado genera un movimiento de salida en el inventario para el producto correspondiente.

---

# Resumen del dominio

| Entidad | Tipo |
|----------|------|
| Caja | MASTER DATA |
| AperturaCaja | TRANSACCIONAL |
| CierreCaja | TRANSACCIONAL |
| MovimientoCaja | TRANSACCIONAL |
| Venta | TRANSACCIONAL |
| DetalleVenta | TRANSACCIONAL |

---

# Conclusión

El dominio Ventas y Caja constituye el núcleo operativo de CajaFácil.

Toda venta genera automáticamente los movimientos necesarios sobre inventario y, cuando corresponde, sobre caja, garantizando la integridad de la información, la trazabilidad de las operaciones y la compatibilidad con la arquitectura Offline First.