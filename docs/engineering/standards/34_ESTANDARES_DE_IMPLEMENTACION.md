# 34_ESTANDARES_DE_IMPLEMENTACION.md

**Versión:** 1.0  
**Estado:** 📜 Aprobado (Sprint 16)  
**Última actualización:** 2026-07-23  
**Documento:** Estándares Oficiales de Implementación  

---

# 1. Estructura Obligatoria de un Módulo

Cada módulo (Bounded Context) en el backend de CajaFácil debe seguir una estructura estricta de cuatro capas alineada con **Clean Architecture** y **DDD**. Ningún archivo de una capa externa puede ser importado directamente por una capa interna.

```text
backend/app/modules/<modulo_name>/
├── __init__.py                  # Exporta el router de presentación
├── domain/                      # CAPA DE DOMINIO (Núcleo inmutable)
│   ├── __init__.py
│   ├── entities/                # Agregados y entidades (Python puro, dataclasses)
│   ├── exceptions/              # Excepciones de negocio del dominio
│   ├── events/                  # Eventos del dominio
│   └── repositories/            # Interfaces/contratos abstractos de repositorios
├── application/                 # CAPA DE APLICACIÓN (Casos de uso y orquestación)
│   ├── __init__.py
│   ├── use_cases/               # Implementación de los casos de uso (Commands/Queries)
│   ├── ports/                   # Puertos de integración con otros contextos (lookups)
│   └── event_dispatcher.py      # Despachador de eventos síncronos en memoria
├── data/                        # CAPA DE INFRAESTRUCTURA Y DATOS
│   ├── __init__.py
│   ├── models.py                # Modelos ORM de base de datos (SQLAlchemy)
│   ├── mappers/                 # Traductores bidireccionales Dominio <-> ORM
│   └── repositories/            # Implementación física del repositorio
└── presentation/                # CAPA DE PRESENTACIÓN (Interfaz externa)
    ├── __init__.py
    ├── routers/                 # Enrutadores API REST (FastAPI)
    ├── dto/                     # Esquemas de entrada/salida (Pydantic DTOs)
    └── dependencies/            # Inyección de dependencias (get_db, use cases)
```

---

# 2. Convenciones de Nombres y Carpetas

### Convenciones de Carpetas (Snake Case)
Todas las carpetas y archivos del código fuente deben utilizar `snake_case`.
* **Ejemplo correcto:** `app/modules/inventario/data/mappers/movimiento_mapper.py`
* **Ejemplo incorrecto:** `app/modules/Inventario/Data/Mappers/movimientoMapper.py`

### Convenciones para Entidades y Agregados
* Definidas como `@dataclass` tradicionales.
* Idioma: Español (Lenguaje Ubicuo).
* Naming: CamelCase.
* **Ejemplo:**
  ```python
  @dataclass
  class MovimientoInventario:
      id: UUID
      company_id: UUID
      ...
  ```

### Convenciones para Excepciones
* Ubicación: `domain/exceptions/`.
* Heredan de: `CajaFacilException` o `ValidationException` (`app.common.exceptions`).
* Naming: CamelCase con sufijo `Exception`.
* **Ejemplo:** `StockInsuficienteException(CajaFacilException)`

### Convenciones para Eventos
* Ubicación: `domain/events/`.
* Definidos como `@dataclass(frozen=True)` (Inmutables).
* Naming: CamelCase en tiempo pasado pasivo o sustantivo de acción.
* **Ejemplo:** `InventarioActualizado`, `CajaCerrada`

### Convenciones para Repositorios (Interfaces y Concretos)
* **Interfaz (Domain):** CamelCase con sufijo `Repository`.
  * **Ejemplo:** `MovimientoInventarioRepository(ABC)`
* **Implementación (Data):** CamelCase con sufijo `RepositoryImpl`. Hereda de `BaseRepository[DBModel]` e implementa la interfaz del dominio.
  * **Ejemplo:** `MovimientoInventarioRepositoryImpl(BaseRepository[DBMovimiento], MovimientoInventarioRepository)`

### Convenciones para Casos de Uso (Use Cases)
* Ubicación: `application/use_cases/`.
* Nombre de archivo: `snake_case` con sufijo `_use_case.py`.
* Clase: CamelCase con sufijo `UseCase`.
* Métodos: El método principal de ejecución debe llamarse estrictamente `execute`.
* **Ejemplo:**
  ```python
  class RegistrarMovimientoUseCase:
      def execute(self, command: RegistrarMovimientoCommand) -> MovimientoInventario:
          ...
  ```

### Convenciones para DTO (Data Transfer Objects)
* Ubicación: `presentation/dto/`.
* Naming: CamelCase con sufijo `Request` (para datos de entrada) o `Response` (para datos de salida).
* **Ejemplo:** `RegistrarAjusteRequest`, `MovimientoInventarioResponse`

### Convenciones para Mappers
* Ubicación: `data/mappers/`.
* Naming del archivo: `snake_case` con sufijo `_mapper.py`.
* Métodos obligatorios:
  * `to_db(domain_entity)`: Convierte entidad de dominio a modelo SQLAlchemy.
  * `to_domain(db_model)`: Convierte modelo SQLAlchemy a entidad de dominio.
  * `update_db_model(db_model, domain_entity)`: Actualiza campos modificables en un registro existente.

### Convenciones para Routers
* Ubicación: `presentation/routers/`.
* Naming del archivo: `snake_case` con sufijo `_router.py`.
* Rutas expuestas: Uso exclusivo de `ApiResponse[DTO]` como tipo de retorno uniforme.
* Prefijo y etiquetas: Registrados en `app/main.py` bajo `/api/v1/<contexto>`.
