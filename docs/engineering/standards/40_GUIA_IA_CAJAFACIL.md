# 40_GUIA_IA_CAJAFACIL.md

**Versión:** 1.0  
**Estado:** 📜 Aprobado (Sprint 16)  
**Última actualización:** 2026-07-23  
**Documento:** Guía de Colaboración y Directrices para IAs (AI Assistant Guide)  

---

# 1. Rol y Límites del Asistente de IA

Esta guía establece el marco de operación para cualquier Inteligencia Artificial que colabore en el desarrollo de CajaFácil. Su propósito es preservar la integridad de la arquitectura modular y evitar la spaghettización del código.

---

# 2. Protocolo de Trabajo por Fases (Obligatorio)

Cuando una IA trabaje en una tarea de desarrollo, debe respetar rigurosamente el flujo por fases del proyecto:

### Fase 1: Análisis Funcional
* **Qué hace la IA:** Investiga las reglas operativas y documenta el análisis funcional en Markdown.
* **Restricción:** No debe sugerir tablas, tipos de datos técnicos, modelos ORM ni tecnologías FastAPI. Debe enfocarse únicamente en el valor del negocio.

### Fase 2: Diseño de Dominio
* **Qué hace la IA:** Define agregados, entidades, value objects, invariantes y eventos usando Python abstracto y lenguaje ubicuo.
* **Restricción:** Sin bases de datos ni frameworks.

### Fase 3: Diseño Arquitectónico
* **Qué hace la IA:** Define la estrategia de capas, contratos abstractos de repositorio, casos de uso, eventos y comunicación permitida/prohibida.

### Fase 4: Implementación y Pruebas
* **Qué hace la IA:** Genera el código correspondiente a cada capa respetando las dependencias. Escribe y ejecuta la suite de pruebas unitarias e integración en SQLite.

---

# 3. Qué puede Modificar una IA y Qué NO

### Permitido Modificar (Bajo Especificación)
* Archivos del módulo en desarrollo actual (`app/modules/<modulo_actual>/`).
* Archivos de pruebas correspondientes a ese módulo.
* Registro de routers en `app/main.py` e importaciones de metadatos en `app/database/base.py`.

### Prohibido Modificar (Criterio de Exclusión)
* ❌ **Dominio o infraestructura de módulos ya congelados y aprobados** (ej. Ventas, Inventario, Company, etc.) a menos que exista un conflicto técnico de metadatos (como el renombrado de tablas mock del Sprint 14).
* ❌ **BaseRepository y lógica común del núcleo** (`app/database/repositories.py`).
* ❌ **Estrategia transaccional (Unit of Work):** No inyectar `db.commit()` en repositorios ni saltarse el event dispatcher.
* ❌ **Reglas de negocio ya consolidadas** (`RN-100` a `RN-500` series).

---

# 4. Directrices de Auditoría y Documentación

Antes de entregar cualquier tarea, la IA debe realizar una auto-auditoría verificando:
1. **Puntualidad de Commits:** No hacer commit automático; delegarlo al desarrollador.
2. **Aislamiento Multitenant:** Asegurar que todo caso de uso y consulta filtre estrictamente por `company_id`.
3. **Rollback en Fallos:** Correr las pruebas transaccionales locales y verificar que un fallo en event handlers deshace la persistencia SQLite.
4. **Walkthrough:** Generar una bitácora detallando archivos alterados, cobertura funcional y deuda identificada.
