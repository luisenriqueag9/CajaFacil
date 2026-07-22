# 00 - LEEME
Versión: 1.0
Estado: Aprobado
Última actualización: 2026-07-21
Tipo: Estándar Oficial para Inteligencias Artificiales

## 1. Objetivo del documento

Este documento define las reglas de operación, directrices técnicas y restricciones de diseño que cualquier Inteligencia Artificial (IA) generadora de código, agente autónomo o asistente de programación (ej. ChatGPT, Antigravity, Cursor, etc.) debe comprender y acatar antes de realizar cualquier lectura o escritura en el repositorio de **CajaFácil**.

El propósito de esta carpeta `docs/ai/` es servir como un adaptador de contexto optimizado para agentes artificiales. Su meta es asegurar que cualquier propuesta de código respete de forma estricta la arquitectura establecida, prevenga la introducción de código muerto, evite la duplicación de lógica y mantenga la separación estricta de responsabilidades del sistema.

---

## 2. ¿Qué es CajaFácil?

**CajaFácil** es un ecosistema de punto de venta (POS) multi-tenant diseñado bajo el modelo de Software como Servicio (SaaS), enfocado en micro, pequeñas y medianas empresas. Su arquitectura técnica está dividida en un backend de alto rendimiento desarrollado en Python con FastAPI y un cliente de escritorio responsivo multiplataforma desarrollado en Flutter.

El sistema se rige bajo un enfoque *offline-first*. El cliente local procesa transacciones e inventarios de forma independiente utilizando una base de datos local SQLite y sincroniza el estado operativo hacia una base de datos centralizada PostgreSQL en la nube cuando detecta conectividad de red estable.

El diseño del backend sigue un patrón modular cerrado. Cada entidad de negocio (ej. empresas, productos, categorías) opera de manera aislada dentro de su propio espacio lógico, lo que asegura escalabilidad, facilidad de pruebas y un mantenimiento independiente del ciclo de vida de cada agregado.

---

## 3. Principio Fundamental

En CajaFácil rige una regla dorada que gobierna todas las decisiones técnicas:

> [!IMPORTANT]  
> **Toda decisión técnica debe estar subordinada a las reglas del negocio.**

Si en algún momento del desarrollo surge un conflicto entre una facilidad de implementación técnica (ya sea de librerías, de FastAPI, de base de datos o de Flutter) y una regla operativa del negocio descrita en la documentación de requerimientos, **siempre prevalece el negocio**. La IA nunca debe deformar, flexibilizar ni modificar el modelo del negocio con el propósito de simplificar el código o facilitar su implementación tecnológica.

---

## 4. Rol esperado de una IA

Cuando participes en el desarrollo de CajaFácil, debes operar bajo las siguientes pautas de ingeniería de software:

* **Respetar la arquitectura existente:** No alteres la división de carpetas ni el flujo establecido de control y datos sin una justificación de diseño aprobada.
* **Reutilizar antes de crear:** Inspecciona siempre las clases genéricas, los manejadores de excepciones y las utilidades compartidas del core antes de proponer código nuevo.
* **Proteger la modularidad:** Mantén el acoplamiento entre módulos en el mínimo nivel posible. La comunicación entre distintas áreas debe realizarse a través de contratos claros.
* **Mantener Clean Architecture y DDD:** Asegura la separación física de las capas de presentación, aplicación, dominio y persistencia.
* **Proponer mejoras antes de implementar:** Presenta un análisis formal de impacto técnico de cualquier cambio antes de modificar los archivos existentes.
* **Garantizar la inmutabilidad de reglas del negocio:** Nunca alteres las reglas, tasas fiscales o flujos financieros descritos en la documentación sin validación explícitamente firmada.

---

## 5. Estado actual del proyecto

Antes de sugerir o escribir cualquier cambio en el repositorio, la IA debe realizar una fase de reconocimiento técnico basada en los siguientes puntos:

* **Analizar la estructura física actual del proyecto:** Validar qué directorios existen y evitar asumir la presencia de archivos que aún no se han creado.
* **Identificar el módulo involucrado:** Localizar con precisión los archivos del dominio específico en los que incide el requerimiento.
* **Revisar el estado real de implementación:** Determinar si un módulo se encuentra en estado de esqueleto (directorios y modelo de datos únicamente) o si ya cuenta con lógica funcional completa.
* **Detectar componentes reutilizables:** Comprobar si hay repositorios base, excepciones genéricas o configuraciones estables del sistema que deban heredarse.
* **Confirmar la consistencia de la documentación:** Validar que las directrices escritas sigan reflejando el estado real del código.

