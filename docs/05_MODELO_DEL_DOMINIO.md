# 05_MODELO_DEL_DOMINIO.md

**Versión:** 1.0
**Estado:** Aprobado (Arquitectura)
**Última actualización:** 2026-07-19
**Documento:** Modelo del Dominio

# Modelo del Dominio de CajaFácil

## Objetivo

Definir la estructura oficial del dominio de negocio de CajaFácil utilizando principios de Domain-Driven Design (DDD).

Este documento establece los límites de cada contexto, sus responsabilidades, relaciones y reglas para garantizar una arquitectura mantenible, escalable y preparada para SaaS.

---

# Principios

- El negocio gobierna el diseño.
- Cada contexto tiene una única responsabilidad.
- Los contextos se comunican mediante casos de uso o eventos.
- Ningún contexto modifica directamente los datos internos de otro.
- Todo dato maestro tiene un único propietario.

---

# Mapa del Dominio

```text
Empresa
│
├── Seguridad
│   ├── Usuario
│   ├── Rol
│   └── Permiso
│
├── Catálogo
│   ├── Producto
│   ├── Categoría
│   ├── Marca
│   └── Unidad
│
├── Compras
│   ├── Compra
│   └── Proveedor
│
├── Inventario
│   ├── Existencia
│   ├── MovimientoInventario
│   └── Merma
│
├── Ventas
│   ├── Venta
│   └── Comprobante
│
├── Caja
│   ├── Caja
│   ├── MovimientoCaja
│   └── Arqueo
│
├── Clientes
│   ├── Cliente
│   └── Crédito
│
└── Reportes
```

---

# Bounded Contexts

## Empresa

Responsable de la configuración general y el aislamiento multiempresa.

**Aggregate Root**

- Empresa

---

## Seguridad

Responsable de autenticación, autorización y permisos.

**Aggregate Roots**

- Usuario
- Rol

---

## Catálogo

Responsable de los datos maestros de productos.

**Aggregate Root**

- Producto

Entidades relacionadas:

- Categoría
- Marca
- Unidad

---

## Compras

Gestiona el ingreso de mercancía.

**Aggregate Root**

- Compra

Entidades:

- Proveedor

Publica:

- CompraRegistrada

---

## Inventario

Administra únicamente existencias y movimientos.

**Aggregate Root**

- MovimientoInventario

Entidades:

- Existencia
- Merma

Publica:

- InventarioActualizado

---

## Ventas

Gestiona las ventas del negocio.

**Aggregate Root**

- Venta

Entidades:

- Comprobante

Publica:

- VentaConfirmada
- VentaAnulada

---

## Caja

Gestiona el flujo de dinero.

**Aggregate Root**

- Caja

Entidades:

- MovimientoCaja
- Arqueo

Publica:

- CajaAbierta
- CajaCerrada

---

## Clientes

Gestiona clientes y créditos.

**Aggregate Roots**

- Cliente
- Crédito

Publica:

- CreditoCreado
- AbonoRegistrado

---

## Reportes

Contexto de consulta.

No modifica información.

---

# Relaciones permitidas

- Compras → Inventario
- Ventas → Inventario
- Ventas → Caja
- Ventas → Clientes
- Inventario → Catálogo (solo lectura)
- Compras → Catálogo (solo lectura)
- Ventas → Catálogo (solo lectura)

---

# Relaciones prohibidas

- Inventario no modifica Producto.
- Caja no modifica Venta.
- Compras no modifica Existencias directamente.
- Ventas no modifica Caja directamente.
- Ningún contexto accede a tablas internas de otro.

---

# Eventos del Dominio

- ProductoCreado
- ProductoActualizado
- CompraRegistrada
- VentaConfirmada
- VentaAnulada
- InventarioActualizado
- CajaAbierta
- CajaCerrada
- CreditoCreado
- AbonoRegistrado

---

# Invariantes

- El inventario solo cambia mediante MovimientoInventario.
- La caja solo cambia mediante MovimientoCaja.
- Los productos con historial no se eliminan.
- Las ventas históricas nunca cambian de importe.
- Toda operación pertenece a una Empresa.

---

# Value Objects comunes

- Dinero
- Impuesto
- Precio
- Cantidad
- CódigoBarras
- Dirección
- Teléfono

---

# Servicios de Dominio

Cuando una regla involucre múltiples entidades deberá implementarse mediante un Servicio de Dominio, nunca dentro de la interfaz.

---

# Sincronización

Cada Aggregate Root deberá contar con:

- UUID global.
- Empresa propietaria.
- Fecha de creación.
- Fecha de modificación.
- Versión de sincronización.
- Estado de sincronización.

---

# Reglas para Antigravity

Toda generación automática deberá:

- Respetar los límites de cada contexto.
- No duplicar reglas de negocio.
- No acceder directamente a otro contexto.
- Implementar casos de uso por contexto.
- Mantener Aggregate Roots como único punto de modificación.

---

# Observaciones

Este documento constituye el mapa oficial del dominio de CajaFácil. Toda nueva funcionalidad deberá ubicarse dentro de un Bounded Context existente o justificar la creación de uno nuevo mediante una Decisión Arquitectónica (ADR).