# 28_DISENO_ARQUITECTONICO_INVENTARIO.md

**Versión:** 1.0  
**Estado:** Listo para Revisión de Arquitectura  
**Última actualización:** 2026-07-23  
**Documento:** Diseño Arquitectónico del Módulo Inventario  

---

# Objetivo

Establecer de forma rigurosa y exhaustiva el **Diseño Arquitectónico** para el módulo de **Inventario** (Inventory) en el backend de CajaFácil. Este documento especifica la distribución de capas, el flujo de control, los agregados, los contratos de repositorio, los casos de uso, los eventos, el desacoplamiento de bounded contexts y las pautas transaccionales que gobiernan la implementación, respetando estrictamente los principios de **Clean Architecture**, **Domain-Driven Design (DDD)** y la **Arquitectura General del Proyecto**.

---

# 1. Responsabilidades Arquitectónicas por Capa

El módulo de Inventario se estructura en cuatro capas claramente diferenciadas y desacopladas para mantener la cohesión y la mantenibilidad.

```text
backend/app/modules/venta/
backend/app/modules/inventario/  <-- Estructura homóloga a Ventas
├── domain/            <-- Núcleo inmutable. Reglas de negocio puras.
├── application/       <-- Orquestación de casos de uso y lógica de coordinación.
├── infrastructure/    <-- Persistencia (SQLAlchemy), adaptadores y mappers.
└── presentation/      <-- Enrutadores FastAPI, esquemas Pydantic (DTO).
```

### Capa de Dominio (`domain/`)
* **Responsabilidad:** Define el agregado raíz `MovimientoInventario`, las entidades asociadas (`Merma`, `AjusteInventario`), los objetos de valor, excepciones de negocio y el contrato abstracto del repositorio.
* **Restricción:** Código en Python puro. No puede importar frameworks externos (FastAPI, Pydantic) ni librerías de persistencia (SQLAlchemy). No tiene dependencias externas.

### Capa de Aplicación (`application/`)
* **Responsabilidad:** Coordina los casos de uso (registrar movimientos, mermas, ajustes y consulta de stock), controla las transacciones (Unit of Work) y despacha los eventos de dominio de forma síncrona en memoria a través del `EventDispatcher`.
* **Restricción:** No interactúa directamente con la base de datos física ni con la red. Se comunica mediante puertos abstractos.

### Capa de Persistencia e Infraestructura (`infrastructure/`)
* **Responsabilidad:** Define los modelos SQLAlchemy ORM para las tablas físicas de la base de datos, implementa el repositorio concreto heredando de `BaseRepository` y gestiona el mapeo de tipos y traducción bidireccional mediante el Mapper.
* **Restricción:** No toma decisiones de negocio. Solo ejecuta operaciones persistentes y flushes delegados por la aplicación.

### Capa de Presentación (`presentation/`)
* **Responsabilidad:** Expone la API REST mediante routers FastAPI, realiza validación sintáctica de peticiones mediante Pydantic (Request DTOs), serializa salidas (Response DTOs) e inyecta las dependencias necesarias.
* **Restricción:** No realiza cálculos de stock ni validaciones de inventario negativo.

---

# 2. Agregado Raíz, Entidades y Objetos de Valor

El contexto de Inventario está estructurado jerárquicamente bajo un único Aggregate Root.

```text
                     ┌──────────────────────────┐
                     │ MovimientoInventario(AR) │
                     └─────────────┬────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    ▼                             ▼
              ┌───────────┐                 ┌───────────┐
              │Merma (Ent)│                 │Ajuste(Ent)│
              └───────────┘                 └───────────┘
```

### Agregado Raíz (Aggregate Root)
* **`MovimientoInventario`** (Entidad transaccional): Hecho histórico inmutable de cambio físico en el stock.
  * **Atributos:**
    * `id: UUID` (Identificador del movimiento)
    * `company_id: UUID` (Tenant)
    * `product_id: UUID` (Referencia lógica al producto)
    * `type: TipoMovimiento` (Value Object Enum: `ENTRADA`, `SALIDA`)
    * `concept: ConceptoMovimiento` (Value Object Enum: `COMPRA`, `VENTA`, `ANULACION_VENTA`, `MERMA`, `AJUSTE`, `DEVOLUCION_PROVEEDOR`, `INVENTARIO_INICIAL`)
    * `quantity: Decimal` (Cantidad física movilizada)
    * `origin_document_id: UUID | None` (Identificador del documento que lo justifica: VentaId, CompraId, etc.)
    * `notes: str | None` (Comentarios adicionales)
    * `created_at: datetime` (Fecha/Hora del movimiento)
    * `created_by: UUID` (Usuario que realiza la operación)

