# 31_DISENO_DOMINIO_CAJA.md

**Versión:** 1.0  
**Estado:** 📝 En Revisión (Fase 2: Diseño del Dominio)  
**Última actualización:** 2026-07-23  
**Documento:** Diseño del Dominio de Caja  

---

# 1. ¿Qué es una Caja dentro del dominio?

En el dominio de CajaFácil, una **Caja** representa una **sesión o turno de operación financiera activa** de un terminal físico de cobro, asignada a un usuario custodio responsable durante una ventana de tiempo específica. Es la entidad encargada de controlar el flujo de dinero, gobernar el estado de autorización de transacciones monetarias y coordinar auditorías físicas.

---

# 2. ¿Cuál es su responsabilidad exclusiva?

La responsabilidad exclusiva de la entidad Caja es:
* **Gobernar el ciclo de vida de cobro en mostrador:** Autorizar ingresos o egresos basándose en el estado operativo (`ABIERTA`/`CERRADA`).
* **Custodiar el balance y flujos de efectivo del terminal:** Ser la única fuente de la verdad para el saldo del dinero físico en el punto de venta.
* **Proteger la inmutabilidad de las auditorías de cuadre:** Registrar arqueos y diferencias de caja de forma inalterable.

---

# 3. ¿Qué conceptos pertenecen realmente al contexto Caja?

Pertenecen estrictamente a este bounded context:
* **Caja (Aggregate Root):** La sesión del turno de caja.
* **MovimientoCaja (Entidad):** Transacción elemental que afecta el saldo lógico (ventas, retiros, gastos).
* **ArqueoCaja (Entidad):** Conciliación física entre el sistema y el dinero real contado.
* **FondoCaja (Value Object):** Importe base de apertura.
* **EstadoCaja (Value Object Enum):** Estados de la sesión (`ABIERTA`, `CERRADA`).
* **MetodoPago (Value Object Enum):** Medios de cobro (`EFECTIVO`, `TARJETA`, `TRANSFERENCIA`, `CREDITO`).

---

# 4. ¿Qué conceptos NO pertenecen al contexto Caja?

Quedan fuera del dominio para evitar acoplamiento:
* **Detalle de productos o inventarios:** La caja desconoce los artículos vendidos, mermas físicas de stock o niveles de almacén.
* **Cálculo de impuestos e IVA:** El cálculo de impuestos se resuelve en Ventas o Compras. Caja solo recibe el total de dinero consolidado a registrar.
* **Identidad comercial del cliente:** Caja solo procesa el cobro; la asignación y límites de crédito son de Clientes y Crédito.

---

# 5. ¿Cuál debe ser el Aggregate Root?

El Aggregate Root es **Caja** (la sesión operativa).
* Toda adición de movimiento de caja o arqueo de auditoría física debe realizarse obligatoriamente a través del agregado `Caja`.
* Esto garantiza que la raíz valide sus invariantes (por ejemplo, validar que el estado de la sesión sea `ABIERTA` antes de permitir registrar un gasto o un cobro).

---

# 6. ¿Qué entidades viven dentro del agregado?

* **`MovimientoCaja` (Entidad interna):**
  * Representa un flujo individual de dinero.
  * Atributos: `Id`, `CajaId`, `Tipo` (Enum: `INGRESO`, `EGRESO`), `Monto`, `MetodoPago`, `Concepto` (venta, gasto, abono, retiro, ajuste), `FechaMovimiento`, `DocumentoOrigenId`.
* **`ArqueoCaja` (Entidad interna):**
  * Detalla una auditoría física de efectivo.
  * Atributos: `Id`, `CajaId`, `EfectivoFisico`, `EfectivoEsperado`, `Diferencia`, `FechaArqueo`, `SupervisorId` (opcional).

---

# 7. ¿Qué Objetos de Valor existen?

* **Monto:** Cantidad decimal no negativa que representa dinero.
* **Diferencia:** Valor decimal (puede ser positivo/sobrante, negativo/faltante, o cero/cuadrado).
* **MetodoPago:** Enum (`EFECTIVO`, `TARJETA`, `TRANSFERENCIA`, `CREDITO`).
* **TipoMovimientoCaja:** Enum (`INGRESO`, `EGRESO`).
* **ConceptoMovimientoCaja:** Enum (`VENTA`, `COMPRA`, `RETIRO`, `GASTO`, `ABONO_CREDITO`, `AJUSTE_ARQUEO`).

---

