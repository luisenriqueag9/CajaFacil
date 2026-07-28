# 06_REGLAS_DE_NEGOCIO.md

**Versión:** 1.0  
**Estado:** Aprobado (Arquitectura)  
**Última actualización:** 2026-07-19  
**Documento:** Reglas de Negocio

# Reglas de Negocio de CajaFácil

## Objetivo

Centralizar las reglas de negocio globales que gobiernan CajaFácil.

Este documento es la fuente oficial de todas las reglas funcionales del sistema. Ningún dominio deberá redefinir una regla aquí descrita; únicamente podrá referenciarla.

---

# Principios Generales

## RN-001
Toda información pertenece a una Empresa.

## RN-002
Toda operación debe ejecutarse por un Usuario autenticado.

## RN-003
Toda operación crítica debe respetar permisos.

## RN-004
Nunca se elimina información con historial; se conserva mediante estados y auditoría.

## RN-005
Toda operación crítica debe ser trazable.

---

# Productos

## RN-100
Un producto pertenece a una Empresa.

## RN-101
El código interno es único por Empresa.

## RN-102
Los productos con historial nunca se eliminan físicamente.

## RN-103
Los productos inactivos no pueden venderse.

## RN-104
El Dominio Producto administra únicamente información maestra.

---

# Inventario

## RN-200
El inventario nunca se modifica directamente.

## RN-201
Todo cambio de existencias genera un Movimiento de Inventario.

## RN-202
Nunca se ejecutará una actualización directa del stock como mecanismo de negocio.

## RN-203
Las existencias se calculan a partir de sus movimientos.

## RN-204
Toda merma genera un Movimiento de Inventario.

---

# Compras

## RN-300
Toda compra confirmada genera Movimientos de Inventario.

## RN-301
Una compra confirmada conserva su historial.

## RN-302
Compras consulta el catálogo, pero no modifica directamente los productos.

---

# Ventas

## RN-400
Toda venta confirmada genera Movimientos de Inventario.

## RN-401
Toda venta confirmada genera Movimientos de Caja.

## RN-402
Las ventas históricas no cambian su importe.

## RN-403
Las anulaciones preservan el historial.

## RN-404
Las ventas de contado utilizan Consumidor Final cuando el cliente no se identifica.

---

# Caja

## RN-500
El saldo de caja nunca se modifica directamente.

## RN-501
Todo cambio de dinero genera un Movimiento de Caja.

## RN-502
Toda caja debe abrirse antes de registrar ventas.

## RN-503
Toda caja debe cerrarse mediante un proceso formal.

---

# Clientes y Crédito

## RN-600
El cliente es opcional para ventas de contado.

## RN-601
El cliente es obligatorio para créditos.

## RN-602
Todo abono disminuye el saldo del crédito mediante un movimiento registrado.

---

# Auditoría

## RN-700
Las operaciones críticas generan auditoría.

## RN-701
La auditoría es inmutable.

---

# Sincronización

## RN-800
Toda entidad sincronizable posee UUID.

## RN-801
Toda entidad sincronizable posee versión.

## RN-802
La sincronización nunca bloquea la operación local.

---

# Seguridad

## RN-900
Ocultar opciones en la interfaz no reemplaza la validación de permisos.

## RN-901
Las reglas de autorización se validan en la lógica del negocio.

---

# Referencias

Los documentos de dominio deberán referenciar estas reglas por identificador (RN-xxx) en lugar de duplicar su contenido.

---

# Reglas para Antigravity

- No duplicar reglas de negocio.
- Referenciar los identificadores RN correspondientes.
- No implementar lógica fuera de Domain/Application.
- Respetar la trazabilidad y las transacciones.

---

# Observaciones

Toda modificación de estas reglas requiere una Decisión Arquitectónica (ADR). Los cambios deben evaluarse por su impacto en la documentación, el código, la base de datos y la sincronización.