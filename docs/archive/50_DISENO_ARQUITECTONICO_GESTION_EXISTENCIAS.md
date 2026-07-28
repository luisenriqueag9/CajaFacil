# 50_DISENO_ARQUITECTONICO_GESTION_EXISTENCIAS.md

**Versión:** 1.1  
**Estado:** 📜 Aprobado e Inmutable (Sprint 19)  
**Última actualización:** 2026-07-24  
**Documento:** Diseño Arquitectónico del Módulo de Gestión de Existencias  

---

# 1. Estructura y Responsabilidades por Capa

El dominio de existencias se implementará como una extensión integrada bajo el Bounded Context de **Inventario**, organizando sus componentes en las cuatro capas estándar:

```text
backend/app/modules/inventario/
├── domain/                      # Capa de Dominio (Pureza)
│   ├── entities/                # ExistenciaProducto (AR), MovimientoInventario (AR)
│   ├── exceptions/              # StockInsuficienteException
│   ├── events/                  # ExistenciaModificada, StockCriticoAlcanzado
│   └── repositories/            # ExistenciaRepository (Interfaz)
├── application/                 # Capa de Aplicación (Casos de Uso)
│   ├── use_cases/               # DecrementarStock, IncrementarStock, AjustarStock
│   └── ports/                   # StockCheckerPort (Lookup para Ventas/Compras)
├── data/                        # Capa de Datos (Infraestructura)
│   ├── models.py                # Modelo SQLAlchemy para tabla 'existencia_producto'
│   └── repositories/            # ExistenciaRepositoryImpl
└── presentation/                # Capa de Presentación (Enrutadores y DTOs)
    └── routers/                 # Endpoint de lectura rápida de stock
```

### Responsabilidades por Capa:
* **Domain:** Define las invariantes de negocio de `ExistenciaProducto` y determina si es factible reducir el saldo.
* **Application:** Orquesta el Unit of Work para garantizar atomicidad y expone la interfaz de lectura rápida (`StockCheckerPort`) para otros módulos.
* **Data:** Soportará la persistencia física del balance de existencias por producto, realizando flushes en base de datos.
* **Presentation:** Expone endpoints rápidos para la consulta del stock remanente en mostrador.

---

# 2. Justificación del Patrón Arquitectónico: CQRS Transaccional Co-localizado

Para cumplir con el requisito de que la consulta sea prácticamente inmediata en el punto de venta sin degradar el rendimiento con el crecimiento del Kardex, se adopta el patrón **CQRS Transaccional Co-localizado**:

```text
                        ┌─────────────────────────────────┐
                        │   Caso de Uso (Aplicación)      │
                        └───────────────┬─────────────────┘
                                        │ (Unit of Work)
                       ┌────────────────┴────────────────┐
                       ▼                                 ▼
         [COMMAND - Escritura]                  [QUERY - Lectura Rápida]
       Registrar Movimiento en DB               Actualizar ExistenciaProducto
          (MovimientoInventario)                    (Saldo Acumulado)
```

### Justificación:
* **Segregación:** El `MovimientoInventario` (Kardex) actúa como el modelo de escritura detallado de auditoría. La `ExistenciaProducto` actúa como el modelo de lectura/proyección pre-calculado del saldo neto de existencias.
* **Co-localización y Atomicidad:** Para evitar desalineaciones de stock lógicos, ambos lados (Kardex y Balance) se escriben síncronamente en la misma transacción física relacional.
* **Resultado:** Las consultas de stock de mostrador se ejecutan en complejidad $O(1)$ sobre un simple registro indexado en lugar de realizar agregaciones complejas sobre el historial de movimientos.

---

# 3. Casos de Uso del Módulo

* **`ConsultarExistenciaDisponibleQuery`:**
  * Retorna el saldo neto rápido de `ExistenciaProducto` para un `product_id` y `company_id`.
* **`DecrementarExistenciaUseCase`:**
  * Ejecutado tras una venta. Carga la `ExistenciaProducto`, aplica la invariante de no-sobreventa (`allows_negative`), descuenta y registra el `MovimientoInventario` de salida de forma atómica.
* **`IncrementarExistenciaUseCase`:**
  * Ejecutado tras compras o devoluciones. Carga la `ExistenciaProducto`, incrementa el saldo y registra el `MovimientoInventario` de entrada de forma atómica.
* **`AjustarExistenciaUseCase`:**
  * Corrige el stock lógicos comparándolo con un conteo real. Reemplaza el saldo de `ExistenciaProducto` y calcula la diferencia neta para registrarla en Kardex.
