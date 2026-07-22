# 01 - Patrón Oficial de Módulo Maestro
Versión: 1.0
Estado: Aprobado
Última actualización: 2026-07-21
Tipo: Patrón Arquitectónico Oficial

## 1. Objetivo

Este documento establece el estándar arquitectónico oficial de CajaFácil para el diseño, desarrollo e integración de cualquier módulo maestro o catálogo en el backend. Define de forma taxativa la segregación de responsabilidades, el flujo de datos y las restricciones de acoplamiento que deben cumplir los desarrolladores y las Inteligencias Artificiales colaboradoras, garantizando la uniformidad y mantenibilidad del sistema a largo plazo.

---

## 2. Alcance

El patrón detallado en esta norma técnica debe ser aplicado obligatoriamente a todos los módulos maestros actuales y futuros del sistema. Estos módulos incluyen, de forma enunciativa pero no limitativa:

* **Product** (Módulo patrón actual)
* **Category** (Categorías de productos)
* **Brand** (Marcas)
* **Unit** (Unidades de medida)
* **Customer** (Clientes)
* **Supplier** (Proveedores)

Cualquier catálogo secundario o entidad maestra que actúe como registro base del sistema deberá estructurarse siguiendo este patrón sin excepciones.

---
## 3. Ciclo oficial de construcción de un módulo

Todo módulo maestro de CajaFácil debe desarrollarse siguiendo el siguiente orden de implementación:

```text
Análisis del negocio
        ↓
Modelado del Dominio
        ↓
Persistencia
        ↓
Aplicación
        ↓
Presentación
        ↓
Pruebas
        ↓
Revisión Arquitectónica
```
No se debe alterar este orden salvo aprobación explícita del arquitecto del proyecto.

Este flujo garantiza que las decisiones técnicas siempre se construyan sobre un modelo de negocio previamente validado y no al contrario.

## 4. Arquitectura General

El sistema backend se rige por los principios de **Clean Architecture** combinados con **Domain-Driven Design (DDD)**. Las capas de comunicación se aíslan físicamente para proteger el núcleo del negocio de cambios en la tecnología de infraestructura (frameworks, ORM o bases de datos).

El flujo lógico del control arquitectónico y la estructura de capas operan en la siguiente jerarquía unidireccional:

```text
  [ Capa externa ]          Presentation  (FastAPI / Routers / DTOs)
                                 │
                                 ▼
                            Application   (Use Cases / Commands)
                                 │
                                 ▼
                               Domain     (Entities / Repository Interfaces)
                                 ▲
                                 │
  [ Capa externa ]          Persistence   (SQLAlchemy / Repository Impl / Mappers)
                                 │
                                 ▼
                              Database    (SQLite / PostgreSQL)
```

---

## 5. Estructura Oficial de Carpetas

Todo módulo maestro debe presentar exactamente la siguiente distribución de archivos y directorios:

```text
backend/app/modules/[module_name]/
├── __init__.py
├── application/
│   ├── __init__.py
│   └── use_cases/
│       ├── __init__.py
│       ├── create_[module_name]_use_case.py
│       ├── update_[module_name]_use_case.py
│       ├── deactivate_[module_name]_use_case.py
│       ├── get_[module_name]_use_case.py
│       └── list_[module_name]s_use_case.py
├── data/
│   ├── __init__.py
│   ├── mappers/
│   │   ├── __init__.py
│   │   └── [module_name]_mapper.py
│   ├── models.py
│   └── repositories/
│       ├── __init__.py
│       └── [module_name]_repository_impl.py
├── domain/
│   ├── __init__.py
│   ├── entities/
│   │   ├── __init__.py
│   │   └── [module_name].py
│   ├── exceptions/
│   │   ├── __init__.py
│   │   ├── [module_name]_not_found_exception.py
│   │   ├── [module_name]_already_exists_exception.py
│   │   └── invalid_[module_name]_exception.py
│   └── repositories/
│       ├── __init__.py
│       └── [module_name]_repository.py
└── presentation/
    ├── __init__.py
    ├── dependencies/
    │   ├── __init__.py
    │   └── [module_name]_dependencies.py
    ├── dto/
    │   ├── __init__.py
    │   ├── create_[module_name]_request.py
    │   ├── update_[module_name]_request.py
    │   └── [module_name]_response.py
    └── routers/
        ├── __init__.py
        └── [module_name]_router.py
```

---

## 6. Responsabilidad de cada Capa