### Entidades Internas
* **`Merma`** (Entidad interna): Proporciona detalle detallado sobre pérdidas físicas por merma.
  * **Atributos:**
    * `id: UUID`
    * `movimiento_id: UUID` (FK a MovimientoInventario)
    * `reason: str` (Enum: `ROTURA`, `VENCIMIENTO`, `ROBO`, `OTRO`)
    * `description: str | None`
* **`AjusteInventario`** (Entidad interna): Detalla una corrección física realizada tras auditoría.
  * **Atributos:**
    * `id: UUID`
    * `movimiento_id: UUID` (FK a MovimientoInventario)
    * `physical_quantity: Decimal` (Conteo real)
    * `system_quantity: Decimal` (Existencia registrada)
    * `difference: Decimal` (Diferencia física)

### Objetos de Valor (Value Objects)
* **`TipoMovimiento`**: Enum (`ENTRADA`, `SALIDA`).
* **`ConceptoMovimiento`**: Enum que representa los motivos del negocio, evitando dependencias directas entre módulos.

---

# 3. Contrato del Repositorio (Repository Port)

La interfaz en la capa de dominio define el puerto de acceso a la persistencia para el agregado:

```python
from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional
from app.modules.inventario.domain.entities.movimiento import MovimientoInventario

class MovimientoInventarioRepository(ABC):
    @abstractmethod
    def save(self, movimiento: MovimientoInventario) -> MovimientoInventario:
        """
        Guarda un movimiento de inventario en la sesión activa.
        No ejecuta commit.
        """
        pass

    @abstractmethod
    def get_by_id(self, movimiento_id: UUID) -> Optional[MovimientoInventario]:
        """
        Retorna un movimiento por su identificador único.
        """
        pass

    @abstractmethod
    def get_by_product_id(self, company_id: UUID, product_id: UUID) -> List[MovimientoInventario]:
        """
        Retorna el histórico de movimientos (Kardex) para un producto.
        """
        pass

    @abstractmethod
    def search(self, company_id: UUID, filters: dict) -> List[MovimientoInventario]:
        """
        Búsqueda avanzada de movimientos aplicando filtros de fecha, tipo, concepto y usuario.
        """
        pass
```

---

# 4. Casos de Uso del Negocio (Application Layer)

### A. `RegistrarMovimientoUseCase`
* **Responsabilidad:** Registra movimientos de entrada o salida ordinarios de stock.
* **Lógica clave:**
  1. Consulta a través de `ProductLookup` si el producto existe, maneja stock y está activo.
  2. Calcula el balance neto de existencias acumuladas sumando y restando el histórico.
  3. Si es una `SALIDA` y el producto tiene `PermiteStockNegativo = False`, valida que la cantidad solicitada no resulte en stock negativo; si lo hace, aborta lanzando `StockInsuficienteException`.
  4. Crea el agregado `MovimientoInventario`, lo persiste a través del repositorio y despacha `InventarioActualizado`.

### B. `RegistrarMermaUseCase`
* **Responsabilidad:** Registra la pérdida de stock por daño o merma.
* **Lógica clave:**
  1. Instancia un `MovimientoInventario` con tipo `SALIDA` y concepto `MERMA`.
  2. Valida invariantes y existencias.
  3. Crea el registro de `Merma` asociado.
  4. Persiste el agregado y despacha `MermaRegistrada` junto con `InventarioActualizado`.

### C. `RegistrarAjusteUseCase`
* **Responsabilidad:** Sincroniza el conteo físico con el saldo del sistema.
* **Lógica clave:**
  1. Calcula el stock del sistema actual del producto.
  2. Determina la diferencia: $\text{Diferencia} = \text{Cantidad Física} - \text{Cantidad Sistema}$.
  3. Si la diferencia es positiva, registra una `ENTRADA` con concepto `AJUSTE`.
  4. Si es negativa, registra una `SALIDA` con concepto `AJUSTE`.
  5. Crea la entidad `AjusteInventario` y despacha `AjusteInventarioRegistrado`.

### D. `ObtenerStockProductoUseCase`
* **Responsabilidad:** Retorna la existencia disponible de un producto.
* **Lógica clave:**
  1. Ejecuta una consulta agregada sobre los movimientos para retornar el balance actual.

---

# 5. Eventos de Dominio y Propósito

