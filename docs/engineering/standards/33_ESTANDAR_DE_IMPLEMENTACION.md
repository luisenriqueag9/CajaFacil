---
id: CF-DOC-033
title: "Estándar de Implementación y Constitución Técnica"
owner: "lead-architect"
status: "approved"
last_reviewed: 2026-07-25
role: "canonical"
---

# Constitución Técnica de CajaFácil

Este documento constituye la **Constitución Técnica y Guía de Estándares de Implementación Oficial** para el proyecto CajaFácil. Cualquier desarrollo futuro de backend, frontend o base de datos deberá alinearse estrictamente y de forma obligatoria con las normas de diseño, patrones de codificación y convenciones arquitectónicas descritas en este estándar.

---

## 1. Filosofía de Implementación

CajaFácil está diseñado para ser un sistema POS comercial SaaS robusto, mantenible a 10 años, extensible y con capacidades avanzadas de ejecución local. Para lograr este objetivo, la ingeniería se basa en cuatro pilares fundamentales:

1. **Domain-Driven Design (DDD) Táctico**: El núcleo del negocio está modelado de forma pura en el dominio, libre de dependencias de frameworks o bases de datos. Los agregados son los guardianes de las invariantes y de la consistencia.
2. **Clean Architecture (Arquitectura Limpia)**: Estricto aislamiento en capas. La dirección de las dependencias es siempre hacia adentro. La capa interna (Dominio) no conoce la existencia de capas externas (Persistencia, APIs, Frameworks).
3. **Modularidad Estricta**: Cada contexto acotado (Bounded Context) es un módulo independiente que interactúa con otros contextos únicamente a través de interfaces bien definidas (Ports) o mediante la publicación y consumo de **Eventos de Dominio**.
4. **Offline-First & Transaccionalidad Segura**: El sistema está preparado para operar localmente y sincronizar datos de forma asíncrona. La base de datos local gestiona la integridad referencial y las transacciones de manera atómica mediante un patrón de Unit of Work.

---

## 2. Organización Obligatoria de Carpetas

### 2.1. Backend (Python/FastAPI)
Cada módulo dentro del backend (`backend/app/modules/<modulo_name>/`) debe organizarse estrictamente bajo la siguiente topología de cuatro capas:

```text
backend/app/modules/<modulo_name>/
├── __init__.py                  # Exporta el router y dependencias públicas
├── domain/                      # CAPA 1: DOMINIO (Lógica de negocio pura - Python estándar)
│   ├── __init__.py
│   ├── entities/                # Agregados y entidades (Clases tradicionales y @dataclass)
│   ├── exceptions/              # Excepciones específicas del negocio y de invariantes
│   ├── events/                  # Eventos del dominio
│   └── repositories/            # Interfaces abstractas (contratos) de repositorios
├── application/                 # CAPA 2: APLICACIÓN (Casos de uso y orquestación)
│   ├── __init__.py
│   ├── use_cases/               # Implementación de los casos de uso (Commands/Queries)
│   └── ports/                   # Interfaces / Puertos de consulta cruzada de dominios
├── data/                        # CAPA 3: INFRAESTRUCTURA Y DATOS (Acceso a BD, Mappers)
│   ├── __init__.py
│   ├── models.py                # Modelos ORM (SQLAlchemy Declarative Base)
│   ├── mappers/                 # Mapeadores de traducción bidireccional (Dominio <-> DB)
│   └── repositories/            # Implementación concreta del repositorio (RepositoryImpl)
└── presentation/                # CAPA 4: PRESENTACIÓN (Endpoints HTTP, API)
    ├── __init__.py
    ├── routers/                 # Enrutadores REST (FastAPI Routers)
    ├── dto/                     # Esquemas de entrada y salida (Pydantic Models)
    └── dependencies/            # Inyección de dependencias para los endpoints
```

### 2.2. Frontend (Flutter/Dart)
Los módulos del frontend (`desktop_app/lib/app/modules/<modulo_name>/`) deben estructurarse de la siguiente manera:

