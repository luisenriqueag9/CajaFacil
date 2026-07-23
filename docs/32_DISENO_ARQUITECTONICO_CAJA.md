# 32_DISENO_ARQUITECTONICO_CAJA.md

**Versión:** 1.0  
**Estado:** Listo para Revisión de Arquitectura  
**Última actualización:** 2026-07-23  
**Documento:** Diseño Arquitectónico del Módulo Caja  

---

# Objetivo

Establecer de forma rigurosa y exhaustiva el **Diseño Arquitectónico** para el módulo de **Caja** (Cash / Cash Register) en el backend de CajaFácil. Este documento especifica la distribución de capas, el flujo de control, los agregados, los contratos de repositorio, los casos de uso, los eventos, el desacoplamiento de bounded contexts y las pautas transaccionales que gobiernan la implementación, respetando estrictamente los principios de **Clean Architecture**, **Domain-Driven Design (DDD)** y la **Arquitectura General del Proyecto**.

---

# 1. Responsabilidades Arquitectónicas por Capa

Siguiendo el estándar de modularidad de CajaFácil consolidado en los Sprints 13 y 14, el módulo de Caja se estructura en cuatro capas desacopladas:

```text
backend/app/modules/venta/
backend/app/modules/inventario/
backend/app/modules/caja/        <-- Estructura homóloga y desacoplada
├── domain/            <-- Núcleo inmutable. Reglas de negocio puras.
├── application/       <-- Orquestación de casos de uso y lógica de coordinación.
├── infrastructure/    <-- Persistencia (SQLAlchemy), adaptadores y mappers.
└── presentation/      <-- Enrutadores FastAPI, esquemas Pydantic (DTO).
```

### Capa de Dominio (`domain/`)
* **Responsabilidad:** Define el agregado raíz `Caja`, las entidades internas (`MovimientoCaja`, `ArqueoCaja`), los objetos de valor, las excepciones de negocio y el contrato abstracto del repositorio.
* **Restricción:** Python puro. Sin dependencias externas ni de persistencia (SQLAlchemy, Pydantic).

### Capa de Aplicación (`application/`)
* **Responsabilidad:** Coordina los casos de uso (abrir caja, registrar movimientos de ingreso/egreso, arqueos y cierre de caja), controla las transacciones (Unit of Work) y despacha los eventos de dominio de forma síncrona en memoria a través del `EventDispatcher`.
* **Restricción:** Desconoce detalles de frameworks web o drivers de bases de datos.

### Capa de Persistencia e Infraestructura (`infrastructure/`)
* **Responsabilidad:** Define los modelos SQLAlchemy ORM para las tablas físicas, implementa el repositorio concreto heredando de `BaseRepository` y gestiona la traducción de estados de negocio bidireccional mediante el Mapper.
* **Restricción:** No toma decisiones de negocio. Ejecuta operaciones sobre la sesión y flushes delegados por la aplicación.

### Capa de Presentación (`presentation/`)
* **Responsabilidad:** Expone la API REST mediante routers FastAPI, realiza validación sintáctica de peticiones mediante Pydantic (Request DTOs), serializa salidas (Response DTOs) e inyecta las dependencias necesarias.
* **Restricción:** No realiza sumas lógicas de arqueos ni validaciones de estado de caja.

---

# 2. Agregado Raíz, Entidades y Objetos de Valor

El contexto de Caja está estructurado bajo un único Aggregate Root.

```text
                        ┌────────────────────────┐
                        │       Caja (AR)        │
                        └──────────┬─────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    ▼                             ▼
          ┌────────────────────┐       ┌────────────────────┐
          │ MovimientoCaja(Ent)│       │  ArqueoCaja (Ent)  │
          └────────────────────┘       └────────────────────┘
```

### Agregado Raíz (Aggregate Root)
* **`Caja`** (Entidad transaccional): Representa la sesión o turno de operación del terminal.
  * **Atributos:**
    * `id: UUID` (Identificador de la sesión de caja)
    * `company_id: UUID` (Tenant)
    * `user_id: UUID` (Usuario/Cajero custodio)
    * `status: EstadoCaja` (Value Object Enum: `ABIERTA`, `CERRADA`)
    * `opening_balance: Decimal` (Fondo inicial base)
    * `opened_at: datetime` (Fecha/Hora de inicio del turno)
    * `closed_at: datetime | None` (Fecha/Hora de cierre del turno)
    * `movements: list[MovimientoCaja]` (Lista de transacciones)
    * `audits: list[ArqueoCaja]` (Historial de arqueos de control)

