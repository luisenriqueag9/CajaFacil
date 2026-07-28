---
id: CF-DOC-088
title: "Bitácora de Migración Documental"
owner: "cto"
status: "approved"
last_reviewed: 2026-07-24
role: "historical"
---

# Bitácora de Migración Documental - CajaFácil

Esta bitácora es el registro cronológico y acumulativo oficial de todos los dominios y documentos migrados durante el Sprint de Reorganización Documental de CajaFácil. Cada entrada requiere el visto bueno formal del CTO.

---

## Registro Histórico de Migraciones

### Entrada #1: Fase 1 - Empresa y Seguridad
*   **Fecha de Migración:** 2026-07-24
*   **Dominio Funcional:** Empresa (Multi-Tenant) y Seguridad (Autenticación y Permisos).
*   **Documentos Migrados:**
    *   `docs/13_DOMINIO_EMPRESA.md` ➔ `docs/business/13_DOMINIO_EMPRESA.md`
    *   `docs/12_DOMINIO_SEGURIDAD.md` ➔ `docs/business/12_DOMINIO_SEGURIDAD.md`
    *   `docs/16_MODELO_LOGICO_EMPRESA_SEGURIDAD.md` ➔ `docs/engineering/database/16_MODELO_LOGICO_EMPRESA_SEGURIDAD.md`
*   **Cambios Realizados:**
    *   Inyección de Frontmatter YAML minimalista en los tres archivos.
    *   Configuración de notas de dependencia con links cruzados al inicio de `16_MODELO_LOGICO_EMPRESA_SEGURIDAD.md`.
    *   Actualización del listado en `docs/business/README.md` y `docs/MATRIZ_DE_DOCUMENTOS.md`.
*   **Riesgos Encontrados:** Enlaces antiguos en otros documentos pendientes de migración. Riesgo bajo, controlado vía equivalencias.
*   **Estado:** ✅ COMPLETADO
*   **Aprobación del CTO:** Aprobado formalmente el 2026-07-24.

---

### Entrada #2: Fase 2 - Producto (Catálogo)
*   **Fecha de Migración:** 2026-07-24
*   **Dominio Funcional:** Producto (Catálogo Maestro de Artículos, Categorías y Unidades).
*   **Documentos Migrados:**
    *   `docs/04_DOMINIO_PRODUCTO.md` ➔ `docs/business/04_DOMINIO_PRODUCTO.md`
    *   `docs/17_MODELO_LOGICO_PRODUCTOS_INVENTARIO.md` ➔ `docs/engineering/database/17_MODELO_LOGICO_PRODUCTOS_INVENTARIO.md`
*   **Cambios Realizados:**
    *   Corrección metodológica: Se renombró de vuelta `16_MODELO_LOGICO_EMPRESA.md` a `16_MODELO_LOGICO_EMPRESA_SEGURIDAD.md` en su nueva ubicación, y se mantuvo `17_MODELO_LOGICO_PRODUCTOS_INVENTARIO.md` sin renombrar prematuramente ya que representan múltiples dominios.
    *   Inyección de Frontmatter YAML y notas de dependencia canónica.
    *   Actualización de la tabla de migración en `docs/INDEX.md`.
*   **Riesgos Encontrados:** Vinculación directa e indivisa con el módulo de Inventario en el diseño de base de datos relacional.
*   **Estado:** ✅ COMPLETADO
*   **Aprobación del CTO:** Aprobado formalmente el 2026-07-24.

---

### Entrada #3: Fase 3 - Ventas (Cobros)
*   **Fecha de Migración:** 2026-07-24
*   **Dominio Funcional:** Ventas y cobros transaccionales.
*   **Documentos Migrados:**
    *   `docs/09_DOMINIO_VENTAS.md` ➔ `docs/business/09_DOMINIO_VENTAS.md`
    *   `docs/19_MODELO_LOGICO_VENTAS_CAJA.md` ➔ `docs/engineering/database/19_MODELO_LOGICO_VENTAS_CAJA.md`
    *   `docs/24_DISENO_ARQUITECTONICO_VENTAS.md` ➔ `docs/engineering/architecture/24_DISENO_ARQUITECTONICO_VENTAS.md`
*   **Cambios Realizados:**
    *   Traslado físico de archivos a través de `git mv`.
    *   Inyección de Frontmatter YAML e inyección de la nota de dependencias canónicas.
    *   Corrección de destino de `24_DISENO_ARQUITECTONICO_VENTAS.md` hacia `architecture/` para separarlo de los estándares globales.
    *   Actualización de la tabla de control de migración en `docs/INDEX.md` y `docs/MATRIZ_DE_DOCUMENTOS.md`.
*   **Riesgos Encontrados:** Fuerte dependencia de persistencia compartida con Caja en `19_MODELO_LOGICO_VENTAS_CAJA.md` (mitigado al mantener el nombre inalterado) y dependencia conceptual con "Formas de Pago".
*   **Estado:** ✅ COMPLETADO
*   **Aprobación del CTO:** Aprobado formalmente el 2026-07-24.


