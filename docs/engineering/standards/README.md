# Categoría Documental: Engineering / Standards (Estándares y Guías Técnicas)

## Propósito
Esta carpeta centraliza todos los estándares de programación, convenciones de desarrollo de backend y frontend, políticas de transaccionalidad, pautas para pruebas automáticas y guías de onboarding rápido.

## Alcance
*   **Qué pertenece aquí:** Estándares de Clean Architecture y DDD aplicados al código, guías de testing local en memoria con pytest, directrices de sincronización offline-first local y configuraciones estilísticas.
*   **Qué NO pertenece aquí:** Decisiones históricas puntuales (deben ir en `docs/adr/`) o diagramas macro de arquitectura.

## Propietario
*   **Rol:** Backend Lead / Frontend Lead.

## Documentos Canónicos
*   `22_BACKEND_ARQUITECTURA.md` (CF-DOC-030): Estructura física y dependencias de FastAPI.
*   `23_FRONTEND_ARQUITECTURA.md` (CF-DOC-031): Arquitectura del cliente Flutter.
*   `34_ESTANDARES_DE_IMPLEMENTACION.md` (CF-DOC-032): Directrices de codificación en capas y flujos de datos.
*   `35_ESTANDARES_DDD.md` (CF-DOC-033): Uso de dataclasses e invariantes del dominio en memoria.
*   `36_ESTANDARES_TRANSACCIONALES.md` (CF-DOC-034): Manejo de Unit of Work y control de sesiones.
*   `37_ESTANDARES_OFFLINE_FIRST.md` (CF-DOC-035): Políticas de base de datos embebida SQLite local y stock caché.
*   `38_ESTANDARES_DE_PRUEBAS.md` (CF-DOC-036): Pautas de testing y aislamiento de base de datos relacional.
*   `39_GUIA_DESARROLLO_CAJAFACIL.md` (CF-DOC-037): Onboarding y guías rápidas de configuración de entorno.
*   `40_GUIA_IA_CAJAFACIL.md` (CF-DOC-038): Guía de integración de directrices de desarrollo para asistentes de IA.
