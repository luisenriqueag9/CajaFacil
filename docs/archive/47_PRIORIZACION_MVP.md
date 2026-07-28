# 47_PRIORIZACION_MVP.md

**Versión:** 1.1  
**Estado:** 📜 Aprobado e Inmutable (Sprint 18)  
**Última actualización:** 2026-07-24  
**Documento:** Priorización de Funcionalidades para el MVP Comercial  

---

# 1. Metodología de Priorización

Para establecer la hoja de ruta del MVP comercial de CajaFácil, cada funcionalidad se evalúa bajo los criterios de **Impacto Operativo**, **Riesgo Fiscal/Legal**, **Complejidad Técnica** y **Dependencias**, clasificándolas en cuatro niveles de prioridad:
* **Crítica para el MVP:** Bloquea el lanzamiento comercial básico. Sin ella, el sistema no es operable en un comercio real.
* **Condicionalmente Crítica:** Obligatoria si el comercio requiere facturar legalmente, vender a crédito o registrar clientes nominales, pero no para cobros rápidos anónimos de mostrador.
* **Importante para la Primera Versión (v1.0):** Agrega alto valor competitivo y facilita la adopción inicial del usuario.
* **Diferible (v1.5):** Puede esperar de 3 a 6 meses después del lanzamiento.
* **Largo Plazo (v2.0):** Lógica avanzada o escalabilidad corporativa.

---

# 2. Matriz de Evaluación de Funcionalidades

---

### A. Existencias Acumuladas (CQRS de Lectura / Caché de Stock)
* **Problema que resuelve:** Límite técnico de velocidad. Actualmente, calcular existencias recorre y suma todos los movimientos del Kardex en tiempo real. Con miles de registros, la latencia colapsaría el POS offline.
* **Impacto operativo:** Alto. Determina la velocidad del checkout y previene bloqueos por stock insuficiente en mostrador.
* **Riesgo de no implementarla:** Degradación progresiva del sistema hasta quedar inoperable.
* **Complejidad estimada:** Media. Requiere implementar proyecciones de lectura mediante event handlers que actualicen síncronamente una tabla de saldo disponible.
* **Dependencias:** Módulo de Inventario.
* **Prioridad:** **Crítica para el MVP (Máxima Prioridad Técnica)**

---

### B. Módulo de Impresión
* **Problema que resuelve:** Necesidad de salida física de documentos. El terminal offline POS requiere emitir tickets de venta, reportes de corte de caja de turnos, recibos de arqueos de control, etiquetas de código de barras para estanterías y futuros documentos tributarios.
* **Impacto operativo:** Alto. Agiliza la atención al comprador y formaliza el control interno del supervisor.
* **Riesgo de no implementarla:** Abandono del sistema por lentitud de flujos manuales de facturación.
* **Complejidad estimada:** Media (requiere soporte local para comandos de impresión ESC/POS).
* **Dependencias:** Ventas y Caja.
* **Prioridad:** **Crítica para el MVP**

---

### C. Usuarios y Permisos de Seguridad
* **Problema que resuelve:** Vulnerabilidad a fraudes internos en mostrador. Regula que los cajeros no posean privilegios ilimitados para anular ventas ya cobradas, autorizar arqueos con faltantes de caja, aplicar descuentos discrecionales fuera de política o cambiar precios de venta sin la verificación de un supervisor.
* **Impacto operativo:** Alto. Brinda certeza financiera al dueño de la empresa sobre las operaciones del cajero.
* **Riesgo de no implementarla:** Pérdidas de efectivo descontroladas por anulaciones fraudulentas en mostrador.
* **Complejidad estimada:** Media.
* **Dependencias:** Empresa (Company), Caja y Ventas.
* **Prioridad:** **Crítica para el MVP**

---

### D. Asistente de Configuración Inicial (Wizard de Primer Inicio)
* **Problema que resuelve:** Barrera de adopción y onboarding del usuario. Guía paso a paso al dueño del negocio en su primera ejecución del sistema para crear de forma integrada la empresa, su usuario administrador, la caja física inicial, la configuración tributaria base y la carga de catálogos iniciales.
* **Impacto operativo:** Alto. Asegura que el sistema inicie en un estado operativo consistente y listo para facturar.
* **Riesgo de no implementarla:** Abandono del software debido a errores del usuario durante la configuración manual de dependencias cruzadas.
* **Complejidad estimada:** Baja-Media.
* **Dependencias:** Empresa, Tributación, Caja y Producto.
* **Prioridad:** **Crítica para el MVP**

---