```text
desktop_app/lib/app/modules/<modulo_name>/
├── application/                 # Lógica de aplicación, Controllers, Providers y Riverpod States
├── data/                        # Acceso a datos locales (SQLite/Drift), llamadas HTTP y mappers
│   ├── datasources/             # Clientes HTTP locales o clientes de base de datos local
│   ├── models/                  # Modelos de datos de red o persistencia
│   └── repositories/            # Implementaciones de repositorios
├── domain/                      # Entidades del dominio del negocio y contratos de repositorios
│   ├── entities/                # Entidades inmutables puras de Flutter
│   └── repositories/            # Interfaces de repositorios
└── presentation/                # Interfaz de usuario (Widgets, Pages)
    ├── pages/                   # Vistas principales de pantalla completa
    └── widgets/                 # Componentes visuales reutilizables específicos del módulo
```

---

## 3. Convenciones de Nombres

### 3.1. Convención General del Código
- **Backend (Python)**:
  - Archivos, variables y funciones: `snake_case` (ej. `confirmar_venta_use_case.py`, `total_amount`).
  - Clases, Excepciones y Modelos: `CamelCase` (ej. `VentaDetail`, `VentaVaciaException`).
- **Frontend (Dart)**:
  - Archivos y carpetas: `snake_case` (ej. `login_page.dart`, `app_colors.dart`).
  - Clases: `CamelCase` (ej. `LoginPage`, `AppButton`).
- **Idioma Obligatorio**: Español para toda la nomenclatura del negocio y el lenguaje ubicuo (ej. `Venta`, `DetalleVenta`, `Existencia`, `Compra`). Los términos del framework e infraestructura técnica se permiten en inglés (ej. `RepositoryImpl`, `UseCase`, `BaseModel`, `router`).

---

## 4. Cómo crear un Aggregate Root (Backend)

Un **Aggregate Root** (Raíz del Agregado) es una clase de dominio pura que agrupa entidades relacionadas para gestionar cambios de estado consistentes.

### Reglas obligatorias:
1. Usar `@dataclass` tradicionales (sin congelar en la raíz si requiere mutar estado interno a través de métodos específicos del negocio).
2. Proteger las invariantes de negocio en el método `__post_init__` y mediante un método `validate()`.
3. Todo cambio de estado crítico debe ocurrir a través de métodos de negocio explícitos (ej. `anular()`), nunca alterando propiedades directamente desde el exterior.
4. Utilizar `Decimal` para cualquier importe monetario o cantidad para evitar imprecisiones de coma flotante.

### Ejemplo oficial:
```python
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from app.common.exceptions import ValidationException

@dataclass
class DetalleVenta:
    id: UUID
    product_id: UUID
    quantity: Decimal
    unit_price: Decimal

    def validate(self) -> None:
        if self.quantity <= Decimal("0.00"):
            raise ValidationException("La cantidad debe ser mayor que cero.")
        if self.unit_price < Decimal("0.00"):
            raise ValidationException("El precio unitario no puede ser negativo.")

@dataclass
class Venta:
    id: UUID
    company_id: UUID
    status: str  # CONFIRMADA, ANULADA
    created_at: datetime
    details: list[DetalleVenta] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        if not self.company_id:
            raise ValidationException("La empresa es obligatoria.")
        if self.status not in {"CONFIRMADA", "ANULADA"}:
            raise ValidationException("Estado inválido.")
        if not self.details:
            raise ValidationException("Debe tener al menos un detalle.")
        for item in self.details:
            item.validate()

    def anular(self) -> None:
        if self.status == "ANULADA":
            raise ValidationException("La venta ya está anulada.")
        self.status = "ANULADA"
        self.validate()
```

---

## 5. Cómo crear una Entidad (Backend)

Una **Entidad** posee un identificador de identidad único y persistente a lo largo del tiempo, y sus propiedades pueden cambiar.

### Reglas obligatorias:
1. Tener una identidad única (`id: UUID`).
2. Declarar validaciones de consistencia interna.
3. No heredar de bases de ORM; debe ser una clase de Python pura.

---

## 6. Cómo crear un Value Object (Backend)

Un **Value Object** (Objeto de Valor) no tiene identidad conceptual; se define exclusivamente por el valor de sus propiedades.

### Reglas obligatorias:
1. Usar `@dataclass(frozen=True)` para asegurar la inmutabilidad absoluta.
2. Toda modificación genera una nueva instancia.
3. Validar los valores en `__post_init__`.

