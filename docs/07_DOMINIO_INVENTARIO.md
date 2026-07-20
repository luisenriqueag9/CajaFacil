# 07_DOMINIO_INVENTARIO.md

**Versión:** 1.0
**Estado:** Aprobado (Arquitectura)
**Última actualización:** 2026-07-19
**Documento:** Dominio Inventario

# Dominio Inventario

## Objetivo

Administrar las existencias y todos los movimientos de inventario de CajaFácil.

El dominio de Inventario es el único responsable del estado de las existencias. Ningún otro dominio puede modificar el stock directamente.

---

# Responsabilidad

- Mantener las existencias.
- Registrar movimientos de inventario.
- Gestionar ajustes.
- Gestionar mermas.
- Gestionar devoluciones que afecten existencias.
- Exponer existencias disponibles para consulta.

---

# No es responsabilidad

- Crear productos.
- Registrar compras.
- Registrar ventas.
- Administrar caja.
- Administrar clientes.

---

# Aggregate Root

## MovimientoInventario

Todo cambio en las existencias debe representarse mediante un MovimientoInventario.

---

# Entidades

- Existencia
- MovimientoInventario
- Merma
- AjusteInventario

---

# Value Objects

- Cantidad
- UnidadMedida
- MotivoMovimiento
- Ubicación (preparado para futuras versiones)

---

# Casos de Uso

- Registrar entrada por compra.
- Registrar salida por venta.
- Registrar ajuste.
- Registrar merma.
- Registrar devolución.
- Consultar existencias.
- Consultar historial de movimientos.

---

# Eventos del Dominio

- InventarioActualizado
- MermaRegistrada
- AjusteInventarioRegistrado

---

# Relaciones

## Consume información de

- Producto (solo lectura)

## Recibe solicitudes de

- Compras
- Ventas

## Publica eventos para

- Reportes
- Sincronización

---

# Reglas aplicables

Este dominio se rige por:

- RN-200
- RN-201
- RN-202
- RN-203
- RN-204

---

# Arquitectura

Las existencias son un dato derivado de los movimientos registrados.

No se debe implementar lógica de negocio basada en modificar directamente el campo de stock.

---

# Preparado para futuras versiones

La arquitectura permitirá incorporar sin romper compatibilidad:

- Lotes.
- Fechas de vencimiento.
- Números de serie.
- Múltiples bodegas.
- Reservas de inventario.
- Transferencias entre sucursales.

Estas capacidades podrán habilitarse gradualmente sin modificar el modelo principal.

---

# Sincronización

Toda entidad sincronizable deberá incluir:

- UUID
- Empresa
- Fecha de creación
- Fecha de modificación
- Versión
- Estado de sincronización

---

# Reglas para Antigravity

- No modificar existencias directamente.
- Toda operación genera MovimientoInventario.
- Mantener la lógica en Domain/Application.
- Respetar las reglas RN-200 a RN-204.

---

# Observaciones

Inventario constituye uno de los dominios centrales de CajaFácil. Su diseño prioriza consistencia, trazabilidad y evolución futura manteniendo una implementación inicial simple y orientada a negocios pequeños.