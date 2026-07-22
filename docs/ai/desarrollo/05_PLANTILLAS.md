# 05 - Plantillas Oficiales

## 1. Objetivo

Este documento constituye una biblioteca de referencia rápida que define la estructura jerárquica, ubicación y responsabilidades lógicas de todos los componentes de software requeridos para construir cualquier módulo en **CajaFácil**. Actúa como una guía de consulta inmediata para asegurar que toda creación de componentes se realice respetando los límites de diseño e inyección de dependencias aprobados.

---

## 2. Plantilla de Módulo

Cada módulo del sistema debe replicar con exactitud el siguiente árbol estructural de carpetas y archivos base:

```text
backend/app/modules/[nombre_modulo]/
├── __init__.py
├── application/
│   ├── __init__.py
│   └── use_cases/
│       ├── __init__.py
│       ├── create_[nombre_modulo]_use_case.py
│       ├── update_[nombre_modulo]_use_case.py
│       ├── deactivate_[nombre_modulo]_use_case.py
│       ├── get_[nombre_modulo]_use_case.py
│       └── list_[nombre_modulo]s_use_case.py
├── data/
│   ├── __init__.py
│   ├── mappers/
│   │   ├── __init__.py
│   │   └── [nombre_modulo]_mapper.py
│   ├── models.py
│   └── repositories/
│       ├── __init__.py
│       └── [nombre_modulo]_repository_impl.py
├── domain/
│   ├── __init__.py
│   ├── entities/
│   │   ├── __init__.py
│   │   └── [nombre_modulo].py
│   ├── exceptions/
│   │   ├── __init__.py
│   │   ├── [nombre_modulo]_not_found_exception.py
│   │   ├── [nombre_modulo]_already_exists_exception.py
│   │   └── invalid_[nombre_modulo]_exception.py
│   └── repositories/
│       ├── __init__.py
│       └── [nombre_modulo]_repository.py
└── presentation/
    ├── __init__.py
    ├── dependencies/
    │   ├── __init__.py
    │   └── [nombre_modulo]_dependencies.py
    ├── dto/
    │   ├── __init__.py
    │   ├── create_[nombre_modulo]_request.py
    │   ├── update_[nombre_modulo]_request.py
    │   └── [nombre_modulo]_response.py
    └── routers/
        ├── __init__.py
        └── [nombre_modulo]_router.py
```
La estructura presentada es la plantilla de referencia para un módulo maestro.

Dependiendo de las necesidades del negocio, algunos componentes podrán omitirse (por ejemplo, un módulo que no requiera operaciones de actualización o desactivación), siempre que la decisión esté justificada y no rompa la arquitectura definida para el proyecto.
---

## 3. Plantilla de Entity

* **Responsabilidad:** Representar el modelo de negocio puro (invariantes de datos) a nivel lógico en memoria. Implementa la auto-validación de constraints lógicas (como no-negatividad de importes) en su inicialización post-constructor, garantizando que el objeto nunca entre en un estado inconsistente.
* **Ubicación:** `domain/entities/[nombre_modulo].py`
* **Archivos Relacionados:** `domain/exceptions/invalid_[nombre_modulo]_exception.py` (lanzada por sus validaciones internas).

---

## 4. Plantilla de Repository Interface

* **Responsabilidad:** Definir el contrato abstracto de persistencia del módulo que la aplicación consumirá de forma desacoplada. Obliga a que todas las operaciones y búsquedas de colecciones reciban y retornen únicamente tipos de dominio nativos o primitivos.
* **Ubicación:** `domain/repositories/[nombre_modulo]_repository.py`
* **Dependencias Permitidas:** Únicamente imports de tipado de la entidad del dominio y librerías estándar. Prohibido importar ORMs o drivers de base de datos.

---

## 5. Plantilla de Repository Implementation

* **Responsabilidad:** Implementar el acceso físico a base de datos traduciendo operaciones relacionales. Hereda del repositorio base genérico y de la interfaz de dominio. Gestiona consultas filtradas estrictamente por `company_id` (aislamiento multi-tenant) y Gestiona el acceso a la persistencia aplicando las reglas técnicas necesarias, como el aislamiento multiempresa y la conversión entre dominio y persistencia.
* **Ubicación:** `data/repositories/[nombre_modulo]_repository_impl.py`
* **Relación con ORM:** Interactúa directamente con SQLAlchemy Core/ORM (`Session`, `select`, etc.) mapeando los resultados desde y hacia objetos de dominio nativos de forma inmediata.
* **Uso de Mapper:** Invoca funciones del Mapper para transformar modelos de persistencia a entidades lógicas antes de retornarlos.

---

## 6. Plantilla de Mapper

* **Responsabilidad:** Servir de adaptador bidireccional y barrera de traducción entre la base de datos (persistencia física) y el dominio (entidades lógicas).
* **Ubicación:** `data/mappers/[nombre_modulo]_mapper.py`
* **Conversiones:**
  * Traducción de Entidad a Modelo ORM.
  * Traducción de Modelo ORM a Entidad.
  * Mapeo de campos editables para actualizaciones in-place.
* **Reglas:** Centraliza las conversiones necesarias entre el dominio y la persistencia.

---

## 7. Plantilla de Use Case

