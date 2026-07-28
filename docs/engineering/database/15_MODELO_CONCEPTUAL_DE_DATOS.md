# 15_MODELO_CONCEPTUAL_DE_DATOS.md

**Versión:** 1.0
**Estado:** Aprobado (Arquitectura)
**Última actualización:** 2026-07-19
**Documento:** Modelo Conceptual de Datos

# Objetivo

Definir el modelo conceptual del negocio que servirá como puente entre el modelo de dominio (DDD) y el diseño físico de la base de datos.

---

# Principios

- El modelo representa conceptos del negocio, no tablas.
- Cada entidad pertenece a un único Aggregate Root.
- Toda entidad pertenece exactamente a una Empresa.
- Las relaciones siguen los límites de los Bounded Contexts.

---

# Entidades principales

## Empresa
Propietaria de toda la información del sistema.

## Sucursal
Unidad operativa perteneciente a una Empresa.

## Usuario
Persona autorizada para utilizar el sistema.

## Rol
Conjunto de permisos asignables a usuarios.

## Producto
Artículo comercializable.

## Categoría
Agrupa productos con características comunes.

## Proveedor
Entidad que suministra productos.

## Compra
Registro de adquisición de mercancía.

## DetalleCompra
Línea individual de una compra.

## MovimientoInventario
Evento que modifica existencias.

## Venta
Transacción comercial con un cliente o consumidor final.

## DetalleVenta
Línea individual de una venta.

## Caja
Sesión de operación de una caja registradora.

## MovimientoCaja
Movimiento monetario asociado a una caja.

## Cliente
Persona o empresa que compra al crédito o requiere identificación.

## Crédito
Obligación de pago generada por una venta.

## AbonoCredito
Pago aplicado a un crédito.

---

# Relaciones principales

- Empresa 1 ── N Sucursal
- Empresa 1 ── N Usuario
- Empresa 1 ── N Producto
- Empresa 1 ── N Compra
- Empresa 1 ── N Venta
- Empresa 1 ── N Caja
- Empresa 1 ── N Cliente

- Compra 1 ── N DetalleCompra
- Venta 1 ── N DetalleVenta
- Producto 1 ── N MovimientoInventario
- Caja 1 ── N MovimientoCaja
- Cliente 1 ── N Crédito
- Crédito 1 ── N AbonoCredito

---

# Ownership

- Empresa es propietaria de todos los datos.
- Compra es propietaria de DetalleCompra.
- Venta es propietaria de DetalleVenta.
- Crédito es propietario de AbonoCredito.
- Caja es propietaria de MovimientoCaja.

---

# Restricciones conceptuales

- No existen productos sin Empresa.
- No existen ventas sin al menos un detalle.
- No existen compras sin al menos un detalle.
- No existen créditos sin una venta de origen.
- Los movimientos de inventario nunca existen sin un producto.
- Los movimientos de caja nunca existen sin una caja.

---

# Datos derivados

No se almacenan directamente:

- Existencias.
- Saldo de caja.
- Saldo del crédito.

Se calculan a partir de sus movimientos.

---

# Preparado para evolución

El modelo soporta:

- Multiempresa.
- Múltiples sucursales.
- Múltiples cajas.
- Múltiples cajeros.
- Sincronización offline.
- Expansión internacional.

---

# Conclusión

Este modelo conceptual constituye la referencia para el diseño lógico y físico de la base de datos. Cualquier cambio estructural deberá realizarse primero aquí y posteriormente reflejarse en el diseño de SQLite y PostgreSQL.