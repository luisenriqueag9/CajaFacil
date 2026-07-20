# 13_DOMINIO_EMPRESA.md

**Versión:** 1.0
**Estado:** Aprobado (Arquitectura)
**Última actualización:** 2026-07-19
**Documento:** Dominio Empresa

# Dominio Empresa

## Objetivo

Administrar la configuración de cada empresa y garantizar el aislamiento de la información dentro de la arquitectura multiempresa (Multi-Tenant) de CajaFácil.

---

# Responsabilidad

- Registrar empresas.
- Administrar sucursales.
- Mantener la configuración general.
- Definir parámetros fiscales y comerciales.
- Identificar la empresa propietaria de toda la información.

---

# No es responsabilidad

- Registrar ventas.
- Administrar inventario.
- Administrar caja.
- Administrar créditos.
- Gestionar permisos.

---

# Aggregate Root

## Empresa

Representa el negocio propietario de todos los datos del sistema.

---

# Entidades

- Empresa
- Sucursal
- ConfiguracionEmpresa
- SerieComprobante

---

# Value Objects

- RTN
- Moneda
- ZonaHoraria
- DireccionFiscal
- CorreoEmpresa

---

# Casos de Uso

- Registrar empresa.
- Actualizar configuración.
- Administrar sucursales.
- Configurar numeraciones.
- Consultar información de la empresa.

---

# Estados

## Empresa

- Activa
- Inactiva

---

# Eventos del Dominio

- EmpresaRegistrada
- ConfiguracionActualizada
- SucursalRegistrada

---

# Relaciones

## Provee información a

- Todos los dominios del sistema.

## Publica eventos para

- Sincronización
- Auditoría

---

# Reglas aplicables

Este dominio se rige por:

- RN-001
- RN-800
- RN-801
- RN-802

---

# Arquitectura

Toda entidad de negocio pertenece exactamente a una Empresa.

Los datos nunca deben compartirse entre empresas.

El aislamiento entre empresas es obligatorio tanto en la base de datos como en la lógica de negocio y las consultas.

---

# Preparado para futuras versiones

La arquitectura permitirá incorporar:

- Multiempresa SaaS.
- Múltiples sucursales.
- Configuración por sucursal.
- Personalización de comprobantes.
- Múltiples monedas.
- Configuración tributaria por país.
- Expansión internacional.

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

- Toda entidad debe asociarse a una Empresa.
- Nunca mezclar información entre empresas.
- Mantener el aislamiento multiempresa.
- Respetar RN-001 y RN-800 a RN-802.

---

# Observaciones

El dominio Empresa constituye la base de la arquitectura SaaS de CajaFácil. Todo el sistema depende de este contexto para garantizar el aislamiento de datos, la configuración independiente de cada negocio y la futura escalabilidad hacia cientos o miles de empresas.