### Entidades Internas
* **`MovimientoCaja`** (Entidad interna): Transacción elemental de dinero.
  * **Atributos:**
    * `id: UUID`
    * `caja_id: UUID` (FK a Caja)
    * `type: TipoMovimientoCaja` (Value Object Enum: `INGRESO`, `EGRESO`)
    * `amount: Decimal` (Monto transaccionado)
    * `payment_method: MetodoPago` (Value Object Enum: `EFECTIVO`, `TARJETA`, `TRANSFERENCIA`, `CREDITO`)
    * `concept: ConceptoMovimientoCaja` (Value Object Enum: `VENTA`, `COMPRA`, `RETIRO`, `GASTO`, `ABONO_CREDITO`, `FONDO_APERTURA`, `AJUSTE_ARQUEO`)
    * `origin_document_id: UUID | None` (Enlace lógico para trazabilidad)
    * `created_at: datetime`
* **`ArqueoCaja`** (Entidad interna): Conciliación de auditoría física de efectivo.
  * **Atributos:**
    * `id: UUID`
    * `caja_id: UUID` (FK a Caja)
    * `physical_amount: Decimal` (Efectivo real contado)
    * `system_amount: Decimal` (Monto lógico esperado)
    * `difference: Decimal` (Discrepancia calculada)
    * `created_at: datetime`
    * `supervisor_id: UUID | None` (Supervisor autorizante del descuadre)

### Objetos de Valor (Value Objects)
* **`EstadoCaja`**: Enum (`ABIERTA`, `CERRADA`).
* **`TipoMovimientoCaja`**: Enum (`INGRESO`, `EGRESO`).
* **`MetodoPago`**: Enum (`EFECTIVO`, `TARJETA`, `TRANSFERENCIA`, `CREDITO`).
* **`ConceptoMovimientoCaja`**: Enum que asocia la procedencia comercial.

---

# 3. Contrato del Repositorio (Repository Port)

La interfaz en la capa de dominio define el puerto de acceso a la persistencia para el agregado:

```python
from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional
from app.modules.caja.domain.entities.caja import Caja

class CajaRepository(ABC):
    @abstractmethod
    def save(self, caja: Caja) -> Caja:
        """
        Guarda o actualiza una sesión de caja y sus entidades internas.
        No ejecuta commit automático.
        """
        pass

    @abstractmethod
    def get_by_id(self, caja_id: UUID) -> Optional[Caja]:
        """
        Retorna la sesión de caja por su identificador único.
        """
        pass

    @abstractmethod
    def get_active_by_user(self, company_id: UUID, user_id: UUID) -> Optional[Caja]:
        """
        Retorna la sesión activa (abierta) de un usuario.
        Sirve para validar la regla de custodia única.
        """
        pass

    @abstractmethod
    def search(self, company_id: UUID, filters: dict) -> List[Caja]:
        """
        Historial de sesiones aplicando aislamiento multi-tenant y filtros.
        """
        pass
```

---

# 4. Casos de Uso del Negocio (Application Layer)

### A. `AbrirCajaUseCase`
* **Responsabilidad:** Inicializa un turno de caja para un usuario.
* **Lógica clave:**
  1. Verifica mediante el repositorio que el usuario no tenga una sesión de caja actualmente `ABIERTA` (fuerza `RN-504`).
  2. Crea el agregado `Caja` con estado `ABIERTA` y registra el fondo de apertura.
  3. Agrega automáticamente el primer `MovimientoCaja` de tipo `INGRESO` por concepto `FONDO_APERTURA`.
  4. Guarda la entidad y despacha `CajaAbierta`.

### B. `RegistrarMovimientoCajaUseCase`
* **Responsabilidad:** Registra cobros de ventas, gastos, retiros o abonos.
* **Lógica clave:**
  1. Recupera la sesión de caja del repositorio.
  2. Valida que el estado sea `ABIERTA` (fuerza `RN-502` / `RN-505`).
  3. Instancia y asocia el `MovimientoCaja` al agregado.
  4. Guarda los cambios y despacha `MovimientoCajaRegistrado`.

