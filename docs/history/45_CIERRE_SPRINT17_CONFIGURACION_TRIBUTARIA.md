# 45_CIERRE_SPRINT17_CONFIGURACION_TRIBUTARIA.md

**Versión:** 1.0  
**Estado:** 📜 Aprobado e Inmutable  
**Última actualización:** 2026-07-24  
**Documento:** Acta de Cierre del Sprint 17 (Configuración Tributaria)  

---

# 1. Objetivo del Sprint

El Sprint 17 tuvo como finalidad modelar, diseñar e implementar el módulo de **Configuración Tributaria (Tributación)** en el backend de CajaFácil. El objetivo del negocio era proveer un mecanismo flexible y modular que permita a las empresas escalar desde operaciones exentas de impuestos (como pequeños comercios o monotributos) hasta regímenes gravados generales o especiales, sin requerir reescrituras de código ni alterar las bases de datos de otros contextos ante futuras reformas fiscales.

---

# 2. Alcance Implementado

Se cumplió al 100% el alcance planificado para las cuatro fases del ciclo de vida del Sprint:
1. **Análisis Funcional:** Delimitación de responsabilidades y segregación de propiedad.
2. **Diseño del Dominio:** Agregado `ConfiguracionTributaria`, entidad `TasaImpuesto`, y el servicio de dominio `MotorTributario` con el Value Object `DesgloseImpuesto`.
3. **Diseño Arquitectónico:** Especificación de puertos (`TaxConfigurationLookup`) y snapshots transaccionales.
4. **Implementación y Pruebas:** Módulo estructurado, routers API, persistencia SQLAlchemy e integración con pruebas unitarias y de integración transaccional (rollback).

---

# 3. Resumen del Análisis Funcional

* **Problema Resuelto:** Rigidez tributaria para pequeños comercios y riesgos de recálculo retroactivo en facturas históricas ante reformas fiscales.
* **Propiedad de la Información:** El módulo pertenece a la **Empresa (Company)**, debido a su impacto multimodular (afecta a Ventas, Compras y Reportes).
* **Aislamiento Impositivo:** Los módulos de **Inventario** y **Caja** permanecen desacoplados y desconocen las tasas impositivas.

---

# 4. Resumen del Diseño del Dominio

* **Aggregate Root:** `ConfiguracionTributaria` (políticas fiscales fechadas de la empresa).
* **Entidades Internas:** `TasaImpuesto` (porcentajes y códigos, ej: `IVA_GENERAL`).
* **Value Objects:** `Porcentaje`, `TipoCalculoImpuesto` (Incluido/Adicionado) y `DesgloseImpuesto` (snapshot de impuestos para transacciones).
* **Invariantes:** Exclusividad de vigencia temporal por empresa, inmutabilidad de versiones históricas ya expiradas, tasas no negativas y códigos únicos de tasa por versión.
* **Motor Tributario (`MotorTributario`):** Modelado como un **Servicio de Dominio (Domain Service)** stateless que calcula el desglose impositivo cruzando precios de ítems y clasificaciones de productos.

---

# 5. Resumen del Diseño Arquitectónico

* **Integración Desacoplada (Ports):** Ventas y Compras interactúan mediante la interfaz de puerto `TaxConfigurationLookup` para resolver la configuración tributaria activa del tenant de forma síncrona.
* **Snapshots Transaccionales:** Las ventas y compras persisten la lista de Value Objects `DesgloseImpuesto` en sus propias tablas como una copia física inmutable.
* **Estrategia Offline-First:** Las tasas se sincronizan de la nube al terminal local en SQLite como solo lectura. El POS offline ejecuta el `MotorTributario` localmente en SQLite, calculando impuestos al instante sin internet.

---

# 6. Resumen de la Implementación

* **Domain:** `ConfiguracionTributaria`, `TasaImpuesto`, `DesgloseImpuesto`, `MotorTributario` y excepciones en `backend/app/modules/tributacion/domain/`.
* **Application:** Use cases `CrearConfiguracionTributaria`, `ActivarConfiguracionTributaria`, `ObtenerConfiguracionActiva` y `CalcularImpuestoTransaccion`.
* **Data:** Tablas relacionales `configuracion_tributaria` y `tasa_impuesto` mapeadas mediante `tributacion_mapper`. Repositorio con flush sin autocommit.
* **Presentation:** Rutas REST FastAPI bajo `/api/v1/taxes/` con validación de DTOs.

---

# 7. Integraciones Realizadas con otros Módulos

* **Empresa (Company):** Aislamiento multi-tenant por `company_id`.
* **Productos (Product):** Consumo del Value Object `CategoriaTributariaProducto` en la ficha de producto de catálogo.
* **Ventas (Sales) y Compras (Purchase):** Integración mediante el puerto de lectura `TaxConfigurationLookup` y el almacenamiento del Value Object `DesgloseImpuesto` en sus bases de datos locales.

---

# 8. Pruebas Ejecutadas y Resultados

Se incorporó una suite de 6 pruebas unitarias e integración en [test_tributacion_use_cases.py](file:///c:/Users/User/Desktop/CajaFacil/backend/tests/test_tributacion_use_cases.py):
* **Invariantes:** Bloqueos ante porcentajes negativos, duplicados de código impositivo y tipo de cálculo inválido.
* **Cálculos del Motor:** Verificación matemática de desgloses de impuestos adicionados e incluidos, y fallback de tasa 0% para monotributos.
* **Consistencia Transaccional (UoW):** Verificación de que fallos de dispatching en event listeners provocan el rollback íntegro en SQLite en memoria.
* **Resultados:** 44 pruebas de la suite de CajaFácil ejecutadas con 100% de éxito (0 fallos).

---

# 9. Riesgos Identificados para Futuras Versiones

* **Riesgo 1: Reformas Retroactivas Complejas:** Modificaciones legales que afecten a productos ya facturados.
  * *Mitigación:* Se previene gracias a que la transacción almacena un snapshot inmutable plano (`DesgloseImpuesto`) inmune a cambios del catálogo.
* **Riesgo 2: Concurrencia de Activación:** Modificación y activación simultánea de políticas en múltiples terminales offline.
  * *Mitigación:* Forzar que la activación de configuraciones se efectúe estrictamente desde el servidor central de administración.

---

# 10. Decisiones Arquitectónicas Importantes Adoptadas

* **Motor Tributario como Domain Service:** Aísla el cálculo impositivo matemático de los agregados `Venta` y `ConfiguracionTributaria`.
* **DesgloseImpuesto como Value Object Snapshot:** Impide los `JOINs` hacia las tablas de impuestos en consultas históricas y blinda la inmutabilidad de facturas del pasado.

---

# 11. Beneficios Obtenidos para CajaFácil

* **Escalabilidad del Negocio:** Acompaña al pequeño comercio desde la exención hasta regímenes complejos sin migración de software.
* **Seguridad SaaS:** Catálogos de productos compartidos pero con impuestos calculados según la localización o régimen de cada tenant.
* **Mantenibilidad:** Reformas fiscales aplicadas administrativamente sin alterar código de checkout.

---

# 12. Estado Final del Sprint y Lecciones Aprendidas

* **Estado:** ✅ CONCLUIDO Y CERRADO.
* **Lecciones Aprendidas:**
  * Separar la naturaleza impositiva del producto (Clasificación) de la tasa impositiva de la empresa (Configuración) evita la necesidad de editar miles de productos en el catálogo ante reformas tributarias, simplificando el mantenimiento del POS.
  * La consistencia de hechos históricos se simplifica radicalmente almacenando snapshots planos de cálculos derivados en la base de datos local en vez de dependencias lógicas complejas.
