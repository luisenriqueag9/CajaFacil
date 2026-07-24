# 46_ANALISIS_FUNCIONAL_FLUJO_OPERATIVO_MVP.md

**Versión:** 1.0  
**Estado:** 📝 En Revisión (Fase 1: Análisis Funcional)  
**Última actualización:** 2026-07-24  
**Documento:** Análisis Funcional del Flujo Operativo Completo (MVP)  

---

# 1. Trazabilidad del Flujo Operativo Completo (Paso a Paso)

Este flujo simula el ciclo de vida operativa completo de una jornada comercial típica en un comercio (ej: ferretería o minisúper) utilizando exclusivamente la lógica de los módulos de CajaFácil ya implementados:

```text
  Configuración          Inventario             Operación Mostrador
 ┌─────────────┐       ┌─────────────┐       ┌──────────────────────┐
 │ 1. Empresa  │       │ 5. Proveedor│       │ 8. Apertura de Caja  │
 │ 2. Impuestos│ ───►  │ 6. Compras  │ ───►  │ 9. Checkout de Venta │
 │ 3. Catálogo │       │ 7. Stock    │       │ 10. Movimiento Caja  │
 └─────────────┘       └─────────────┘       │ 11. Cierre y Arqueo  │
                                             └──────────────────────┘
```

### Paso 1: Inicialización del Comercio (Tenant)
Se da de alta el registro maestro de la `Company` (Empresa), obteniendo un identificador de tenant único `company_id`.

### Paso 2: Gobernación Fiscal (Configuración Tributaria)
Se crea la `ConfiguracionTributaria` activa para la empresa (Régimen General) definiendo el tipo de cálculo (ej: `ADICIONADO`) y las tasas impositivas habilitadas en la región (ej: `IVA_GENERAL` = 15.00%, `IVA_EXENTO` = 0.00%).

### Paso 3: Categorización de Catálogo
Se crean en el catálogo las marcas y las categorías de artículos en el ámbito del tenant para estructurar el inventario.

### Paso 4: Registro de Productos
Se ingresan los productos al catálogo especificando costo, precio de venta, el flag de control de stock (`controls_stock = True`), y asociándolos a su clasificación fiscal intrínseca (`CategoriaTributariaProducto`: `TASA_GENERAL` o `EXENTO`).

### Paso 5: Alta de Proveedores
Se registran los proveedores comerciales en el directorio del sistema con sus datos de contacto.

### Paso 6: Abastecimiento y Compras
Se registra una orden de `Compra` en el sistema detallando proveedor, productos, costos y cantidades adquiridas.

### Paso 7: Entrada de Inventario (Kardex)
Al confirmarse la compra, el sistema reacciona y registra movimientos de `ENTRADA` de inventario por concepto `COMPRA` para cada producto, inicializando el stock lógico disponible.

### Paso 8: Apertura de Caja (Inicio de Turno)
Al iniciar la jornada en el mostrador, el cajero abre la sesión de `Caja` declarando un saldo base (fondo inicial de efectivo para cambio) de $100.00. La sesión cambia a estado `ABIERTA` y genera automáticamente un ingreso por fondo de apertura.

### Paso 9: Venta en Mostrador (Checkout)
Un cliente realiza una compra. El caso de uso de checkout en Ventas realiza las siguientes validaciones y cálculos cruzados:
* Consulta si la caja del cajero está activa y `ABIERTA` (fuerza `RN-502`).
* Valida que exista stock físico disponible en el inventario para evitar saldos negativos (si `allows_negative = False`).
* Resuelve la configuración tributaria de la empresa y ejecuta el `MotorTributario` síncronamente (local en el dispositivo), calculando el desglose de IVA/ISV según las clasificaciones de productos.
* Confirma la venta de contado.

### Paso 10: Cobro y Afectación de Caja
La confirmación de la venta de contado genera de manera atómica un `MovimientoCaja` de tipo `INGRESO` por concepto `VENTA` en el turno activo de la caja, acumulando el efectivo lógico esperado.

### Paso 11: Cierre de Caja y Arqueo (Fin de Turno)
Al finalizar la jornada, el cajero realiza el conteo de efectivo físico del cajón y declara $250.00. El supervisor realiza la auditoría:
* El sistema calcula el efectivo esperado (Fondo de apertura + Ingresos efectivo - Egresos efectivo).
* Registra el `ArqueoCaja` detallando la diferencia (faltante o sobrante).
* Transiciona la caja a estado `CERRADA`, inhabilitando lógicamente cualquier venta adicional bajo ese turno.

---

# 2. Análisis Crítico de Integración y Brechas

### ¿Existe algún paso imposible de realizar con los módulos actuales?
* **Técnicamente no**, todos los pasos del flujo transaccional core son resolubles mediante los casos de uso implementados.
* **Sin embargo, a nivel de negocio**, las ventas y cobros ocurren de forma anónima. Falta el módulo de **Clientes** para asociar transacciones nominativas (necesario para la emisión de crédito y facturación con RUC/RTN nominativa).

### ¿Qué procesos manuales deberían ser automatizados en el MVP?
* **Actualización Automática de Stock ante Ventas:** Actualmente, el registro del movimiento de inventario derivado de una venta recae en la coordinación de la aplicación mediante event handlers locales. Esta reacción síncrona debe ser monitoreada para evitar bloqueos por latencia en el POS offline.
* **Proceso de Sincronización:** La subida de transacciones locales SQLite hacia la nube al recuperar conexión a internet requiere un Worker automatizado en background.

### ¿Qué información es imprescindible para operar un negocio un día completo?
* **Gestión de Roles y Permisos de Usuarios:** El sistema requiere validar que un cajero común no pueda anular ventas o autorizar un arqueo de cierre con faltantes altos sin el ID del supervisor verificado.
* **Impresión de Tickets Físicos:** El POS de mostrador necesita generar un formato plano apto para impresoras térmicas de 58mm u 80mm.

---

# 3. Clasificación de Funcionalidades para el Roadmap

### Funcionalidades Imprescindibles (MVP Comercial)
* **Caché de Existencias (Stock actual):** Reemplazar la sumatoria histórica de movimientos en tiempo real en cada consulta de stock por una tabla de balance acumulado por producto (CQRS de lectura), evitando degradación de rendimiento.
* **Cortes de Caja de Turno (Corte X y Corte Z):** Generación de reportes de cierre de turno legibles para el supervisor.
* **Módulo Mínimo de Clientes:** Para registrar nombre y número de identificación tributaria en la factura.

### Funcionalidades Diferibles (Versiones Posteriores)
* **Facturación Electrónica Oficial:** La integración XML con los entes fiscales nacionales puede esperar; se puede iniciar operando con ticket fiscal local.
* **Transferencias entre Múltiples Almacenes:** El MVP operará con una bodega física única por sucursal.
* **Cuentas por Cobrar (Crédito Completo):** El cobro a plazos con cobradores y límites de crédito avanzados se diferirá a la versión 1.5.

---

# 4. Conclusiones y Mejoras Necesarias

1. **Garantía de Desacoplamiento:** La matriz de integración modular mediante puertos de lectura (lookups) y snapshots transaccionales ha demostrado ser robusta, impidiendo la spaghettización de la base de datos.
2. **Prioridad Inmediata Pre-Lanzamiento:** Optimizar el cálculo de stock derivado implementando el CQRS de lectura. Ejecutar una consulta agregada sobre millones de registros de inventario colapsará los terminales locales en menos de un mes de operación real.
