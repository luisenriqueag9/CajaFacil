# 01_ESPECIFICACION_FUNCIONAL_V1.md

Versión: 1.0
Estado: Aprobado

Última actualización: 2026-07-18
Documento: Especificación Funcional

# Especificación Funcional de CajaFácil 1.0
## Alcance de esta especificación
La primera versión estará enfocada principalmente en:

- Pulperías.
- Minisúper.
- Supermercados pequeños.
- Ferreterías.
- Tiendas de conveniencia.

El sistema debe ser rápido, modular, fácil de aprender y capaz de trabajar sin conexión permanente a Internet.

---

# Objetivo principal

Permitir que un negocio pueda controlar de forma confiable:

- Productos.
- Compras.
- Inventario.
- Caja.
- Ventas.
- Clientes opcionales.
- Crédito.
- Usuarios.
- Reportes.
- Respaldos.

---

# Requisitos funcionales

## 1. Empresas y configuración

El sistema permitirá configurar:

- Nombre comercial.
- Razón social.
- RTN.
- Dirección.
- Teléfono.
- Correo electrónico.
- Logo.
- Moneda.
- Impuestos.
- Formato del comprobante.
- Opciones activas del negocio.

---

## 2. Usuarios, roles y permisos

Se incluirán inicialmente los roles:

- Administrador.
- Supervisor.
- Cajero.

Los permisos deberán controlar acciones como:

- Registrar ventas.
- Aplicar descuentos.
- Anular ventas.
- Registrar compras.
- Registrar mermas.
- Ajustar inventario.
- Abrir y cerrar caja.
- Consultar reportes.
- Administrar usuarios.
- Cambiar precios.

---

## 3. Productos

Cada producto podrá incluir:

- Nombre.
- Descripción.
- Categoría.
- Marca.
- Código interno.
- Uno o varios códigos de barras.
- Unidad de medida.
- Precio de venta.
- Costo.
- Impuesto.
- Existencia mínima.
- Control de inventario.
- Venta por cantidad decimal.
- Estado activo o inactivo.
- Condición de producto perecedero.
- Imagen opcional.

Los productos no se eliminarán cuando tengan historial.

Solo podrán desactivarse.

---

## 4. Unidades de medida

El sistema permitirá manejar productos vendidos por:

- Unidad.
- Libra.
- Kilogramo.
- Gramo.
- Litro.
- Mililitro.
- Caja.
- Paquete.
- Metro.

La arquitectura permitirá agregar nuevas unidades posteriormente.

---

## 5. Proveedores

Se podrá registrar:

- Nombre.
- Empresa.
- RTN.
- Teléfono.
- Correo.
- Dirección.
- Observaciones.
- Estado activo o inactivo.

---

## 6. Compras

El sistema permitirá:

- Registrar compras a proveedores.
- Registrar productos y cantidades.
- Registrar costos de compra.
- Registrar descuentos.
- Registrar impuestos.
- Registrar número de factura.
- Registrar fecha de compra.
- Registrar forma de pago.
- Generar entradas de inventario.
- Consultar historial de compras.
- Anular una compra mediante un proceso controlado.

Una compra nunca modificará el inventario sin generar movimientos.

---

## 7. Inventario

El inventario se controlará mediante movimientos.

Tipos iniciales de movimiento:

- Entrada por compra.
- Salida por venta.
- Entrada por devolución de cliente.
- Salida por devolución a proveedor.
- Salida por merma.
- Ajuste positivo.
- Ajuste negativo.
- Salida por uso interno.
- Transferencia futura entre sucursales.

El sistema mantendrá:

- Stock actual para consultas rápidas.
- Historial completo de movimientos para auditoría.

---

## 8. Mermas

Se podrán registrar pérdidas por:

- Producto vencido.
- Producto dañado.
- Descomposición.
- Rotura.
- Derrame.
- Robo.
- Pérdida de peso.
- Uso interno.
- Error de conteo.
- Otra causa autorizada.

Cada merma deberá guardar:

- Producto.
- Cantidad.
- Motivo.
- Observación.
- Fecha y hora.
- Usuario responsable.
- Caja o sucursal cuando corresponda.

---

## 9. Caja

El sistema permitirá:

- Apertura de caja.
- Registro de efectivo inicial.
- Ventas asociadas a la caja.
- Ingresos adicionales.
- Gastos.
- Retiros de efectivo.
- Cierre de caja.
- Arqueo.
- Diferencias de caja.
- Historial de aperturas y cierres.

No se permitirá registrar una venta finalizada sin una caja abierta, salvo una configuración administrativa especial.

---

## 10. Ventas

El sistema permitirá:

- Venta rápida sin registrar cliente.
- Búsqueda por nombre.
- Lectura de código de barras.
- Venta por unidad.
- Venta por peso o cantidad decimal.
- Modificación de cantidades.
- Descuentos autorizados.
- Impuestos.
- Diferentes métodos de pago.
- Pago combinado.
- Impresión de comprobante.
- Reimpresión de comprobante.
- Anulación controlada.
- Devolución parcial o total.

