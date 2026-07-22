# 06 - Checklist Oficial de Revisión

## 1. Objetivo

Este documento establece el checklist de auditoría técnica oficial que el Arquitecto Principal del proyecto debe emplear para evaluar, rechazar o aprobar cualquier incremento de software (Sprint) antes de autorizar su integración definitiva en la base de código de **CajaFácil**. Define los controles obligatorios sobre reglas lógicas, separación física de capas, tipado de datos, seguridad multi-tenant e integridad de Git.

---

## 2. Revisión del Negocio

El objetivo primordial es verificar la fidelidad de la solución respecto a las necesidades del cliente:

* [ ] **Cumplimiento de Reglas de Negocio:** El código implementa con precisión matemática y funcional todas las políticas comerciales descritas en las directivas de reglas de negocio.
* [ ] **Alcance Correcto:** La implementación satisface de manera exacta y completa los requerimientos técnicos y funcionales acordados para el Sprint activo.
* [ ] **Sin Funcionalidades Extra:** Se confirma la total ausencia de atajos, utilidades redundantes o características que no forman parte del alcance aprobado del Sprint (no hay "feature creep").

---

## 3. Revisión Arquitectónica

Controlar que el diseño se alinee con Clean Architecture y DDD:

* [ ] **Respeto de Capas:** Aislamiento estricto de componentes. No existen importaciones de infraestructura (FastAPI, SQLAlchemy) en Dominio o Aplicación.
* [ ] **Dependencias Permitidas:** Cada clase o archivo del módulo cumple de forma estricta con la tabla de dependencias autorizadas para su respectiva capa.
* [ ] **Acoplamiento Débil:** Los controladores no instancian clases de negocio y las respuestas HTTP no exponen entidades lógicas del Dominio directamente.
* [ ] **Alta Cohesión:** Cada clase, caso de uso y archivo está enfocado en cumplir una sola y única responsabilidad estructural.
* [ ] **Reutilización del Core:** No se han reimplementado helpers, wrappers de respuestas, validaciones genéricas o estructuras de datos abstractas ya provistas por `common`, `core` o `database`.

---

## 4. Revisión de Código

Inspección estilística y de calidad de programación:

* [ ] **Estándares de Código:** Cumplimiento total de las pautas estilísticas del lenguaje y de las directrices de formateo del proyecto.
* [ ] **Tipado Fuerte:** Declaración obligatoria de *Type Hints* en parámetros y valores de retorno. Uso estricto de `Decimal` en valores numéricos monetarios/fraccionarios y `UUID` en identificadores lógicos.
* [ ] **Nombres Convencionales:** Clases en `PascalCase`, variables y funciones en `snake_case`, constantes en `UPPER_SNAKE_CASE` y sufijos adecuados según el patrón de diseño.
* [ ] **Complejidad Controlada:** Funciones y métodos pequeños (bajo las 30 líneas de código) y profundidad de anidamiento plano (máximo 3 niveles mediante cláusulas de guarda).
* [ ] **Estructura de Clases:** Constructores dedicados exclusivamente a la asignación e inyección, atributos privados prefijados con guion bajo (`_`) y preferencia por composición.

---

## 5. Revisión de Persistencia

Validación del esquema físico de la base de datos y su acceso:

* [ ] **Modelado ORM:** Los modelos locales SQLAlchemy están unificados en la base declarativa del core y sus columnas están tipadas congruentemente con el Dominio.
* [ ] **Migraciones Seguras:** Las migraciones de Alembic son lineales, reversibles y utilizan la cláusula de lotes (`render_as_batch=True`) para garantizar la compatibilidad con SQLite.
* [ ] **Integridad y Restricciones:** Las políticas de eliminación y actualización de relaciones deberán ser coherentes con las reglas del negocio y las convenciones arquitectónicas del proyecto.
* [ ] **Índices de Unicidad:** Restricciones lógicas de unicidad respaldadas por índices físicos compuestos en base de datos.
* [ ] **Identificadores UUID:** Verificación de que todas las primary keys y foreign keys se almacenan físicamente como tipos de datos UUID.
* [ ] **Multiempresa (Multi-tenancy):** Comprobación de que toda consulta de persistencia y query relacional aplica estrictamente el filtrado sobre `company_id`.

---

## 6. Revisión de API

Verificación del contrato público expuesto por la red:

