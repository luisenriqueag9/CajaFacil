# 04 - Convenciones del Proyecto

## 1. Objetivo

Este documento establece las convenciones de desarrollo globales y permanentes que rigen el ciclo de vida del software en **CajaFácil**. Define las decisiones de ingeniería inmutables en cuanto a idioma, tipos de datos, tratamiento del dinero, control de versiones e interfaces de red, con el fin de unificar el criterio técnico y eliminar discusiones redundantes en el equipo.

---

## 2. Principios Generales

Las convenciones y normas descritas en esta directiva técnica existen para cumplir con cuatro metas operativas:

* **Mantener consistencia:** Asegurar que cualquier desarrollador o Inteligencia Artificial externa pueda leer y comprender cualquier archivo de la base de código bajo las mismas reglas cognitivas.
* **Facilitar mantenimiento:** Disminuir la fricción al depurar, optimizar o refactorizar código gracias a una distribución e instrumentación homogénea.
* **Reducir discusiones técnicas:** Resolver por definición previa cualquier debate estilístico o de formato, permitiendo al equipo enfocarse en resolver problemas lógicos y de negocio.
* **Permitir evolución del sistema:** Diseñar una base estable que admita el escalamiento horizontal del código, la agregación de nuevos microservicios y la transición a arquitecturas complejas sin alterar los cimientos.

---

## 3. Idioma Oficial

El proyecto adopta un enfoque bilingüe estrictamente segregado por áreas de responsabilidad:

* **Código (Variables, Clases, Funciones, Módulos):** Escrito exclusivamente en **inglés**.
* **Base de Datos (Tablas, Columnas, Índices, Constraints):** Definido exclusivamente en **inglés**.
* **API (Rutas, Parámetros, JSON Keys, payloads):** Expuesto exclusivamente en **inglés**.
* **Documentación (Guías, Walkthroughs, Especificaciones):** Redactado exclusivamente en **español**.
* **Comentarios del Código:** Escritos en **español** solo cuando sea necesario detallar excepciones lógicas o justificar decisiones complejas del negocio.
* **Capa de Negocio Lógica (Variables conceptuales explícitas):** Permite el uso de términos del negocio en español cuando se definen estados operativos del negocio en el Dominio (ej. `"ACTIVO"`, `"INACTIVO"`).

---

## 4. Convenciones de Nombres

### Carpetas y Paquetes
Escritas en minúsculas sostenidas, en singular y utilizando `snake_case` (ej. `category`, `product_category`).

### Archivos
Nombres en minúsculas, utilizando `snake_case` y con sufijos correspondientes al patrón del componente (ej. `[name]_use_case.py`, `[name]_mapper.py`, `[name]_router.py`).

### Clases
Nombres en singular, escritos en `PascalCase` (UpperCamelCase), iniciando con mayúscula (ej. `CreateCompanyCommand`, `ProductResponse`).

### Funciones y Métodos
Nombres en `snake_case` que utilicen un verbo de acción infinitivo o indicativo (ej. `to_db`, `get_by_id`, `validate_uniqueness`).

### Variables
Nombres descriptivos en `snake_case` que reflejen su contenido (ej. `created_product`, `validation_errors`). Evitar abreviaciones sin sentido o letras solas.

### Constantes
Mayúsculas sostenidas en `UPPER_SNAKE_CASE` (ej. `DOMAIN_TO_DB_STATUS`, `ALLOWED_UPDATE_FIELDS`).

### Tablas de Base de Datos
Escritas en minúsculas, singular y utilizando `snake_case` (ej. `company`, `product`, `brand`).

### Columnas de Base de Datos
Escritas en minúsculas, singular y utilizando `snake_case` (ej. `business_name`, `internal_code`, `created_at`).

---

## 5. Identificadores

