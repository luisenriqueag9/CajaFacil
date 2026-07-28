# 01_MASTER_ROADMAP_CAJAFACIL.md

**Versión:** 1.0  
**Estado:** 📜 Aprobado e Inmutable  
**Última actualización:** 2026-07-24  
**Documento:** Tablero Maestro y Roadmap del Proyecto CajaFácil  

---

# 1. Visión del Producto

**CajaFácil** es un sistema de punto de venta (POS) y facturación multiplataforma y SaaS diseñado específicamente para micro, pequeños y medianos comercios minoristas en América Latina. Su visión central es democratizar el acceso a la gestión comercial profesional y el control tributario estricto mediante una solución que no requiera conocimientos técnicos previos, que sea extremadamente rápida y que garantice la continuidad operativa bajo cualquier circunstancia física de conectividad.

---

# 2. Filosofía de CajaFácil

La construcción de CajaFácil se rige por tres pilares inquebrantables:
1. **Offline-First Absoluto**: El mostrador nunca debe detenerse. Toda la lógica de facturación, cálculo impositivo y control de stock se ejecuta de forma local en terminales locales con bases de datos embebidas (SQLite), sincronizándose en segundo plano con la nube de forma asíncrona.
2. **Desacoplamiento Funcional (DDD y Clean Architecture)**: El sistema se divide en contextos delimitados (Bounded Contexts) estrictos. Los módulos interactúan a través de puertos estables (Ports) e interfaces, impidiendo el acoplamiento rígido de bases de datos.
3. **Velocidad de Operación Mostrador**: Prioridad máxima a la latencia de lectura en los puntos de venta. El diseño de cacheo transaccional co-localizado asegura consultas de stock y precios en complejidad de tiempo $O(1)$.

---

# 3. Estado General del Proyecto

* **Fase Actual**: Consolidación del Backend e Inicialización de la Hoja de Ruta del MVP.
* **Salud Técnica**: Excelente. Cobertura de pruebas unitarias e integración relacional del 100% en todos los módulos clave.
* **Hito Reciente**: Aprobación del backend de CajaFácil como la versión oficial **Release Candidate v0.1.0 (RC1)**.

---

# 4. Versionado Actual

* **Backend Core**: `v0.1.0-RC1`
* **Especificación Funcional**: `v1.0.0`
* **Base de Datos**: Schema `v1.0.0` (SQLite y PostgreSQL compatible).

---

# 5. Hitos del Proyecto

```mermaid
gantt
    title Hitos de CajaFácil (Línea de Tiempo Funcional)
    dateFormat  YYYY-MM-DD
    section Backend Core
    Sprints 13-17: Base & Tributación       :done,    h1, 2026-06-01, 2026-07-15
    Sprint 18: Flujo Operativo MVP          :done,    h2, 2026-07-15, 2026-07-20
    Sprint 19: Existencias (Stock Caché)    :done,    h3, 2026-07-20, 2026-07-23
    Sprint 20: Auditoría & RC1              :active,  h4, 2026-07-24, 2026-07-25
    section MVP Ready
    Sprint 21: Ajustes Críticos             :         h5, 2026-07-26, 2026-08-05
    Sprint 22: Módulo de Impresión           :         h6, 2026-08-05, 2026-08-15
    Sprint 23: Onboarding & Usuarios        :         h7, 2026-08-15, 2026-08-30
```

---

# 6. Roadmap Funcional (Foco MVP)

1. **Catálogo de Productos Ampliado** (Sprint 21): Incorporación del flag `allows_negative` en la ficha de producto.
2. **Listado Consolidado de Existencias** (Sprint 21): Vista de inventarios consolidados por tenant para auditoría rápida de stock.
3. **Módulo de Impresión** (Sprint 22): Sustituye a la "Ticketera Térmica". Responsable central de tickets de venta, cortes de caja, etiquetas de precio y reportes impresos.
4. **Usuarios y Permisos Básicos** (Sprint 23): Control de accesos en caja para autorizar anulaciones de facturas, reembolsos y descuentos en el mostrador.
5. **Asistente de Configuración Inicial** (Sprint 23): Wizard de onboarding para configuración ágil de la empresa, sucursales y tasas tributarias en el primer inicio.

---

# 7. Roadmap Técnico

* **CQRS Multi-Almacén (Post-MVP)**: Escalabilidad del modelo de stock caché para soportar llaves primarias `(company_id, product_id, warehouse_id)`.
* **Caché Distribuido en Nube**: Integración de Redis sobre el puerto `StockCheckerPort` para optimizar consultas masivas en el backend central SaaS.
* **Sincronización Bidireccional Asíncrona**: Diseño del motor de sincronización offline-online con resolución automatizada y log de conflictos de stock.

---

# 8. Estado de cada Módulo

| Módulo | Capa Domain | Capa Application | Capa Data/Infra | Capa Presentation | Estado Final |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Company** | 🟢 100% | 🟢 100% | 🟢 100% | 🟢 100% | Estable |
| **Product** | 🟢 100% | 🟢 100% | 🟡 90% | 🟢 100% | Pendiente campo `allows_negative` |
| **Inventario**| 🟢 100% | 🟡 90% | 🟢 100% | 🟡 90% | Pendiente endpoint listado general |
| **Purchase** | 🟢 100% | 🟢 100% | 🟢 100% | 🟢 100% | Estable |
| **Venta** | 🟢 100% | 🟢 100% | 🟢 100% | 🟢 100% | Estable |
| **Caja** | 🟢 100% | 🟢 100% | 🟢 100% | 🟢 100% | Estable |
| **Tributación**| 🟢 100% | 🟢 100% | 🟢 100% | 🟢 100% | Estable (Aprobado Sprint 17) |