---

### Entrada #4: Fase 4 - Inventario (Existencias)
*   **Fecha de Migración:** 2026-07-24
*   **Dominio Funcional:** Inventario (Movimiento de existencias, Kardex, mermas e integración síncrona).
*   **Documentos Migrados:**
    *   `docs/07_DOMINIO_INVENTARIO.md` ➔ `docs/business/07_DOMINIO_INVENTARIO.md`
    *   `docs/26_ANALISIS_FUNCIONAL_INVENTARIO.md` ➔ `docs/business/26_ANALISIS_FUNCIONAL_INVENTARIO.md`
    *   `docs/27_DISENO_DOMINIO_INVENTARIO.md` ➔ `docs/business/27_DISENO_DOMINIO_INVENTARIO.md`
    *   `docs/28_DISENO_ARQUITECTONICO_INVENTARIO.md` ➔ `docs/engineering/architecture/28_DISENO_ARQUITECTONICO_INVENTARIO.md`
    *   `docs/29_CIERRE_SPRINT14_INVENTARIO.md` ➔ `docs/history/29_CIERRE_SPRINT14_INVENTARIO.md`
*   **Cambios Realizados:**
    *   Mapeo de dependencias de Kardex y existencias con Compras y Ventas.
    *   Moviendo archivos en Git y aplicando Frontmatter YAML con dependencias cruzadas.
    *   Actualización de catálogos e índices.
*   **Riesgos Encontrados:** Modificaciones directas al stock prohibidas (RN-200), que requiere que todas las dependencias usen eventos en lugar de mutaciones directas.
*   **Estado:** ✅ COMPLETADO
*   **Aprobación del CTO:** Aprobado formalmente el 2026-07-24.

---

### Entrada #5: Fase 5 - Caja (Cash Box)
*   **Fecha de Migración:** 2026-07-24
*   **Dominio Funcional:** Caja registradora (Aperturas, cierres, arqueos, diferencias e integración de ventas en efectivo).
*   **Documentos Migrados:**
    *   `docs/10_DOMINIO_CAJA.md` ➔ `docs/business/10_DOMINIO_CAJA.md`
    *   `docs/30_ANALISIS_FUNCIONAL_CAJA.md` ➔ `docs/business/30_ANALISIS_FUNCIONAL_CAJA.md`
    *   `docs/31_DISENO_DOMINIO_CAJA.md` ➔ `docs/business/31_DISENO_DOMINIO_CAJA.md`
    *   `docs/32_DISENO_ARQUITECTONICO_CAJA.md` ➔ `docs/engineering/architecture/32_DISENO_ARQUITECTONICO_CAJA.md`
*   **Cambios Realizados:**
    *   Mapeo de dependencias de flujo de efectivo en checkout e invariantes de arqueos/turnos.
    *   Traslado de archivos físicos en Git y aplicación de Frontmatters YAML con dependencias.
    *   Actualización de índices, READMEs y referencias cruzadas (ej: en `09_DOMINIO_VENTAS.md`).
*   **Riesgos Encontrados:** Alto acoplamiento en base de datos (`19_MODELO_LOGICO_VENTAS_CAJA.md`). Mitigado al mantener el modelo lógico compartido bajo base de datos con doble vínculo explícito.
*   **Estado:** ✅ COMPLETADO
*   **Aprobación del CTO:** Aprobado formalmente el 2026-07-24.

---

## Lecciones Aprendidas de la Migración

### 1. Dominios de Empresa y Seguridad (Fase 1)
*   **Evitar Renombres Prematuros:** Los documentos lógicos o físicos que representen esquemas compartidos no deben renombrarse a un solo dominio para evitar desinformar al equipo técnico.

### 2. Dominio de Producto (Fase 2)
*   **Acoplamiento de Persistencia:** Los modelos lógicos de base de datos relacionales a menudo acoplan Producto e Inventario. Al migrar de forma incremental, es fundamental mantener los nombres físicos originales e inyectar notas de dependencia explícitas.

### 3. Dominio de Ventas (Fase 3)
*   **Separación de Diseño y Estándares:** Los planos de diseño detallado de un módulo específico pertenecen a `architecture/` y no a `standards/` (que debe reservarse para guías de estilo globales).
*   **Dependencia de Formas de Pago:** Venta depende de la definición inmutable de las formas de pago en el checkout, constituyendo una invariante crítica del negocio.

### 4. Dominio de Inventario (Fase 4)
*   **Stock como Valor Derivado:** La documentación debe reforzar que las existencias no son campos editables directos, sino agregaciones del Kardex. Esto previene que desarrolladores intenten implementar atajos no-transaccionales que rompan el sistema multi-tenant offline-first.

### 5. Dominio de Caja (Fase 5)
*   **Custodia Temporal frente a Ventas:** Caja no debe mezclar flujos de facturación comercial con el resguardo del dinero. Turnos (`Apertura`/`Cierre`) y `Arqueos` son mecanismos exclusivos de control de efectivo, no del total de la facturación.