# 8. Invariantes del Dominio (Reglas Indestructibles)

* **Invariante 1: Balance Derivado inalterable:** El saldo de caja no se edita directamente; es la sumatoria algebraica de sus movimientos.
* **Invariante 2: Validación de Estado Abierto:** Ningún movimiento financiero puede ser registrado si la sesión de caja está en estado `CERRADA`.
* **Invariante 3: Custodia Única Activa:** Un cajero no puede abrir una sesión de caja si ya tiene otra abierta simultáneamente en la misma empresa.
* **Invariante 4: Cierre Definitivo e Inmutable:** Una vez cerrada una caja, se congela su estado. No puede reabrirse ni modificarse su historial.
* **Invariante 5: Positividad del Importe:** Todo movimiento de dinero debe tener un monto estrictamente mayor que cero ($> 0$).
* **Invariante 6: Declaración del Conteo al Cierre:** La transición al estado `CERRADA` exige un arqueo final donde se declare el efectivo físico contado.

---

# 9. Eventos de Dominio de Caja

* **`CajaAbierta`:** Contiene `CajaId`, `CompanyId`, `UserId`, `FondoApertura` y `Fecha`.
* **`MovimientoCajaRegistrado`:** Contiene `MovimientoId`, `CajaId`, `Monto`, `Tipo` y `Concepto`.
* **`ArqueoRealizado`:** Contiene `ArqueoId`, `CajaId`, `EfectivoFisico`, `Diferencia` y `Fecha`.
* **`CajaCerrada`:** Contiene `CajaId`, `CompanyId`, `EfectivoFisico`, `EfectivoEsperado`, `Diferencia` y `Fecha`.

---

# 10. Representación de la Apertura de Caja

La **Apertura de Caja** es la **instanciación del agregado**. Se inicializa con estado `ABIERTA`, guardando fecha, custodio y terminal. Automáticamente, el monto de apertura (base o fondo) genera el primer `MovimientoCaja` de tipo `INGRESO` por concepto `FONDO_APERTURA`.

---

# 11. Representación del Cierre de Caja

El **Cierre de Caja** es una **transición de estado** ejecutada sobre la sesión de caja existente. Requiere:
1. Validar que la caja esté actualmente `ABIERTA`.
2. Registrar un `ArqueoCaja` de cierre con el dinero real contado.
3. Evaluar diferencias (faltante/sobrante) y registrar movimientos correctivos automáticos si el negocio lo requiere.
4. Transicionar a estado `CERRADA`, inhabilitando escrituras.

---

# 12. Representación del MovimientoCaja

Es la transacción inmutable vinculada al agregado `Caja` que detalla el flujo monetario y lo asocia lógicamente al documento que lo detonó (compra, venta, etc.), manteniendo desacoplado el dominio.

---

# 13. Representación del Arqueo de Caja

Es el registro inmutable de auditoría que documenta una conciliación de efectivo física, comparando el monto en sistema versus el dinero real contado.

---

# 14. Relación de Caja con otros Módulos

* **Ventas:** Solicita síncronamente registrar un `INGRESO` por cobro de contado. Caja valida que la sesión del usuario esté `ABIERTA`; si no, rechaza el cobro, abortando la venta.
* **Compras:** Solicita registrar un `EGRESO` por concepto `GASTO` si se compra insumos con efectivo del mostrador.
* **Crédito:** Solicita registrar un `INGRESO` por concepto `ABONO_CREDITO` cuando un cliente paga su saldo.
* **Inventario:** Ninguna relación directa (baja cohesión).

---

# 15. Reglas de Inmutabilidad de Caja Cerrada

* El método `agregar_movimiento()` de `Caja` valida: `if self.estado == EstadoCaja.CERRADA: raise CajaCerradaException()`.
* Las actualizaciones persistentes se restringen lógicamente en la capa de datos una vez la columna `status` es `"CLOSED"`.

---

# 16. Evolución Futura del Modelo (Soporte sin ruptura)

* **Cambio de turno / Cajeros múltiples:** Permitir asociar múltiples cajeros secuencialmente a una sola sesión de terminal.
* **Múltiples Monedas (Multidivisa):** Permitir movimientos expresados en diferentes denominaciones monetarias.
* **Retiros de Seguridad automáticos:** Validar y disparar alarmas si el efectivo disponible en caja supera un tope configurado.
* **Integración con Terminales QR/POS electrónicos:** Validar confirmaciones de cobro de pasarelas de pago de forma integrada en el movimiento.
