# 04_DOMINIO_PRODUCTO.md

Versión: 1.0
Estado: Aprobado
Última actualización: 2026-07-18
Documento: Dominio Producto

# Dominio Producto

## Objetivo

Administrar toda la información relacionada con los productos comercializados por el negocio.

Este dominio será responsable de la creación, actualización, consulta y control de los productos, garantizando la integridad de su información y proporcionando los datos necesarios para los demás dominios del sistema.

---

# Responsabilidades

El dominio Producto será responsable de:

- Registrar productos.
- Modificar productos.
- Consultar productos.
- Activar productos.
- Desactivar productos.
- Administrar códigos de barras.
- Administrar precios.
- Administrar costos.
- Administrar impuestos.
- Administrar categorías.
- Administrar marcas.
- Administrar unidades de medida.
- Definir si un producto controla inventario.
- Definir si un producto permite cantidades decimales.
- Definir si un producto es perecedero.

---

# Lo que NO hace

Este dominio NO será responsable de:

- Descontar existencias.
- Aumentar existencias.
- Registrar compras.
- Registrar ventas.
- Registrar mermas.
- Calcular utilidades.
- Registrar movimientos de inventario.

Todas esas responsabilidades pertenecen a otros dominios.

---

# Entidad Principal

## Producto

Representa un artículo que puede comprarse, almacenarse y venderse.

---

# Atributos del Producto

Cada producto tendrá como mínimo los siguientes atributos:

- Id
- Código interno
- Nombre
- Descripción
- Categoría
- Marca
- Unidad de medida
- Precio de venta
- Costo
- Impuesto
- Existencia mínima
- Controla inventario (Sí/No)
- Permite cantidades decimales (Sí/No)
- Perecedero (Sí/No)
- Imagen
- Estado (Activo/Inactivo)
- Fecha de creación
- Fecha de modificación
- Usuario creador
- Usuario modificador

---

# Reglas de Negocio

## RN-001

Todo producto deberá tener un nombre.

---

## RN-002

Todo producto deberá tener un precio de venta mayor que cero.

---

## RN-003

Todo producto deberá pertenecer a una unidad de medida.

---

## RN-004

Un producto podrá tener uno o varios códigos de barras.

---

## RN-005

El código interno deberá ser único.

---

## RN-006

Un producto podrá desactivar el control de inventario.

Ejemplos:

- Servicio de instalación.
- Servicio técnico.
- Recarga telefónica.

---

## RN-007

Si el producto controla inventario, podrá tener existencia mínima.

---

## RN-008

Los productos con historial nunca podrán eliminarse físicamente.

Únicamente podrán desactivarse.

---

## RN-009

Un producto inactivo no podrá venderse.

---

## RN-010

Un producto perecedero podrá utilizar posteriormente fechas de vencimiento cuando esa funcionalidad sea incorporada.

---

# Casos de Uso

- Crear producto.
- Editar producto.
- Consultar producto.
- Buscar producto.
- Activar producto.
- Desactivar producto.
- Consultar precio.
- Consultar costo.
- Consultar códigos de barras.

---

# Validaciones

Antes de guardar un producto el sistema deberá validar:

- Nombre obligatorio.
- Precio válido.
- Unidad de medida obligatoria.
- Código interno único.
- Precio mayor que cero.
- Costo mayor o igual que cero.

---

# Eventos del Dominio

Este dominio podrá generar los siguientes eventos:

- ProductoCreado
- ProductoActualizado
- ProductoActivado
- ProductoDesactivado
- PrecioActualizado
- CostoActualizado

---

# Permisos

El sistema deberá controlar como mínimo los siguientes permisos:

- Crear productos.
- Modificar productos.
- Consultar productos.
- Cambiar precios.
- Cambiar costos.
- Activar productos.
- Desactivar productos.

---

# Auditoría

Las siguientes operaciones deberán registrarse:

- Creación.
- Modificación.
- Cambio de precio.
- Cambio de costo.
- Activación.
- Desactivación.

La auditoría deberá almacenar:

- Usuario.
- Fecha.
- Hora.
- Acción.
- Valor anterior.
- Valor nuevo.

---

# Relación con otros dominios

## Inventario

Consulta información del producto.

Nunca modifica productos.

---

## Compras

Consulta el costo.

Puede actualizar el costo promedio en futuras versiones.

---

## Ventas

Consulta:

- Nombre.
- Precio.
- Impuesto.
- Estado.
- Unidad.

Nunca modifica productos.

---

## Caja

No tiene relación directa.

---

## Clientes

No tiene relación directa.

---

# Consideraciones para Base de Datos

Tabla principal:

producto

Relaciones iniciales:

- categoria
- marca
- unidad_medida

Índices recomendados:

- codigo_interno
- nombre
- estado

---

# Consideraciones para API

Operaciones principales:

- Crear producto.
- Actualizar producto.
- Consultar producto.
- Buscar productos.
- Activar producto.
- Desactivar producto.

---

# Consideraciones para la Interfaz

La pantalla de productos deberá permitir:

- Buscar rápidamente.
- Crear productos.
- Editar productos.
- Activar o desactivar productos.
- Ver precio.
- Ver costo.
- Ver existencia (solo consulta).
- Ver estado.

---

# Decisiones Arquitectónicas

## DP-001

Los productos nunca serán eliminados físicamente cuando tengan historial.

Estado:

Aprobada.

---

## DP-002

El dominio Producto nunca modificará existencias.

Estado:

Aprobada.

---

## DP-003

El dominio Producto será únicamente responsable de la información maestra del producto.

Estado:

Aprobada.

---

# Pendientes para futuras versiones

- Productos compuestos.
- Kits.
- Variantes (talla, color).
- Lotes.
- Fechas de vencimiento.
- Múltiples listas de precios.
- Promociones.
- Precios por cliente.

---

# Observaciones

El dominio Producto representa el catálogo maestro del negocio.

Toda modificación relacionada con existencias deberá realizarse exclusivamente mediante el Dominio Inventario.

Este principio garantiza la integridad de la información y evita inconsistencias entre el catálogo de productos y el inventario.