### C. `RealizarArqueoUseCase`
* **Responsabilidad:** Registra una auditoría intermedia de efectivo.
* **Lógica clave:**
  1. Recupera la caja abierta y calcula el saldo esperado de efectivo sumando entradas y restando salidas.
  2. Crea el registro `ArqueoCaja` calculando la diferencia.
  3. Si existe discrepancia, opcionalmente registra un movimiento correctivo por concepto `AJUSTE_ARQUEO`.
  4. Despacha `ArqueoRealizado`.

### D. `CerrarCajaUseCase`
* **Responsabilidad:** Finaliza la jornada de un terminal y bloquea operaciones.
* **Lógica clave:**
  1. Recupera la sesión activa.
  2. Ejecuta un arqueo final de cierre con el efectivo real reportado.
  3. Cambia el estado del agregado a `CERRADA`.
  4. Guarda y despacha `CajaCerrada` en bloque transaccional.

---

# 5. Eventos de Dominio y Propósito

* **`CajaAbierta`**: Notifica al sistema el inicio del turno operativo.
* **`MovimientoCajaRegistrado`**: Propaga flujos financieros para auditoría en tiempo real.
* **`ArqueoRealizado`**: Reporta resultados de auditorías físicas.
* **`CajaCerrada`**: Notifica el cierre e inactividad de la terminal para fines contables y de reportes.

---

# 6. Desacoplamiento de Bounded Contexts y Reglas de Comunicación

### Comunicación Permitida
* **Consumo de Eventos de Terceros**: Registra event handlers que reaccionan a:
  * `VentaConfirmada` (Ventas) $\rightarrow$ Registra un movimiento de ingreso por cobro de contado.
  * `VentaAnulada` (Ventas) $\rightarrow$ Registra un movimiento de egreso por devolución en efectivo.
  * `AbonoRegistrado` (Créditos) $\rightarrow$ Registra un movimiento de ingreso por abono.
* **Consumo Síncrono a nivel de Aplicación**: Los servicios de Ventas o Créditos pueden interrogar al puerto de Caja para verificar si el usuario tiene una sesión activa abierta antes de habilitar el botón de cobro en UI/API.

### Comunicación Prohibida
* **Caja no lee base de datos de Ventas o Compras**: No lee facturas ni órdenes directamente.
* **Caja no tiene dependencias de clases o repositorios externos**: Los cobros se enlazan exclusivamente por identificadores lógicos (`origin_document_id`) y el enum `ConceptoMovimientoCaja`, garantizando aislamiento absoluto.

---

# 7. Estrategia Transaccional (Unit of Work)

El módulo de Caja implementa el patrón transaccional del proyecto:

1. **Repository sin Commit**: La implementación `CajaRepositoryImpl` no llamará a `db.commit()` en sus métodos de almacenamiento. Realizará `self.db.add(...)` y `self.db.flush()`.
2. **Coordinación de Transacción en Use Case**: El commit es responsabilidad única de la capa de aplicación. Cuando un caso de uso inicia, abre un bloque transaccional:
   ```python
   try:
       with self.db.begin_nested():
           self.repository.save(caja)
           self.event_dispatcher.dispatch(event)
       self.db.commit()
   except Exception as e:
       self.db.rollback()
       raise e
   ```

---

# 8. Estrategia Offline-First para Caja

Para garantizar la fiabilidad del dinero en el SQLite local sin internet:

1. **Estado persistido transaccionalmente**: El SQLite del cliente almacena el estado de la sesión (`ABIERTA`). Si la terminal se apaga bruscamente, al reconectar se lee el estado actual del SQLite y el cajero continúa sin interrupciones.
2. **Sincronización Cronológica**: Los arqueos y movimientos offline se graban con la marca de tiempo local del cliente, subiéndose secuencialmente en el orden real en que ocurrieron los hechos.
3. **Consistencia Cierre-Apertura**: El SQLite local no permite abrir un nuevo turno si el turno anterior en el dispositivo no se ha cerrado formalmente con su correspondiente arqueo local.

---

# 9. Declaración de Confirmaciones de Consistencia Funcional

Se ratifican los siguientes compromisos de consistencia:
* **MovimientoCaja** representa estrictamente el **único hecho histórico** del contexto que altera los saldos lógicos.
* **El saldo esperado** en el sistema es un **valor derivado** de la sumatoria acumulativa de los movimientos.
* **Ningún usuario ni proceso** del sistema puede editar directamente el saldo acumulado de una caja.
* **Una caja en estado CERRADA** es completamente **inmutable** y bloquea lógicamente cualquier escritura adicional.