### Capa de Presentación (`presentation/`)
* **Qué hace:** Actúa como adaptador HTTP. Recibe peticiones externas, valida la forma y tipo de los payloads entrantes mediante esquemas Pydantic (DTOs), resuelve dependencias de servicios por inyección y delega el flujo al caso de uso correspondiente para devolver la respuesta serializada.
* **Qué NO debe hacer:** Nunca debe validar reglas de negocio o realizar cálculos financieros. Tampoco debe instanciar entidades de dominio ni conectarse de forma directa a repositorios concretos o a la base de datos.

### Capa de Aplicación (`application/`)
* **Qué hace:** Orquesta el flujo de trabajo del negocio. Implementa los casos de uso individuales, valida condiciones compuestas de negocio (como exclusividad de códigos mediante consultas previas), instancia las entidades de dominio y coordina su persistencia a través de la interfaz abstracta del repositorio.
* **Qué NO debe hacer:** No debe importar FastAPI, dependencias HTTP, esquemas DTO o SQLAlchemy. Debe desconocer qué motor de base de datos o qué framework web está activo.

### Capa de Dominio (`domain/`)
* **Qué hace:** Constituye el núcleo inmutable del módulo. Define las entidades de negocio puras (invariantes de datos), valida campos numéricos no negativos y estados válidos, declara las excepciones lógicas y expone la interfaz de repositorio abstracta que define las operaciones de acceso a datos.
* **Qué NO debe hacer:** No debe contener dependencias de red, frameworks ni ORMs. No realiza llamadas directas a base de datos.

### Capa de Persistencia/Datos (`data/`)
* **Qué hace:** Implementa el almacenamiento físico y la traducción de modelos. Alberga el modelo de persistencia ORM de SQLAlchemy, implementa los repositorios concretos (heredando del repositorio genérico del core y del contrato de dominio) y ejecuta la conversión de datos mediante el Mapper.
* **Qué NO debe hacer:** No debe interactuar con lógica web (FastAPI, enrutadores) ni tomar decisiones lógicas autónomas sobre el comportamiento de negocio.

---

## 7. Flujo Oficial de Datos (End-to-End)

El ciclo de vida de una petición de escritura (ej. creación de registro) sigue de forma obligatoria el siguiente flujo secuencial:

1. **HTTP Request:** El cliente envía una petición HTTP con un payload JSON al servidor.
2. **Router:** El enrutador intercepta la petición en FastAPI.
3. **DTO (Validation):** El payload JSON se parsea y valida sintácticamente usando el esquema Pydantic Request DTO.
4. **Command:** El Router extrae la información del Request DTO y construye un objeto Command simple (inyección de parámetros desacoplada).
5. **UseCase:** El Router invoca al caso de uso de aplicación correspondiente pasándole el objeto Command.
6. **Entidad de Dominio:** El caso de uso inicializa la Entidad de Dominio, lo cual ejecuta automáticamente las validaciones lógicas del negocio.
7. **Reglas de Negocio:** El caso de uso realiza comprobaciones relacionales y lógicas utilizando las llamadas al Repositorio.
8. **Repository Interface:** El caso de uso envía la Entidad de Dominio a la interfaz abstracta del Repositorio.
9. **Repository Implementation:** La persistencia intercepta la llamada en la clase concreta de acceso a datos.
10. **Mapper (to_db):** El repositorio utiliza el Mapper del módulo para traducir la entidad pura de Dominio en un modelo SQLAlchemy, aplicando cualquier traducción de estados técnica.
11. **SQLAlchemy ORM:** El repositorio inserta el modelo ORM en la sesión y confirma la transacción.
12. **Mapper (to_domain):** El modelo persistido se vuelve a mapear a Entidad de Dominio pura para devolverlo a la aplicación.
13. **Response DTO:** El Router toma la entidad retornada por el caso de uso, la transforma en el Response DTO y la devuelve serializada como JSON HTTP.

---

## 8. Dependencias Permitidas

La siguiente matriz especifica qué librerías y componentes del proyecto tiene permitido importar cada una de las capas del módulo:

