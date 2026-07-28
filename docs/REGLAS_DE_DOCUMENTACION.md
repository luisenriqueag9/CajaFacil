---
id: CF-DOC-004
title: "Reglas de Documentación Oficiales"
owner: "cto"
status: "approved"
last_reviewed: 2026-07-24
role: "canonical"
---

# Reglas de Documentación Oficiales - CajaFácil

Este documento constituye la norma técnica y metodológica obligatoria para la creación, modificación, organización y ciclo de vida de la documentación del proyecto CajaFácil.

---

## 1. Políticas de Nombres y Estilo

Para mantener un orden legible para humanos e inteligencias artificiales, se aplican las siguientes reglas obligatorias de nomenclatura:

### 1.1. Nombres de Directorios (Carpetas)
*   **Convención:** Minúsculas sostenidas utilizando `snake_case` o una sola palabra simple (ej. `business`, `architecture`, `database`, `standards`, `adr`, `reference`, `templates`, `history`).
*   Está prohibido utilizar números en el nombre de las carpetas.

### 1.2. Nombres de Archivos
*   **Formato general:** Minúsculas sostenidas utilizando `snake_case` (ej. `plan_reorganizacion_documental.md`, `mapa_documental.md`).
*   Está prohibido usar mayúsculas, espacios en blanco o caracteres especiales en los nombres de archivo.

### 1.3. Uso de Prefijos Numéricos
*   **Regla general:** *No se utilizarán prefijos numéricos* (ej. `01_`, `02_`) en el nombre físico de los nuevos archivos de documentación activa, para evitar la re-indexación masiva al agregar documentos intermedios.
*   **Excepción para Históricos y Catálogos de Transición:** Se permite conservar los prefijos numéricos existentes heredados en los archivos originales reubicados únicamente para no romper las referencias cruzadas externas de corto plazo, pero toda nueva documentación se creará sin prefijos numéricos.
*   **Identificador único:** La jerarquía y orden lógico se gestiona mediante el campo `id` del Frontmatter y no por el nombre físico del archivo.

---

## 2. El Ciclo de Vida Documental

Todo documento en CajaFácil pasa por un ciclo de vida con estados estrictamente definidos mediante el metadato `status`:

```text
[ DRAFT ] ➔ [ IN-REVIEW ] ➔ [ APPROVED ] ➔ [ HISTORICAL ] u [ OBSOLETE ]
```

### 2.1. Estados del Ciclo de Vida:
*   **DRAFT (Borrador):**
    *   *Significado:* El documento está en fase de redacción o discusión inicial.
    *   *Regla:* No se considera fuente de verdad. El linter o la IA no deben extraer reglas ni asumir compromisos desde un borrador.
*   **IN-REVIEW (En Revisión):**
    *   *Significado:* El documento está terminado y en proceso de validación técnica o comercial por parte del responsable de la categoría.
*   **APPROVED (Aprobado):**
    *   *Significado:* Es la especificación oficial y canónica del sistema que describe la realidad exacta del software en producción.
    *   *Regla:* Es de lectura obligatoria y vinculante para desarrolladores y agentes de IA.
*   **HISTORICAL (Histórico):**
    *   *Significado:* Un reporte o acta de un hito completado en el pasado (sprints, auditorías pasadas).
    *   *Regla:* Nunca se modifica. Se conserva únicamente para fines de auditoría y trazabilidad histórica. Se almacena físicamente en `docs/history/`.
*   **OBSOLETE (Obsoleto):**
    *   *Significado:* El documento describe un comportamiento, regla de negocio o arquitectura técnica discontinuada o desechada.
    *   *Regla:* Debe removerse de las carpetas activas, marcarse con `status: obsolete` en su Frontmatter y guardarse en `docs/history/`.

---

## 3. Estándar de Contenido y Plantilla Frontmatter

Todos los archivos markdown de documentación (exceptuando plantillas) deben iniciar con el siguiente encabezado YAML Frontmatter:

```yaml
---
id: CF-DOC-XXX                  # Formato correlativo CF-DOC-###
title: "Título Semántico"        # Describe claramente el tema
owner: "cto | lead-architect | backend-lead | frontend-lead | product-owner | ai-architect"
status: "approved | historical | obsolete"
last_reviewed: YYYY-MM-DD       # Fecha del último cambio en el archivo
role: "canonical | dependent | reference"
---
```

---

## 4. Política del README de Carpeta

Cada carpeta principal de documentación en el repositorio debe contener un archivo `README.md` obligatorio estructurado de la siguiente forma:

1.  **Propósito:** Breve explicación de qué conocimiento almacena esta carpeta.
2.  **Índice de Contenidos:** Lista ordenada de archivos y su identificador `CF-DOC-XXX`.
3.  **Fuera de Alcance:** Qué tipos de documentos **no deben** guardarse en esta carpeta (ej. en `docs/architecture/` no deben guardarse guías de sintaxis de código o manuales de bases de datos de bajo nivel).
4.  **Propietario:** El rol responsable del mantenimiento del directorio.
5.  **Lista Canónica:** Los documentos marcados como `role: canonical` dentro del directorio.
