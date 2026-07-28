---
id: CF-DOC-003
title: "Matriz de Reorganización Documental"
owner: "cto"
status: "approved"
last_reviewed: 2026-07-24
role: "canonical"
---

# Matriz de Reorganización Documental - CajaFácil

Esta matriz detalla la clasificación oficial, el estado actual y la acción requerida para cada uno de los archivos documentales detectados dinámicamente en el repositorio.

---

## Matriz de Transición de Archivos

| Documento Actual | Nueva Ubicación Propuesta | Estado | Acción Requerida |
| :--- | :--- | :---: | :--- |
| `00_MANIFIESTO_CAJA_FACIL.md` | `docs/business/00_MANIFIESTO_CAJA_FACIL.md` | **approved** | Mover. Agregar YAML con `role: canonical` y `owner: cto`. |
| `01_ESPECIFICACION_FUNCIONAL_V1.md` | `docs/business/01_ESPECIFICACION_FUNCIONAL.md` | **approved** | Mover y renombrar. Agregar YAML con `role: canonical` y `owner: product-owner`. |
| `01_MASTER_ROADMAP_CAJAFACIL.md` | `docs/business/01_MASTER_ROADMAP_CAJAFACIL.md` | **approved** | Mover. Agregar YAML con `role: reference` y `owner: cto`. |
| `02_ARQUITECTURA_GENERAL.md` | `docs/architecture/02_ARQUITECTURA_GENERAL.md` | **approved** | Mover. Agregar YAML con `role: canonical` y `owner: lead-architect`. |
| `03_DICCIONARIO_DEL_NEGOCIO.md` | `docs/business/03_DICCIONARIO_DEL_NEGOCIO.md` | **approved** | Mover. Agregar YAML con `role: canonical` y `owner: product-owner`. |
| `04_DOMINIO_PRODUCTO.md` | `docs/business/04_DOMINIO_PRODUCTO.md` | **migrated** | Mover. Agregar YAML con `role: canonical` y `owner: product-owner`. |
| `05_MODELO_DEL_DOMINIO.md` | `docs/architecture/05_MODELO_DEL_DOMINIO.md` | **approved** | Mover. Agregar YAML con `role: canonical` y `owner: lead-architect`. |
| `06_REGLAS_DE_NEGOCIO.md` | `docs/business/06_REGLAS_DE_NEGOCIO.md` | **approved** | Mover. Agregar YAML con `role: canonical` y `owner: product-owner`. |
| `07_DOMINIO_INVENTARIO.md` | `docs/business/07_DOMINIO_INVENTARIO.md` | **migrated** | Mover. Agregar YAML con `role: canonical` y `owner: product-owner`. |
| `08_DOMINIO_COMPRAS.md` | `docs/business/08_DOMINIO_COMPRAS.md` | **migrated** | Mover. Agregar YAML con `role: canonical` y `owner: product-owner`. |
| `09_DOMINIO_VENTAS.md` | `docs/business/09_DOMINIO_VENTAS.md` | **migrated** | Mover. Agregar YAML con `role: canonical` y `owner: product-owner`. |
| `10_DOMINIO_CAJA.md` | `docs/business/10_DOMINIO_CAJA.md` | **migrated** | Mover. Agregar YAML con `role: canonical` y `owner: product-owner`. |
| `11_DOMINIO_CLIENTES_CREDITO.md` | `docs/business/11_DOMINIO_CLIENTES_CREDITO.md` | **approved** | Mover. Agregar YAML con `role: canonical` y `owner: product-owner`. |
| `12_DOMINIO_SEGURIDAD.md` | `docs/business/12_DOMINIO_SEGURIDAD.md` | **migrated** | Mover. Agregar YAML con `role: canonical` y `owner: product-owner`. |
| `13_DOMINIO_EMPRESA.md` | `docs/business/13_DOMINIO_EMPRESA.md` | **migrated** | Mover. Agregar YAML con `role: canonical` y `owner: product-owner`. |
| `14_REVISION_ARQUITECTONICA.md` | `docs/architecture/14_REVISION_ARQUITECTONICA.md` | **approved** | Mover. Agregar YAML con `role: canonical` y `owner: lead-architect`. |
| `15_MODELO_CONCEPTUAL_DE_DATOS.md` | `docs/engineering/database/15_MODELO_CONCEPTUAL_DE_DATOS.md` | **approved** | Mover. Agregar YAML con `role: canonical` y `owner: lead-architect`. |
| `16_MODELO_LOGICO_EMPRESA_SEGURIDAD.md` | `docs/engineering/database/16_MODELO_LOGICO_EMPRESA_SEGURIDAD.md` | **migrated** | Mover. Agregar YAML con `role: dependent` y link canónico. |
| `17_MODELO_LOGICO_PRODUCTOS_INVENTARIO.md` | `docs/engineering/database/17_MODELO_LOGICO_PRODUCTOS_INVENTARIO.md` | **migrated** | Mover. Agregar YAML con `role: dependent` y link canónico. |
| `18_MODELO_LOGICO_COMPRAS.md` | `docs/engineering/database/18_MODELO_LOGICO_COMPRAS.md` | **approved** | Mover. Agregar YAML con `role: canonical` y `owner: lead-architect`. |
| `19_MODELO_LOGICO_VENTAS_CAJA.md` | `docs/engineering/database/19_MODELO_LOGICO_VENTAS_CAJA.md` | **migrated** | Mover. Agregar YAML con `role: dependent` y link canónico. |
| `20_MODELO_LOGICO_CLIENTES_CREDITO.md` | `docs/engineering/database/20_MODELO_LOGICO_CLIENTES_CREDITO.md` | **approved** | Mover. Agregar YAML con `role: dependent` y link canónico. |
| `21_DISENO_BASE_DE_DATOS.md` | `docs/engineering/database/21_DISENO_BASE_DE_DATOS.md` | **approved** | Mover. Agregar YAML con `role: canonical` y `owner: lead-architect`. |
| `22_BACKEND_ARQUITECTURA.md` | `docs/standards/22_BACKEND_ARQUITECTURA.md` | **approved** | Mover. Agregar YAML con `role: canonical` y `owner: backend-lead`. |
| `23_FRONTEND_ARQUITECTURA.md` | `docs/standards/23_FRONTEND_ARQUITECTURA.md` | **approved** | Mover. Agregar YAML con `role: canonical` y `owner: frontend-lead`. |
| `24_DISENO_ARQUITECTONICO_VENTAS.md` | `docs/engineering/architecture/24_DISENO_ARQUITECTONICO_VENTAS.md` | **migrated** | Mover. Agregar YAML con `role: dependent` y link explícito a `09_DOMINIO_VENTAS.md`. |
| `25_CIERRE_SPRINT13_VENTAS.md` | `docs/history/25_CIERRE_SPRINT13_VENTAS.md` | **historical** | Mover. Cambiar metadato `status` a `historical`. |
| `26_ANALISIS_FUNCIONAL_INVENTARIO.md` | `docs/business/26_ANALISIS_FUNCIONAL_INVENTARIO.md` | **migrated** | Mover. Agregar YAML con `role: dependent` y link a `07_DOMINIO_INVENTARIO.md`. |
| `27_DISENO_DOMINIO_INVENTARIO.md` | `docs/business/27_DISENO_DOMINIO_INVENTARIO.md` | **migrated** | Mover. Agregar YAML con `role: dependent` y link a `07_DOMINIO_INVENTARIO.md`. |
| `28_DISENO_ARQUITECTONICO_INVENTARIO.md` | `docs/engineering/architecture/28_DISENO_ARQUITECTONICO_INVENTARIO.md` | **migrated** | Mover. Agregar YAML con `role: dependent` y link a `07_DOMINIO_INVENTARIO.md`. |
| `29_CIERRE_SPRINT14_INVENTARIO.md` | `docs/history/29_CIERRE_SPRINT14_INVENTARIO.md` | **migrated** | Mover. Cambiar metadato `status` a `historical`. |
| `30_ANALISIS_FUNCIONAL_CAJA.md` | `docs/business/30_ANALISIS_FUNCIONAL_CAJA.md` | **migrated** | Mover. Agregar YAML con `role: dependent` y link a `10_DOMINIO_CAJA.md`. |
| `31_DISENO_DOMINIO_CAJA.md` | `docs/business/31_DISENO_DOMINIO_CAJA.md` | **migrated** | Mover. Agregar YAML con `role: dependent` y link a `10_DOMINIO_CAJA.md`. |
| `32_DISENO_ARQUITECTONICO_CAJA.md` | `docs/engineering/architecture/32_DISENO_ARQUITECTONICO_CAJA.md` | **migrated** | Mover. Agregar YAML con `role: dependent` y link a `10_DOMINIO_CAJA.md`. |
| `33_ESTANDAR_DE_IMPLEMENTACION.md` | `docs/standards/33_ESTANDAR_DE_IMPLEMENTACION.md` | **migrated** | Creado. Constitución Técnica y Estándar de Implementación oficial. |
| `34_ESTANDARES_DE_IMPLEMENTACION.md` | `docs/standards/34_ESTANDARES_DE_IMPLEMENTACION.md` | **approved** | Mover. Agregar YAML con `role: canonical` y `owner: lead-architect`. Corregir regla `__init__.py`. |
| `35_ESTANDARES_DDD.md` | `docs/standards/35_ESTANDARES_DDD.md` | **approved** | Mover. Agregar YAML con `role: canonical` y `owner: lead-architect`. |
| `36_ESTANDARES_TRANSACCIONALES.md` | `docs/standards/36_ESTANDARES_TRANSACCIONALES.md` | **approved** | Mover. Agregar YAML con `role: canonical` y `owner: lead-architect`. |
| `37_ESTANDARES_OFFLINE_FIRST.md` | `docs/standards/37_ESTANDARES_OFFLINE_FIRST.md` | **approved** | Mover. Agregar YAML con `role: canonical` y `owner: lead-architect`. |
| `38_ESTANDARES_DE_PRUEBAS.md` | `docs/standards/38_ESTANDARES_DE_PRUEBAS.md` | **approved** | Mover. Agregar YAML con `role: canonical` y `owner: lead-architect`. |
| `39_GUIA_DESARROLLO_CAJAFACIL.md` | `docs/standards/39_GUIA_DESARROLLO_CAJAFACIL.md` | **approved** | Mover. Agregar YAML con `role: canonical` y `owner: lead-architect`. |
| `40_GUIA_IA_CAJAFACIL.md` | `docs/standards/40_GUIA_IA_CAJAFACIL.md` | **approved** | Mover. Agregar YAML con `role: canonical` y `owner: ai-architect`. |
| `42_ANALISIS_FUNCIONAL_CONFIGURACION_TRIBUTARIA.md` | `docs/business/42_ANALISIS_FUNCIONAL_CONFIGURACION_TRIBUTARIA.md` | **approved** | Mover. Agregar YAML con `role: dependent` y link a `06_REGLAS_DE_NEGOCIO.md`. |
| `43_DISENO_DOMINIO_CONFIGURACION_TRIBUTARIA.md` | `docs/business/43_DISENO_DOMINIO_CONFIGURACION_TRIBUTARIA.md` | **approved** | Mover. Agregar YAML con `role: dependent` y link a `06_REGLAS_DE_NEGOCIO.md`. |
| `44_DISENO_ARQUITECTONICO_CONFIGURACION_TRIBUTARIA.md` | `docs/standards/44_DISENO_ARQUITECTONICO_CONFIGURACION_TRIBUTARIA.md` | **approved** | Mover. Agregar YAML con `role: dependent` y link a `06_REGLAS_DE_NEGOCIO.md`. |
| `45_CIERRE_SPRINT17_CONFIGURACION_TRIBUTARIA.md` | `docs/history/45_CIERRE_SPRINT17_CONFIGURACION_TRIBUTARIA.md` | **historical** | Mover. Cambiar metadato `status` a `historical`. |
| `46_ANALISIS_FUNCIONAL_FLUJO_OPERATIVO_MVP.md` | `docs/business/46_ANALISIS_FUNCIONAL_FLUJO_OPERATIVO_MVP.md` | **approved** | Mover. Agregar YAML con `role: dependent` y link a `01_ESPECIFICACION_FUNCIONAL.md`. |
| `47_PRIORIZACION_MVP.md` | `docs/business/47_PRIORIZACION_MVP.md` | **approved** | Mover. Agregar YAML con `role: dependent` y link a `01_ESPECIFICACION_FUNCIONAL.md`. |
| `48_ANALISIS_FUNCIONAL_GESTION_EXISTENCIAS.md` | `docs/business/48_ANALISIS_FUNCIONAL_GESTION_EXISTENCIAS.md` | **approved** | Mover. Agregar YAML con `role: dependent` y link a `07_DOMINIO_INVENTARIO.md`. |
| `49_DISENO_DOMINIO_GESTION_EXISTENCIAS.md` | `docs/business/49_DISENO_DOMINIO_GESTION_EXISTENCIAS.md` | **approved** | Mover. Agregar YAML con `role: dependent` y link a `07_DOMINIO_INVENTARIO.md`. |
| `50_DISENO_ARQUITECTONICO_GESTION_EXISTENCIAS.md` | `docs/standards/50_DISENO_ARQUITECTONICO_GESTION_EXISTENCIAS.md` | **approved** | Mover. Agregar YAML con `role: dependent` y link a `07_DOMINIO_INVENTARIO.md`. |
| `51_CIERRE_SPRINT19_GESTION_EXISTENCIAS.md` | `docs/history/51_CIERRE_SPRINT19_GESTION_EXISTENCIAS.md` | **historical** | Mover. Cambiar metadato `status` a `historical`. |
| `52_AUDITORIA_TRANSVERSAL_BACKEND.md` | `docs/history/52_AUDITORIA_TRANSVERSAL_BACKEND.md` | **historical** | Mover. Cambiar metadato `status` a `historical`. |
| `53_PLAN_ACCION_AUDITORIA_BACKEND.md` | `docs/history/53_PLAN_ACCION_AUDITORIA_BACKEND.md` | **historical** | Mover. Cambiar metadato `status` a `historical`. |
| `54_ANALISIS_FUNCIONAL_ENDURECIMIENTO_RC_V0_1_0.md` | `docs/business/54_ANALISIS_FUNCIONAL_ENDURECIMIENTO_RC_V0_1_0.md` | **approved** | Mover. Agregar YAML con `role: dependent` y link a `01_ESPECIFICACION_FUNCIONAL.md`. |
| `99_PROYECTO_CAJAFACIL_AI.md` | `docs/history/99_PROYECTO_CAJAFACIL_AI.md` | **obsolete** | Mover. Cambiar a `status: obsolete`. Enlazar a `docs/ai/00_LEEME.md`. |

