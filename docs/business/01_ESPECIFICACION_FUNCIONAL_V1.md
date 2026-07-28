# 01_ESPECIFICACION_FUNCIONAL_V1.md

**Versión:** 1.1  
**Estado:** ✅ APROBADO  
**Última actualización:** 2026-07-19  
**Documento:** Especificación Funcional

# Especificación Funcional de CajaFácil 1.1

## Alcance de esta especificación

La primera versión estará enfocada principalmente en:

- Pulperías.
- Minisúper.
- Supermercados pequeños.
- Ferreterías.
- Tiendas de conveniencia.

El sistema deberá ser rápido, modular, fácil de aprender, operar sin conexión permanente a Internet y funcionar como una plataforma SaaS multiempresa.

---

# Objetivo principal

Permitir administrar de forma confiable:

- Empresas
- Usuarios
- Productos
- Categorías
- Marcas
- Unidades
- Proveedores
- Compras
- Inventario
- Caja
- Ventas
- Clientes opcionales
- Crédito
- Reportes
- Auditoría
- Respaldos

---

# Plataforma Multiempresa

CajaFácil permitirá administrar múltiples empresas de forma completamente aislada.

Cada empresa tendrá usuarios, productos, inventario, reportes, configuración y respaldos propios.

La información nunca podrá mezclarse entre empresas.

---

# Perfil del negocio

El sistema permitirá seleccionar un perfil inicial (Pulpería, Minisúper, Ferretería, Tienda de conveniencia, etc.). El perfil únicamente configurará valores iniciales; no modificará la arquitectura.

---

# Requisitos funcionales

## Empresas y configuración
- Nombre comercial
- Razón social
- RTN
- Dirección
- Teléfono
- Correo
- Logo
- Moneda
- Impuestos
- Formato del comprobante

## Usuarios
Roles:
- Administrador
- Supervisor
- Cajero

Permisos configurables para ventas, compras, descuentos, inventario, caja, reportes y administración.

## Productos
Cada producto podrá tener:
- Nombre
- Descripción
- Categoría
- Marca
- Código interno
- Código de barras principal
- Códigos alternativos
- Unidad
- Precio
- Costo
- Impuesto
- Existencia mínima
- Control de inventario
- Venta decimal
- Estado
- Perecedero
- Imagen

Los productos con historial nunca se eliminarán físicamente.

## Compras

Toda compra que afecte existencias deberá generar movimientos de inventario.

## Inventario

El inventario nunca se modificará directamente.

Todo cambio de existencias deberá generar un movimiento.

## Caja

El saldo de caja nunca se modificará directamente.

Toda variación deberá provenir de un movimiento autorizado.

## Ventas

Permitirá venta rápida, código de barras, búsqueda, venta decimal, descuentos autorizados, múltiples métodos de pago, impresión, reimpresión, devoluciones y anulación controlada.

Las ventas de contado utilizarán Consumidor Final por defecto.

## Clientes

Solo serán obligatorios para crédito, facturas nominativas o cuando el negocio lo requiera.

## Crédito

Venta al crédito, abonos, cuentas por cobrar y estado de cuenta.

## Métodos de pago

- Efectivo
- Tarjeta
- Transferencia
- Crédito
- Pago combinado

## Reportes

Ventas, compras, inventario, caja, mermas, productos, cuentas por cobrar y utilidad estimada.

## Auditoría

Registrará usuario, acción, fecha, entidad, registro afectado, cambios, equipo, caja y sucursal cuando aplique.

## Funcionamiento sin Internet

Las ventas, compras, caja e inventario deberán continuar funcionando sin conexión. La sincronización ocurrirá posteriormente.

## Respaldos

Respaldos manuales, automáticos, restauración, historial, copia cifrada en la nube y verificación de integridad.

## Rendimiento

- Inicio rápido
- Búsquedas prácticamente inmediatas
- Operaciones críticas mediante transacciones
- Interfaz fluida

## Reglas generales del negocio

- Ningún producto puede existir sin empresa.
- Ningún producto puede existir sin categoría.
- Ningún producto puede existir sin marca.
- Ningún producto puede existir sin unidad.
- El inventario nunca cambia sin un movimiento.
- La caja nunca cambia sin un movimiento.
- Los catálogos no se eliminan físicamente.
- Debe conservarse el historial.
- El sistema debe operar sin Internet.

# Observaciones

Este documento define el alcance funcional y las principales reglas operativas de CajaFácil.