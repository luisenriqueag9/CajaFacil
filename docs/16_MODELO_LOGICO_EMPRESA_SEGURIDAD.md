# 16_MODELO_LOGICO_EMPRESA_SEGURIDAD.md

Versión: 1.0

Estado: Aprobado

Última actualización: 2026-07-20

Documento: Modelo Lógico de Datos

---

# Objetivo

Definir el modelo lógico del dominio Empresa y Seguridad.

Este documento será la referencia oficial para el diseño de la base de datos, el backend, el frontend y la sincronización del sistema.

No define tipos físicos de SQLite o PostgreSQL; define las entidades, atributos, relaciones y restricciones del dominio.

---

# Alcance

Este documento comprende las siguientes entidades:

- Empresa
- ConfiguracionEmpresa
- Sucursal
- Usuario
- Rol
- Permiso
- SesionUsuario

---

# Convenciones

## Tipos de entidades

### MASTER DATA

Información relativamente estable que representa entidades principales del negocio.

### CONFIGURACIÓN

Información utilizada para parametrizar el funcionamiento del sistema.

### CATÁLOGO

Información de referencia utilizada por otras entidades.

### TRANSACCIONAL

Información generada por las operaciones del negocio.

### HISTÓRICO

Información que nunca debe modificarse.

### AUDITORÍA

Información técnica utilizada para trazabilidad.

---

# Dominio Empresa

---

# Empresa

## Descripción

Representa la empresa propietaria de toda la información almacenada en CajaFácil.

Toda la información del sistema pertenece exactamente a una Empresa.

Empresa constituye el límite superior del modelo Multiempresa (Multi-Tenant).

---

## Tipo de entidad

MASTER DATA

---

## Aggregate Root

Empresa

---

## Atributos del negocio

| Campo | Tipo | Obligatorio |
|--------|------|-------------|
| NombreComercial | Texto(150) | Sí |
| RazonSocial | Texto(200) | Sí |
| RTN | Texto(20) | Sí |
| Pais | Catálogo | Sí |
| MonedaPrincipal | Catálogo | Sí |
| Correo | Email | No |
| Telefono | Texto(30) | No |
| Direccion | Texto(300) | No |
| SitioWeb | URL | No |
| Logo | Archivo | No |

---

## Atributos técnicos

| Campo | Tipo |
|--------|------|
| Id | UUID |
| Version | Integer |
| CreadoEn | DateTime UTC |
| ActualizadoEn | DateTime UTC |
| CreadoPor | UUID |
| ActualizadoPor | UUID |
| Eliminado | Boolean |
| EliminadoEn | DateTime UTC |
| EstadoSincronizacion | Enum |

---

## Relaciones

- Empresa 1 → N Usuarios
- Empresa 1 → N Productos
- Empresa 1 → N Compras
- Empresa 1 → N Ventas
- Empresa 1 → N Clientes
- Empresa 1 → N Cajas
- Empresa 1 → N Sucursales
- Empresa 1 → 1 ConfiguracionEmpresa

---

## Restricciones

- Debe existir un NombreComercial.
- Debe existir una RazonSocial.
- Debe existir un País.
- Debe existir una MonedaPrincipal.
- No se permite eliminación física.
- Toda entidad pertenece exactamente a una Empresa.

---

## Observaciones

Empresa almacena únicamente la identidad legal y comercial del negocio.

Toda configuración operativa será administrada mediante ConfiguracionEmpresa.

---

# ConfiguracionEmpresa

## Descripción

Contiene todos los parámetros de funcionamiento de una Empresa.

Permite modificar el comportamiento del sistema sin alterar la identidad de la empresa.

---

## Tipo de entidad

CONFIGURACIÓN

---

## Aggregate Root

Empresa

---

## Atributos del negocio

