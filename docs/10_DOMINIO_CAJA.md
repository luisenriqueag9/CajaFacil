# 10_DOMINIO_CAJA.md

**Versión:** 1.0
**Estado:** Aprobado (Arquitectura)
**Última actualización:** 2026-07-19
**Documento:** Dominio Caja

# Dominio Caja

## Objetivo

Administrar el flujo de dinero de cada caja registradora mediante movimientos trazables, garantizando el control del efectivo y otros medios de pago.

---

# Responsabilidad

- Administrar aperturas y cierres de caja.
- Registrar ingresos y salidas de dinero.
- Registrar arqueos.
- Mantener el historial de movimientos.
- Exponer el saldo calculado para consulta.

---

# No es responsabilidad

- Registrar ventas.
- Administrar inventario.
- Crear clientes.
- Administrar productos.
- Modificar créditos.

---

# Aggregate Root

## Caja

La Caja representa una sesión de operación de una caja registradora.

---

# Entidades

- Caja
- MovimientoCaja
- ArqueoCaja

---

# Value Objects

- Monto
- TipoMovimiento
- FormaPago
- DiferenciaArqueo

---

# Casos de Uso

- Abrir caja.
- Registrar ingreso.
- Registrar salida.
- Registrar gasto.
- Registrar retiro.
- Registrar arqueo.
- Cerrar caja.
- Consultar historial.

---

# Estados

- Cerrada
- Abierta

Los movimientos registrados son inmutables.

---

# Eventos del Dominio

- CajaAbierta
- MovimientoCajaRegistrado
- ArqueoRealizado
- CajaCerrada

---

# Relaciones

## Recibe solicitudes de

- Ventas
- Crédito

## Publica eventos para

- Reportes
- Auditoría
- Sincronización

---

# Reglas aplicables

Este dominio se rige por:

- RN-500
- RN-501
- RN-502
- RN-503

---

# Arquitectura

El saldo de caja es un dato derivado de los movimientos registrados.

Ningún dominio puede modificar directamente el saldo.

Toda operación monetaria debe registrarse mediante un MovimientoCaja.

---

# Preparado para futuras versiones

La arquitectura permitirá incorporar:

- Múltiples cajas registradoras.
- Múltiples cajeros.
- Cambios de turno.
- Diversos métodos de pago.
- Múltiples monedas.
- Integración con terminales de pago.

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
- Toda operación monetaria genera un MovimientoCaja.
- Mantener la lógica en Domain/Application.
- Respetar RN-500 a RN-503.

---

# Observaciones

El dominio Caja administra exclusivamente el flujo de dinero. Las ventas, créditos y otros dominios deben solicitar operaciones a Caja, preservando el desacoplamiento entre contextos y garantizando trazabilidad completa.