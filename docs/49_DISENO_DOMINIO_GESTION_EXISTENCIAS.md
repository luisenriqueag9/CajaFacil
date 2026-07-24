# 49_DISENO_DOMINIO_GESTION_EXISTENCIAS.md

**Versión:** 1.1  
**Estado:** 📜 Aprobado e Inmutable (Sprint 19)  
**Última actualización:** 2026-07-24  
**Documento:** Diseño del Dominio de la Gestión de Existencias  

---

# 1. Representación Conceptual de la Existencia Disponible

Dentro del dominio de CajaFácil, la Existencia Disponible se representa mediante el concepto de **`ExistenciaProducto`** (o `Existencia`).

Este concepto encapsula:
* La cantidad física y contable (un valor numérico decimal) disponible para uso del negocio.
* La vinculación unívoca al producto y a la empresa (tenant).
* Las reglas operativas que determinan si la cantidad puede seguir disminuyendo.

---

# 2. Clasificación DDD del Concepto: Aggregate Root Operativo

Para garantizar alta cohesión y bajo acoplamiento:
* **`ExistenciaProducto` se modela como un Aggregate Root (Agregado Raíz) independiente** dentro del Bounded Context de Inventario.

### Justificación de su naturaleza como Aggregate Root:
1. **Representación de Estado Derivado:** Conceptualmente, la existencia disponible es un estado derivado resultante del historial cronológico de movimientos (Kardex).
2. **Protección de Invariantes de Negocio:** Aunque sea un dato derivado, se modela formalmente como un Aggregate Root operativo para controlar las invariantes del negocio en tiempo real (por ejemplo, evitar que la cantidad caiga por debajo de cero si el producto no permite sobreventas).
3. **Consistencia Transaccional:** Actúa como el límite transaccional atómico que previene colisiones concurrentes y dobles descargas al actualizar saldos.
4. **Desacoplamiento de Catálogo:** Segrega las modificaciones de stock de alta frecuencia (que ocurren en cada checkout en mostrador) de la ficha estática del producto (`Producto`), evitando bloqueos innecesarios en la base de datos.
5. **No es un mero Value Object:** Posee identidad operativa persistente (llave compuesta de `product_id` + `company_id`) y un ciclo de vida independiente del catálogo de productos.

---

# 3. Propietario del Dato

El propietario exclusivo es el Bounded Context de **Inventario (Inventory)**.
* Cualquier caso de uso que requiera conocer o alterar el stock debe invocar contratos o suscribirse a eventos definidos bajo las reglas de este contexto.

---

# 4. Invariantes del Dominio (Reglas de Consistencia)

El agregado `ExistenciaProducto` gobierna e instrumenta las siguientes invariantes lógicas:
* **Invariante 1: Control de Negativo (No Sobreventa Lícita):**
  * Si la configuración del producto especifica que no se permite stock negativo (`allows_negative = False`), el stock disponible nunca debe caer por debajo de $0.00$.
  * Intentar reducir el stock por debajo de cero en este escenario debe disparar una excepción de dominio (`StockInsuficienteException`).
* **Invariante 2: Aislamiento Multi-Tenant:**
  * Toda `ExistenciaProducto` debe pertenecer a un único `company_id` válido. Es imposible transferir o restar stock entre empresas distintas.
* **Invariante 3: Coherencia Decimal:**
  * Las unidades de stock aceptan decimales si el flag de unidad de medida lo permite (`allows_decimal = True`). En caso contrario, la cantidad a descontar o sumar debe representarse como entero.

---

# 5. Eventos de Dominio que Afectan la Existencia

`ExistenciaProducto` reacciona y se sincroniza a través del consumo de los siguientes eventos:
* **`CompraConfirmada` (Entradas):** Incrementa el stock al confirmarse el arribo de mercancía.
* **`VentaConfirmada` (Salidas):** Disminuye el stock disponible al concretarse el cobro en mostrador.
* **`MermaRegistrada` (Salidas correctivas):** Disminuye el stock por descarte de productos defectuosos.
* **`AjusteInventarioRegistrado` (Nivelación):** Modifica el stock (aumenta o reduce) para alinear la cantidad lógica con el conteo real realizado.
* **`DevolucionClienteConfirmada` (Entradas):** Aumenta el stock al reingresar artículos aptos para la venta.

---

# 6. Responsabilidades Fuera del Dominio

Para evitar sobreingeniería y acoplamiento spaguetti, no pertenecen a este agregado:
* **Precios y Valorizaciones:** El costo de compra y el precio de venta al público pertenecen a `Producto` y `Venta`.
* **Cálculo de Impuestos:** El IVA/ISV corresponde a `Tributación`.
* **Lógica del Turno de Caja:** Las existencias no conocen si hay una caja abierta o cerrada.

---

# 7. Integración Desacoplada con Ventas

La interacción entre el mostrador (Ventas) y las existencias (Inventario) se instrumenta mediante puertos de lectura desacoplados:

```text
  Bounded Context: Ventas                   Bounded Context: Inventario
 ┌───────────────────────┐                 ┌───────────────────────────┐
 │   VentaUseCase        │                 │ ExistenciaProducto (AR)   │
 └───────────┬───────────┘                 └─────────────▲─────────────┘
             │                                           │
             │ (Consulta disponibilidad)                 │ (Escucha y afecta)
             ▼                                           │
 ┌───────────────────────┐                 ┌─────────────┴─────────────┐
 │   StockCheckerPort    ├────────────────►│      InventoryModule      │
 └───────────────────────┘                 └───────────────────────────┘
```

1. **Consulta (Checkout):** Durante la venta, el caso de uso de checkout consulta la interfaz `StockCheckerPort` expuesta por Inventario para certificar si hay suficientes unidades lógicas del producto en el local.
2. **Afectación (Confirmación):** Al finalizar la venta, el módulo publica el evento `VentaConfirmada`. El event handler en Inventario reacciona síncronamente disminuyendo la `ExistenciaProducto` correspondiente.

---

# 8. Consistencia y Flujo Unidireccional con el Kardex

Para estructurar la consistencia entre el saldo rápido (`ExistenciaProducto`) y el historial detallado (`MovimientoInventario`), se adopta la regla del **Flujo Unidireccional de Información**:

```text
       MovimientoInventario  (Bitácora Histórica / Kardex)
                │
                ▼ (Alimenta y actualiza)
       ExistenciaProducto   (Balance de Estado Disponible)
```

### Principios del Flujo Unidireccional:
1. **El Kardex Alimenta la Existencia:** Toda transacción física (compras, ventas, ajustes, mermas) registra en primer lugar un `MovimientoInventario`. A partir de este hecho de Kardex, se actualiza el saldo de `ExistenciaProducto`.
2. **No Retroalimentación:** La `ExistenciaProducto` (saldo rápido) representa únicamente el estado transitorio actual y **nunca se utiliza para reconstruir, modificar o alterar la bitácora histórica del Kardex**.
3. **Escritura Transaccional Atómica (Unit of Work):** Para evitar descuadres, ambos pasos se graban en la misma transacción:
   - El registro del `MovimientoInventario` (Kardex).
   - El incremento o reducción matemática en la `ExistenciaProducto` actual.