La mayoría de las ventas utilizarán automáticamente:

- Consumidor final.

---

## 11. Clientes

El cliente será opcional en una venta normal.

Se utilizará principalmente para:

- Ventas al crédito.
- Facturas con nombre.
- Facturación a empresas.
- Historial de compras.
- Devoluciones identificadas.
- Programas de fidelidad futuros.

Datos posibles:

- Nombre.
- Identidad.
- RTN.
- Empresa.
- Teléfono.
- Correo.
- Dirección.
- Límite de crédito.
- Estado activo o inactivo.

---

## 12. Crédito

CajaFácil 1.0 permitirá:

- Venta al crédito.
- Selección obligatoria de cliente.
- Registro de saldo pendiente.
- Registro de abonos.
- Historial de pagos.
- Estado de la cuenta.
- Comprobante de abono.
- Consulta de cuentas por cobrar.

La primera versión no incluirá cálculos financieros complejos ni planes de cuotas avanzados.

---

## 13. Métodos de pago

Métodos iniciales:

- Efectivo.
- Tarjeta.
- Transferencia.
- Crédito.
- Pago combinado.

Cada pago deberá quedar asociado a la venta y a la caja correspondiente.

---

## 14. Reportes

Reportes esenciales de la versión 1.0:

- Ventas por día.
- Ventas por período.
- Ventas por usuario.
- Ventas por producto.
- Productos más vendidos.
- Productos con bajo inventario.
- Existencias actuales.
- Historial de inventario.
- Mermas.
- Compras.
- Movimientos de caja.
- Cierres de caja.
- Cuentas por cobrar.
- Utilidad estimada.

---

## 15. Auditoría

El sistema registrará las acciones importantes:

- Inicio de sesión.
- Cambio de precios.
- Cambio de costos.
- Anulación de ventas.
- Devoluciones.
- Ajustes de inventario.
- Mermas.
- Aperturas y cierres de caja.
- Cambios de configuración.
- Creación y modificación de usuarios.

La auditoría debe guardar:

- Usuario.
- Acción.
- Fecha y hora.
- Entidad afectada.
- Identificador del registro.
- Valores anteriores cuando corresponda.
- Valores nuevos cuando corresponda.

---

## 16. Funcionamiento sin Internet

Las operaciones principales deberán funcionar sin conexión:

- Inicio de sesión local autorizado.
- Consulta de productos.
- Ventas.
- Caja.
- Inventario.
- Compras.
- Clientes.
- Reportes locales.

Internet se utilizará para:

- Respaldos en la nube.
- Sincronización.
- Actualizaciones.
- Validación de licencias.
- Funciones futuras.

---

## 17. Respaldos

La versión 1.0 debe permitir:

- Respaldo local manual.
- Respaldo local automático.
- Restauración controlada.
- Historial de respaldos.
- Copia cifrada en la nube.
- Verificación de integridad del respaldo.

Los respaldos no se guardarán únicamente en la misma computadora.

---

## 18. Rendimiento

El sistema deberá priorizar:

- Inicio rápido.
- Búsqueda inmediata de productos.
- Lectura rápida de códigos de barras.
- Venta sin pausas innecesarias.
- Operaciones críticas mediante transacciones.
- Consultas optimizadas.
- Interfaz fluida en equipos modestos.

---

# Funciones fuera del alcance de CajaFácil 1.0

No se incluirán inicialmente:

- Restaurantes.
- Mesas y comandas.
- Aplicación móvil completa.
- Comercio electrónico.
- Nómina.
- Contabilidad general.
- Integraciones bancarias automáticas.
- Facturación electrónica gubernamental.
- Inteligencia artificial.
- Programa de puntos.
- Franquicias.
- Producción y manufactura.
- Múltiples sucursales con sincronización completa.
- Variantes complejas de ropa.
- Recetas médicas.
- Control farmacéutico especializado.

Estas funciones podrán incorporarse en versiones futuras mediante módulos independientes.

---

# Criterios para considerar terminada la versión 1.0

CajaFácil 1.0 estará terminada cuando un negocio real pueda:

1. Instalar la aplicación.
2. Configurar su empresa.
3. Crear usuarios.
4. Registrar productos.
5. Registrar proveedores.
6. Registrar compras.
7. Consultar inventario.
8. Registrar mermas.
9. Abrir caja.
10. Realizar ventas rápidamente.
11. Cobrar con diferentes métodos.
12. Imprimir comprobantes.
13. Registrar clientes cuando sea necesario.
14. Vender al crédito.
15. Registrar abonos.
16. Cerrar y cuadrar caja.
17. Consultar reportes.
18. Crear y restaurar respaldos.
19. Trabajar sin Internet.
20. Recuperarse correctamente después de un cierre inesperado.

---

# Observaciones

Este documento describe las funcionalidades que deberá ofrecer CajaFácil 1.0.

No define la arquitectura interna del sistema, las reglas de negocio detalladas ni el diseño técnico de cada módulo. Dichos aspectos serán desarrollados en los documentos de arquitectura y dominios correspondientes.