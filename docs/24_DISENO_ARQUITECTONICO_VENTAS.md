# 24_DISENO_ARQUITECTONICO_VENTAS.md

**Versión:** 1.0  
**Estado:** Listo para Revisión de Arquitectura  
**Última actualización:** 2026-07-23  
**Documento:** Diseño Arquitectónico del Módulo Ventas  

---

# Objetivo

Establecer de forma rigurosa y exhaustiva el **Diseño Arquitectónico** para el módulo de **Ventas** (Sales) en el backend de CajaFácil. Este documento especifica la distribución de capas, el flujo de control, los agregados, los contratos de repositorio, los casos de uso, los eventos y las pautas transaccionales que gobiernan la implementación, respetando estrictamente los principios de **Clean Architecture**, **Domain-Driven Design (DDD)** y la **Arquitectura General del Proyecto**.

---

# 1. Responsabilidades Arquitectónicas por Capa

Siguiendo el estándar de modularidad de CajaFácil definido en [backend/app/modules/company](file:///c:/Users/User/Desktop/CajaFacil/backend/app/modules/company), el módulo de Ventas se estructura en cuatro capas claramente diferenciadas y desacopladas.

```text
backend/app/modules/venta/
├── domain/            <-- Núcleo inmutable. Reglas de negocio puras.
├── application/       <-- Orquestación de casos de uso y lógica de coordinación.
├── infrastructure/    <-- Persistencia (SQLAlchemy), adaptadores y mappers.
└── presentation/      <-- Enrutadores FastAPI, esquemas Pydantic (DTO).
```

### Capa de Dominio (`domain/`)
* **Responsabilidad:** Contiene las definiciones del agregado raíz `Venta`, sus entidades asociadas (`DetalleVenta`), objetos de valor (Value Objects), excepciones lógicas de negocio, enums comerciales y los contratos de repositorio (interfaces).
* **Restricción:** No puede importar frameworks externos (FastAPI, Pydantic) ni herramientas de persistencia (SQLAlchemy). Su código debe ser Python puro e inmutable ante cambios tecnológicos.

### Capa de Aplicación (`application/`)
* **Responsabilidad:** Coordina el flujo de los casos de uso (como `ConfirmarVenta` y `AnularVenta`), gestiona las transacciones lógicas y coordina la ejecución de las invariantes que involucran consultas externas a través de las interfaces de repositorio del dominio.
* **Restricción:** Desconoce la existencia del motor de base de datos (SQLite/PostgreSQL) y de la interfaz HTTP. Se comunica exclusivamente con el dominio y las abstracciones del core.

### Capa de Persistencia e Infraestructura (`infrastructure/`)
* **Responsabilidad:** Implementa el repositorio físico de acceso a datos utilizando SQLAlchemy Core/ORM, define los esquemas de tablas relacionales (modelos ORM) y realiza el mapeo bidireccional entre la entidad pura del dominio y el modelo de base de datos mediante el Mapper.
* **Restricción:** No toma decisiones de negocio por sí sola. Traduce y persiste los comandos que la aplicación le delega.

### Capa de Presentación (`presentation/`)
* **Responsabilidad:** Define los puntos de entrada HTTP (FastAPI Routes), valida la forma y tipos de datos de las peticiones mediante esquemas de validación Pydantic (Request DTOs), expone la API pública (Response DTOs) y resuelve el árbol de dependencias del módulo mediante inyección de dependencias.
* **Restricción:** Ninguna lógica comercial, cálculo tributario o descuento de precios puede residir en esta capa.

---

# 2. Agregados, Entidades y Objetos de Valor

El agregado de Ventas se estructura como un modelo jerárquico cuyo único punto de entrada es la entidad raíz `Venta`.

```text
                        ┌────────────────────────┐
                        │      Venta (AR)        │
                        └──────────┬─────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    ▼                             ▼
         ┌────────────────────┐        ┌────────────────────┐
         │ DetalleVenta (Ent) │        │ FormaPagoAceptada  │ (Value Object)
         └────────────────────┘        └────────────────────┘
```

### Agregado Raíz (Aggregate Root)
* **`Venta`** (Entidad transaccional): Representa el hecho comercial consolidado.
  * **Atributos:**
    * `id: UUID` (IdentificadorVenta)
    * `company_id: UUID` (Tenant)
    * `box_id: UUID` (Caja donde se realiza)
    * `user_id: UUID` (Usuario/Cajero que vende)
    * `client_id: UUID | None` (Cliente receptor; nulo si es Consumidor Final)
    * `invoice_number: str | None` (Número correlativo oficial)
    * `subtotal: Decimal` (Suma de precios unitarios por cantidades antes de descuentos e impuestos)
    * `discount: Decimal` (Total de descuentos aplicados)
    * `tax: Decimal` (Total de impuestos agregados)
    * `total: Decimal` (Importe neto comercial final)
    * `status: EstadoVenta` (Enum: `CONFIRMADA`, `ANULADA`)
    * `created_at: datetime` (Fecha/Hora de confirmación)
    * `updated_at: datetime`
    * `details: list[DetalleVenta]` (Líneas de venta)
    * `payments: list[FormaPagoAceptada]` (Cobertura del importe)

### Entidades Internas
* **`DetalleVenta`** (Entidad interna): Identifica un ítem específico dentro del agregado.
  * **Atributos:**
    * `id: UUID` (Identificador de línea)
    * `product_id: UUID` (Referencia al producto vendido)
    * `quantity: Decimal` (Cantidad vendida)
    * `unit_price: Decimal` (Precio pactado en el instante de la venta)
    * `discount: Decimal` (Descuento específico para esta línea)
    * `tax_rate: Decimal` (Tasa porcentual de impuesto aplicada, ej. `0.15`)
    * `tax_amount: Decimal` (Valor monetario del impuesto para esta línea)
    * `subtotal: Decimal` (Importe parcial sin impuestos/descuentos)
    * `total: Decimal` (Importe total neto de la línea)

### Objetos de Valor (Value Objects)
* **`FormaPagoAceptada`** (Value Object / Entidad interna): Define cómo se cubrió la obligación financiera de la venta.
  * **Atributos:**
    * `payment_method: str` (Enum: `EFECTIVO`, `TARJETA`, `CREDITO`)
    * `amount: Decimal` (Monto cubierto por este medio)
    * `transaction_reference: str | None` (Código de transacción bancaria o ID de crédito si aplica)

---

# 3. Interfaces Públicas y Contrato de Persistencia

El dominio del módulo Ventas publica la interfaz abstracta `VentaRepository` para desvincular el acceso a datos.

```python
from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional
# Nota: La importación utiliza la ruta del paquete lógico del backend.
from app.modules.venta.domain.entities.venta import Venta

class VentaRepository(ABC):
    
    @abstractmethod
    def save(self, venta: Venta) -> Venta:
        """
        Persiste de forma atómica el agregado completo (Venta, detalles y pagos).
        Si la venta ya existe (en caso de anulación), actualiza su estado.
        """
        pass
        
    @abstractmethod
    def get_by_id(self, venta_id: UUID) -> Optional[Venta]:
        """
        Recupera el agregado completo por su UUID.
        Retorna None si no existe en la persistencia.
        """
        pass
        
    @abstractmethod
    def get_by_invoice_number(self, company_id: UUID, invoice_number: str) -> Optional[Venta]:
        """
        Recupera la venta por su número de comprobante/factura en el tenant correspondiente.
        """
        pass
        
    @abstractmethod
    def search(self, company_id: UUID, filters: dict) -> List[Venta]:
        """
        Busca ventas aplicando criterios multi-tenant (rango de fechas, cliente, caja, cajero).
        """
        pass
```

---

# 4. Casos de Uso del Módulo

Se especifican de forma taxativa los casos de uso lógicos de la capa de aplicación, cada uno implementado en su propio archivo físico:

### A) `ConfirmarVentaUseCase` (`confirmar_venta_use_case.py`)
* **Propósito:** Registrar un hecho comercial consumado en el negocio.
* **Flujo lógico:**
  1. Recibe un objeto de entrada `ConfirmarVentaCommand` desde la presentación.
  2. Valida la invariante de Caja Abierta (se verifica que `box_id` esté activo).
  3. Si la venta incluye pagos en `CREDITO`, verifica con el módulo de Crédito que el `client_id` esté identificado y tenga cupo de crédito aprobado.
  4. Valida la consistencia de existencias en catálogo (solo lectura) y construye la entidad de dominio `Venta`.
  5. Invoca a `venta.confirmar()`, lo que dispara internamente la validación de las invariantes del agregado (Invariante de Cantidad Positiva, Invariante de Coherencia de Cobertura Total del Importe, etc.).
  6. Si las invariantes fallan, lanza la excepción de negocio correspondiente (`ImporteIncoherenteException`, `PagoInsuficienteException`).
  7. Inicia una transacción SQLite única a través del coordinador de la Unidad de Trabajo (Unit of Work) en la capa de aplicación.
  8. Persiste el agregado `Venta` llamando a `VentaRepository.save(venta)`.
  9. Instancia y despacha en memoria de forma síncrona el evento de dominio `VentaConfirmada` dentro de la misma transacción local activa.
  10. Los handlers de Inventario, Caja y Crédito capturan el evento síncronamente y aplican sus mutaciones (por ejemplo, registrar salida de mercadería, registrar ingreso de caja o generar deuda al cliente) a través de sus propios repositorios concretos.
  11. Confirma (commit) de forma atómica la transacción de base de datos completa únicamente si todas las persistencias de los repositorios participantes tienen éxito. Si cualquiera de las capas o handlers reporta error, ejecuta rollback.
  12. Retorna la entidad registrada.

### B) `AnularVentaUseCase` (`anular_venta_use_case.py`)
* **Propósito:** Reversar los efectos de una venta confirmada manteniendo su registro inalterado.
* **Flujo lógico:**
  1. Recibe `AnularVentaCommand` con `venta_id`, `user_id` (del supervisor) y la `justificacion`.
  2. Recupera la venta mediante `VentaRepository.get_by_id(venta_id)`. Si no existe, lanza `VentaNoEncontradaException`.
  3. Valida que el estado actual sea `CONFIRMADA`. Si ya está anulada, lanza `VentaYaAnuladaException`.
  4. Valida que el `user_id` provisto posea los permisos necesarios de supervisor.
  5. Ejecuta `venta.anular(supervisor_id, justificacion)`. Esto muta su estado a `ANULADA` y registra los campos de auditoría.
  6. Inicia una transacción SQLite única a través del coordinador de la Unidad de Trabajo.
  7. Persiste el cambio de estado del agregado llamando a `VentaRepository.save(venta)`.
  8. Instancia y despacha en memoria de forma síncrona el evento de dominio `VentaAnulada` dentro de la misma transacción activa.
  9. Los handlers de Inventario, Caja y Crédito capturan el evento y aplican las reversiones correspondientes en sus propios agregados y repositorios.
  10. Confirma (commit) la transacción completa o realiza rollback ante cualquier fallo de persistencia.
  11. Retorna la entidad actualizada.

### C) `ObtenerVentaPorIdUseCase` y `BuscarHistorialVentasUseCase`
* Casos de uso dedicados exclusivamente a la lectura e historial, aplicando obligatoriamente el aislamiento por `company_id`.

---

# 5. Eventos de Dominio

Los eventos representan cambios de estado significativos del negocio y son consumidos por otros contextos para mantener la consistencia eventual. El dominio de Ventas **declara** los siguientes eventos:

### `VentaConfirmada`
* **Definición:** Hecho de que la venta ha sido aceptada y persistida en el sistema.
* **Payload de negocio:**
  * `venta_id: UUID`
  * `company_id: UUID`
  * `box_id: UUID`
  * `client_id: UUID | None`
  * `invoice_number: str | None`
  * `total: Decimal`
  * `items: list[dict]` (donde cada dict contiene: `product_id: UUID`, `quantity: Decimal`, `unit_price: Decimal`)
  * `cash_amount: Decimal` (Monto pagado en efectivo)
  * `credit_amount: Decimal` (Monto asignado a crédito)
  * `timestamp: datetime`

### `VentaAnulada`
* **Definición:** Hecho de que una venta confirmada ha sido reversada comercialmente.
* **Payload de negocio:**
  * `venta_id: UUID`
  * `company_id: UUID`
  * `box_id: UUID`
  * `client_id: UUID | None`
  * `total: Decimal`
  * `items: list[dict]` (para reposición de inventario)
  * `cash_amount: Decimal` (para contra-movimiento de caja)
  * `credit_amount: Decimal` (para reversión de saldo de cuentas por cobrar)
  * `supervisor_id: UUID`
  * `reason: str`
  * `timestamp: datetime`

---

# 6. Dependencias Permitidas e Integración Modular

El módulo de Ventas debe operar de manera independiente, minimizando el acoplamiento con otros Bounded Contexts.

```text
       [ Módulo Catálogo ]  (Solo lectura de catálogo maestro)
               ▲
               │
      ┌────────┴────────┐
      │   Ventas (BC)   │ ──────► [ Event Dispatcher ]
      └────────┬────────┘                      │
               │                               ▼
               │              ┌────────────────┼────────────────┐
               │              ▼                ▼                ▼
               │       [ Inventario ]       [ Caja ]       [ Crédito ]
               ▼
     [ Proceso de Cobro ] (Orquestador transaccional temporal en Aplicación)
```

### Matriz de Acoplamiento Permitida
* **Hacia Catálogo (Product):** Ventas tiene permitido leer el catálogo maestro (`product`) en la capa de Aplicación/Dominio únicamente para verificar la existencia del producto y validar que no esté inactivo (`RN-103`). No puede modificar registros de productos ni stock.
* **Hacia Inventario (Inventory):** Ventas **no conoce** el módulo de Inventario. La reducción de existencias se maneja de manera reactiva: Inventario se suscribe al evento `VentaConfirmada` y registra el correspondiente `MovimientoInventario`.
* **Hacia Caja (Cash Box):** Ventas **no conoce** el módulo de Caja. El registro de ingresos se gestiona de manera reactiva: Caja se suscribe a `VentaConfirmada`, filtra si hay montos en `cash_amount` y crea un `MovimientoCaja`.
* **Hacia Clientes y Crédito (Credit):** Ventas **no conoce** el agregador Crédito. El módulo de Créditos se suscribe a `VentaConfirmada`, filtra si hay montos en `credit_amount` y genera la deuda en la cuenta corriente del cliente.
* **Hacia el Futuro Módulo de Cobro (Payment):** El proceso de cobro se resuelve en la capa de Aplicación antes de invocar el caso de uso `ConfirmarVenta`. El cobro interactúa con pasarelas de pago y valida la transacción física. Una vez resuelto con éxito, le pasa la información de pagos al caso de uso de Ventas.

---

# 7. Reglas de Transaccionalidad

1. **Unidad de Trabajo y Transaccionalidad de Repositorio:** Cada repositorio del sistema persiste estrictamente su propio agregado. `VentaRepository` es responsable únicamente de persistir la entidad raíz `Venta` y sus entidades internas (`DetalleVenta` y `FormaPagoAceptada`). La coordinación transaccional general no se delega a `VentaRepository`.
2. **Consistencia Local e Inter-Módulos (SQLite Local):** La consistencia local síncrona se garantiza a nivel de la capa de Aplicación:
   - El caso de uso (`ConfirmarVentaUseCase` o `AnularVentaUseCase`) inicia y coordina una transacción atómica de base de datos SQLite (Unit of Work).
   - Los eventos de dominio (`VentaConfirmada` / `VentaAnulada`) se despachan síncronamente en memoria dentro del mismo hilo y transacción de base de datos.
   - Los handlers suscritos (Inventario, Caja, Crédito) ejecutan sus respectivas actualizaciones usando sus propios repositorios dedicados y compartiendo la misma sesión/transacción de base de datos abierta.
   - La transacción completa se consolida (`commit`) solo si todos los repositorios y handlers finalizan con éxito. Si ocurre cualquier error o excepción, se ejecuta un `rollback` total.
3. **Consistencia en la Sincronización Nube:** Al sincronizar ventas offline con PostgreSQL en la nube, el proceso es unidireccional y diferido. Las ventas se insertan cronológicamente y los eventos en la nube se ejecutan de manera asíncrona mediante colas de mensajería locales del servidor, asegurando que la latencia de internet no bloquee la operación local.

---

# 8. Riesgos Arquitectónicos y Decisiones Adoptadas

### Riesgo 1: Conflictos de Stock en Sincronización Diferida (Offline)
* **Contexto:** Dos cajeros venden el mismo producto sin internet. El producto tiene existencia de 1. Ambos logran registrar la venta localmente (ya que sus bases de datos SQLite individuales reportan existencia disponible). Al volver la conexión, ambas ventas se sincronizan.
* **Decisión:** **Las ventas inmutables son hechos históricos y prevalecen sin excepciones.** La base de datos en la nube debe registrar ambas ventas. El inventario pasará a tener saldo negativo temporal en la nube (Existencia = -1), y el sistema emitirá una alerta de inconsistencia o "quiebre de stock" para que administración resuelva el desfase mediante una auditoría o un ajuste físico. Nunca se cancela o rechaza una venta histórica confirmada de forma retroactiva durante la sincronización.

### Riesgo 2: Pérdida de Eventos de Consistencia Local por Fallo Crítico
* **Contexto:** Se confirma la venta en SQLite, pero la computadora se apaga justo antes de que el handler local descuente el stock de Inventario o agregue el dinero a Caja.
* **Decisión:** Para garantizar la atomicidad en SQLite local, se utiliza una implementación de **Outbox Pattern** en memoria o una transacción integrada a nivel de base de datos local. El despachador de eventos local procesa la confirmación de la venta y los handlers de inventario y caja dentro del mismo bloque transaccional `BEGIN TRANSACTION` / `COMMIT` del ORM local. Si la actualización de saldo de caja o stock falla, la venta completa se revierte en la base de datos de la estación de trabajo.

### Riesgo 3: Modificaciones de Precios en el Servidor mientras se Opera Offline
* **Contexto:** La oficina central cambia el precio de un artículo de L 100 a L 120 en la nube. Un cajero offline sigue vendiendo el artículo a L 100.
* **Decisión:** La Venta almacena el precio pactado al que se realizó la operación en la estación de trabajo. Al sincronizarse, la base de datos central respeta el precio enviado por la estación de trabajo (L 100). Las reglas de negocio de consistencia e inmutabilidad comercial (`RN-402`) exigen que el precio histórico reportado por la venta sea respetado de forma absoluta en el backend del servidor.

### Riesgo 4: Validación de Límites de Crédito Offline
* **Contexto:** Un cliente tiene un límite de crédito de L 1,000. Realiza una venta a crédito offline por L 800 en una terminal y otra por L 500 en otra terminal.
* **Decisión:** En modo offline, el sistema valida el crédito utilizando la última información sincronizada en la estación local. Durante la sincronización central en la nube, el sistema de cuentas por cobrar aceptará y procesará ambas ventas para no dejar la transacción comercial en el limbo, pero colocará la cuenta corriente del cliente en estado "Sobregirada", bloqueando futuras solicitudes de crédito hasta que se liquide el saldo vencido.
