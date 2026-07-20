# 08_DOMINIO_COMPRAS.md

**Versión:** 1.0
**Estado:** Aprobado (Arquitectura)
**Última actualización:** 2026-07-19
**Documento:** Dominio Compras

# Dominio Compras

## Objetivo

Administrar el ciclo de vida de las compras de mercancía y registrar su recepción de forma consistente con la arquitectura de CajaFácil.

---

# Responsabilidad

- Registrar compras.
- Administrar proveedores.
- Registrar recepción de mercancía.
- Mantener el historial de compras.
- Proporcionar información de costos al dominio de Inventario.

---

# No es responsabilidad

- Modificar existencias directamente.
- Crear productos.
- Administrar caja.
- Registrar ventas.
- Administrar clientes.

---

# Aggregate Root

## Compra

La Compra representa la transacción comercial entre la empresa y un proveedor.

---

# Entidades

- Compra
- DetalleCompra
- Proveedor
- RecepcionCompra

---

# Value Objects

- PrecioCompra
- Cantidad
- Descuento
- Impuesto
- NúmeroDocumento

---

# Casos de Uso

- Registrar compra.
- Editar compra en borrador.
- Confirmar compra.
- Registrar recepción.
- Anular compra.
- Consultar historial.

---

# Estados

- Borrador
- Confirmada
- Anulada

La arquitectura queda preparada para soportar recepciones parciales en versiones futuras.

---

# Eventos del Dominio

- CompraRegistrada
- CompraConfirmada
- CompraAnulada
- RecepcionRegistrada

---

# Relaciones

## Consulta

- Producto
- Proveedor

## Solicita

- Inventario.RegistrarEntrada()

## Publica eventos para

- Reportes
- Sincronización

---

# Reglas aplicables

Este dominio se rige por:

- RN-300
- RN-301
- RN-302

---

# Arquitectura

Compras nunca modifica existencias directamente.

Toda recepción confirmada solicita al dominio Inventario el registro de un MovimientoInventario.

---

# Preparado para futuras versiones

La arquitectura permitirá incorporar:

- Recepciones parciales.
- Órdenes de compra.
- Compras internacionales.
- Costos adicionales (flete, seguros, impuestos).
- Múltiples proveedores por producto.
- Flujo de aprobación de compras.

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

- No modificar inventario directamente.
- Toda compra confirmada debe generar la solicitud de entrada a Inventario.
- Mantener la lógica en Domain/Application.
- Respetar RN-300 a RN-302.

---

# Observaciones

El dominio Compras administra exclusivamente el proceso comercial de adquisición de mercancía. La actualización de existencias pertenece al dominio Inventario, manteniendo el desacoplamiento entre contextos y facilitando la evolución del sistema.