| Campo | Tipo | Obligatorio |
|--------|------|-------------|
| EmpresaId | UUID | Sí |
| ZonaHoraria | Catálogo | Sí |
| MonedaSecundaria | Catálogo | No |
| PermiteVentasCredito | Boolean | Sí |
| ControlarInventario | Boolean | Sí |
| PermitirStockNegativo | Boolean | No |
| FormatoTicket | Catálogo | Sí |
| NumeracionAutomatica | Boolean | Sí |

---

## Atributos técnicos

Los mismos campos técnicos estándar definidos para las entidades persistentes.

---

## Relaciones

- Empresa 1 → 1 ConfiguracionEmpresa

---

## Restricciones

- Solo puede existir una configuración por empresa.

---

# Sucursal

## Descripción

Representa un establecimiento físico perteneciente a una Empresa.

---

## Tipo de entidad

MASTER DATA

---

## Aggregate Root

Sucursal

---

## Atributos del negocio

| Campo | Tipo | Obligatorio |
|--------|------|-------------|
| EmpresaId | UUID | Sí |
| Nombre | Texto(150) | Sí |
| Codigo | Texto(20) | Sí |
| Direccion | Texto(300) | No |
| Telefono | Texto(30) | No |
| Principal | Boolean | Sí |

---

## Relaciones

- Empresa 1 → N Sucursales
- Sucursal 1 → N Usuarios
- Sucursal 1 → N Cajas

---

## Restricciones

- El código debe ser único dentro de la empresa.
- Solo puede existir una sucursal principal.

---

# Dominio Seguridad

---

# Usuario

## Descripción

Representa una persona autorizada para utilizar CajaFácil.

---

## Tipo de entidad

MASTER DATA

---

## Aggregate Root

Usuario

---

## Atributos del negocio

| Campo | Tipo | Obligatorio |
|--------|------|-------------|
| EmpresaId | UUID | Sí |
| SucursalId | UUID | Sí |
| RolId | UUID | Sí |
| Nombre | Texto(150) | Sí |
| Usuario | Texto(50) | Sí |
| Correo | Email | No |
| Activo | Boolean | Sí |

---

## Relaciones

- Empresa 1 → N Usuarios
- Rol 1 → N Usuarios
- Sucursal 1 → N Usuarios

---

## Restricciones

- El nombre de usuario debe ser único dentro de la empresa.

---

# Rol

## Descripción

Agrupa permisos para controlar el acceso a las funcionalidades del sistema.

---

## Tipo de entidad

CATÁLOGO

---

## Relaciones

- Rol 1 → N Usuarios
- Rol N → N Permisos

---

# Permiso

## Descripción

Representa una acción específica que puede ejecutar un usuario.

Ejemplos:

- Crear venta
- Anular venta
- Abrir caja
- Cerrar caja
- Registrar compras
- Crear usuarios

---

## Tipo de entidad

CATÁLOGO

---

## Relaciones

- Permiso N → N Roles

---

# SesionUsuario

## Descripción

Representa una sesión iniciada por un usuario dentro del sistema.

---

## Tipo de entidad

AUDITORÍA

---

## Atributos principales

| Campo | Tipo |
|--------|------|
| UsuarioId | UUID |
| FechaInicio | DateTime |
| FechaFin | DateTime |
| Equipo | Texto |
| DireccionIP | Texto |
| Estado | Enum |

---

## Restricciones

- Una sesión pertenece a un único usuario.
- El historial nunca se elimina.

---

# Resumen del dominio

| Entidad | Tipo |
|----------|------|
| Empresa | MASTER DATA |
| ConfiguracionEmpresa | CONFIGURACIÓN |
| Sucursal | MASTER DATA |
| Usuario | MASTER DATA |
| Rol | CATÁLOGO |
| Permiso | CATÁLOGO |
| SesionUsuario | AUDITORÍA |

---

# Conclusión

El dominio Empresa y Seguridad establece la base organizativa de CajaFácil.

Todas las demás entidades del sistema dependerán directa o indirectamente de estas definiciones, garantizando un modelo multiempresa, modular y preparado para la sincronización Offline First.