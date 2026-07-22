# 02 - Estándares de Código

## 1. Objetivo

Este documento define las normas, convenciones y buenas prácticas de programación que deben regir el desarrollo del backend de **CajaFácil**. Establece un marco de calidad obligatorio para asegurar que todo el código escrito (tanto por desarrolladores humanos como por Inteligencias Artificiales) sea legible, homogéneo, fácil de probar y libre de acoplamientos indeseados.

---

## 2. Principios Generales
### Principio de Consistencia

Cuando exista más de una forma técnicamente válida de implementar una solución, deberá elegirse aquella que mantenga la mayor consistencia con el resto del proyecto.

La consistencia tiene prioridad sobre las preferencias personales del desarrollador o de la Inteligencia Artificial.

Si un patrón ya ha sido aprobado e implementado correctamente en CajaFácil, deberá reutilizarse antes de proponer una variante diferente.

Todo desarrollo dentro del sistema debe respetar los siguientes principios rectores:

* **Legibilidad:** El código debe ser limpio y autoexplicativo. Se escribe código para que sea leído por humanos antes que por máquinas.
* **Simplicidad (KISS):** Favorece soluciones sencillas y directas. Evita la sobreingeniería y abstracciones innecesarias.
* **Responsabilidad Única (SRP):** Cada clase, función, método y archivo debe tener una sola razón para cambiar, resolviendo un único problema a la vez.
* **Bajo Acoplamiento:** Los componentes deben interactuar a través de contratos e interfaces abstractas, minimizando la dependencia mutua.
* **Alta Cohesión:** Los elementos lógicos que componen un módulo deben estar estrechamente relacionados con su propósito.
* **Reutilización:** Evita duplicar lógica. Centraliza comportamientos transversales e instrumenta herencias solo cuando exista una relación estructural clara.
* **Consistencia:** Mantén la coherencia estilística e instrumental del código en todo el proyecto. Si un patrón ya funciona en un módulo, replícalo idénticamente.

---

## 3. Convenciones de Nombres

El proyecto utiliza nomenclatura en inglés para variables, funciones y estructuras lógicas, y en español únicamente para variables conceptuales del negocio explícitas. Se deben aplicar las siguientes reglas estilísticas según el elemento:

* **Módulos y Paquetes:** Carpetas escritas en minúsculas y en singular (ej. `brand`, `category`, `product`).
* **Archivos:** Nombres en minúsculas utilizando `snake_case`, agregando el sufijo correspondiente al patrón (ej. `[domain]_router.py`, `[domain]_repository_impl.py`).
* **Clases:** Escritas en `PascalCase` (UpperCamelCase), iniciando con mayúscula.
* **Interfaces (Contratos):** Clases abstractas escritas en `PascalCase` sin prefijo 'I' pero con sufijo de responsabilidad (ej. `ProductRepository`).
* **Métodos y Funciones:** Nombres descriptivos en `snake_case` que utilicen verbos de acción (ej. `get_by_id`, `validate_uniqueness`).
* **Variables:** Nombres autodescriptivos en `snake_case` (ej. `created_product`, `validation_errors`). Evita el uso de letras solas como nombres de variables.
* **Constantes:** Escritas en mayúsculas sostenidas utilizando `UPPER_SNAKE_CASE` (ej. `ALLOWED_UPDATE_FIELDS`, `DB_TO_DOMAIN_STATUS`).
* **DTO (Data Transfer Objects):** Clases escritas en `PascalCase` con los sufijos `Request` o `Response` (ej. `CreateProductRequest`, `ProductResponse`).
* **UseCase:** Clases escritas en `PascalCase` con el sufijo `UseCase` (ej. `CreateProductUseCase`).
* **Repository (Implementación):** Clases escritas en `PascalCase` con el sufijo `RepositoryImpl` (ej. `ProductRepositoryImpl`).
* **Mapper:** Archivos de mapeo escritos en `snake_case` con el sufijo `_mapper.py` y nombres de funciones utilitarias en verbo infinitivo (`to_db`, `to_domain`).
* **Router:** Archivo escrito en `snake_case` con el sufijo `_router.py`. La variable de enrutamiento de FastAPI debe llamarse siempre `router`.

---

## 4. Organización de Archivos

* **Una Clase por Archivo:** Cada caso de uso, repositorio, router, entidad de dominio y DTO debe residir en su propio archivo independiente. Esto facilita el aislamiento de cambios y reduce conflictos en el control de versiones.
* **Longitud del Archivo:** Los archivos deben ser concisos. Se recomienda mantener los archivos pequeños y cohesionados. Como referencia general, un archivo no debería superar aproximadamente las 300 líneas de código. Si el crecimiento del archivo comienza a afectar la legibilidad o mezcla responsabilidades distintas, deberá dividirse en componentes más pequeños.

