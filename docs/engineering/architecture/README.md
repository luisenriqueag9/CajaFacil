# Categoría Documental: Engineering / Architecture (Arquitectura Macro)

## Propósito
Esta carpeta documenta el diseño de alto nivel del sistema, los patrones globales aplicados (Clean Architecture, DDD, CQRS) y la delimitación lógica de los Bounded Contexts.

## Alcance
*   **Qué pertenece aquí:** Guías de arquitectura general, diagramas de módulos macro, flujos generales de comunicación de datos y políticas de desacoplamiento a nivel de dominio.
*   **Qué NO pertenece aquí:** Detalles de sintaxis de base de datos o convenciones de código de bajo nivel.

## Propietario
*   **Rol:** Lead Architect.

## Documentos Canónicos
*   `02_ARQUITECTURA_GENERAL.md` (CF-DOC-010): Estructura de capas, dependencias y flujo general.
*   `05_MODELO_DEL_DOMINIO.md` (CF-DOC-011): Definición de agregados, entidades y Bounded Contexts.
*   `14_REVISION_ARQUITECTONICA.md` (CF-DOC-012): Auditoría de diseño técnico inicial.

## Documentos Dependientes (Diseños Detallados de Módulo)
*   `24_DISENO_ARQUITECTONICO_VENTAS.md` (CF-DOC-024): Diseño técnico en capas del módulo de Ventas.
*   `28_DISENO_ARQUITECTONICO_INVENTARIO.md` (CF-DOC-028): Diseño técnico en capas del módulo de Inventario.
*   `32_DISENO_ARQUITECTONICO_CAJA.md` (CF-DOC-032): Diseño técnico en capas del módulo de Caja.

## Documentos Relacionados
*   Estándares de implementación en `docs/engineering/standards/`.
*   Diseño físico de tablas en `docs/engineering/database/`.