### E. Cortes de Caja X y Z (Cierre de Turno)
* **Problema que resuelve:** Opacidad en el cuadre diario. El supervisor no puede conciliar el efectivo recaudado del cajón ni certificar las discrepancias al final del día sin un resumen formal.
* **Impacto operativo:** Alto. Instrumenta la auditoría de mostrador y previene robos.
* **Riesgo de no implementarla:** Pérdida de control del efectivo en el local.
* **Complejidad estimada:** Baja. Requiere reportes planos de sumatorias agrupadas de la sesión de caja.
* **Dependencias:** Caja (Cash).
* **Prioridad:** **Crítica para el MVP**

---

### F. Clientes Básicos (Directorio y Facturación)
* **Problema que resuelve:** Incapacidad de realizar transacciones nominativas y control de saldos a plazos.
* **Impacto operativo:** Medio-Alto. Obligatoria para emitir facturas legales con RUC/RTN y control de abonos de crédito.
* **Riesgo de no implementarla:** Pérdida de ventas a clientes corporativos.
* **Justificación de Clasificación:** Para una pulpería o negocio pequeño de cobro anónimo rápido en efectivo, no es requerida para iniciar, pero sí para comercios con cuenta corriente o créditos.
* **Dependencias:** Ventas y Crédito.
* **Prioridad:** **Condicionalmente Crítica**

---

### G. Reportes Administrativos Básicos (Ganancias, Margen y Kardex)
* **Problema que resuelve:** Falta de visibilidad para el dueño. El comerciante no sabe qué productos se venden más, cuál es su margen de ganancia real ni la rentabilidad mensual.
* **Impacto operativo:** Medio-Alto.
* **Riesgo de no implementarla:** El sistema se reduce a una registradora de mostrador sin valor de gestión comercial.
* **Complejidad estimada:** Baja-Media.
* **Dependencias:** Ventas, Compras e Inventario.
* **Prioridad:** **Importante para la primera versión**

---

### H. Respaldos y Restauración de Base de Datos Local
* **Problema que resuelve:** Pérdida definitiva de datos locales por daños en el disco duro o robo de la terminal offline del local.
* **Impacto operativo:** Bajo a nivel de mostrador, pero alto para seguridad de continuidad.
* **Riesgo de no implementarla:** Pérdida de historial de meses de operación.
* **Complejidad estimada:** Baja (copias de seguridad del archivo SQLite local).
* **Dependencias:** Base de datos común.
* **Prioridad:** **Importante para la primera versión**

---

### I. Facturación Electrónica Oficial
* **Problema que resuelve:** Cumplimiento tributario en países donde la factura electrónica en la nube es obligatoria por ley para todos los comercios.
* **Impacto operativo:** Medio.
* **Riesgo de no implementarla:** El comercio no puede operar legalmente en ciertos regímenes o países de alta regulación fiscal.
* **Complejidad estimada:** Alta (integraciones con firma digital, XMLs específicos del gobierno y servidores de validación).
* **Dependencias:** Tributación (Taxes) y Ventas.
* **Prioridad:** **Diferible (v1.5)**

---

### J. Crédito Avanzado (Cobradores y Gestión de Cuotas)
* **Problema que resuelve:** Falta de control sobre la cartera de créditos. No hay herramientas para que cobradores visiten clientes, generen estados de cuenta con intereses o gestionen cuotas semanales/mensuales.
* **Impacto operativo:** Medio.
* **Riesgo de no implementarla:** Alta tasa de impagos en ventas a plazos.
* **Complejidad estimada:** Alta.
* **Dependencias:** Clientes y Ventas.
* **Prioridad:** **Diferible (v1.5)**

---

### K. Soporte Multibodega (Transferencias de Inventario)
* **Problema que resuelve:** Imposibilidad de distribuir inventario si la empresa cuenta con múltiples almacenes físicos, bodegas de distribución o sucursales que se transfieren mercadería entre sí.
* **Impacto operativo:** Medio-Bajo en el lanzamiento inicial.
* **Riesgo de no implementarla:** Incapacidad de vender a cadenas de tiendas medianas.
* **Complejidad estimada:** Alta.
* **Dependencias:** Inventario.
* **Prioridad:** **Largo Plazo (v2.0)**

---

# 3. Hoja de Ruta Propuesta (Roadmap MVP)

```text
       Sprints 19-20 (Crítico MVP)                 Sprints 21-22 (v1.0 Importante)
 ┌───────────────────────────────────────┐   ┌────────────────────────────────────────┐
 │ * CQRS Caché de Stock (Máxima Prior.) │   │ * Clientes Básicos (Nominal/Crédito)   │
 │ * Módulo de Impresión (ESC/POS)       │──►│ * Reportes Margen/Ganancia             │
 │ * Usuarios, Permisos y Autorizaciones │   │ * Copias de Seguridad SQLite            │
 │ * Wizard de Configuración Inicial     │   │ * Ajustes finales UI                   │
 └───────────────────────────────────────┘   └────────────────────────────────────────┘
```
