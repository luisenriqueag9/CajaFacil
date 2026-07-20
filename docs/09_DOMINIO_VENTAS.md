# 09_DOMINIO_VENTAS.md

**Versión:** 1.0
**Estado:** Aprobado (Arquitectura)
**Última actualización:** 2026-07-19
**Documento:** Dominio Ventas

# Dominio Ventas

## Objetivo

Administrar el proceso completo de ventas de CajaFácil, coordinando los dominios involucrados sin asumir responsabilidades que pertenecen a otros contextos.

---

# Responsabilidad

- Registrar ventas.
- Gestionar el ciclo de vida de la venta.
- Calcular importes, descuentos e impuestos.
- Emitir comprobantes.
- Solicitar movimientos a Inventario y Caja.
- Iniciar el proceso de crédito cuando corresponda.

---

# No es responsabilidad

- Modificar existencias directamente.
- Modificar saldos de caja.
- Administrar productos.
- Administrar clientes.
- Administrar créditos.

---

# Aggregate Root

## Venta

La Venta representa la transacción comercial entre la empresa y el cliente.

---

# Entidades

- Venta
- DetalleVenta
- ComprobanteVenta

---

# Value Objects

- PrecioVenta
- Cantidad
- Descuento
- Impuesto
- FormaPago

---

# Casos de Uso

- Crear venta.
- Agregar productos.
- Confirmar venta.
- Anular venta.
- Emitir comprobante.
- Consultar historial.

---

# Estados

- Borrador
- Finalizada
- Anulada

Las ventas finalizadas son inmutables.

---

# Eventos del Dominio

- VentaConfirmada
- VentaAnulada
- ComprobanteEmitido

---

# Relaciones

## Consulta

- Producto
- Cliente

## Solicita

- Inventario.RegistrarSalida()
- Caja.RegistrarMovimiento()
- Credito.CrearCredito()

## Publica eventos para

- Reportes
- Auditoría
- Sincronización

---

# Reglas aplicables

Este dominio se rige por:

- RN-400
- RN-401
- RN-402
- RN-403
- RN-404

---

# Arquitectura

Ventas coordina el proceso comercial.

No modifica directamente Inventario, Caja ni Crédito; solicita operaciones a los dominios correspondientes.

---

# Preparado para futuras versiones

La arquitectura permitirá incorporar:

- Cotizaciones.
- Facturación electrónica.
- Múltiples formas de pago.
- Devoluciones.
- Apartados.
- Promociones.
- Programas de fidelización.
- Descuentos avanzados.

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

- No modificar Inventario ni Caja directamente.
- Mantener la lógica en Domain/Application.
- Respetar RN-400 a RN-404.
- Tratar la Venta como Aggregate Root.

---

# Observaciones

El dominio Ventas es el coordinador del proceso comercial. Su responsabilidad es orquestar la operación respetando los límites de cada Bounded Context, preservando la trazabilidad y facilitando la evolución futura del sistema.