---

## Matriz de Transición del Adaptador de IA (`docs/ai/`)

| Documento Actual | Nueva Ubicación Propuesta | Estado | Acción Requerida |
| :--- | :--- | :---: | :--- |
| `docs/ai/00_LEEME.md` | `docs/ai/00_LEEME.md` | **approved** | Mantener. Agregar Frontmatter YAML con `role: canonical` y `owner: ai-architect`. |
| `docs/ai/arquitectura/01_PATRON_MODULO_MAESTRO.md` | `docs/ai/arquitectura/01_PATRON_MODULO_MAESTRO.md` | **approved** | Mantener. Agregar Frontmatter YAML con `role: canonical` y `owner: lead-architect`. |
| `docs/ai/desarrollo/02_ESTANDARES_DE_CODIGO.md` | `docs/ai/desarrollo/02_ESTANDARES_DE_CODIGO.md` | **approved** | Mantener. Agregar Frontmatter YAML con `role: canonical` y `owner: lead-architect`. |
| `docs/ai/desarrollo/03_WORKFLOW_SPRINTS.md` | `docs/ai/desarrollo/03_WORKFLOW_SPRINTS.md` | **approved** | Mantener. Agregar Frontmatter YAML con `role: canonical` y `owner: cto`. |
| `docs/ai/desarrollo/04_CONVENCIONES_DE_PROYECTO.md` | `docs/ai/desarrollo/04_CONVENCIONES_DE_PROYECTO.md` | **approved** | Mantener. Agregar Frontmatter YAML con `role: canonical` y `owner: lead-architect`. |
| `docs/ai/desarrollo/05_PLANTILLAS.md` | `docs/ai/desarrollo/05_PLANTILLAS.md` | **approved** | Mantener. Agregar Frontmatter YAML con `role: canonical` y `owner: lead-architect`. |
| `docs/ai/desarrollo/06_CHECKLIST_DE_REVISION.md` | `docs/ai/desarrollo/06_CHECKLIST_DE_REVISION.md` | **approved** | Mantener. Agregar Frontmatter YAML con `role: canonical` y `owner: lead-architect`. |
