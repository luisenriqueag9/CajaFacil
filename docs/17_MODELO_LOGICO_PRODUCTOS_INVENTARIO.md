# 17_MODELO_LOGICO_PRODUCTOS_INVENTARIO.md

Versión: 1.0

Estado: Aprobado

Última actualización: 2026-07-20

Documento: Modelo Lógico de Datos

---

# Objetivo

Definir el modelo lógico del dominio Productos e Inventario.

Este documento será la referencia oficial para el diseño de la base de datos, el backend, el frontend y la sincronización del módulo de productos e inventario.

No define tipos físicos de SQLite o PostgreSQL; define las entidades, atributos, relaciones y restricciones del dominio.

---

# Alcance

Este documento comprende las siguientes entidades:

- CategoriaProducto
- UnidadMedida
- Producto
- Proveedor
- MovimientoInventario

---

# Convenciones

## Tipos de entidades

### MASTER DATA

Información relativamente estable.

### CATÁLOGO

Información utilizada como referencia.

### TRANSACCIONAL

Información generada por las operaciones del negocio.

---

# Dominio Productos

---

# CategoriaProducto

## Descripción

Permite clasificar los productos del negocio.

---

## Tipo de entidad

CATÁLOGO

---

## Aggregate Root

CategoriaProducto

---

## Atributos del negocio

| Campo | Tipo | Obligatorio |
|--------|------|-------------|
| EmpresaId | UUID | Sí |
| Nombre | Texto(100) | Sí |
| Descripcion | Texto(200) | No |
| Activa | Boolean | Sí |

---

## Relaciones

- Empresa 1 → N Categorias
- CategoriaProducto 1 → N Productos

---

## Restricciones

- El nombre debe ser único dentro de la empresa.
- No puede eliminarse si existen productos asociados.

---

# UnidadMedida

## Descripción

Representa la unidad utilizada para controlar inventario y ventas.

Ejemplos:

- Unidad
- Caja
- Libra
- Kilogramo
- Litro
- Metro

---

## Tipo de entidad

CATÁLOGO

---

## Aggregate Root

UnidadMedida

---

## Atributos del negocio

| Campo | Tipo | Obligatorio |
|--------|------|-------------|
| EmpresaId | UUID | Sí |
| Nombre | Texto(60) | Sí |
| Abreviatura | Texto(10) | Sí |

---

## Relaciones

- UnidadMedida 1 → N Productos

---

## Restricciones

- La abreviatura debe ser única por empresa.

---

# Producto

## Descripción

Representa cualquier artículo que pueda comprarse, venderse o administrarse dentro del sistema.

---

## Tipo de entidad

MASTER DATA

---

## Aggregate Root

Producto

---

## Atributos del negocio

| Campo | Tipo | Obligatorio |
|--------|------|-------------|
| EmpresaId | UUID | Sí |
| CategoriaId | UUID | Sí |
| UnidadMedidaId | UUID | Sí |
| CodigoInterno | Texto(50) | Sí |
| CodigoBarras | Texto(50) | No |
| Nombre | Texto(200) | Sí |
| Descripcion | Texto(300) | No |
| Marca | Texto(100) | No |
| PrecioCompra | Dinero | Sí |
| PrecioVenta | Dinero | Sí |
| ManejaInventario | Boolean | Sí |
| PermiteStockNegativo | Boolean | No |
| Activo | Boolean | Sí |

---

## Atributos técnicos

| Campo | Tipo |
|--------|------|
| Id | UUID |
| Version | Integer |
| CreadoEn | DateTime UTC |
| ActualizadoEn | DateTime UTC |
| EstadoSincronizacion | Enum |

---

## Relaciones

- CategoriaProducto 1 → N Productos
- UnidadMedida 1 → N Productos
- Producto 1 → N MovimientoInventario
- Producto N → N Proveedores (mediante Compras)

---

## Restricciones

- El código interno debe ser único por empresa.
- El precio de venta no puede ser negativo.
- El precio de compra no puede ser negativo.
- Si ManejaInventario = No, no se generan movimientos de inventario.

---

## Observaciones

El stock NO se almacena en Producto.

El stock se calcula utilizando MovimientoInventario.

---

# Proveedor

## Descripción

Representa una empresa o persona que suministra productos.

---

## Tipo de entidad

MASTER DATA

---

## Aggregate Root

Proveedor

---

## Atributos del negocio

| Campo | Tipo | Obligatorio |
|--------|------|-------------|
| EmpresaId | UUID | Sí |
| Nombre | Texto(200) | Sí |
| RTN | Texto(30) | No |
| Telefono | Texto(30) | No |
| Correo | Email | No |
| Direccion | Texto(300) | No |
| Activo | Boolean | Sí |

---

## Relaciones

- Proveedor 1 → N Compras

---

## Restricciones

- El nombre del proveedor debe existir.

---

# Dominio Inventario

---

# MovimientoInventario

## Descripción

Representa cualquier entrada o salida de inventario.

Es la única entidad autorizada para modificar las existencias.

---

## Tipo de entidad

TRANSACCIONAL

---

## Aggregate Root

MovimientoInventario

---

## Atributos del negocio

| Campo | Tipo | Obligatorio |
|--------|------|-------------|
| EmpresaId | UUID | Sí |
| ProductoId | UUID | Sí |
| TipoMovimiento | Enum | Sí |
| Cantidad | Decimal | Sí |
| DocumentoOrigen | Texto(50) | Sí |
| FechaMovimiento | DateTime | Sí |
| Observaciones | Texto(300) | No |

---

## Relaciones

- Producto 1 → N MovimientoInventario

---

## Restricciones

- Todo movimiento pertenece a un producto.
- La cantidad debe ser mayor que cero.
- No se permite modificar un movimiento confirmado.

---

## Observaciones

Las existencias siempre se calculan sumando entradas y restando salidas.

Nunca se actualizará directamente un campo llamado Stock.

---

# Resumen del dominio

| Entidad | Tipo |
|----------|------|
| CategoriaProducto | CATÁLOGO |
| UnidadMedida | CATÁLOGO |
| Producto | MASTER DATA |
| Proveedor | MASTER DATA |
| MovimientoInventario | TRANSACCIONAL |

---

# Conclusión

El dominio Productos e Inventario establece las bases para controlar los artículos comercializados por la empresa.

Toda modificación de existencias se realizará exclusivamente mediante MovimientoInventario, garantizando trazabilidad, auditoría y compatibilidad con la arquitectura Offline First.