| Capa | Importaciones Permitidas |
| :--- | :--- |
| **Domain** | Librería estándar de Python (`typing`, `uuid`, `datetime`, `decimal`, `dataclasses`). Excepciones del mismo módulo. |
| **Application** | Capa de Dominio del módulo (Entidades, Repositorios abstractos, Excepciones). Excepciones genéricas del core (`app.common.exceptions`). |
| **Persistence (Data)** | Capa de Dominio del módulo. Modelos ORM locales (`data/models.py`). Repositorio base (`app.database.repositories.base.BaseRepository`). SQLAlchemy Core y ORM. |
| **Presentation** | Capa de Aplicación del módulo (Use Cases y Commands). Capa de Dominio del módulo (únicamente Entidades para propósitos de tipado). FastAPI, Pydantic, esquemas DTO locales, utilidades de respuestas genéricas (`app.common.presentation.responses`). |

---

## 9. Dependencias Prohibidas

La siguiente matriz detalla qué importaciones están estrictamente prohibidas y constituyen una violación inmediata de la arquitectura:

| Capa | Importaciones Prohibidas (No utilizar) |
| :--- | :--- |
| **Domain** | **Prohibido:** SQLAlchemy, Pydantic, FastAPI, Enrutadores, cualquier archivo de la capa `data/` o `presentation/`, sesiones de base de datos. |
| **Application** | **Prohibido:** FastAPI, dependencias web, esquemas DTO, modelos SQLAlchemy, sesiones directas de base de datos, clases concretas de persistencia (`*_repository_impl.py`). |
| **Persistence (Data)** | **Prohibido:** FastAPI, esquemas DTO, enrutadores, lógica web de presentación. |
| **Presentation** | **Prohibido:** SQLAlchemy, clases de persistencia concreta, modelos de base de datos, llamadas de base de datos sin pasar por Casos de Uso. |

---

## 10. Patrón Repository

* **Propósito:** Desacoplar por completo la infraestructura de almacenamiento de la lógica del negocio.
* **Estructura:**
  * La **Interfaz de Repositorio** (en `domain/repositories/`) es una clase abstracta pura (`ABC`) que establece el contrato. Todas las firmas de métodos deben aceptar y retornar únicamente objetos de dominio nativos o primitivos.
  * La **Implementación de Repositorio** (en `data/repositories/`) hereda de `BaseRepository` y de la interfaz abstracta. Realiza las consultas físicas a base de datos y mapea de forma inmediata los resultados utilizando el Mapper del módulo antes de retornarlos.
* **Seguridad Multi-Tenant:** Todas las consultas del repositorio que involucren lecturas de colecciones o búsquedas lógicas deben exigir e indexar obligatoriamente la variable de tenant `company_id`.

---

## 11. Patrón Mapper

* **Propósito:** Actuar como traductor bidireccional y barrera de desacoplamiento entre el Dominio y la Persistencia.
* **Responsabilidades:**
  * Convertir entidades puras de dominio a instancias de modelos SQLAlchemy.
  * Convertir modelos de persistencia SQLAlchemy a entidades puras de dominio.
  * Realizar la correspondencia (mapping) de actualización de campos editables.
  * **Traducción de Estados:** Es el único componente del sistema autorizado para convertir estados de lenguaje de negocio en español (ej. `"ACTIVO"`, `"INACTIVO"`) a valores técnicos de persistencia de base de datos en inglés (ej. `"ACTIVE"`, `"INACTIVE"`). El repositorio solo invoca funciones del Mapper y desconoce estos valores físicos.
  * **Errores:** Las conversiones deben ser estrictas y basarse en constantes asociativas claras. Si llega un estado inválido, el Mapper debe lanzar inmediatamente una excepción (`KeyError` o similar) y nunca resolver el error con un valor predeterminado silencioso.

---

## 12. Patrón Use Case

* **Propósito:** Encapsular una única acción de negocio del sistema, actuando como el orquestador del flujo.
* **Lineamientos:**
  * **Responsabilidad Única:** Un caso de uso equivale a un archivo y a un único comportamiento operativo (ej. `Create<Module>UseCase` solo crea, `List<Module>UseCase` solo lista).
  * **Independencia Tecnológica:** Su lógica opera únicamente con entidades de dominio, interfaces abstractas e inyectores genéricos. No conoce tecnologías de base de datos.
  * **Gestión de Excepciones:** Debe atrapar errores lógicos de persistencia y lanzar excepciones semánticas declaradas en el dominio, asegurando que las anomalías se reporten de forma inteligible para el usuario.

---

## 13. Patrón Router

* **Propósito:** Actuar como la interfaz HTTP del sistema.
* **Lineamientos:**
  * Su única tarea es procesar la petición HTTP, verificar la validez del Request DTO, mapear la entrada hacia un objeto Command (si se requiere desacoplar la creación) o pasar los IDs de ruta directamente, invocar al Caso de Uso y retornar la estructura Response DTO.
  * El enrutador no debe contener lógica de validación de reglas de negocio, ni comparaciones numéricas de datos, ni inicializar propiedades internas del dominio.