* **Criterio de División:** Si un archivo empieza a importar dependencias de distintas capas, acumula múltiples responsabilidades independientes o excede las 300 líneas, debe ser refactorizado y fragmentado bajo los principios de responsabilidad única.

---

## 5. Estándares para Clases

* **Responsabilidad Delimitada:** Una clase debe implementar la lógica inherente a su definición arquitectónica. Las entidades modelan el dominio; los casos de uso coordinan el flujo; los repositorios persisten.
* **Constructores Limpios:** Los constructores (`__init__`) deben dedicarse exclusivamente a inicializar atributos y recibir inyecciones de dependencias. Evita realizar llamadas de red, queries o validaciones pesadas dentro del constructor.
* **Encapsulación (Atributos y Métodos Privados):** Cualquier propiedad o método auxiliar interno de la clase que no forme parte de su interfaz pública debe prefijarse con un guion bajo (`_`) para indicar privacidad y proteger el estado interno.
* **Composición sobre Herencia:** Favorece el uso de composición para dotar de comportamiento a una clase. La herencia queda reservada únicamente para la implementación de contratos abstractos (como las interfaces de repositorio) o modelos base transversales.

---

## 6. Estándares para Métodos y Funciones

* **Nombres Descriptivos:** El nombre de una función debe reflejar exactamente lo que hace sin ambigüedades. Es preferible un nombre largo y descriptivo a uno corto y críptico.
* **Tamaño Reducido:** Las funciones deben ser pequeñas. Se sugiere mantenerlas por debajo de las 30 líneas de código para garantizar su legibilidad y facilitar las pruebas unitarias.
* **Evitar Anidamiento Profundo:** Evita estructuras de control profundamente anidadas (máximo 3 niveles). Utiliza cláusulas de guarda (`guard clauses`) para retornar de forma anticipada y aplanar el flujo lógico.
* **Funciones Auxiliares Privadas:** Si un método realiza múltiples pasos de procesamiento, extrae dichos pasos en métodos privados auxiliares dentro de la misma clase.
* **Sin Efectos Secundarios Ocultos:** Un método no debe modificar parámetros mutables recibidos como argumentos a menos que esa sea la responsabilidad explícita y documentada del método (ej. un mapper de actualización).

---

## 7. Tipado Obligatorio (Type Hints)

* **Tipado Estricto:** Es obligatorio declarar el tipo de datos para todos los parámetros de entrada y los valores de retorno de funciones y métodos públicos en Python.
* **Precisión Financiera:** Queda terminantemente prohibido utilizar el tipo primitivo `float` para montos de dinero, tasas de impuestos o cantidades que admitan decimales. Se debe importar y utilizar exclusivamente el tipo **`Decimal`** para resguardar la precisión aritmética.
* **Identificadores Únicos:** Todos los identificadores (claves primarias y foráneas) deben tiparse y manejarse como objetos **`UUID`** en lugar de strings simples.
* **Opcionales:** Utiliza la sintaxis estándar de Python (`T | None` o `Optional[T]`) para explicitar atributos o retornos que puedan adoptar valores nulos.

---

## 8. Manejo de Excepciones

* **Excepciones Específicas:** Lanza siempre excepciones de dominio específicas y descriptivas. No utilices excepciones genéricas del sistema para errores de lógica de negocio.
* **Evitar `except Exception` Genérico:** No atrapes excepciones genéricas a menos que te encuentres en un middleware de logging global. Atrapar excepciones generales oculta bugs e interrumpe el flujo normal de depuración.
* **Prohibido Silenciar Errores:** Nunca utilices bloques `except` vacíos o con la directiva `pass`. Si se captura un error, debe registrarse en el logger, resolverse explícitamente o volverse a lanzar.
* **Mensajes e Información Útil:** Las excepciones deben llevar un mensaje claro y un diccionario de detalles (`details`) con las variables que provocaron el error para facilitar el diagnóstico.

---

## 9. Reutilización de Código

Antes de escribir una función utilitaria o un componente de acceso a datos, se debe verificar su existencia en el repositorio en el siguiente orden obligatorio:

1. **Revisar `backend/app/common/`:** Contiene respuestas estandarizadas, middlewares y esquemas transversales.
2. **Revisar `backend/app/core/`:** Alberga configuraciones globales, logs y servicios de negocio compartidos.
3. **Revisar `backend/app/database/`:** Contiene el repositorio genérico base y configuraciones de sesiones.
4. **Revisar el módulo Product:** Al ser el módulo de referencia arquitectónica, sus patrones de mapeo y consulta deben servir de plantilla.
5. **Solo tras descartar duplicaciones** se procederá a implementar código nuevo.

---

## 10. Uso de Constantes

* **Evitar Valores Mágicos:** Queda prohibido escribir cadenas de texto o números directamente en el flujo lógico de las funciones (ej. estados permitidos, límites de paginación o campos permitidos).
* **Declaración:** Extrae todos estos valores a constantes semánticas escritas en mayúsculas sostenidas (`UPPER_SNAKE_CASE`) en la cabecera del archivo o en un archivo centralizado de configuración si son transversales.

