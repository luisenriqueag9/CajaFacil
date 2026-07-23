# 30_ANALISIS_FUNCIONAL_CAJA.md

**Versión:** 1.0  
**Estado:** 📝 En Revisión (Fase 1: Análisis Funcional)  
**Última actualización:** 2026-07-23  
**Documento:** Análisis Funcional del Módulo de Caja  

---

# 1. ¿Qué problema del negocio resuelve el módulo Caja?

El módulo de **Caja** atiende las siguientes necesidades operativas del negocio:
* **Descuadres financieros al cierre de jornada:** Identifica diferencias entre el dinero cobrado por el sistema y el dinero físico real que custodia el cajero en el terminal.
* **Fuga de efectivo (robo hormiga):** Lleva control detallado de retiros de efectivo no justificados o faltantes no explicados.
* **Opacidad de transacciones menores:** Registra egresos pequeños realizados directamente desde el mostrador (caja chica) para insumos o entregas.
* **Exceso de efectivo en mostrador:** Facilita la programación de retiros parciales de seguridad, reduciendo el riesgo de pérdidas ante asaltos.
* **Falta de asignación de responsabilidades:** Asegura que cada fondo de dinero tenga un cajero custodio único responsable por los importes operados durante su turno.

---

# 2. ¿Por qué existe Caja dentro de un sistema POS?

En un punto de venta (POS), la facturación y la entrega física de productos están ligadas al flujo del dinero. El software no es solo un emisor de facturas; es el punto de cobro. Caja existe para actuar como el **vínculo de control** entre las ventas lógicas del sistema y la realidad física del efectivo resguardado, controlando las aperturas de turnos, arqueos, mermas de dinero y cierres de caja diarios.

---

# 3. ¿Qué es una Caja desde el punto de vista del negocio?

Desde la perspectiva operativa, la **Caja** no representa el objeto de metal o plástico de la registradora. Representa una **sesión de operación y custodia financiera controlada** (un turno de trabajo) asociada a un cajón físico de dinero, a un cajero custodio autenticado, a un terminal y a una ventana de tiempo específica.

---

# 4. ¿Cuál es la responsabilidad exclusiva del módulo Caja?

La responsabilidad exclusiva del módulo de Caja es:
* **Gobernar el estado de transaccionalidad monetaria:** Validar si un terminal está autorizado para recibir cobros en efectivo (Estado: `ABIERTA`) o si la jornada ha finalizado (Estado: `CERRADA`).
* **Mantener la inmutabilidad de los flujos monetarios:** Garantizar que todo ingreso o egreso de caja sea registrado de forma inalterable.
* **Certificar las auditorías de cuadre (Arqueos):** Documentar las conciliaciones físicas de efectivo declarando discrepancias de forma transparente.

---

# 5. ¿Qué NO pertenece al contexto Caja?

Para mantener límites claros de bounded context:
* **Cálculo de impuestos e IVA:** Caja no sabe ni calcula si una venta lleva 15% de IVA o si el producto tiene descuentos. Solo recibe el importe neto final a cobrar.
* **Fichas de Productos o Inventarios:** Caja no sabe qué productos físicos se entregaron en el mostrador.
* **Cuentas y Datos Maestros de Clientes:** Caja solo procesa el pago; la gestión de cartera de clientes pertenece al contexto de Clientes.
* **Facturación a proveedores:** Caja registra la salida de dinero si se paga a un repartidor en efectivo, pero no gestiona la factura ni los términos de compra.

---

# 6. Diferencias entre Términos del Dominio

* **Caja:** Representa el turno o sesión de operación (Aggregate Root). Tiene un estado (`ABIERTA`, `CERRADA`), un custodio y fecha de operación.
* **MovimientoCaja:** Es la transacción elemental inmutable que aumenta o disminuye el saldo lógico (ej: cobro de venta, pago de gasto, retiro).
* **AperturaCaja:** El proceso de inicio de sesión donde el cajero declara la cantidad de efectivo inicial con la que arranca (fondo de caja o base).
* **CierreCaja:** El proceso formal de culminación de la jornada donde el cajero declara el efectivo físico contado al finalizar.
* **ArqueoCaja:** La auditoría donde se compara el dinero físico real frente al saldo esperado en el sistema para calcular diferencias.

---

# 7. Hechos del Negocio que Generan Movimientos de Caja

* **Cobro de Venta de Contado (`VENTA`):** Ingreso de dinero (efectivo, tarjeta, transferencia) por checkout de venta.
* **Abono de Cliente a Crédito (`ABONO_CREDITO`):** Ingreso de efectivo de un cliente para saldar deudas.
* **Retiro de Seguridad / Depósito (`RETIRO`):** Egreso de fondos para resguardo en caja fuerte.
* **Gasto de Caja Chica (`GASTO`):** Egreso definitivo para pago inmediato de insumos o servicios menores.
* **Ajuste Correctivo (`AJUSTE`):** Ingreso o egreso correctivo para cuadrar la caja tras auditoría.

---

# 8. Reglas para Abrir una Caja