* **`RecalcularExistenciaDesdeKardexUseCase`:**
  * **Mecanismo Excepcional de Recuperación (Fallback):** Caso de uso administrativo que recorre todo el Kardex histórico de un producto para regenerar el saldo en `ExistenciaProducto` si ocurre corrupción de base de datos.
  * **Uso exclusivo:** Se limita únicamente a tareas de mantenimiento, auditoría de cuadre anual, migraciones de versión o recuperación ante desastres. **No forma parte del flujo operativo diario ni normal de las cajas o el mostrador.**

---

# 4. Interfaces (Ports) de Desacoplamiento

El módulo de Inventario expone el siguiente puerto de lectura síncrona para consumo del POS y de Ventas:

```python
from abc import ABC, abstractmethod
from uuid import UUID
from decimal import Decimal
from typing import Optional

class StockCheckerPort(ABC):
    """
    Interface definition (Port) allowing Sales (Checkout) to query 
    product stock availability in a fully decoupled manner.
    """
    @abstractmethod
    def has_sufficient_stock(
        self, 
        company_id: UUID, 
        product_id: UUID, 
        quantity: Decimal
    ) -> bool:
        """
        Verifies if there is enough stock available for a checkout transaction,
        taking into account the allows_negative product rules.
        """
        pass
```

---

# 5. Estrategia Transaccional y Fuentes de Verdad

Para garantizar la consistencia indestructible del stock, se definen los siguientes principios:

### Fuentes de Verdad Oficiales:
* **`MovimientoInventario` (Kardex):** Constituye la **fuente oficial y definitiva de todo el historial** de operaciones. Ningún movimiento físico puede alterarse ni omitirse de este registro inmutable.
* **`ExistenciaProducto` (Balance):** Constituye la **fuente oficial del estado operativo actual** del inventario. Determina si el POS mostrador permite realizar la venta de forma ágil en el presente.

### Consistencia mediante Transacción Única:
Ambas fuentes de verdad deben mantenerse sincronizadas de forma inquebrantable:
1. El repositorio de existencias y el de Kardex **no ejecutan commits automáticos**.
2. Los casos de uso de la aplicación abren una transacción física única relacional (Unit of Work).
3. Se graba secuencialmente el hecho en `MovimientoInventario` y se actualiza matemáticamente `ExistenciaProducto`.
4. Si ocurre cualquier fallo (ej: `StockInsuficienteException` al validar invariantes), la transacción completa ejecuta un `rollback()`, impidiendo descuadres lógicos de stock en la base de datos.

---

# 6. Estrategia Offline-First y Resolución de Conflictos

* **Operación y Lectura Local:** SQLite local en el cliente almacena la tabla física `existencia_producto`. El checkout del POS local offline consulta la tabla local de forma síncrona, descontando el stock disponible transaccionalmente ante cada ticket.
* **Sincronización Unidireccional en Lote:**
  * Al recuperar internet, el POS sube la lista de ventas locales offline.
  * El servidor registra los movimientos históricos en la bitácora central y recalcula la existencia central del tenant.
  * Finalmente, el servidor descarga la tabla maestra de `existencia_producto` actualizada hacia el cliente, sobreescribiendo el saldo local para reflejar compras centrales o ventas de otras cajas concurrentes.

### Resolución de Conflictos ante Sobreventas Offline:
Si dos terminales offline venden de forma concurrente el mismo artículo (que tenía saldo 1 y no permite stock negativo), al reconectarse a la nube se detectará una sobreventa (el balance acumulado del servidor caerá a -1).

**Estrategia de Conciliación:**
1. **No se rechaza la sincronización:** Dado que la transacción de venta física ya ocurrió en el mundo real ante el cliente, la nube **no puede rechazar retrospectivamente las facturas**, puesto que esto generaría inconsistencias contables graves.
2. **Registro de Sobregiro Operativo:** El servidor registra el saldo negativo real temporal en la tabla maestra de `existencia_producto`.
3. **Bitácora de Conflicto:** Se escribe automáticamente un registro en la tabla de auditoría `conflict_stock_log` identificando las terminales involucradas, el producto y la diferencia del descuadre físico.
4. **Alerta Crítica al Administrador:** El sistema dispara una alarma en el panel ERP central para que el administrador proceda a realizar una auditoría manual física (ej: registrar un ajuste de inventario o una entrada correctiva por ingreso omitido).

---

# 7. Riesgos Arquitectónicos y Mitigaciones

* **Riesgo 1: Descuadres Lógicos entre Kardex y Existencia:**
  * *Mitigación:* Se mitiga obligando a que la base de datos contenga un *Foreign Key constraint* o trigger que impida registrar existencias sin un movimiento de Kardex asociado, gobernado por transacciones atómicas a nivel de aplicación.
* **Riesgo 2: Venta Concurrente de la Última Unidad Offline:**
  * *Mitigación:* Mitigado mediante la estrategia de conciliación administrativa descrita en la Sección 6, permitiendo el saldo negativo transitorio en el servidor central sin bloquear los flujos de cobro ya ejecutados.