* **Uso Obligatorio de UUID:** Todos los registros e identificadores del sistema (claves primarias y foráneas) deben generarse y almacenarse como objetos del tipo **`UUID`** (versión 4).
* **Prohibición de Autoincrementales:** Queda estrictamente prohibido exponer números enteros autoincrementales (`INTEGER AUTOINCREMENT` / `SERIAL`) como identificadores públicos ante las APIs o clientes del sistema. 
* **Relaciones Físicas y Lógicas:** Los enlaces relacionales entre tablas y agregados en base de datos se configuran de forma obligatoria a través de columnas de tipo UUID.

---

## 6. Tipos de Datos

* **Monetarios y Decimales:** Toda propiedad o variable que exprese dinero, precios, costos, tasas de impuestos o cantidades que admitan fracciones debe tiparse estrictamente utilizando la clase **`Decimal`**. Queda prohibido usar float.
* **Estados y Banderas:** Los estados lógicos de activación de funcionalidades o configuraciones binarias deben almacenarse utilizando el tipo **`Boolean`**.
* **Identificadores Lógicos:** Utilizar de manera obligatoria la clase de abstracción **`UUID`** del sistema.
* **Marcas Temporales:** Registrar fechas y horas bajo el tipo **`DateTime`** forzando la inclusión de información de zona horaria (`timezone=True`).

---

## 7. Fechas y Horas

* **UTC como Estándar Interno:** Toda fecha y hora procesada en el backend o guardada en la base de datos PostgreSQL/SQLite debe calcularse, guardarse y compararse en el estándar **UTC (Coordinated Universal Time)**.
* **Conversión en Capa Externa:** La conversión de marcas temporales a la zona horaria local de la empresa/usuario se realiza exclusivamente en la capa de presentación del cliente (Frontend) o mediante formato DTO si el API lo requiere de forma explícita.
* **Formato de Intercambio:** La serialización de fechas para transferencias en las APIs REST debe seguir de forma estricta el estándar **ISO-8601** (`YYYY-MM-DDTHH:MM:SSZ`).

---

## 8. Dinero y Cálculos Financieros

* **Uso de Decimal:** El cálculo financiero (costos, precios, impuestos, subtotales, totales) exige el tipo **`Decimal`** para evitar los errores acumulativos inherentes al redondeo binario de coma flotante.
* **Reglas de Redondeo Centralizadas:** Los cálculos intermedios de tasas deben realizarse con precisión extendida (mínimo 4 decimales) y redondearse al final a la precisión monetaria local establecida por la moneda de la empresa (ej. 2 decimales para USD o HNL) utilizando la estrategia de redondeo especificada por el negocio (`ROUND_HALF_UP`).

---

## 9. Desactivación Lógica (Soft Delete)

* **Preferencia por Desactivación Lógica:** CajaFácil adopta como estrategia predeterminada la desactivación lógica (Soft Delete) para preservar la integridad referencial, el historial operativo y la capacidad de auditoría.

La eliminación física solo se permitirá cuando la naturaleza del dato lo justifique y exista una aprobación arquitectónica explícita.
* **Mecanismo:** La remoción se traduce operativamente a una inactivación lógica, modificando la columna de control `status` al valor correspondiente de inactivación (`"INACTIVO"` en dominio, `"INACTIVE"` en persistencia) y forzando la actualización de la columna de auditoría `updated_at`.
* **Excepciones:** El borrado físico solo se autoriza en tablas de caché temporal o registros que no contengan dependencias y cuya eliminación sea aprobada por arquitectura.

---

## 10. Multiempresa (Multi-tenancy)

* **Pertenencia Obligatoria:** Todo registro operativo, catálogo o transacción pertenece obligatoriamente a una única empresa (tenant).
* **Filtro company_id:** Toda consulta deberá filtrar explícitamente por el identificador de la empresa (`company_id`) correspondiente al contexto autenticado.
* **Aislamiento Total:** Está estrictamente prohibido ejecutar consultas que puedan cruzar o exponer información de una empresa ante otra. El backend actúa como la barrera de seguridad de datos SaaS.

---

## 11. Base de Datos