* **Responsabilidad:** Implementar y orquestar una única acción o flujo del negocio de forma aislada. Valida condiciones complejas mediante llamadas a la interfaz de repositorio abstracta, coordina la mutación del estado e invoca la persistencia.
* **Ubicación:** `application/use_cases/[operacion]_[nombre_modulo]_use_case.py`
* **Dependencias:** Consume únicamente entidades del dominio, excepciones y la interfaz abstracta del repositorio. Desconoce por completo a los DTOs, frameworks web y bases de datos físicas.

---

## 8. Plantilla de Command

* **Responsabilidad:** Estructurar y portar los parámetros requeridos para iniciar una operación compleja de escritura (Use Case). Actúa como un contenedor de datos simple (`dataclass`) para evitar que la capa de aplicación reciba objetos Request DTO del framework web de forma directa.
* **Ubicación:** Declarado en la cabecera de su respectivo archivo de caso de uso de escritura (ej. `Create[NombreModulo]Command` dentro de `create_[nombre_modulo]_use_case.py`).
* **Relación con Use Case:** El método `execute()` del caso de uso de escritura correspondiente recibe este comando como su único parámetro de entrada.

---

## 9. Plantilla de DTO Request

* **Responsabilidad:** Actuar como el contrato HTTP de entrada. Define y valida sintácticamente el payload JSON recibido en las peticiones REST.
* **Ubicación:** `presentation/dto/create_[nombre_modulo]_request.py` y `update_[nombre_modulo]_request.py`.
* **Validaciones:** Comprueba formatos de cadenas de texto, rangos numéricos generales y nulidades usando tipado fuerte de Pydantic antes de delegar la información.

---

## 10. Plantilla de DTO Response

* **Responsabilidad:** Actuar como el contrato HTTP de salida. Filtra y define los campos de datos JSON retornados al cliente en las respuestas exitosas de las APIs REST.
* **Ubicación:** `presentation/dto/[nombre_modulo]_response.py`
* **No Exponer Entidades:** Evita retornar entidades de dominio de forma directa al cliente web. Esto aísla los cambios estructurales internos del negocio y previene fugas accidentales de datos de auditoría o configuraciones internas.

---

## 11. Plantilla de Router

* **Responsabilidad:** Adaptar la entrada de red (HTTP) hacia los casos de uso lógicos del sistema. Intercepta peticiones REST, valida payloads con DTO Requests, mapea entradas a comandos, resuelve inyecciones de dependencias lógicas y devuelve DTO Responses envueltos en la respuesta genérica del sistema.
* **Ubicación:** `presentation/routers/[nombre_modulo]_router.py`
* **Límites:** El router tiene estrictamente prohibido instanciar entidades de dominio, conectarse a repositorios directos o ejecutar reglas de negocio lógicas.

---

## 12. Plantilla de Migración

* **Responsabilidad:** Evolucionar de manera lineal y segura el esquema físico de la base de datos relacional.
* **Ubicación:** `backend/app/database/migrations/versions/[id_migracion]_[nombre].py`
* **Creación:** Autogenerada mediante comandos de CLI de Alembic, importando los metadatos consolidados desde `backend/app/database/base.py`.
* **Buenas Prácticas:**
  * Toda alteración de tablas (`alter_table`) debe configurarse bajo la directiva de lotes (`render_as_batch=True`) para sortear las limitantes de SQLite local.
  * Definir siempre restricciones de Foreign Keys con cascadas seguras Las políticas de eliminación y actualización deberán definirse de acuerdo con las reglas del negocio y las convenciones del proyecto..
  * Incluir siempre funciones de reversión (`downgrade()`) simétricas.

---

## 13. Checklist de Módulo Completo

Antes de declarar un módulo maestro como finalizado e integrado, se debe validar que contenga de forma obligatoria los siguientes componentes mínimos en el backend:

* [ ] **Modelo ORM de Persistencia:** Tabla registrada en `data/models.py` e importada en `app/database/base.py`.
* [ ] **Migración de Alembic:** Archivo de migración autogenerado, revisado y aplicado con éxito en la base de datos de desarrollo.
* [ ] **Entidad de Dominio:** Dataclass pura con método de autovalidación de invariantes estructurado.
* [ ] **Interfaz del Repositorio:** Clase abstracta de dominio que especifica los contratos de persistencia.
* [ ] **Excepciones de Dominio:** Definición de excepciones de no encontrado, duplicación y validación.
* [ ] **Implementación de Persistencia:** Repositorio que hereda de `BaseRepository` y aplica filtros multi-tenant.
* [ ] **Mapper del Módulo:** Centralizador de conversiones y traducciones de estados del negocio.
* [ ] **Casos de Uso Completos:** Lógica de negocio encapsulada por separado para crear, actualizar, inactivar, obtener y listar.
* [ ] **Esquemas DTO Pydantic:** Estructuras de Request y Response que aíslan los datos de intercambio REST.
* [ ] **Inyector de Dependencias:** Archivo de inyecciones FastAPI para suministrar los repositorios y casos de uso.
* [ ] **Router Registrado:** Controlador REST configurado e importado/registrado formalmente en `app/main.py`.
* [ ] ¿Toda la documentación del módulo fue actualizada cuando fue necesario?