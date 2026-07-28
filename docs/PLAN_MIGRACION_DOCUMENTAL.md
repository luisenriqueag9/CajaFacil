---
id: CF-DOC-005
title: "Plan de Migración Documental"
owner: "cto"
status: "approved"
last_reviewed: 2026-07-24
role: "canonical"
---

# Plan de Migración Documental - CajaFácil

Este documento establece la hoja de ruta técnica y metodológica para realizar la transición física de archivos documentales en el repositorio de CajaFácil. Su propósito es asegurar que la migración ocurra sin pérdida de conocimiento, sin romper enlaces relacionales y manteniendo la continuidad de lectura para desarrolladores e Inteligencias Artificiales.

---

## 1. Justificación de Decisiones de Estructura

Tras la auditoría del plan inicial, se adoptaron dos decisiones fundamentales de gobernanza:

### 1.1. Adopción de la Estructura Híbrida (`docs/engineering/`)
En lugar de mantener un listado plano de carpetas tecnológicas en la raíz (`backend`, `frontend`, `database`, `standards`, `adr`), se consolidan bajo un directorio común llamado `docs/engineering/`.
*   *Mantenibilidad:* Separa limpiamente el "Qué" (Business / Reglas del negocio) del "Cómo" (Engineering / Solución técnica).
*   *Escalabilidad:* Permite añadir subcategorías técnicas en el futuro (ej. `devops`, `infrastructure`, `monitoring`) bajo un mismo paraguas sin saturar la raíz `/docs`.
*   *Facilidad de Navegación:* Un desarrollador sabe que todo lo concerniente a código, testing y bases de datos está dentro de `engineering/`.

### 1.2. Preservación del Glosario Numérico Correlativo
Se decide **no eliminar** los prefijos numéricos existentes (ej. `00_`, `01_`, `17_`), sino elevarlos a una **Clasificación Numérica Oficial por Rangos** (ver `docs/INDEX.md`).
*   *Trazabilidad:* Evita romper los enlaces relativos de Git y los registros históricos de commits que hacían referencia a archivos específicos por su nombre original.
*   *Orden de Lectura:* Mantiene una secuencia de aprendizaje secuencial recomendada para nuevos ingenieros.
*   *Facilidad de Búsqueda:* Un prefijo numérico actúa como un identificador único rápido en búsquedas de archivos en el editor de código.

---

## 2. Hoja de Ruta de la Migración (Paso a Paso)

Para minimizar riesgos de enlaces rotos, la ejecución de la migración física se dividirá en 5 fases secuenciales:

### Fase 1: Creación de la Estructura y READMEs de Carpeta (Sprint 21A)
1.  Crear los directorios físicos correspondientes a la taxonomía híbrida.
2.  Escribir los archivos `README.md` específicos para cada carpeta (que detallan el alcance y los propietarios) en sus rutas de destino definitivas.
3.  *Estado:* Cero archivos movidos. Rutas preparadas.

### Fase 2: Reubicación por Bloques de Menor Impacto (Sprint 21B)
1.  Mover los reportes de sprints pasados y auditorías a `docs/history/`.
2.  Mover los documentos externos y de proveedores a `docs/reference/`.
3.  Actualizar sus Frontmatters a `status: historical` u `status: obsolete`.
4.  *Riesgo:* Muy bajo. Estos archivos son inmutables y no tienen dependencias activas con el código en producción.

### Fase 3: Reubicación de la Capa de Negocio (`docs/business/`)
1.  Mover manifiesto, glosario y especificaciones funcionales al directorio `docs/business/`.
2.  Inyectar el Frontmatter YAML mínimo a cada archivo.
3.  Declarar explícitamente cuáles son los Documentos Canónicos en el `README.md` del directorio.

### Fase 4: Reubicación de Ingeniería (`docs/engineering/`)
1.  Mover los archivos de diseño técnico y bases de datos a `docs/engineering/architecture/`, `docs/engineering/database/` y `docs/engineering/standards/`.
2.  Inyectar el Frontmatter YAML definiendo su rol (`dependent` o `reference`).
3.  Reemplazar las explicaciones duplicadas por enlaces explícitos markdown a los documentos canónicos en `docs/business/`.

### Fase 5: Auditoría de Enlaces y De-commissioning de Monolito
1.  Actualizar el Frontmatter de `99_PROYECTO_CAJAFACIL_AI.md` a `status: obsolete` y moverlo a `docs/history/`.
2.  Ejecutar una auditoría manual de enlaces markdown para comprobar que ningún archivo tenga rutas rotas.
3.  Realizar commit, push y solicitar aprobación del CTO.
