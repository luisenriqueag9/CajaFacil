# 03_DICCIONARIO_DEL_NEGOCIO.md

**Versión:** 2.0  
**Estado:** Aprobado (Revisión Arquitectónica)  
**Última actualización:** 2026-07-19  
**Documento:** Diccionario del Negocio (Lenguaje Ubicuo)

# Diccionario del Negocio de CajaFácil

## Objetivo

Definir el lenguaje oficial de CajaFácil para que negocio, arquitectura, desarrollo, base de datos, documentación y pruebas utilicen exactamente los mismos conceptos.

Este documento constituye el **Lenguaje Ubicuo (Ubiquitous Language)** del proyecto.

---

# Principios

- Un concepto tiene un único nombre oficial.
- Evitar sinónimos.
- El lenguaje del negocio gobierna el diseño del software.
- Toda nueva funcionalidad deberá utilizar los términos definidos aquí.
- Ningún término oficial podrá cambiarse sin evaluar su impacto.

---

# Organización por dominios

## Empresa

### Empresa

**Definición**

Negocio propietario de la información almacenada en CajaFácil.

**Responsabilidades**

- Configuración general.
- Propiedad de los datos.
- Aislamiento multiempresa.

**Relacionado con**

Usuarios, Productos, Ventas, Compras, Caja.

---

## Seguridad

### Usuario

Persona autorizada para utilizar el sistema.

### Rol

Conjunto de permisos asignados a un usuario.

### Permiso

Autorización para ejecutar una acción específica.

---

## Catálogo

### Producto

Artículo comercial que puede comprarse, almacenarse y venderse.

**Genera**

- Movimientos de inventario (indirectamente mediante operaciones).

**No debe**

- Modificar existencias directamente.

**Relacionado con**

- Categoría
- Marca
- Unidad
- Proveedor

**Sinónimos prohibidos**

Artículo, Ítem, Mercancía.

---

### Categoría

Agrupa productos con características similares.

### Marca

Fabricante o identificación comercial de un producto.

### Unidad de Medida

Unidad utilizada para controlar cantidades.

Ejemplos:

- Unidad
- Libra
- Kilogramo
- Litro

---

## Inventario

### Inventario

Conjunto de existencias administradas por el sistema.

### Existencia

Cantidad disponible de un producto.

### Movimiento de Inventario

Registro histórico que incrementa o disminuye existencias.

**Ejemplos**

- Compra
- Venta
- Ajuste
- Merma
- Devolución

### Merma

Pérdida de inventario por daño, vencimiento, robo u otras causas distintas a una venta.

### Ajuste

Corrección autorizada del inventario mediante un movimiento registrado.

---

## Compras

### Compra

Operación mediante la cual ingresan productos al inventario.

### Proveedor

Persona o empresa que suministra productos al negocio.

---

## Ventas

### Venta

Operación mediante la cual se entregan productos a cambio de un pago.

**Genera**

- Movimiento de Inventario.
- Movimiento de Caja.
- Auditoría cuando corresponda.

**No debe**

- Modificar existencias directamente.
- Modificar saldos de caja directamente.

### Cliente

Persona o empresa que realiza una compra.

En ventas de contado podrá utilizarse el cliente genérico **Consumidor Final**.

### Crédito

Venta cuyo pago queda pendiente total o parcialmente.

### Abono

Pago aplicado para disminuir el saldo pendiente de un crédito.

### Comprobante

Documento emitido como resultado de una venta.

Puede representarse como:

- Ticket
- Factura
- Recibo

El término oficial del negocio será **Comprobante**.

---

## Caja

### Caja

Sesión de trabajo donde se registran operaciones monetarias.

### Apertura de Caja

Inicio oficial de una sesión de caja.

### Cierre de Caja

Finalización oficial de una sesión de caja.

### Movimiento de Caja

Registro histórico que incrementa o disminuye el dinero administrado por una caja.

### Arqueo

Comparación entre el dinero esperado y el dinero contado físicamente.

---

## Reportes

### Reporte

Documento que resume información del negocio.

---

## Auditoría

### Auditoría

Registro histórico e inmutable de acciones relevantes.

Nunca debe eliminarse.

---

## Respaldo y Sincronización

### Respaldo

Copia de seguridad de la información.

### Sincronización

Proceso que intercambia información entre SQLite y PostgreSQL.

---

## Estados

### Activo

Elemento disponible para operar.

### Inactivo

Elemento conservado por historial, pero no disponible para nuevas operaciones.

---

# Sinónimos prohibidos

| Término oficial | Evitar |
|-----------------|---------|
| Producto | Artículo, Ítem, Mercancía |
| Venta | Transacción comercial |
| Compra | Adquisición |
| Comprobante | Ticket, Factura (como término genérico) |
| Movimiento de Inventario | Cambio de stock |
| Movimiento de Caja | Cambio de saldo |

---

# Relación entre conceptos

- Una Empresa posee Usuarios.
- Una Empresa posee Productos.
- Un Producto pertenece a una Categoría, Marca y Unidad.
- Una Compra genera Movimientos de Inventario.
- Una Venta genera Movimientos de Inventario.
- Una Venta genera Movimientos de Caja.
- Un Crédito puede recibir Abonos.
- Una Caja registra Movimientos de Caja.
- La Auditoría registra operaciones críticas.

---

# Observaciones

Este documento es la referencia oficial del lenguaje utilizado en CajaFácil.

Toda documentación, código, base de datos y generación automática con Antigravity deberá utilizar estos términos de forma consistente.