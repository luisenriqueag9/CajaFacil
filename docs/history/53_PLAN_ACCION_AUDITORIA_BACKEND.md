# 53_PLAN_ACCION_AUDITORIA_BACKEND.md

**Versión:** 1.0  
**Estado:** 📜 Aprobado e Inmutable  
**Última actualización:** 2026-07-24  
**Documento:** Plan de Acción y Tratamiento de Hallazgos de Auditoría del Backend  

---

# 1. Introducción

Este documento define la hoja de ruta y el plan de tratamiento oficial para los hallazgos de calidad técnica y de arquitectura identificados en la auditoría transversal del backend del proyecto **CajaFácil** ([52_AUDITORIA_TRANSVERSAL_BACKEND.md](file:///c:/Users/User/Desktop/CajaFacil/docs/52_AUDITORIA_TRANSVERSAL_BACKEND.md)). 

El objetivo es clasificar, priorizar y agendar la resolución de estas observaciones dentro del ciclo de desarrollo de los próximos sprints, garantizando la estabilidad y mantenibilidad de la aplicación sin detener la entrega de valor de negocio del MVP.

---

# 2. Resumen de Clasificación del Plan de Acción

| Identificador | Clasificación del Tratamiento | Prioridad | Sprint Propuesto |
| :--- | :--- | :---: | :---: |
| **H1** | 🚨 Corrección obligatoria antes del MVP | Alta | Sprint 21 |
| **H2** | 📦 Deuda técnica aceptada / Mitigada | Media | Sprint 20 |
| **H3** | 🛠️ Corrección recomendada | Media | Sprint 22 |
| **H4** | 📦 Deuda técnica aceptada | Baja | Sprint 21 |
| **H5** | 🚨 Corrección obligatoria antes del MVP | Alta | Sprint 21 |
| **H6** | 🚀 Mejora futura (Post-MVP) | Baja | Fase Cloud |

---

# 3. Detalle del Plan por Hallazgo

---

### H1: Falta de Campo `allows_negative` en el Modelo de Producto
* **Clasificación**: 🚨 Corrección obligatoria antes del MVP.
* **Prioridad**: Alta.
* **Riesgo**: Medio.
* **Impacto**: Impide habilitar el stock negativo (sobreventa permitida) de forma individual para ciertos productos en la base de datos física, forzando un comportamiento rígido en el POS.
* **Acción Recomendada**:
  1. Diseñar e inyectar la migración de base de datos SQLAlchemy para añadir la columna booleana `allows_negative` en la tabla `product`.
  2. Modificar el DTO de creación/edición de Producto en la capa de presentación.
  3. Modificar el mapeador y el repositorio para sincronizar este atributo en la entidad de dominio.
* **Sprint Sugerido**: Sprint 21.
* **Justificación de la Prioridad**: Permitir o bloquear stock negativo es un requisito de negocio de nivel crítico especificado en el análisis funcional de existencias, esencial para el MVP.

---

### H2: Aislamiento Completo de Inicialización de Paquetes (`__init__.py` vacíos)
* **Clasificación**: 📦 Deuda técnica aceptada (Mitigada en código).
* **Prioridad**: Media.
* **Riesgo**: Bajo.
* **Impacto**: Previene las colisiones por importaciones circulares en el backend al inicializar metadatos.
* **Acción Recomendada**:
  * Formalizar e incorporar una sección específica en el documento [34_ESTANDARES_DE_IMPLEMENTACION.md](file:///c:/Users/User/Desktop/CajaFacil/docs/34_ESTANDARES_DE_IMPLEMENTACION.md) que prohíba estrictamente la importación de capas externas (FastAPI routers, application services) dentro de los archivos `__init__.py` raíces de los módulos.
* **Sprint Sugerido**: Sprint 20 (Cierre actual).
* **Justificación de la Prioridad**: El problema de dependencias circulares ya fue resuelto físicamente en el Sprint 19, pero requiere institucionalizar la regla para evitar regresiones en sprints futuros por parte del equipo de desarrollo.

---

### H3: Acoplamiento de Tablas de Mock en Pruebas de Ventas
* **Clasificación**: 🛠️ Corrección recomendada.
* **Prioridad**: Media.
* **Riesgo**: Medio.
* **Impacto**: Oculta inconsistencias de esquemas reales y FKs relacionales entre el módulo de Ventas y los módulos reales de Inventario y Caja en la base de datos de integración.
* **Acción Recomendada**:
  * Diseñar un conjunto de pruebas de integración de fin a fin (E2E) que reemplace los mocks de base de datos (`MockMovimientoInventarioRepositoryImpl`, `MockMovimientoCajaRepositoryImpl`) en las pruebas de checkout de Ventas, utilizando los repositorios reales vinculados a la base de datos SQLite en memoria.
* **Sprint Sugerido**: Sprint 22.
* **Justificación de la Prioridad**: Permite asegurar la alineación de constraints reales sin interrumpir el desarrollo del catálogo en el sprint inmediato (Sprint 21).

---

### H4: Falta de Validación de UUIDs en SQLite en Memoria (Tipos Numéricos)
* **Clasificación**: 📦 Deuda técnica aceptada.
* **Prioridad**: Baja.
* **Riesgo**: Bajo.
* **Impacto**: Genera errores de conversión a float en tests que utilicen UUIDs con representaciones hexadecimales compuestas enteramente de dígitos numéricos, debido a la afinidad de tipos de SQLite.
* **Acción Recomendada**:
  * Añadir una advertencia técnica en la guía de estándares de pruebas ([38_ESTANDARES_DE_PRUEBAS.md](file:///c:/Users/User/Desktop/CajaFacil/docs/38_ESTANDARES_DE_PRUEBAS.md)) instruyendo el uso mandatorio de `uuid.uuid4()` o cadenas con caracteres alfanuméricos mixtos para prevenir conversiones no deseadas a tipos numéricos en SQLite.
* **Sprint Sugerido**: Sprint 21.
* **Justificación de la Prioridad**: No es un error del sistema de producción (donde PostgreSQL almacena UUIDs de forma nativa) y el comportamiento está completamente contenido controlando las variables de prueba.

---

### H5: Inexistencia de un Endpoint Oficial para el Listado de Existencias
* **Clasificación**: 🚨 Corrección obligatoria antes del MVP.
* **Prioridad**: Alta.
* **Riesgo**: Medio.
* **Impacto**: El operador no puede renderizar eficientemente la grilla consolidada de existencias físicas en el POS o en el panel administrativo centralizado.
* **Acción Recomendada**:
  1. Diseñar el caso de uso `ListarExistenciasUseCase` en el contexto de Inventario.
  2. Implementar el endpoint `GET /api/v1/inventario/existencias` aceptando filtros de paginación e identificador de empresa (`company_id`).
* **Sprint Sugerido**: Sprint 21.
* **Justificación de la Prioridad**: Es indispensable que la interfaz de usuario del mostrador pueda mostrar la lista total de productos y sus stocks de un solo vistazo sin realizar peticiones por separado.

---

### H6: Ausencia de una Capa de Caché en Memoria para Lecturas del POS
* **Clasificación**: 🚀 Mejora futura (Post-MVP).
* **Prioridad**: Baja.
* **Riesgo**: Bajo.
* **Impacto**: Sobrecarga el motor relacional de base de datos central en la nube ante ráfagas de facturación en entornos SaaS concurrentes.
* **Acción Recomendada**:
  * Diseñar un decorador de caché sobre la implementación de `StockCheckerPort` utilizando Redis para almacenar la existencia durante la facturación, invalidando la clave del producto ante cada evento `InventarioActualizado`.
* **Sprint Sugerido**: Fase de Despliegue en la Nube (Post-MVP).
* **Justificación de la Prioridad**: No aporta valor crítico para la instalación local offline en terminales SQLite simples del MVP inicial.

---

# 4. Aprobación y Firma

Este plan de acción queda congelado e inmutable para su posterior tratamiento a partir del inicio del **Sprint 21**.

**Emitido por:**  
*Equipo de Desarrollo del Backend de CajaFácil*

**Aprobado por:**  
*Arquitecto Principal del Proyecto CajaFácil*
