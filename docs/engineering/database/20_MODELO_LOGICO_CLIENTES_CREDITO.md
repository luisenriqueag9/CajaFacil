# 20_MODELO_LOGICO_CLIENTES_CREDITO.md

Versión: 1.0

Estado: Aprobado

Última actualización: 2026-07-20

Documento: Modelo Lógico de Datos

---

# Objetivo

Definir el modelo lógico del dominio Clientes y Crédito.

Este documento describe las entidades encargadas de administrar clientes, ventas a crédito y pagos realizados por los clientes.

No define tipos físicos de SQLite o PostgreSQL; define entidades, atributos, relaciones y restricciones del dominio.

---

# Alcance

Este documento comprende las siguientes entidades:

- Cliente
- Credito
- AbonoCredito

---

# Convenciones

## Tipos de entidades

### MASTER DATA

Información relativamente estable.

### TRANSACCIONAL

Información generada por las operaciones del negocio.

---

# Dominio Clientes

---

# Cliente

## Descripción

Representa una persona o empresa registrada para realizar compras a crédito o para emitir facturas con datos fiscales.

El registro de clientes es opcional para las ventas de contado.

---

## Tipo de entidad

MASTER DATA

---

## Aggregate Root

Cliente

---

## Atributos del negocio

| Campo | Tipo | Obligatorio |
|--------|------|-------------|
| EmpresaId | UUID | Sí |
| Nombre | Texto(200) | Sí |
| RTN | Texto(30) | No |
| Telefono | Texto(30) | No |
| Correo | Email | No |
| Direccion | Texto(300) | No |
| LimiteCredito | Dinero | No |
| Activo | Boolean | Sí |

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

- Empresa 1 → N Clientes
- Cliente 1 → N Ventas
- Cliente 1 → N Creditos

---

## Restricciones

- El nombre del cliente es obligatorio.
- No puede eliminarse si posee créditos o ventas asociadas.

---

## Observaciones

Las ventas de contado pueden realizarse sin cliente registrado.

---

# Dominio Crédito

---

# Credito

## Descripción

Representa una deuda generada a partir de una venta a crédito.

Cada crédito nace de una única venta.

---

## Tipo de entidad

TRANSACCIONAL

---

## Aggregate Root

Credito

---

## Atributos del negocio

| Campo | Tipo | Obligatorio |
|--------|------|-------------|
| EmpresaId | UUID | Sí |
| ClienteId | UUID | Sí |
| VentaId | UUID | Sí |
| FechaInicio | DateTime | Sí |
| FechaVencimiento | DateTime | Sí |
| MontoOriginal | Dinero | Sí |
| SaldoPendiente | Dinero | Sí |
| Estado | Enum | Sí |

---

## Relaciones

- Cliente 1 → N Creditos
- Venta 1 → 1 Credito
- Credito 1 → N AbonosCredito

---

## Restricciones

- Todo crédito proviene de una venta.
- El monto original debe ser mayor que cero.
- El saldo pendiente no puede ser negativo.

---

## Observaciones

El saldo pendiente disminuye únicamente mediante abonos.

---

# AbonoCredito

## Descripción

Representa un pago realizado por un cliente para reducir el saldo de un crédito.

---

## Tipo de entidad

TRANSACCIONAL

---

## Aggregate Root

Credito

---

## Atributos del negocio

| Campo | Tipo | Obligatorio |
|--------|------|-------------|
| CreditoId | UUID | Sí |
| CajaId | UUID | Sí |
| UsuarioId | UUID | Sí |
| FechaAbono | DateTime | Sí |
| Monto | Dinero | Sí |
| Observaciones | Texto(300) | No |

---

## Relaciones

- Credito 1 → N AbonosCredito
- Caja 1 → N AbonosCredito
- Usuario 1 → N AbonosCredito

---

## Restricciones

- El monto debe ser mayor que cero.
- No puede registrarse un abono mayor al saldo pendiente.
- Todo abono genera un ingreso en caja.

---

## Observaciones

Cada abono actualiza automáticamente el saldo del crédito y registra el movimiento correspondiente en caja.

---

# Resumen del dominio

| Entidad | Tipo |
|----------|------|
| Cliente | MASTER DATA |
| Credito | TRANSACCIONAL |
| AbonoCredito | TRANSACCIONAL |

---

# Conclusión

El dominio Clientes y Crédito permite administrar las ventas financiadas y el control de las cuentas por cobrar.

La integración entre ventas, créditos, abonos y caja garantiza la trazabilidad completa de las operaciones y mantiene la consistencia del sistema.