> [!WARNING]  
> En este proyecto, **el código existente siempre tiene prioridad absoluta sobre cualquier suposición** del agente. La IA debe verificar el sistema físico antes de actuar.
Si existe una diferencia entre la documentación y el código, la IA debe informar la inconsistencia antes de implementar cambios.

---

## 6. Módulo de referencia

El diseño modular del backend está estandarizado para asegurar la homogeneidad y evitar la duplicación de patrones estructurales.

* **Patrón Oficial:** El módulo **Product** ([`backend/app/modules/product`](../../backend/app/modules/product)) constituye el patrón arquitectónico de referencia oficial para la creación e implementación de módulos maestros y catálogos en el backend.
* **Regla de Réplica:** Cualquier nuevo módulo maestro o catálogo (tales como **Category**, **Brand** o **Unit**) debe replicar de manera exacta la distribución, firmas y flujos del módulo `product`.
* **Prohibición:** Está prohibido reinventar la estructura de capas, la inyección de dependencias o los mecanismos de mapeo para nuevos módulos maestros. Solo se deben adaptar las validaciones y lógicas específicas del dominio correspondiente.

---

## 7. Documentación obligatoria

Antes de escribir cualquier línea de código, debes leer la documentación en el siguiente orden de prelación para asimilar el contexto del proyecto, utilizando únicamente rutas relativas:

1. **[`../00_MANIFIESTO_CAJA_FACIL.md`](../00_MANIFIESTO_CAJA_FACIL.md):** Provee la visión estratégica del producto, sus limitantes técnicas y las metas de experiencia de usuario.
2. **[`../02_ARQUITECTURA_GENERAL.md`](../02_ARQUITECTURA_GENERAL.md):** Describe la topología física, la estrategia de sincronización offline y los flujos de comunicación cliente-servidor.
3. **[`../06_REGLAS_DE_NEGOCIO.md`](../06_REGLAS_DE_NEGOCIO.md):** Contiene la especificación lógica de impuestos, cálculos matemáticos, control de inventario y elegibilidad de venta.
4. **[`01_PATRON_MODULO_MAESTRO.md`](01_PATRON_MODULO_MAESTRO.md) (si existe):** Guía práctica de referencia con la plantilla y estándares para la construcción homogénea de nuevos módulos CRUD en backend y frontend.

---

## 8. Flujo oficial de trabajo

Cualquier cambio propuesto por una IA debe transitar obligatoriamente a través del siguiente flujo de desarrollo estructurado:

```text
Analizar ➔ Proponer ➔ Esperar Aprobación ➔ Implementar ➔ Revisión Arquitectónica ➔ Correcciones ➔ Commit ➔ Push
```

1. **Analizar:** Inspeccionar el estado de los archivos y la base de datos sin realizar modificaciones. Localizar dependencias que puedan verse afectadas.
2. **Proponer:** Generar un documento de plan de implementación detallado (Markdown) que describa las modificaciones necesarias y los nuevos archivos, identificando posibles riesgos.
3. **Esperar Aprobación:** Detener la ejecución del agente y esperar a que el usuario valide de forma explícita la propuesta antes de continuar.
4. **Implementar:** Escribir el código estrictamente acordado, capa por capa, comenzando siempre por las definiciones del Dominio y avanzando hacia la infraestructura.
5. **Revisión Arquitectónica:** Evaluar que el código generado no contenga acoplamientos prohibidos, fugas de multi-tenancy o violaciones de tipos de datos.
6. **Correcciones:** Ajustar el código ante fallos de pruebas, linter o revisiones de diseño.
7. **Commit & Push:** Confirmar la versión en el control de cambios una vez que compile de forma limpia y todas las pruebas de integración pasen con éxito.

---

## 9. Reglas durante un Sprint

Durante la fase de codificación de un Sprint, la IA debe limitar estrictamente su comportamiento operativo bajo las siguientes condiciones:

* **Implementar únicamente el alcance aprobado:** No agregues endpoints, campos ni parámetros adicionales al plan de implementación autorizado.
* **No agregar funcionalidades no solicitadas:** Evita programar atajos, utilidades extras o extensiones de negocio futuras.
* **Documentar mejoras sin programarlas:** Si detectas áreas de optimización técnica o lógica, regístralas en un reporte escrito para futuros sprints, pero no las incorpores en la base de código activa.
* **No realizar refactorizaciones no autorizadas:** No modifiques ni alteres el código de módulos vecinos o del core fuera del alcance delimitado del Sprint actual.

