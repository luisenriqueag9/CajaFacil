# 03_DICCIONARIO_DEL_NEGOCIO.md

Versión: 1.0
Estado: Aprobado
Última actualización: 2026-07-18
Documento: Diccionario del Negocio

# Diccionario del Negocio

## Objetivo

Definir el lenguaje oficial de CajaFácil.

Este documento establece los términos que deberán utilizarse de forma consistente en la documentación, el código, la base de datos y la interfaz de usuario.

Su propósito es evitar ambigüedades y garantizar que todas las personas involucradas en el proyecto utilicen el mismo vocabulario.

---

# Principios

- Un concepto debe tener un único nombre oficial.
- Evitar sinónimos para el mismo concepto.
- La interfaz utilizará términos sencillos para el comerciante.
- El código utilizará nombres claros y consistentes.
- La base de datos utilizará nombres en singular y en minúsculas.

---

# Términos oficiales

## Empresa

Representa el negocio propietario de la información almacenada en CajaFácil.

Ejemplos:

- Pulpería El Centro
- Ferretería Ortiz
- Minisúper López

---

## Usuario

Persona autorizada para utilizar el sistema.

Ejemplos:

- Administrador
- Supervisor
- Cajero

---

## Rol

Conjunto de permisos asignados a un usuario.

Ejemplos:

- Administrador
- Supervisor
- Cajero

---

## Permiso

Autorización para realizar una acción específica dentro del sistema.

Ejemplos:

- Registrar ventas
- Cambiar precios
- Anular ventas

---

## Producto

Artículo comercial que puede comprarse, almacenarse o venderse.

Ejemplos:

- Coca-Cola 2 L
- Martillo
- Arroz

La palabra oficial será **Producto**.

No se utilizarán términos como:

- Artículo
- Ítem
- Mercancía

---

## Categoría

Grupo utilizado para clasificar productos.

Ejemplos:

- Bebidas
- Abarrotes
- Herramientas

---

## Marca

Fabricante o marca comercial del producto.

Ejemplos:

- Coca-Cola
- Bosch
- Corona

---

## Unidad de medida

Unidad utilizada para controlar cantidades.

Ejemplos:

- Unidad
- Libra
- Kilogramo
- Litro

---

## Inventario

Conjunto de existencias disponibles de los productos.

---

## Movimiento de inventario

Registro que modifica la existencia de un producto.

Ejemplos:

- Compra
- Venta
- Ajuste
- Merma

---

## Merma

Pérdida de inventario por causas distintas a una venta.

Ejemplos:

- Producto vencido
- Producto roto
- Robo

---

## Compra

Registro mediante el cual ingresan productos al inventario provenientes de un proveedor.

---

## Proveedor

Persona o empresa que suministra productos al negocio.

---

## Venta

Operación mediante la cual uno o varios productos son entregados a un cliente a cambio de un pago.

---

## Cliente

Persona o empresa que realiza una compra.

En CajaFácil el cliente será opcional para ventas de contado.

Será obligatorio únicamente cuando la venta lo requiera.

---

## Cliente de contado

Cliente genérico utilizado automáticamente cuando una venta no requiere identificar al comprador.

Nombre sugerido:

Consumidor Final.

---

## Crédito

Venta cuyo pago queda pendiente total o parcialmente.

---

## Abono

Pago realizado por un cliente para disminuir el saldo de un crédito.

---

## Caja

Sesión de trabajo donde se registran las operaciones de efectivo de un cajero.

---

## Apertura de caja

Inicio oficial de una sesión de caja.

---

## Cierre de caja

Finalización oficial de una sesión de caja.

---

## Arqueo

Proceso de comparación entre el dinero esperado y el dinero contado físicamente.

---

## Comprobante

Documento generado por una venta.

Dependiendo de la configuración podrá representar:

- Ticket
- Factura
- Recibo

La palabra oficial será **Comprobante**.

---

## Reporte

Documento que presenta información resumida del negocio.

---

## Auditoría

Registro histórico de acciones importantes realizadas dentro del sistema.

---

## Respaldo

Copia de seguridad de la información del negocio.

---

## Sincronización

Proceso mediante el cual la información local se actualiza con la nube.

---

## Estado Activo

Elemento disponible para utilizarse normalmente.

---

## Estado Inactivo

Elemento conservado por historial pero no disponible para nuevas operaciones.

---

# Convenciones de nombres

## Interfaz

La interfaz deberá utilizar palabras fáciles de entender.

Ejemplos:

Correcto:

- Producto
- Compra
- Venta
- Caja

Evitar:

- Artículo Comercial
- Movimiento Contable
- Documento Comercial

---

## Código

Las clases utilizarán PascalCase.

Ejemplos:

Producto

Venta

Compra

MovimientoInventario

Caja

---

## Variables

Las variables utilizarán camelCase.

Ejemplos:

precioVenta

stockActual

fechaCompra

codigoBarras

---

## Base de datos

Las tablas utilizarán nombres en singular.

Ejemplos:

producto

venta

compra

cliente

usuario

---

# Observaciones

Este documento podrá ampliarse conforme aparezcan nuevos conceptos en CajaFácil.

Sin embargo, ningún término oficial deberá modificarse sin evaluar previamente su impacto en la documentación, el código y la base de datos.