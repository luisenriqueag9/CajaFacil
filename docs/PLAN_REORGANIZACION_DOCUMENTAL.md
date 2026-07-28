---
id: CF-DOC-001
title: "Plan de Reorganización Documental"
owner: "cto"
status: "approved"
last_reviewed: 2026-07-24
role: "canonical"
---

# Plan de Reorganización Documental - CajaFácil

Este documento establece la estrategia y política oficial de gobierno documental para CajaFácil. Su objetivo es convertir el repositorio de conocimiento en un sistema estructurado, consistente y libre de redundancias, asegurando la escalabilidad operativa durante toda la vida del proyecto.

---

## 1. Visión y Objetivos

La documentación en CajaFácil es una extensión del software y debe regirse por los mismos principios de calidad.
*   **Simple:** Fácil de buscar y actualizar manualmente. Cero overhead burocrático.
*   **Consistente:** Sin contradicciones estilísticas, estructurales o idiomáticas.
*   **Integrado:** Conexión explícita entre las decisiones técnicas y las reglas operativas del negocio.
*   **Mantenible:** Mecanismo integrado de control de obsolescencia para evitar conocimiento podrido (stale knowledge).

---

## 2. Taxonomía y Organización del Repositorio (`docs/`)

Para evitar la dispersión de archivos y facilitar la navegación de desarrolladores y agentes de Inteligencia Artificial (IA), el repositorio de documentación se segmentará en carpetas especializadas por dominio de conocimiento:

```text
docs/
├── business/        # Negocio, manifiesto, reglas conceptuales y lenguaje ubicuo.
├── architecture/    # Diseño general, bounded contexts y flujos del sistema.
├── database/        # Modelos relacionales de datos, llaves foráneas y migraciones.
├── standards/       # Estándares de desarrollo, pruebas locales y linter.
├── adr/             # Registro cronológico de decisiones de arquitectura.
├── reference/       # Leyes fiscales, APIs externas, manuales de proveedores.
├── templates/       # Plantillas base para ADRs y especificaciones técnicas.
└── history/         # Cierre de sprints pasados y documentos obsoletos.
```

---

## 3. El Principio del Documento Canónico

Se establece la regla de **Cero Duplicación de Contenido**:
1.  **Única Fuente de Verdad:** Cada concepto importante de CajaFácil tendrá **uno y solo un** documento canónico (marcado con `role: "canonical"` en su frontmatter).
2.  **Prohibición de Redundancia:** Está prohibido copiar o parafrasear definiciones de reglas de negocio o arquitecturas en múltiples archivos.
3.  **Relaciones mediante Enlaces:** Si un documento de base de datos o backend necesita referenciar una tasa fiscal, deberá colocar un enlace de markdown explícito al documento canónico de impuestos (ej. `[Reglas Impositivas](file:///docs/business/06_REGLAS_DE_NEGOCIO.md)`) en lugar de redescribirlo.

---

## 4. Trazabilidad Documental y Frontmatter Mínimo

Cada documento activo del repositorio (exceptuando plantillas y reportes de sprint cerrado) iniciará obligatoriamente con el siguiente bloque YAML Frontmatter para auditar la vigencia y propiedad:

```yaml
---
id: CF-DOC-XXX                  # Identificador único incremental
title: "Título del Documento"    # Nombre del documento
owner: "cto | lead-architect | backend-lead | frontend-lead" # Rol responsable
status: "approved | historical | obsolete" # Estado actual del ciclo de vida
last_reviewed: YYYY-MM-DD       # Fecha de última revisión manual
role: "canonical | dependent | reference" # Tipo de documento respecto al tema
---
```

### Relación de Roles
*   **Canonical:** El documento oficial que define las reglas de un tema.
*   **Dependent:** Archivos que implementan detalles de un canónico. Deben colocar un enlace markdown al inicio que apunte a la fuente de verdad.
*   **Reference:** Archivos complementarios que citan conceptos para contexto general.

---

## 5. Gobierno Documental y Propietarios

Se asigna la responsabilidad de mantenimiento y vigencia técnica por directorio:

*   **CTO:** Custodio del Manifiesto, estrategia de gobierno y este Plan.
*   **Lead Architect:** Responsable del diseño macro (`architecture`), la base de datos (`database`) y las decisiones de diseño (`adr`).
*   **Product Owner / Business Analyst:** Responsable del área de negocio (`business`).
*   **Backend Lead / Frontend Lead:** Responsables respectivos de los estándares técnicos, pruebas unitarias y guías de desarrollo (`standards`).
*   **AI Architect:** Responsable del adaptador de contexto para IA (`docs/ai/`).

---

## 6. Architecture Decision Records (ADRs)

*   **Ubicación:** `docs/adr/`.
*   **¿Cuándo crear un ADR?** Siempre que se tome una decisión tecnológica compleja, transversal o irreversible (sincronización, persistencia, transacciones, autenticación).
*   **Evitar Duplicidad con la Arquitectura:** El ADR es una bitácora inmutable. Una vez aprobado (`status: approved`), los detalles operativos y guías resultantes de la decisión se documentan en el archivo de arquitectura correspondiente (`docs/architecture/`), enlazando al ADR únicamente como origen de la decisión.

---

## 7. Estrategia contra la Obsolescencia y Ciclo de Vida

Para mantener la documentación alineada con la realidad del código:
1.  **Gatillador de Revisión:** Cada cambio en el código que afecte la arquitectura o las reglas operativas del negocio obliga a actualizar el documento canónico en el mismo Pull Request, modificando el campo `last_reviewed`.
2.  **Ciclo de Vida:**
    *   `approved`: Especificación activa y vigente en producción.
    *   `historical`: Documentos informativos de hitos cerrados. Se mueven físicamente a `docs/history/`.
    *   `obsolete`: Documentos de características discontinuadas o diseños descartados. Se marca su estado como `obsolete` en el frontmatter y se mueven físicamente a `docs/history/`.

---

## 8. Tratamiento de `99_PROYECTO_CAJAFACIL_AI.md`

El archivo monolítico `99_PROYECTO_CAJAFACIL_AI.md` se archiva y posteriormente se elimina. Su contenido ha sido redistribuido en `docs/ai/00_LEEME.md` (adaptador para IA) y `docs/REGLAS_DE_DOCUMENTACION.md` (manual estilístico).
1.  Se cambia su estado a `status: obsolete`.
2.  Se añade una redirección explícita a `docs/ai/00_LEEME.md`.
3.  Se mueve a `docs/history/`.
4.  Se eliminará en un posterior sprint de saneamiento una vez estabilizada la nueva estructura.