### Ejemplo oficial:
```python
from dataclasses import dataclass
from decimal import Decimal
from app.common.exceptions import ValidationException

@dataclass(frozen=True)
class Dinero:
    monto: Decimal
    divisa: str = "NIO"

    def __post_init__(self) -> None:
        if self.monto < Decimal("0.00"):
            raise ValidationException("El monto no puede ser negativo.")
        if not self.divisa or len(self.divisa) != 3:
            raise ValidationException("Divisa inválida. Debe ser código ISO de 3 letras.")

    def sumar(self, otro: "Dinero") -> "Dinero":
        if self.divisa != otro.divisa:
            raise ValidationException("No se pueden sumar montos de distintas divisas.")
        return Dinero(self.monto + otro.monto, self.divisa)
```

---

## 7. Cómo crear un Repository (Backend)

El repositorio proporciona una abstracción para acceder a la colección de agregados persistidos.

### Reglas obligatorias:
1. **Interfaz en el Dominio**: Una clase abstracta derivada de `abc.ABC` sin dependencias de base de datos.
2. **Implementación en la Capa Data**: Clase que hereda de `BaseRepository[DBModel]` (proporcionado en `core/`) e implementa la interfaz del Dominio.
3. **Sin commits dentro de la implementación**: El repositorio interactúa con la sesión de SQLAlchemy agregando o eliminando objetos, pero **nunca ejecuta `db.commit()` o `db.rollback()`**. La transacción y su cierre definitivo es responsabilidad exclusiva del caso de uso o del Unit of Work en la capa de aplicación.

### Ejemplo de Interfaz (Domain):
```python
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.venta.domain.entities.venta import Venta

class VentaRepository(ABC):
    @abstractmethod
    def save(self, venta: Venta) -> Venta:
        pass

    @abstractmethod
    def get_by_id(self, id: UUID) -> Venta | None:
        pass
```

### Ejemplo de Implementación (Data):
```python
from uuid import UUID
from sqlalchemy.orm import Session
from app.database.repositories.base import BaseRepository
from app.modules.venta.domain.entities.venta import Venta
from app.modules.venta.domain.repositories.venta_repository import VentaRepository
from app.modules.venta.data.models import Venta as DBOVenta
from app.modules.venta.data.mappers.venta_mapper import VentaMapper

class VentaRepositoryImpl(BaseRepository[DBOVenta], VentaRepository):
    def __init__(self, db: Session):
        super().__init__(DBOVenta, db)

    def save(self, venta: Venta) -> Venta:
        db_model = VentaMapper.to_db(venta)
        # Adds object to sqlalchemy session and flushes to database
        self.db.add(db_model)
        self.db.flush()
        return VentaMapper.to_domain(db_model)

    def get_by_id(self, id: UUID) -> Venta | None:
        db_model = self.db.query(DBOVenta).filter(DBOVenta.id == id).first()
        return VentaMapper.to_domain(db_model) if db_model else None
```

---

## 8. Cómo crear un Mapper (Backend)

El Mapper traduce los datos entre los modelos de persistencia del ORM (SQLAlchemy) y las entidades puras del dominio.

### Reglas obligatorias:
1. Métodos de clase estáticos: `to_db`, `to_domain` y `update_db_model`.
2. Encapsular la lógica de traducción de relaciones complejas recursivamente usando otros mappers si es necesario.

### Ejemplo oficial:
```python
from app.modules.venta.domain.entities.venta import Venta, DetalleVenta
from app.modules.venta.data.models import Venta as DBOVenta, VentaDetail as DBOVentaDetail

class VentaMapper:
    @staticmethod
    def to_db(domain: Venta) -> DBOVenta:
        db_details = [
            DBOVentaDetail(
                id=d.id,
                product_id=d.product_id,
                quantity=d.quantity
            ) for d in domain.details
        ]
        return DBOVenta(
            id=domain.id,
            company_id=domain.company_id,
            status=domain.status,
            details=db_details,
            created_at=domain.created_at
        )

    @staticmethod
    def to_domain(db: DBOVenta) -> Venta:
        details = [
            DetalleVenta(
                id=d.id,
                product_id=d.product_id,
                quantity=d.quantity
            ) for d in db.details
        ]
        return Venta(
            id=db.id,
            company_id=db.company_id,
            status=db.status,
            details=details,
            created_at=db.created_at,
            updated_at=db.updated_at
        )
```

