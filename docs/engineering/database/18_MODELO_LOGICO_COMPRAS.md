# 18_MODELO_LOGICO_COMPRAS.md

Versión: 1.0

Estado: Aprobado

Última actualización: 2026-07-20

Documento: Modelo Lógico de Datos

---

# Objetivo

Definir el modelo lógico del dominio Compras.

Este documento describe las entidades involucradas en el proceso de abastecimiento de productos, desde el registro de una compra hasta su impacto en el inventario.

No define tipos físicos de SQLite o PostgreSQL; define entidades, atributos, relaciones y restricciones del dominio.

---

# Alcance

Este documento comprende las siguientes entidades:

- Compra
- DetalleCompra

---

# Convenciones

## Tipos de entidades

### TRANSACCIONAL

Información generada por las operaciones del negocio.

---

# Dominio Compras

---

# Compra

## Descripción

Representa una compra realizada a un proveedor.

Una compra puede contener uno o varios productos y constituye el documento principal del proceso de abastecimiento.

Al confirmarse una compra, el sistema genera automáticamente los movimientos de inventario correspondientes.

---

## Tipo de entidad

TRANSACCIONAL

---

## Aggregate Root

Compra

---

## Atributos del negocio

| Campo | Tipo | Obligatorio |
|--------|------|-------------|
| EmpresaId | UUID | Sí |
| ProveedorId | UUID | Sí |
| NumeroDocumento | Texto(50) | No |
| FechaCompra | DateTime | Sí |
| Subtotal | Dinero | Sí |
| Descuento | Dinero | No |
| Impuesto | Dinero | No |
| Total | Dinero | Sí |
| Observaciones | Texto(300) | No |
| Estado | Enum | Sí |

---

## Atributos técnicos

| Campo | Tipo |
|--------|------|
| Id | UUID |
| Version | Integer |
| CreadoEn | DateTime UTC |
| ActualizadoEn | DateTime UTC |
| EstadoSincronizacion | Enum |

---

## Relaciones

- Empresa 1 → N Compras
- Proveedor 1 → N Compras
- Compra 1 → N DetalleCompra

---

## Restricciones

- Toda compra debe tener un proveedor.
- Debe contener al menos un detalle.
- No puede modificarse una compra confirmada.
- El total debe ser mayor que cero.

---

## Observaciones

La compra no modifica directamente el inventario.

La confirmación de la compra genera automáticamente los movimientos de inventario.

---

# DetalleCompra

## Descripción

Representa cada producto adquirido dentro de una compra.

Cada registro corresponde a una línea de la factura del proveedor.

---

## Tipo de entidad

TRANSACCIONAL

---

## Aggregate Root

Compra

---

## Atributos del negocio

| Campo | Tipo | Obligatorio |
|--------|------|-------------|
| CompraId | UUID | Sí |
| ProductoId | UUID | Sí |
| Cantidad | Decimal | Sí |
| PrecioUnitario | Dinero | Sí |
| Descuento | Dinero | No |
| Impuesto | Dinero | No |
| Subtotal | Dinero | Sí |
| Total | Dinero | Sí |

---

## Relaciones

- Compra 1 → N DetalleCompra
- Producto 1 → N DetalleCompra

---

## Restricciones

- La cantidad debe ser mayor que cero.
- El precio unitario debe ser mayor o igual a cero.
- Un detalle siempre pertenece a una compra.
- No puede eliminarse un detalle de una compra confirmada.

---

## Observaciones

Cada detalle confirmado genera un movimiento de entrada en el inventario para el producto correspondiente.

---

# Resumen del dominio

| Entidad | Tipo |
|----------|------|
| Compra | TRANSACCIONAL |
| DetalleCompra | TRANSACCIONAL |

---

# Conclusión

El dominio Compras registra el abastecimiento de productos y constituye el origen principal de las entradas al inventario.

La información registrada en este módulo será utilizada para actualizar costos, generar movimientos de inventario y mantener la trazabilidad de las adquisiciones realizadas por la empresa.