---

## 10. Principios de desarrollo

Las soluciones propuestas deben regirse bajo los siguientes principios generales:

* **Clean Architecture:** Independencia de frameworks, UI, bases de datos y agentes externos.
* **Domain-Driven Design (DDD):** Lógica del negocio modelada en entidades de dominio enriquecidas e invariantes bien protegidas.
* **SOLID:** Estricta adherencia a los principios de diseño orientado a objetos.
* **Modularidad Aislada:** Cohesión alta dentro de cada módulo y acoplamiento débil con el exterior.
* **Python Puro en Dominio:** Capas de dominio libres de SQLAlchemy, Pydantic, FastAPI o dependencias de red.
* **SaaS Multi-tenant Estricto:** Scopar toda consulta relacional al identificador del cliente (`company_id`).
* **Decimal Precision:** Uso exclusivo del tipo de dato `Decimal` para cualquier cálculo monetario o de stock fraccionario.
* **Bajo Acoplamiento y Alta Cohesión:** Estructuración de responsabilidades simples y claras.

---

## 11. Definición de Terminado (Definition of Done)

Un Sprint o tarea de programación ejecutado por una IA solo se considerará **Terminado (Done)** si cumple de manera exhaustiva con los siguientes criterios:

* **Compilación Correcta:** El backend y el frontend compilan de forma limpia y aprueban la suite completa de pruebas automáticas. El código debe compilar correctamente y ejecutar satisfactoriamente las validaciones, pruebas o verificaciones disponibles para el alcance del Sprint..
* **Respeto a Clean Architecture:** Ninguna capa externa contamina las capas internas (los controladores y modelos no tocan el dominio de forma inapropiada).
* **Respeto a DDD:** Las validaciones de invariantes de negocio residen en la entidad del dominio.
* **Revisión de Capas Exitosa:** No existen importaciones de base de datos u ORMs en la lógica del caso de uso.
* **Aprobación de Arquitectura:** El diseño de la solución es ratificado y aprobado de forma explícita por el arquitecto líder del proyecto.
* **Listo para Commit:** El código se encuentra libre de logs basura, depuradores temporales o comentarios muertos.

---

## 12. Lo que una IA NO debe hacer

Quedan terminantemente prohibidas las siguientes acciones durante el desarrollo:

* **No modificar la arquitectura sin aprobación:** No alterar la estructura jerárquica de carpetas ni el patrón de capas establecido.
* **No crear nuevas capas:** No introducir niveles adicionales de abstracción (ej. managers, helpers compartidos fuera de common) no acordados.
* **No mezclar dominio con infraestructura:** Nunca importes drivers de base de datos, ORMs o librerías HTTP en las carpetas `domain/` o `application/`.
* **No colocar lógica de negocio en routers o DTOs:** La validación web se limita a la verificación del tipo de dato; las reglas de negocio pertenecen al dominio.
* **No utilizar SQLAlchemy en el dominio:** Las entidades y repositorios de dominio deben desconocer la persistencia física.
* **No duplicar código existente:** Prohibido escribir mappers manuales o clases CRUD redundantes si ya existe un genérico implementado en `common` o `database`.
* **No asumir reglas del negocio:** Si un requerimiento financiero o de inventario es ambiguo, pregunta al usuario antes de implementar fallbacks silenciosos.

---

## 13. Evolución del documento

Este documento constituye un estándar vivo de ingeniería para el proyecto CajaFácil. 

* **Actualizaciones:** El manual evolucionará a la par del crecimiento del sistema y la introducción de nuevos paradigmas.
* **Prohibición de Edición Autónoma:** Ninguna Inteligencia Artificial tiene autorización para modificar este archivo o cualquier estándar de la carpeta `docs/ai/` de manera autónoma.
* **Aprobación Obligatoria:** Cualquier cambio propuesto a esta guía operativa debe ser analizado, justificado y aprobado de forma explícita por el arquitecto principal del proyecto antes de ser integrado como nueva regla.

---

## 14. Referencias

Los lineamientos específicos de formateo, plantillas de código para capas de backend y lineamientos de widgets responsivos de Flutter se encuentran especificados en los archivos subsiguientes dentro del directorio [`docs/ai/`](01_PATRON_MODULO_MAESTRO.md).
La lectura de este documento es obligatoria para cualquier IA antes de consultar los documentos restantes de docs/ai.