---

## 9. Cómo crear un Use Case (Capa de Aplicación)

El caso de uso coordina la orquestación del negocio.

### Reglas obligatorias:
1. Su nombre de clase debe terminar en `UseCase` y el archivo en `_use_case.py`.
2. Debe recibir parámetros de entrada mediante un objeto de tipo **Command** o **Query** (clase `@dataclass(frozen=True)`).
3. Debe inyectar sus repositorios e integraciones (ports) a través de la interfaz abstracta (inversión de dependencias).
4. El método principal de ejecución debe llamarse estrictamente `execute()`.
5. Debe controlar la consistencia de la base de datos (Unit of Work) a través de la interfaz abstracta `UnitOfWork` (`with self.uow:`), asegurando que la persistencia y la publicación de eventos locales se ejecuten atómicamente.

### Ejemplo oficial:
```python
from dataclasses import dataclass
from uuid import UUID
from app.modules.venta.domain.entities.venta import Venta
from app.modules.venta.domain.repositories.venta_repository import VentaRepository
from app.modules.venta.application.ports.unit_of_work import UnitOfWork
from app.modules.venta.application.ports.product_lookup import ProductLookup

@dataclass(frozen=True)
class ConfirmarVentaCommand:
    company_id: UUID
    box_id: UUID
    user_id: UUID

class ConfirmarVentaUseCase:
    def __init__(
        self,
        repository: VentaRepository,
        uow: UnitOfWork,
        product_lookup: ProductLookup
    ):
        self.repository = repository
        self.uow = uow
        self.product_lookup = product_lookup

    def execute(self, command: ConfirmarVentaCommand) -> Venta:
        # Business checks (using lookups/ports)
        if not self.product_lookup.exists(command.company_id):
            raise Exception("Regla fallida")

        # Construct aggregate
        venta = Venta(id=..., company_id=command.company_id, ...)

        # Persist within a secure transaction
        with self.uow:
            saved_venta = self.repository.save(venta)
        return saved_venta
```

---

## 10. Cómo crear un DTO (Presentation)

Los DTOs representan la forma de entrada y salida del endpoint API.

### Reglas obligatorias:
1. Heredar de `pydantic.BaseModel`.
2. Validar tipos de datos de forma estricta.

### Ejemplo:
```python
from pydantic import BaseModel, Field
from uuid import UUID

class DetalleVentaRequest(BaseModel):
    product_id: UUID = Field(..., description="ID del producto")
    quantity: float = Field(..., gt=0, description="Cantidad mayor que cero")

class ConfirmarVentaRequest(BaseModel):
    company_id: UUID
    details: list[DetalleVentaRequest]
```

---

## 11. Cómo crear una API (Presentation Routers)

### Reglas obligatorias:
1. Usar `fastapi.APIRouter`.
2. Todos los endpoints deben retornar de forma uniforme una estructura de `ApiResponse[DTO]` (definida en `common/responses.py`).
3. Manejar la inyección de dependencias de la sesión de base de datos a través de FastAPI y resolver las instancias concretas en la capa Presentation.

### Ejemplo oficial:
```python
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.common.presentation.responses.api_response import ApiResponse
from app.modules.venta.presentation.dto.venta_dto import ConfirmarVentaRequest, VentaResponse
from app.modules.venta.presentation.dependencies import get_confirmar_venta_use_case
from app.modules.venta.application.use_cases.confirmar_venta_use_case import ConfirmarVentaUseCase

router = APIRouter(prefix="/sales", tags=["Ventas"])

@router.post("", response_model=ApiResponse[VentaResponse], status_code=status.HTTP_201_CREATED)
def create_sale(
    request: ConfirmarVentaRequest,
    use_case: ConfirmarVentaUseCase = Depends(get_confirmar_venta_use_case)
):
    command = request.to_command()
    venta = use_case.execute(command)
    
    response_data = VentaResponse.from_domain(venta)
    return ApiResponse(
        success=True,
        message="Venta confirmada exitosamente.",
        data=response_data
    )
```