* El cajero debe estar activo y autenticado.
* **Regla de Custodia Única:** Un cajero no puede abrir una caja si ya tiene otra sesión activa (abierta) en la misma empresa.
* Se debe registrar obligatoriamente el saldo base inicial de apertura (monto en efectivo con el que inicia el cajón, incluso si es cero).

---

# 9. Reglas para Cerrar una Caja

* La caja debe estar actualmente en estado `ABIERTA`.
* El usuario debe realizar obligatoriamente un conteo físico de dinero (arqueo) y declarar el monto físico real contado al cierre.
* **Regla de Inmutabilidad al Cierre:** Una vez cerrada la caja, su estado es final e inalterable. No se permiten más ventas, gastos o retiros bajo esa sesión de caja.

---

# 10. Cálculo de Efectivo Esperado al Cierre

El saldo lógico esperado de efectivo al cierre se calcula dinámicamente de la siguiente forma:

$$\text{Efectivo Esperado} = \text{Monto Apertura} + \sum (\text{Ingresos en Efectivo}) - \sum (\text{Salidas/Egresos en Efectivo})$$

Al contrastarlo con el dinero contado físicamente se obtiene la diferencia:

$$\text{Diferencia} = \text{Efectivo Físico} - \text{Efectivo Esperado}$$

* Si $\text{Diferencia} = 0$: Caja cuadrada.
* Si $\text{Diferencia} > 0$: Sobrante de caja (ingreso correctivo).
* Si $\text{Diferencia} < 0$: Faltante de caja (egreso correctivo / descuadre).

---

# 11. Diferencias Operativas de Flujo

* **Venta:** Flujo de ingreso asociado al mostrador de ventas.
* **Ingreso:** Entrada de dinero no asociada a facturación directa (ej. aportación de base extra).
* **Retiro:** Salida física de fondos para transferirlos a custodia externa (el dinero sigue perteneciendo al negocio, no se consume).
* **Gasto:** Salida física de fondos consumidos definitivamente para pagos inmediatos en mostrador.
* **Ajuste de Caja:** Corrección tras arqueo para alinear la verdad lógica con la física.

---

# 12. Concurrencia de Sesiones de Caja Abiertas

* **Por Usuario:** **Prohibido.** Un usuario únicamente puede custodiar una sola caja abierta a la vez.
* **Por Sucursal/Terminal:** **Permitido.** Una sucursal con múltiples computadoras/terminales puede operar con múltiples cajas abiertas de forma concurrente, siempre que cada una esté bajo un usuario cajero diferente.
* **Por Empresa (Tenant):** **Permitido.** El aislamiento multi-tenant garantiza que cada empresa opere sus cajas de forma independiente sin interferencias de red.

---

# 13. Soportabilidad ante Apagones Inesperados (Offline-First)

Si la terminal sufre un corte de energía, al reiniciar la aplicación local en SQLite se evalúa el estado de la sesión activa del usuario. Dado que la base de datos local SQLite es transaccional, el estado se recupera como `ABIERTA` de forma íntegra. El cajero puede continuar vendiendo y cobrando sin requerir conexión a internet, asociando los nuevos movimientos a la misma sesión de caja local activa.

---

# 14. Matriz de Interacciones de Caja

* **Ventas:** Solicita síncronamente registrar un cobro de contado. Caja valida si su sesión está `ABIERTA`; si no, rechaza la transacción de venta.
* **Compras:** Solicita un egreso de caja si una compra menor de insumos es pagada en efectivo en mostrador.
* **Crédito:** Solicita registrar un movimiento de ingreso cuando un cliente realiza un abono en efectivo.
* **Empresa:** Delimita el aislamiento multi-tenant del flujo financiero.
* **Inventario:** No interactúa directamente.

---

# 15. Reglas de Negocio Preliminares (RN-500 en adelante)

* **RN-500:** El saldo de caja nunca se modifica directamente.
* **RN-501:** Todo cambio de dinero genera un Movimiento de Caja.
* **RN-502:** Toda caja debe abrirse antes de registrar ventas de contado.
* **RN-503:** Toda caja debe cerrarse mediante un proceso formal de arqueo.
* **RN-504:** Un usuario no puede tener más de una sesión de caja abierta simultáneamente en la misma empresa.
* **RN-505:** Una vez cerrada una caja, su estado es final e inmutable; no se permite registrar nuevos movimientos sobre ella.
* **RN-506:** Todo arqueo de caja debe generar un registro histórico con la diferencia (sobrante o faltante) identificando al supervisor y al cajero.
* **RN-507:** El efectivo esperado al cierre se calcula agregando entradas y restando salidas de efectivo al saldo base de apertura.

---

# 16. Conceptos Candidatos del Dominio

* **Caja (Aggregate Root):** Sesión/turno de caja que encapsula las entidades y reglas de consistencia de la jornada.
* **MovimientoCaja (Entidad interna):** Transacción individual de dinero (monto, tipo de movimiento, método de pago, referencia).
* **ArqueoCaja (Entidad interna):** Detalle de auditoría de arqueo físico.
* **FondoCaja / Monto (Value Object):** Valor decimal no negativo que representa dinero.
* **MetodoPago (Value Object):** EFECTIVO, TARJETA, TRANSFERENCIA (Enum).
* **EstadoCaja (Value Object):** ABIERTA, CERRADA (Enum).