---

## 11. Validaciones

Las validaciones del sistema deben segregarse de forma estricta según su tipo en la capa correspondiente:

* **Validaciones Sintácticas (Formato y Tipos):** Se ejecutan en la **Capa de Presentación** a través de las validaciones de esquemas Pydantic (DTOs). Comprueban formatos de strings, límites numéricos generales y nulidades antes de entrar a la lógica del negocio.
* **Validaciones de Negocio (Invariantes de Dominio):** Se ejecutan en la **Capa de Dominio** (dentro del método `validate()` de la entidad) y en los casos de uso. Comprueban coherencias operativas (ej. valores financieros no negativos o unicidad lógica).
* **Validaciones de Persistencia (Integridad Relacional):** Se ejecutan en la **Capa de Persistencia** a través de los repositorios y las restricciones físicas de la base de datos (ej. existencia de llaves foráneas y unicidad a nivel de índice SQL).

---

## 12. Logging

* **Logger Centralizado:** Utiliza exclusivamente el logger configurado en `app.core.logger.logger`.
* **Nivel de Log Apropiado:** Usa `debug` para trazas de desarrollo detalladas, `info` para eventos del ciclo de vida normales, `warning` para anomalías controladas y `error` para excepciones no controladas acompañadas de su respectivo traceback.
* **Prohibición de `print()`:** Queda terminantemente prohibido utilizar la función nativa `print()` de Python en código definitivo o en commits del repositorio.
* **Información Sensible:** No registrar contraseñas, tokens, secretos, datos bancarios ni información personal de clientes en los logs.

---

## 13. Comentarios y Documentación

* **Código Autoexplicativo:** Prioriza escribir código limpio donde los nombres de las clases y funciones expresen con claridad su propósito, minimizando la necesidad de comentarios explicativos.
* **Comentar el "Por qué", no el "Cómo":** No escribas comentarios que repitan lo que hace la línea de código siguiente. Escribe comentarios únicamente para justificar decisiones de diseño complejas o excepciones a la norma.
* **Docstrings:** Documenta todas las clases públicas y métodos de las interfaces utilizando el estándar de docstrings de Python para definir parámetros, tipos de datos y excepciones lanzadas.

---

## 14. Código Prohibido (Antipatrones)

La presencia de los siguientes elementos en una propuesta de código provocará el rechazo inmediato de la revisión de cambios:

* **Lógica Duplicada:** Escribir código idéntico o muy similar en lugar de extraerlo a un componente genérico o helper común.
* **Números y Strings Mágicos:** Uso de constantes hardcodeadas en medio de la lógica funcional de las operaciones.
* **Imports Innecesarios o Circulares:** Librerías importadas sin usar en la cabecera del archivo o referencias circulares entre módulos vecinos.
* **Código Muerto:** Funciones declaradas pero nunca llamadas, variables sin lectura o archivos huérfanos.
* **Funciones y Clases Gigantes:** Componentes monolíticos que superen los límites recomendados de líneas y responsabilidades.
* **Comentarios Obsoletos:** Texto descriptivo de versiones previas que ya no coincide con el comportamiento real del código.
* **TODOs Permanentes:** Notas de tareas pendientes introducidas en la base de código definitiva sin planificación ni justificación de Sprint.
* **Dependencias innecesarias:** No incorporar librerías externas cuando la funcionalidad ya pueda resolverse con la biblioteca estándar de Python o componentes existentes del proyecto.

---

## 15. Checklist de Calidad

Cualquier Inteligencia Artificial debe autovalidar el código desarrollado respondiendo sí a los siguientes puntos antes de dar por completado un Sprint o tarea de programación:

* [ ] ¿Todos los parámetros y retornos de métodos públicos cuentan con su respectivo Type Hint de Python?
* [ ] ¿Se utiliza exclusivamente la clase `Decimal` para cualquier cálculo monetario o financiero?
* [ ] ¿Están todos los identificadores únicos tipados como objetos `UUID`?
* [ ] ¿El archivo se encuentra libre de cualquier invocación a la función `print()`?
* [ ] ¿Se extrajeron todos los valores de control a constantes `UPPER_SNAKE_CASE` en la cabecera?
* [ ] ¿Las excepciones lanzadas son de dominio específico y heredan de la jerarquía de excepciones del core?
* [ ] ¿Se revisó la estructura de los módulos compartidos (`common`, `core`, `database`) para evitar duplicar código auxiliar?
* [ ] ¿El código se encuentra libre de bloques `except` genéricos que silencian errores con la directiva `pass`?
* [ ] ¿Todas las funciones y métodos públicos cuentan con docstrings descriptivos?
* [ ] ¿La implementación mantiene el mismo estilo, estructura y patrones utilizados en el resto del proyecto?
