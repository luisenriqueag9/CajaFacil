# Categoría Documental: Engineering / ADR (Architecture Decision Records)

## Propósito
Esta carpeta contiene el registro cronológico e inmutable de decisiones arquitectónicas significativas del proyecto CajaFácil. Cada archivo representa una decisión tomada en un instante del tiempo.

## Alcance
*   **Qué pertenece aquí:** Archivos de tipo ADR documentando la resolución de un problema de diseño transversal (persistencia, transacciones, autenticación, etc.).
*   **Qué NO pertenece aquí:** Documentos descriptivos vivos de cómo funciona el código o la base de datos hoy.

## Propietario
*   **Rol:** Lead Architect.

## Estructura de un ADR
Cada documento debe heredar la plantilla oficial ubicada en `docs/templates/adr_template.md` y contener:
1.  **Status:** Proposed, Accepted, Rejected, Superseded.
2.  **Context:** Justificación comercial y técnica de la necesidad.
3.  **Decision:** Alternativa y solución escogida.
4.  **Consequences:** Pros, contras y mitigaciones.

## Documentos Relacionados
*   Guías vivas de arquitectura en `docs/engineering/architecture/`.
