# 03 - Workflow Oficial de Sprints

## 1. Objetivo

Este documento establece la metodología de trabajo obligatoria para la planificación, desarrollo, revisión e integración de cualquier Sprint en **CajaFácil**. Define las fases secuenciales, la división de roles y los criterios de aceptación necesarios para garantizar que cada incremento del software se incorpore con el máximo estándar de calidad, consistencia y seguridad técnica.

---

## 2. Filosofía del Desarrollo

El desarrollo de software en CajaFácil se rige por cuatro pilares metodológicos:

* **El negocio dirige la tecnología:** Toda decisión de diseño, estructura de datos o selección de infraestructura está subordinada a las reglas operativas y requerimientos del negocio. La tecnología es un medio para hacer cumplir las reglas del negocio, no un fin en sí mismo.
* **Calidad sobre velocidad:** Es preferible ralentizar el progreso para asegurar la integridad de la base de código que introducir deuda técnica por prisa. Un código mal estructurado será rechazado inmediatamente.
* **Cambios pequeños e incrementales:** Se favorece la entrega de micro-sprints acotados y atómicos. Las modificaciones masivas y monolíticas aumentan el riesgo de regresiones y dificultan la revisión.
* **Dejar el proyecto mejor de como se encontró (Regla del Boy Scout):** Cada tarea o sprint debe aprovecharse para limpiar código obsoleto, documentar componentes ambiguos o refactorizar estructuras complejas que se encuentren dentro del alcance del desarrollo, elevando progresivamente la calidad general.

---

## 3. Flujo Oficial del Sprint

Cada Sprint en el proyecto debe transitar de forma ineludible por el siguiente flujo de fases ordenadas:

1. **Comprensión del problema:** Leer detalladamente los requerimientos, analizar el código físico existente y aclarar cualquier ambigüedad con el usuario.
2. **Análisis del negocio:** Identificar las reglas lógicas implicadas, restricciones numéricas de campos y dependencias del dominio.
3. **Definición del alcance:** Delimitar con exactitud qué componentes e interacciones se incluirán en el sprint y cuáles quedan explícitamente fuera para evitar desviaciones.
4. **Diseño arquitectónico:** Diseñar las interfaces de los repositorios, la firma de los casos de uso, las conversiones de persistencia y la forma de los DTOs de entrada y salida.
5. **Plan del Sprint:** Documentar el plan de implementación y las tareas del Sprint utilizando las herramientas o mecanismos definidos para el entorno de desarrollo vigente.
6. **Implementación:** Programar la solución siguiendo una progresión modular ascendente (capas internas del Dominio primero, seguidas por Persistencia, Aplicación y Presentación).
7. **Revisión arquitectónica:** Sommetar la base de código a la validación de cumplimiento de estándares, encapsulación de capas y chequeos multi-tenant.
8. **Correcciones:** Resolver cualquier anomalía sintáctica, error en la suite de pruebas o desalineación con respecto a los estándares de codificación.
9. **Aprobación:** Obtener la firma de conformidad explícita por parte del arquitecto principal del proyecto.
10. **Commit:** Confirmar de forma local los cambios mediante commits atómicos y mensajes estructurados.
11. **Push:** Subir la rama al repositorio central únicamente tras la aprobación definitiva de la revisión.

---

## 4. Roles

Para garantizar una gobernanza técnica eficiente, se definen los siguientes roles y responsabilidades en cada sprint:

* **Arquitecto Principal:** Establece las normas de diseño, aprueba los planes de implementación, realiza la revisión arquitectónica final y autoriza la integración del código en la rama principal.
* **Desarrollador (Humano):** Dirige la ejecución del sprint, alinea los requerimientos del negocio con la implementación, escribe pruebas lógicas, coordina a los asistentes artificiales de programación y realiza el despliegue final.
* **Inteligencia Artificial:** Actúa como asistente de codificación de alta fidelidad. Analiza la consistencia del código, sugiere planes de implementación, genera clases y métodos respetando estrictamente las capas y convenciones del proyecto y realiza la autocomprobación de calidad del código entregado.
* **Revisor:** Desarrollador o arquitecto alterno que evalúa los Pull Requests de forma aislada, verifica que no se introduzcan regresiones lógicas y valida la legibilidad y cohesión del código propuesto.

---

## 5. Fases del Sprint (División en Micro-Sprints)

Para evitar la complejidad cognitiva y facilitar la validación continua, un Sprint se fragmenta internamente en micro-sprints progresivos siguiendo la jerarquía del diseño modular:

```text
  Sprint de Módulo
         │
         ├──➔ 1. Micro-Sprint de Dominio (Entities, Exceptions, Repo Interface)
         │
         ├──➔ 2. Micro-Sprint de Persistencia (ORM Models, Mappers, Repo Impl, Migrations)
         │
         ├──➔ 3. Micro-Sprint de Aplicación (Use Cases, Commands)
         │
         ├──➔ 4. Micro-Sprint de Presentación (DTOs, Dependencies, Routers)
         │
         └──➔ 5. Micro-Sprint de Integración y Revisión (Manual Checks, Tests Run)
```

No se iniciará la programación de una capa posterior hasta que la capa subyacente haya sido completamente codificada, probada sintácticamente y verificada en sus interfaces.

