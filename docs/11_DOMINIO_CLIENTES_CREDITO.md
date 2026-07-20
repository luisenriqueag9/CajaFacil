# 11_DOMINIO_CLIENTES_CREDITO.md

**Versión:** 1.0
**Estado:** Aprobado (Arquitectura)
**Última actualización:** 2026-07-19
**Documento:** Dominio Clientes y Crédito

# Dominio Clientes y Crédito

## Objetivo

Administrar la información de los clientes y el ciclo de vida de los créditos otorgados por la empresa, garantizando la trazabilidad de los saldos y los pagos.

---

# Responsabilidad

- Administrar clientes.
- Registrar créditos originados por ventas.
- Registrar abonos.
- Calcular saldo pendiente.
- Consultar historial de pagos.
- Administrar el estado del crédito.

---

# No es responsabilidad

- Registrar ventas.
- Administrar caja.
- Modificar inventario.
- Administrar productos.
- Calcular existencias.

---

# Aggregate Roots

## Cliente

Representa a una persona o empresa con la que existe una relación comercial.

## Crédito

Representa una obligación de pago generada por una venta a crédito.

---

# Entidades

- Cliente
- Crédito
- AbonoCredito
- EstadoCredito

---

# Value Objects

- Saldo
- LímiteCrédito
- FechaVencimiento
- Plazo
- NúmeroDocumento

---

# Casos de Uso

- Registrar cliente.
- Actualizar datos del cliente.
- Crear crédito.
- Registrar abono.
- Liquidar crédito.
- Consultar estado de cuenta.
- Consultar historial de créditos.

---

# Estados

## Cliente

- Activo
- Inactivo

## Crédito

- Activo
- Cancelado
- Vencido

---

# Eventos del Dominio

- ClienteRegistrado
- CreditoCreado
- AbonoRegistrado
- CreditoLiquidado

---

# Relaciones

## Consulta

- Venta

## Solicita

- Caja.RegistrarIngreso()

## Publica eventos para

- Reportes
- Auditoría
- Sincronización

---

# Reglas aplicables

Este dominio se rige por:

- RN-600
- RN-601
- RN-602

---

# Arquitectura

El cliente es opcional para ventas de contado y obligatorio para ventas a crédito.

Los créditos nacen exclusivamente a partir de una venta confirmada.

Los abonos nunca modifican directamente el saldo; generan un registro de AbonoCredito y el saldo se recalcula a partir de los movimientos registrados.

---

# Preparado para futuras versiones

La arquitectura permitirá incorporar:

- Límites de crédito por cliente.
- Múltiples créditos activos por cliente.
- Intereses por mora.
- Refinanciamientos.
- Recordatorios automáticos de pago.
- Bloqueo automático por morosidad.
- Firma digital de contratos.

---

# Sincronización

Toda entidad sincronizable incluirá:

- UUID
- Empresa
- Fecha de creación
- Fecha de modificación
- Versión
- Estado de sincronización

---

# Reglas para Antigravity

- No modificar saldos directamente.
- Todo pago genera un AbonoCredito.
- Mantener la lógica en Domain/Application.
- Respetar RN-600 a RN-602.

---

# Observaciones

El dominio Clientes y Crédito administra exclusivamente la relación financiera con el cliente. Las ventas originan los créditos y la Caja registra los movimientos de dinero, manteniendo la separación de responsabilidades entre dominios.