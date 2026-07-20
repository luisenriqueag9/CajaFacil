# 12_DOMINIO_SEGURIDAD.md

**Versión:** 1.0
**Estado:** Aprobado (Arquitectura)
**Última actualización:** 2026-07-19
**Documento:** Dominio Seguridad

# Dominio Seguridad

## Objetivo

Administrar la autenticación, autorización y control de acceso a CajaFácil, garantizando que cada operación sea realizada únicamente por usuarios autorizados.

---

# Responsabilidad

- Administrar usuarios.
- Administrar roles.
- Administrar permisos.
- Validar autenticación.
- Validar autorización.
- Mantener trazabilidad de accesos.

---

# No es responsabilidad

- Administrar productos.
- Registrar ventas.
- Administrar inventario.
- Administrar caja.
- Administrar créditos.

---

# Aggregate Roots

## Usuario

Representa a una persona autorizada para utilizar el sistema.

## Rol

Define un conjunto de permisos asignables a usuarios.

---

# Entidades

- Usuario
- Rol
- Permiso
- SesionUsuario

---

# Value Objects

- NombreUsuario
- ContraseñaHash
- EstadoUsuario
- TokenSesion

---

# Casos de Uso

- Iniciar sesión.
- Cerrar sesión.
- Registrar usuario.
- Asignar rol.
- Cambiar contraseña.
- Activar usuario.
- Desactivar usuario.
- Consultar permisos.

---

# Estados

## Usuario

- Activo
- Inactivo
- Bloqueado

---

# Eventos del Dominio

- UsuarioRegistrado
- SesionIniciada
- SesionFinalizada
- RolAsignado
- UsuarioBloqueado

---

# Relaciones

## Provee servicios a

- Todos los dominios del sistema.

## Publica eventos para

- Auditoría
- Reportes

---

# Reglas aplicables

Este dominio se rige por:

- RN-002
- RN-003
- RN-900
- RN-901

---

# Arquitectura

Toda operación protegida debe validar autenticación y autorización.

La interfaz puede ocultar funciones, pero la validación definitiva siempre ocurre en Domain/Application.

Los permisos se asignan a través de Roles para facilitar la administración.

---

# Preparado para futuras versiones

La arquitectura permitirá incorporar:

- Autenticación multifactor (MFA).
- Inicio de sesión con proveedores externos.
- Políticas avanzadas de contraseñas.
- Auditoría ampliada de sesiones.
- Restricciones por dispositivo.
- Restricciones por horario.

---

# Sincronización

Toda entidad sincronizable incluirá:

- UUID
- Empresa
- Fecha de creación
- Fecha de modificación
- Versión
- Estado de sincronización

---

# Reglas para Antigravity

- Nunca confiar únicamente en la interfaz.
- Validar permisos en Domain/Application.
- Mantener separación entre autenticación y autorización.
- Respetar RN-002, RN-003, RN-900 y RN-901.

---

# Observaciones

El dominio Seguridad es transversal a todo CajaFácil. Ningún dominio debe implementar su propia lógica de autenticación o autorización; todas las validaciones deben centralizarse en este contexto.