---

## 6. Revisión Arquitectónica

Antes del cierre del Sprint, el código se somete a una auditoría técnica orientada a verificar los siguientes parámetros:

* **Aislamiento de Capas:** Confirmar que no existen importaciones de infraestructura (FastAPI, SQLAlchemy, bases de datos) en las carpetas de dominio o aplicación.
* **Cumplimiento de Estándares:** Validar convenciones de nombres, tipado fuerte (`Decimal`, `UUID`), uso obligatorio de constantes y organización de archivos.
* **Reutilización:** Verificar que no se hayan introducido funciones utilitarias o clases base que dupliquen lo ya provisto por `common`, `core` o `database`.
* **Seguridad Multi-Tenant:** Asegurar que toda query de lectura a base de datos aplique obligatoriamente el filtro de `company_id`.
* **Acoplamiento:** Validar que los routers no instancien entidades del dominio directamente y que las respuestas HTTP utilicen exclusivamente esquemas DTO.
* **Impacto Arquitectónico:** Confirmar que la solución propuesta no rompe la modularidad ni introduce dependencias que dificulten la evolución futura del sistema.

---

## 7. Criterios de Aprobación

Un Sprint solo será aprobado para su fusión e integración en la rama principal cuando cumpla simultáneamente con:

1. **Compilación y Pruebas Limpias:** Cero errores de sintaxis en el linter y aprobación del 100% de la suite de pruebas unitarias e integración.
2. **Estándares Satisfechos:** Verificación completa y positiva del checklist de estándares de codificación.
3. **Respeto Estricto de Capas:** Aislamiento total de las reglas de negocio en la capa interna (Dominio) y de los detalles HTTP en la capa externa (Presentación).
4. **Reglas de Negocio Fieles:** Validación funcional de que el código implementa exactamente las políticas numéricas, de redondeo y fiscales del negocio.
5. **Auditoría de Revisión Superada:** Aprobación explícita documentada por parte del Arquitecto Principal.

---

## 8. Gestión de Git

El control de versiones del Sprint debe seguir buenas prácticas estrictas:

* **Commit Pequeño y Atómico:** Cada commit debe resolver un único problema o introducir una capa lógica atómica concreta. Evita commits gigantescos que mezclen lógica de dominio con migraciones de base de datos o configuraciones de red.
* **Mensajes Claros y Estructurados:** Utiliza el estándar de commits semánticos: `[tipo]([módulo]): [descripción breve en minúsculas]` (ejemplos: `feat(module): implement get product use case`, `fix(database): correct foreign key migration`).
* **Push Controlado:** Queda estrictamente prohibido realizar push de cambios a ramas compartidas o de integración sin haber superado previamente la revisión arquitectónica y obtenido la aprobación formal.

---

## 9. Definition of Done (DoD)

Se define un Sprint como **Terminado (Done)** únicamente cuando se cumplen de forma exhaustiva los siguientes hitos:

1. **Código Compilado:** El incremento corre de forma local sin warnings y el linter no reporta violaciones.
2. **Test Coverage Verificado:** Los nuevos flujos lógicos y casos de uso cuentan con cobertura de pruebas unitarias automáticas funcionales.
3. **Esquemas Validados:** Los esquemas Request y Response DTO restringen de forma correcta los payloads y aíslan las entidades de dominio.
4. **Persistencia Sincronizada:** Las tablas ORM y sus restricciones físicas están alineadas y las migraciones de Alembic correspondientes han sido generadas y aplicadas.
5. **Aislamiento de Capas:** No existen fugas de dependencias tecnológicas externas hacia el núcleo del negocio.
6. **Filtros Multi-Tenant Aplicados:** Se garantiza que ningún endpoint devuelva información cruzada de otra empresa.
7. **Documentación Actualizada:** Toda modificación relevante debe reflejarse en la documentación oficial del proyecto cuando corresponda.
8. **Aprobación del Arquitecto:** El código ha sido revisado y firmado por el Arquitecto Principal del proyecto.

---

## 10. Checklist del Sprint

La Inteligencia Artificial debe autovalidar su entrega respondiendo afirmativamente a los siguientes puntos antes de notificar la finalización del Sprint al usuario:

* [ ] ¿El código del Sprint compila limpiamente y pasa el 100% de los tests automáticos locales?
* [ ] ¿Se crearon los casos de uso por separado, respetando la regla de un único archivo por acción operativa?
* [ ] ¿Se encapsularon las validaciones lógicas dentro de la entidad de dominio y se inician automáticamente?
* [ ] ¿Los enrutadores HTTP se comunican con los casos de uso a través del paso de DTOs o comandos específicos en lugar de instanciar entidades de dominio?
* [ ] ¿Las consultas de búsqueda y listados filtran estrictamente por la variable de tenant `company_id`?
* [ ] ¿Las confirmaciones en Git se agruparon en commits atómicos con descripciones claras de lo realizado?
* [ ] ¿Se eliminaron los logs basura, impresiones `print()` de consola y comentarios muertos en los archivos modificados?
* [ ] ¿Se redactó el walkthrough final resumiendo los cambios realizados y los métodos de prueba ejecutados?
