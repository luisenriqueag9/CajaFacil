# 04_DOMINIO_PRODUCTO.md

**Versión:** 2.0  
**Estado:** Aprobado (Revisión Arquitectónica)  
**Última actualización:** 2026-07-19  
**Documento:** Dominio Producto

# Dominio Producto

## Objetivo

El Dominio Producto administra el **catálogo maestro** de productos de CajaFácil.

Su responsabilidad es mantener la información comercial de los productos de forma consistente, independiente del inventario, las compras y las ventas.

El dominio Producto **no administra existencias** ni dinero.

---

# Propósito dentro de la arquitectura

Producto es un **Maestro de Datos (Master Data)**.

Otros dominios consultan esta información, pero no la modifican directamente.

Este dominio es la única fuente autorizada para:

- Nombre del producto.
- Código interno.
- Códigos de barras.
- Categoría.
- Marca.
- Unidad de medida.
- Precio de venta.
- Configuración comercial.

---

# Aggregate Root

**Producto**

Toda modificación deberá realizarse a través del Aggregate Root Producto.

---

# Responsabilidades

- Crear productos.
- Actualizar productos.
- Consultar productos.
- Activar y desactivar productos.
- Administrar códigos de barras.
- Administrar precios de venta.
- Administrar costo de referencia.
- Administrar impuestos.
- Administrar categoría, marca y unidad.
- Definir si controla inventario.
- Definir si permite cantidades decimales.
- Definir si es perecedero.

---

# Responsabilidades prohibidas

Este dominio nunca deberá:

- Modificar existencias.
- Registrar compras.
- Registrar ventas.
- Registrar movimientos de inventario.
- Registrar movimientos de caja.
- Calcular utilidades históricas.
- Realizar arqueos.
- Registrar créditos.

---

# Entidades

## Producto (Aggregate Root)

Representa un artículo comercial disponible para compra y/o venta.

## Código de Barras

Permite asociar uno o varios códigos de barras a un mismo producto.

---

# Value Objects

- Precio
- Costo
- Impuesto
- Unidad de Medida

---

# Atributos mínimos del Producto

- Id global (UUID)
- Id local
- Empresa
- Código interno
- Nombre
- Descripción
- Categoría
- Marca
- Unidad de medida
- Precio de venta
- Costo de referencia
- Impuesto
- Existencia mínima
- Controla inventario
- Permite cantidades decimales
- Perecedero
- Imagen
- Estado
- Fecha de creación
- Fecha de modificación
- Usuario creador
- Usuario modificador
- Versión para sincronización

---

# Reglas de negocio

## RN-001
Todo producto debe pertenecer a una empresa.

## RN-002
Todo producto debe tener un nombre.

## RN-003
Todo producto debe tener una unidad de medida.

## RN-004
El precio de venta debe ser mayor que cero.

## RN-005
El costo nunca puede ser negativo.

## RN-006
El código interno debe ser único por empresa.

## RN-007
Un producto puede tener múltiples códigos de barras.

## RN-008
Los productos con historial nunca se eliminan físicamente.

## RN-009
Los productos inactivos no pueden venderse.

## RN-010
Si controla inventario podrá definir existencia mínima.

## RN-011
El costo almacenado es únicamente una referencia comercial. El historial pertenece al dominio Compras.

## RN-012
Cambiar el precio no modifica ventas históricas.

---

# Casos de uso

- CrearProducto
- ActualizarProducto
- ConsultarProducto
- BuscarProductos
- ActivarProducto
- DesactivarProducto
- CambiarPrecio
- CambiarCostoReferencia
- AgregarCodigoBarras
- EliminarCodigoBarras

---

# Validaciones

- Nombre obligatorio.
- Unidad obligatoria.
- Precio válido.
- Costo válido.
- Código interno único por empresa.
- Categoría obligatoria.
- Marca opcional.
- Imagen opcional.

---

# Eventos de dominio

- ProductoCreado
- ProductoActualizado
- ProductoActivado
- ProductoDesactivado
- PrecioProductoActualizado
- CostoReferenciaActualizado
- CodigoBarrasAgregado

---

# Permisos

- Crear productos.
- Modificar productos.
- Consultar productos.
- Cambiar precios.
- Cambiar costos.
- Activar productos.
- Desactivar productos.

---

# Auditoría

Registrar:

- Creación.
- Modificación.
- Cambio de precio.
- Cambio de costo.
- Cambio de categoría.
- Cambio de marca.
- Activación.
- Desactivación.

Cada registro deberá almacenar:

- Empresa
- Usuario
- Fecha y hora
- Acción
- Valor anterior
- Valor nuevo

---

# Relaciones con otros dominios

## Inventario

Consulta productos.

Nunca modifica productos.

## Compras

Consulta el catálogo y puede solicitar la actualización del costo de referencia mediante un caso de uso autorizado.

## Ventas

Consulta precio, impuesto, estado y configuración del producto.

Nunca modifica productos.

## Caja

Sin relación directa.

## Clientes

Sin relación directa.

---

# Persistencia

## Tabla principal

producto

## Tablas relacionadas

- producto_codigo_barra
- categoria
- marca
- unidad_medida

## Índices recomendados

- empresa_id + codigo_interno (único)
- empresa_id + nombre
- estado

---

# API

Operaciones:

- Crear
- Actualizar
- Consultar
- Buscar
- Activar
- Desactivar

---

# Interfaz

Debe permitir:

- Búsqueda inmediata.
- Escáner de código de barras.
- Activar/desactivar.
- Vista rápida de precio.
- Vista rápida de costo.
- Estado.
- Indicador de control de inventario.

---

# Decisiones arquitectónicas

## DP-001

Los productos nunca se eliminan físicamente cuando existe historial.

## DP-002

El Dominio Producto nunca modifica existencias.

## DP-003

Producto es un Maestro de Datos.

## DP-004

Todo cambio deberá realizarse únicamente mediante el Aggregate Root Producto.

## DP-005

Los demás dominios consumen Producto mediante casos de uso o repositorios del dominio, nunca mediante acceso directo a la base de datos.

---

# Evolución futura

- Productos compuestos.
- Kits.
- Variantes.
- Lotes.
- Series.
- Fechas de vencimiento.
- Múltiples listas de precios.
- Promociones.
- Precios por cliente.
- Precios por sucursal.

---

# Reglas para Antigravity

Al generar código deberá respetarse:

- Producto es Aggregate Root.
- Ninguna operación modifica inventario desde este dominio.
- Todo acceso se realiza mediante casos de uso.
- Los eventos del dominio son el mecanismo oficial para comunicar cambios.
- Nunca duplicar reglas de negocio en Presentation o Infrastructure.

---

# Observaciones

Producto es un dominio maestro. La información transaccional pertenece a Inventario, Compras, Ventas y Caja. Esta separación garantiza coherencia, facilita la sincronización Offline First y reduce el acoplamiento entre módulos.