* [ ] **Versionado e Interfaces:** Enrutadores REST versionados adecuadamente (prefijo `/api/v1`) y respuestas JSON estructuradas uniformemente en la envoltura genérica de respuestas de éxito.
* [ ] **Uso de DTOs:** Peticiones HTTP de entrada capturadas en DTO Request y respuestas de salida devueltas como DTO Response.
* [ ] **Validación Sintáctica:** DTOs Pydantic configurados con validaciones de tipo, longitud y rangos numéricos.
* [ ] **Códigos de Estado HTTP:** Respuestas y excepciones mapeadas a códigos de estado semánticos apropiados (200, 201, 400, 404, 409).

---

## 7. Revisión de Seguridad

Control de riesgos operativos y de confidencialidad:

* [ ] **Aislamiento Multiempresa Absoluto:** Comprobación lógica de que es matemáticamente imposible que un usuario de la Empresa A consulte, edite o altere datos pertenecientes a la Empresa B.
* [ ] **No Exposición de Dominio:** Ninguna ruta de API expone de forma serializada directa la estructura interna de una entidad del dominio.
* [ ] **Validaciones de Invariantes Protegidas:** Se ejecutan validaciones en la entidad de dominio y los casos de uso para evitar inyecciones lógicas de datos numéricos inconsistentes.
* [ ] **Protección de Datos Sensibles:** Contraseñas, claves criptográficas y tokens de sesión no viajan en plano en payloads ni se exponen de forma insegura.
* [ ] **Logger Seguro:** Los registros del logger no exponen datos sensibles (como claves o información de pago) en los logs consolidados.

---

## 8. Revisión de Documentación

* [ ] **Documentación al Día:** La documentación oficial correspondiente al Sprint fue actualizada cuando el cambio lo requirió.
* [ ] **Consistencia con los Estándares:** Los walkthroughs y especificaciones técnicas no contradicen ninguno de los documentos normativos de la carpeta `docs/ai/`.

---

## 9. Revisión de Git

* [ ] **Commits Atómicos:** La rama del sprint presenta un historial de commits segmentados lógicamente (capa por capa) en lugar de una confirmación monolítica gigante.
* [ ] **Mensajes Semánticos:** Los mensajes de Git respetan la convención semántica definida por el proyecto.
* [ ] **Limpieza de Archivos:** No existen archivos temporales, configuraciones IDE locales o binarios inútiles agregados en la confirmación.
* [ ] **Sin Código Muerto:** Total ausencia de llamadas de depuración (`print()`), comentarios obsoletos, TODOs huérfanos o funciones muertas en los archivos fusionados.

---

## 10. Criterios de Rechazo (Showstoppers)

La detección de cualquiera de las siguientes anomalías durante la revisión obligará al Arquitecto Principal a rechazar de forma inmediata el Sprint para corrección:

* **Violación de Capas:** Importación de ORMs, base de datos o FastAPI en Dominio o Aplicación.
* **Código Duplicado:** Creación redundante de mappers, validadores o repositorios genéricos que deban ser centralizados en el core.
* **Fuga de Datos Multi-Tenant:** Queries de base de datos o endpoints que omitan filtrar por `company_id`.
* **Uso de floats:** Declarar variables de dinero utilizando el tipo float.
* **Uso de print():** Presencia de la función `print()` nativa en código productivo.
* **Incumplimiento del Negocio:** Desviación o alteración de las políticas y requerimientos del negocio.
* **Ausencia de las pruebas requeridas por el alcance del Sprint.:** Módulos lógicos o casos de uso nuevos sin cobertura de tests unitarios funcionales automáticos.

---

## 11. Aprobación Final (Scorecard)

Para la firma final del Sprint, el Arquitecto Principal completará de forma objetiva la siguiente tabla:

| Criterio de Control | Evaluación (Pasa / Falla) | Observaciones |
| :--- | :---: | :--- |
| 1. Compilación y Suite de Tests locales limpia | | |
| 2. Aislamiento físico de dependencias por capas | | |
| 3. Aislamiento de seguridad Multi-Tenant (`company_id`) | | |
| 4. Tipado estricto de precisión (`Decimal` / `UUID`) | | |
| 5. Mapeo y DTOs REST aislados del Dominio | | |
| 6. Historial de commits Git atómico y limpio | | | 
  7. Documentación actualizada | | |

* **Decisión de Integración:** [ APROBADO / RECHAZADO ]
* **Firma del Arquitecto Principal:** _____________________________
* **Fecha de aprobación:** __________________