* **PostgreSQL (Nube/Sincronización):** Motor principal de producción que actúa como almacén centralizado.
* **SQLite (Local/Offline):** Motor ligero utilizado en los clientes de escritorio locales para el procesamiento transaccional offline.
* **Migraciones con Alembic:** Las modificaciones en el esquema relacional de la base de datos se orquestan linealmente usando Alembic.
* **Batch Migrations:** Toda migración de alteración de tablas debe configurarse con soporte de lotes (`render_as_batch=True`) para garantizar la compatibilidad con las limitantes de alteración de esquemas de SQLite.
* **Convenciones de Nombres en BD:**
  * Llave primaria: `id`
  * Llaves foráneas: `[referenced_table]_id`
  * Constraints de unicidad: `uq_[table_name]_[columns]`
  * Constraints de clave foránea: `fk_[table_name]_[referenced_table]`

---

## 12. API (Interfaces de Red)

* **RESTful y JSON:** Las comunicaciones de red exponen interfaces REST utilizando payloads estructurados exclusivamente en formato JSON.
* **Versionado de Rutas:** El API debe incluir versionado explícito en la ruta raíz de los endpoints utilizando el prefijo `/api/v1` (ej. `/api/v1/products`).
* **Uso de DTOs:** Prohibido retornar entidades de dominio o modelos ORM directos. Las entradas y salidas de las rutas deben estar encapsuladas en esquemas Request y Response DTOs de Pydantic.
* **Códigos de Estado HTTP Adecuados:**
  * `200 OK` (Operación exitosa con retorno de datos)
  * `201 Created` (Creación de recurso exitosa)
  * `400 Bad Request` (Errores de validación sintáctica)
  * `401 Unauthorized` (Credenciales inválidas o inexistentes)
  * `403 Forbidden` (Acceso denegado por falta de permisos)
  * `404 Not Found` (Recurso no encontrado en el sistema)
  * `409 Conflict` (Violación de unicidad o colisión de datos)
  * `500 Internal Server Error` (Fallo interno no controlado del backend)
* **Compatibilidad:** Siempre que sea posible, las nuevas versiones de la API deberán mantener compatibilidad hacia atrás para evitar romper integraciones existentes.

---

## 13. Versionado

* **Versionado Semántico (SemVer):** El sistema utiliza la regla de versionado `MAJOR.MINOR.PATCH` para sus componentes de software.
  * **MAJOR:** Cambios de arquitectura o API que rompen la compatibilidad hacia atrás.
  * **MINOR:** Incorporación de nuevas funcionalidades que mantienen la compatibilidad.
  * **PATCH:** Corrección de fallos y bugs menores compatibles.

---

## 14. Gestión de Dependencias

* **Prioridad a la Biblioteca Estándar:** Favorece el uso de las librerías nativas de Python ante la instalación de paquetes de terceros.
* **Evaluación de Paquetes Externos:** La introducción de una nueva dependencia externa requiere la justificación de un beneficio claro ante el Arquitecto Principal (ej. optimización crítica de rendimiento o integración de drivers obligatorios).
* **Seguridad y Ligereza:** Mantén el ecosistema de dependencias libre de paquetes redundantes para evitar vulnerabilidades de cadena de suministro y ralentizaciones de arranque.

---

## 15. Organización del Proyecto

La jerarquía física de carpetas y el acoplamiento modular establecido en la base de código constituyen la estructura oficial del sistema. no deberá modificarse sin aprobación arquitectónica la modificación, eliminación o reubicación de carpetas centrales del core sin la previa autorización firmada por el arquitecto del proyecto.

---

## 16. Cambios a las Convenciones

* **Estándar Inmutable en Desarrollo:** Este documento es normativo y vinculante para todo el equipo de desarrollo.
* **Proceso de Modificación:** Si surge una necesidad tecnológica justificada para alterar alguna convención (como un nuevo tipo de identificador o cambios en el versionado), se deberá presentar una solicitud formal al Arquitecto Principal del proyecto para su evaluación técnica. Ninguna modificación será válida en el repositorio sin la firma y aprobación explícita de la arquitectura.
Toda modificación aprobada deberá registrarse en el historial de cambios del proyecto indicando la justificación técnica y la fecha de entrada en vigor.