---

# 9. Historial de Sprints

* **Sprints 13 - 15 (Núcleo POS)**: Implementación de Ventas básicas, movimientos e histórico de Kardex de inventario y control de caja (apertura, cierres y arqueos).
* **Sprint 16 (Estandarización)**: Definición de directrices de Clean Architecture, DDD, estándares transaccionales y de pruebas SQLite en memoria.
* **Sprint 17 (Tributación)**: Implementación de la configuración tributaria adaptativa y el motor tributario stateless.
* **Sprint 18 (Flujo Operativo MVP)**: Auditoría conceptual de fin a fin de una jornada laboral simulada en un comercio minorista real.
* **Sprint 19 (Gestión de Existencias)**: Implementación del agregado de stock caché `ExistenciaProducto` y del puerto `StockCheckerPort` para desacoplamiento con Ventas.
* **Sprint 20 (Cierre Backend RC1)**: Auditoría transversal de código, saneamiento de inicializadores circulares en subpaquetes y definición del plan de acción para hallazgos de calidad.

---

# 10. Deuda Técnica Aceptada

1. **Aislamiento en Mocks de Test de Ventas**: Las pruebas unitarias de ventas usan mocks para inventario en vez de persistencia relacional real. *Tratamiento: Agendado para refactorización en el Sprint 22.*
2. **SQLite UUID Affinity**: Errores al usar UUIDs formados enteramente por dígitos en SQLite de pruebas. *Tratamiento: Aceptado y mitigado forzando el estándar de UUIDs mixtos en fixtures.*
3. **Caché en Nube Inexistente**: Consulta de existencias rápida golpea directamente la base de datos relacional. *Tratamiento: Aceptado para el MVP local, se corregirá en la fase de escalado SaaS Cloud.*

---

# 11. Riesgos Conocidos

* **Concurrencia Offline (Sobreventa)**: Terminales offline vendiendo el mismo artículo físico al mismo tiempo.
  * *Impacto*: Bajo a nivel operativo (el POS local continúa facturando y cobrando). Medio en el inventario de la nube (genera stock negativo transitorio).
  * *Mitigación*: El servidor central acepta las facturas, genera el log en `conflict_stock_log` y emite una alerta crítica para auditoría física.

---

# 12. Próximos Pasos (Sprint 21)

1. Implementar la migración de base de datos para la columna `allows_negative` en el modelo `Product`.
2. Crear el caso de uso `ListarExistenciasUseCase` para obtener la grilla consolidada de stock rápido en el POS.
3. Actualizar la especificación técnica de pruebas de integración de Inventario y Ventas.

---

# 13. Métricas Generales del Proyecto

* **Total de Pruebas Automatizadas**: 50 pruebas (unitarias e integración).
* **Porcentaje de Aprobación**: 100%.
* **Complejidad de Lectura del Stock Mostrador**: $O(1)$ (Directo desde la proyección rápida indexada).
* **Aislamiento de Regímenes Tributarios**: 100% de desacoplamiento de inventario y caja.

---

# 14. Criterios para Declarar un MVP Comercial

Para congelar la versión comercial del MVP y habilitar el despliegue a producción de las primeras terminales físicas, se deben cumplir obligatoriamente los siguientes criterios:
* **Catálogo Operativo**: Ficha de producto conteniendo control de inventario (`controls_stock`) y política de stock negativo (`allows_negative`) configurables y sincronizados.
* **Punto de Venta Desacoplado**: Checkout de ventas validando el stock disponible instantáneamente a través del puerto `StockCheckerPort`.
* **Módulo de Impresión Integrado**: Impresión física o en PDF de tickets fiscales de venta, cierres de caja (Corte X, Corte Z) y arqueos para auditorías del operador.
* **Control de Apertura y Cierre de Caja**: Flujo operativo cerrado que impida realizar ventas si la caja no cuenta con una apertura física y saldo inicial registrado.
* **Usuarios y Permisos Básicos**: Roles de cajero y administrador definidos para restringir anulaciones o mermas a personal autorizado.

---

# 15. Criterios para Declarar la Versión 1.0 (Escala Cloud/SaaS)

Para el lanzamiento formal de la plataforma SaaS CajaFácil multi-inquilino de alta disponibilidad en la nube, se requiere la consolidación de los siguientes elementos:
* **Sincronización Bidireccional Robusta**: Motor de replicación y sincronización de datos con cola de mensajes offline/online y panel de administración para conciliación de conflictos.
* **Estructura Multibodega**: Soporte nativo para existencias y movimientos segregados por sucursal, almacén y góndola física.
* **Reservas y Layaways**: Diferenciación conceptual y en base de datos entre *Existencia Física* y *Disponibilidad Comercial* para ventas web diferidas, apartados y pedidos futuros.
* **Caché Distribuido de Alto Rendimiento**: Implementación de Redis para interceptar y acelerar las consultas impositivas y de disponibilidad comercial a nivel de inquilino.
* **Seguridad de Nivel Empresarial**: Autenticación OAuth2, control de acceso basado en roles (RBAC) granular e historial completo de auditoría y accesos a la API del backend.