---

## 14. Data Transfer Objects (DTO)

* **Propósito:** Definir de manera formal el contrato de intercambio de datos a través de la API pública.
* **Seguridad e Integridad:**
  * **Request DTO:** Valida la estructura y tipo del JSON de entrada antes de tocar las capas lógicas internas.
  * **Response DTO:** Limita qué campos se devuelven al exterior.
  * **Aislamiento del Dominio:** **Las entidades de dominio nunca deben ser expuestas directamente por los routers en las respuestas HTTP.** Exponer las entidades de dominio acopla la API a la estructura interna del negocio, impidiendo realizar refactorizaciones internas sin romper los clientes externos y provocando riesgos de seguridad de exposición de información confidencial.

---
## 15. Convenciones de nombres

Todos los módulos maestros deberán seguir una nomenclatura uniforme.

Ejemplos:

- `<Module>Repository`
- `<Module>RepositoryImpl`
- `<Module>Mapper`
- `Create<Module>UseCase`
- `Update<Module>UseCase`
- `Deactivate<Module>UseCase`
- `<Module>Router`
- `Create<Module>Request`
- `Update<Module>Request`
- `<Module>Response`

No deben utilizarse nombres arbitrarios, abreviaturas o convenciones diferentes entre módulos.

## 16. Checklist Arquitectónico

Antes de completar la tarea de programación o declarar un Sprint como terminado, la IA colaboradora debe autovalidar el código respondiendo a la siguiente lista de verificación:

* [ ] ¿Las entidades de dominio se encuentran libres de decoradores u objetos provenientes de SQLAlchemy o Pydantic?
* [ ] ¿El caso de uso (`UseCase`) consume únicamente la interfaz abstracta del repositorio (`<Module>Repository` / `CategoryRepository`, etc.) en lugar de la clase concreta `*RepositoryImpl`?
* [ ] ¿Se eliminó cualquier uso de `setattr()` libre para actualizaciones, reemplazándolo por asignaciones explícitas basadas en una lista blanca de campos modificables en el caso de uso?
* [ ] ¿Toda traducción de estados de negocio a base de datos (como `"ACTIVO"` a `"ACTIVE"`) está centralizada de forma exclusiva en el archivo de Mapper correspondiente?
* [ ] ¿El enrutador (`Router`) delega la construcción física de las entidades de dominio a los casos de uso a través del paso de objetos `Command` sencillos?
* [ ] ¿Las firmas de los controladores de API devuelven esquemas `Response DTO` en lugar de las entidades directas del dominio?
* [ ] ¿Las consultas de repositorio y listados aplican de manera obligatoria el filtro por `company_id` para garantizar el aislamiento multi-tenant?
* [ ] ¿Todos los importes son válidos y la ejecución de `pytest` o `flutter test` compila de forma limpia en la consola?

---

## 17. Errores Comunes a Evitar

* **Importación de SQLAlchemy en el Dominio:** Error crítico de Clean Architecture. La base de datos es un detalle tecnológico externo.
* **Mutaciones sin Validar (`setattr` indiscriminado):** Modificar campos en la base de datos sin ejecutar posteriormente la validación de la entidad (`<module>.validate()`) puede resultar en datos inválidos o corruptos en base de datos.
* **Fallas de Tenant (Lecturas Cruzadas):** Omitir el filtro `company_id` en las consultas del repositorio localizadoras de duplicados o de listados generales.
* **Lógica Financiera con Floats:** Usar el tipo de dato primitivo `float` en Pydantic o la entidad de dominio. Se debe usar obligatoriamente `Decimal` para evitar imprecisiones de coma flotante binaria.
* **Traducciones en cascada:** Escribir condicionales de traducción de estados en los archivos de router o repositorio concreto. Toda la traducción técnica pertenece al Mapper.

---

## 18. Módulo de Referencia

El módulo **Product** ([`backend/app/modules/product`](../../backend/app/modules/product)) es la implementación oficial y aprobada de este patrón de arquitectura. 

Cualquier nuevo desarrollo de catálogo maestro o API de mantenimiento básico (tales como **Category**, **Brand** o **Unit**) deberá guiarse por la distribución del módulo `product` como su plantilla estructural idéntica, adaptando únicamente las reglas específicas declaradas en su respectivo dominio.