---

## 12. Cómo crear Migraciones (Alembic)

Debido al soporte Offline-First de CajaFácil y al uso de SQLite a nivel local y PostgreSQL en producción, se deben seguir las siguientes directrices:

1. **Soporte Batch**: Ejecutar migraciones en modo por lotes (`render_as_batch=True` en `env.py`) para permitir modificaciones de esquema complejas (ej. alteración de columnas, cambios de FK) en SQLite.
2. **Generación automática**: Asegurarse de importar los nuevos modelos en `app/database/base.py` antes de ejecutar el comando de generación.
3. **Nombres de archivo**: Nomenclatura descriptiva con prefijo aleatorio e identificador único generado por Alembic.
4. **Comando de creación**:
   ```bash
   alembic revision --autogenerate -m "create_purchase_table"
   ```

---

## 13. Cómo escribir Pruebas

Para mantener la robustez y una alta cobertura (mínimo 80%), las pruebas de software en CajaFácil siguen estas reglas:

### 13.1. Pruebas Unitarias del Dominio
- **Frecuencia**: Obligatorio para todas las entidades y agregados.
- **Enfoque**: Sin dependencias de bases de datos o FastAPI. Pruebas puras de Python que validan invariantes ante diferentes combinaciones de valores.

### 13.2. Pruebas de Integración (Capa Data / Application)
- **Frecuencia**: Obligatorio para casos de uso y repositorios físicos.
- **Base de datos de prueba**: Utilizar una base de datos SQLite en memoria (`sqlite:///:memory:`) o un archivo temporal específico de testing, inicializado y destruido antes y después de cada test de forma aislada.

### Ejemplo de prueba unitaria:
```python
import pytest
from decimal import Decimal
from uuid import uuid4
from app.modules.venta.domain.entities.venta import DetalleVenta
from app.common.exceptions import ValidationException

def test_detalle_venta_monto_negativo_lanza_excepcion():
    with pytest.raises(ValidationException):
        detail = DetalleVenta(
            id=uuid4(),
            product_id=uuid4(),
            quantity=Decimal("-1.5"),
            unit_price=Decimal("10.00")
        )
        detail.validate()
```

---

## 14. Cómo publicar Eventos de Dominio

### Directrices de publicación:
1. Los eventos se definen en `domain/events/` como `@dataclass(frozen=True)`.
2. La publicación ocurre de forma sincrónica dentro de la transacción de base de datos en la capa de aplicación (Use Case), asegurando la atomicidad de la operación local.
3. Se utiliza el componente centralizado de despacho de eventos. Otros módulos se suscriben a través de escuchadores en sus respectivas dependencias de aplicación.

---

## 15. Qué está PROHIBIDO hacer

1. ❌ **PROHIBIDO hacer `db.commit()` en repositorios**. Los repositorios solo manejan la preparación de los cambios en la sesión de base de datos (`flush`, `add`, `delete`). El commit final pertenece a la capa de aplicación (UseCase) o al Unit of Work.
2. ❌ **PROHIBIDO importar dependencias externas en la capa de Dominio**. El dominio no puede importar librerías de persistencia (SQLAlchemy), de presentación (FastAPI, Pydantic) ni código de otros módulos acotados.
3. ❌ **PROHIBIDO duplicar tablas físicas o crear tablas mock** (`mock_movimiento_inventario`, `mock_movimiento_caja`, etc.) en bases de datos de otros contextos. La consistencia inter-módulos se realiza de manera reactiva mediante **Eventos de Dominio** asíncronos o a través de consultas por interfaces de puerto (Ports/Lookups), manteniendo el aislamiento de esquemas.
4. ❌ **PROHIBIDO el uso de números float para dinero**. Todos los cálculos monetarios deben realizarse estrictamente con tipos de datos `Decimal` de Python y mapearse con `Numeric(18, 4)` en base de datos.
5. ❌ **PROHIBIDO saltarse la inyección de dependencias**. No se permite instanciar repositorios concretos o controladores dentro de los casos de uso o de las APIs mediante inicialización directa; todo debe resolverse mediante dependencias inyectadas.