Los eventos se publican en memoria de manera síncrona dentro de la misma transacción:

* **`InventarioActualizado`**: Emitido en cada movimiento. Permite que otros módulos (como alertas o reportes) conozcan el saldo neto en tiempo real.
* **`MermaRegistrada`**: Publica el descarte de productos para auditoría de mermas financieras.
* **`AjusteInventarioRegistrado`**: Reporta correcciones físicas e identifica al supervisor autorizante.

---

# 6. Desacoplamiento de Bounded Contexts y Reglas de Comunicación

### Comunicación Permitida (Entrada/Salida)
* **Lectura Externa (`ProductLookup`)**: El caso de uso consulta a Catálogo (`Product`) utilizando un puerto de consulta para obtener banderas de negocio (`ManejaInventario`, `PermiteStockNegativo`).
* **Consumo de Eventos de Terceros**: Registra event handlers que reaccionan a:
  * `VentaConfirmada` (Ventas) $\rightarrow$ Llama internamente a `RegistrarMovimientoUseCase` (salida).
  * `VentaAnulada` (Ventas) $\rightarrow$ Llama a `RegistrarMovimientoUseCase` (entrada).
  * `CompraRegistrada` (Compras) $\rightarrow$ Llama a `RegistrarMovimientoUseCase` (entrada).

### Comunicación Prohibida
* **Inventario no conoce repositorios de Ventas ni Compras**: No lee de forma directa órdenes de compra ni facturas de ventas. Se entera exclusivamente por medio de los payloads de eventos.
* **Inventario no edita productos**: No tiene acceso de escritura a la base de datos de Catálogo.

### El Principio de Desacoplamiento de Origen (Concepto de Negocio)
Para evitar acoplamiento de código, el agregado `MovimientoInventario` **no importa modelos o entidades externas**. La justificación se encapsula mediante un identificador lógico (`origin_document_id`) y el enum `ConceptoMovimiento`. El inventario solo entiende que la mercancía se moviliza por una "venta", "compra" o "merma", sin necesidad de entender la estructura o atributos de esos módulos.

---

# 7. Estrategia Transaccional (Unit of Work)

El módulo de Inventario adopta estrictamente el patrón consolidado durante el Sprint 13 para salvaguardar la coherencia de datos:

1. **Repository sin Commit**: La implementación `MovimientoInventarioRepositoryImpl` no llamará a `db.commit()` en sus métodos de almacenamiento. Realizará `self.db.add(...)` y `self.db.flush()`.
2. **Coordinación de Transacción en Use Case**: El commit es responsabilidad única de la capa de aplicación. Cuando un caso de uso inicia, abre un bloque transaccional:
   ```python
   try:
       with self.db.begin_nested():
           # 1. Guardar movimiento
           self.repository.save(movimiento)
           # 2. Despachar eventos (los handlers de consistencia se ejecutan síncronamente aquí)
           self.event_dispatcher.dispatch(event)
       self.db.commit()
   except Exception as e:
       self.db.rollback()
       raise e
   ```
   Esto garantiza que si el despacho de eventos de inventario falla o si hay un error al registrar un ajuste, toda la operación local (incluyendo tablas adyacentes) se revierte en bloque.

---

# 8. Estrategia Offline-First para Existencias

Para garantizar que el sistema opere con consistencia sin conexión permanente a Internet:

1. **Balance Histórico Acumulado**: Dado que las existencias son un valor derivado e histórico calculado de la sumatoria de movimientos, las operaciones locales en SQLite se graban con un `created_at` del cliente.
2. **Sincronización por Timestamps del Cliente**: Al sincronizar con la nube, los movimientos se insertan y ordenan cronológicamente según la hora en que ocurrió el hecho en el dispositivo cliente, recalculando las existencias derivadas retrospectivamente de forma correcta para resolver condiciones de carrera.
3. **Identificadores UUID del Cliente**: Los movimientos y mermas se crean en el cliente con UUIDs únicos para evitar colisiones al subir la información al servidor central.

---

# 9. Declaración de Confirmaciones de Consistencia Funcional

Alineado con el análisis funcional oficial:
* **Existencia** representa estrictamente un **valor derivado** calculado a partir de movimientos de inventario.
* **MovimientoInventario** es el **único hecho histórico** del contexto que justifica cambios físicos en base de datos.
* **Ningún usuario ni proceso externo** puede modificar existencias directamente sin registrar un movimiento.
* **Todo cambio físico** (compra, venta, ajuste, merma) genera obligatoriamente un registro en `MovimientoInventario`.
