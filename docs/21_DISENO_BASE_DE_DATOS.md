# 21_DISENO_BASE_DE_DATOS.md

Versión: 1.0

Estado: Aprobado

Última actualización: 2026-07-20

Documento: Diseño de Base de Datos

---

# Objetivo

Definir los estándares técnicos para el diseño físico de la base de datos de CajaFácil.

Este documento establece las reglas que deberán seguir todas las tablas, relaciones, índices y restricciones tanto en SQLite como en PostgreSQL.

---

# Arquitectura de Persistencia

CajaFácil utilizará dos motores de base de datos.

## Base de datos local

SQLite

Responsabilidades

- Trabajar completamente sin Internet.
- Máximo rendimiento.
- Base de datos por empresa.
- Sincronización posterior con la nube.

---

## Base de datos nube

PostgreSQL

Responsabilidades

- Respaldo automático.
- Sincronización.
- Multiempresa.
- Reportes.
- Administración remota.

---

# Estrategia Offline First

Toda operación será registrada primero en SQLite.

Posteriormente será sincronizada hacia PostgreSQL.

Nunca dependeremos de Internet para vender.

---

# Convenciones de nombres

## Tablas

Nombre singular.

Ejemplos

Empresa

Producto

Venta

Compra

Cliente

Caja

---

## Columnas

PascalCase

Ejemplos

EmpresaId

ProductoId

FechaVenta

PrecioVenta

CodigoBarras

---

## Claves primarias

Todas las tablas utilizarán

Id

Tipo

UUID

---

## Claves foráneas

Siempre terminarán en

Id

Ejemplos

EmpresaId

ClienteId

ProductoId

CajaId

UsuarioId

---

# Campos técnicos comunes

Todas las tablas persistentes deberán contener como mínimo

| Campo |
|---------|
| Id |
| Version |
| CreadoEn |
| ActualizadoEn |
| CreadoPor |
| ActualizadoPor |
| EstadoSincronizacion |

---

# Auditoría

Las entidades principales implementarán auditoría.

Campos

CreadoEn

ActualizadoEn

CreadoPor

ActualizadoPor

---

# Eliminación lógica

No se eliminarán registros históricos.

Se utilizará

Eliminado

EliminadoEn

cuando sea necesario.

---

# Relaciones

Todas las relaciones utilizarán claves foráneas.

No existirán relaciones implícitas.

---

# Integridad referencial

Toda clave foránea deberá existir.

No se permitirán registros huérfanos.

---

# Índices

Se crearán índices para

EmpresaId

CodigoInterno

CodigoBarras

Nombre

FechaVenta

FechaCompra

ClienteId

ProductoId

ProveedorId

CajaId

UsuarioId

Estado

---

# Restricciones

UNIQUE

Código interno.

Código de caja.

Nombre de rol.

Nombre de categoría.

---

CHECK

Cantidad mayor que cero.

Precio mayor o igual a cero.

Total mayor que cero.

---

FOREIGN KEY

Todas las relaciones utilizarán restricciones FK.

---

# Enumeraciones

Los valores de negocio utilizarán ENUM.

Ejemplos

EstadoVenta

EstadoCompra

EstadoCredito

TipoMovimientoCaja

TipoMovimientoInventario

TipoVenta

EstadoSincronizacion

---

# Sincronización

Cada registro tendrá

Version

EstadoSincronizacion

FechaUltimaSincronizacion

para controlar conflictos.

---

# Migraciones

Toda modificación de la base de datos deberá realizarse mediante Alembic.

Nunca se modificará una tabla manualmente en producción.

---

# Compatibilidad

La estructura será compatible con

SQLite

PostgreSQL

SQLAlchemy

FastAPI

Flutter

Riverpod

---

# Rendimiento

Las consultas frecuentes deberán utilizar índices.

Se evitarán consultas N+1.

Las operaciones de venta deberán ejecutarse mediante transacciones.

---

# Transacciones

Se utilizarán transacciones para

Registrar compras.

Registrar ventas.

Registrar créditos.

Registrar abonos.

Cerrar caja.

Sincronización.

---

# Seguridad

No se almacenarán contraseñas en texto plano.

Todas las contraseñas utilizarán hash seguro.

---

# Multiempresa

Toda información pertenecerá exactamente a una Empresa.

Nunca existirán datos compartidos entre empresas.

---

# Respaldo

SQLite

Respaldo local.

PostgreSQL

Respaldo automático en la nube.

---

# Escalabilidad

La estructura permitirá incorporar posteriormente

Sucursales múltiples.

Bodegas.

Lotes.

Series.

Impuestos múltiples.

Facturación electrónica.

Pagos múltiples.

Promociones.

Inventario por ubicación.

API pública.

Aplicación móvil.

---

# Conclusión

La base de datos de CajaFácil ha sido diseñada para ofrecer:

- Alto rendimiento.
- Trabajo Offline First.
- Sincronización con la nube.
- Multiempresa.
- Escalabilidad.
- Modularidad.
- Integridad de la información.
- Compatibilidad con SQLite y PostgreSQL.

Este documento constituye la guía oficial para el desarrollo del backend y la persistencia del sistema.