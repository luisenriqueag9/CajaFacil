# 29_CIERRE_SPRINT14_INVENTARIO.md

**Versión:** 1.0  
**Estado:** Listo para Commit  
**Última actualización:** 2026-07-23  
**Documento:** Cierre del Sprint 14 (Módulo Inventario)  

---

# 1. Resumen del Sprint 14

El Sprint 14 concluye con la implementación exitosa de la **Fase de Desarrollo y Pruebas** para el módulo de **Inventario (Inventory)** en el backend de CajaFácil. Se cumplieron todos los objetivos del sprint:

* **Dominio Consolidado**: Implementación del agregado `MovimientoInventario`, entidades `Merma` y `AjusteInventario`, Value Objects y excepciones del dominio. El stock se calcula estrictamente como un valor derivado e histórico (Kardex).
* **Consistencia Transaccional (Unit of Work)**: Casos de uso controlando transacciones en bloque y despachando eventos síncronos en memoria. Repositorios de persistencia sin autocommit.
* **Desacoplamiento Completo**: Inventario se integra lógicamente con otros contextos (Ventas, Compras) mediante event dispatching y payloads, eliminando dependencias directas o importaciones cruzadas de código de repositorio.
* **Auditoría e Integridad**: Se resolvió el conflicto de duplicación de metadatos en SQLAlchemy renombrando los modelos de simulación del Sprint 13 en Ventas a `mock_*`. La suite de 31 pruebas del proyecto se ejecuta con 100% de éxito.

---

# 2. Patrones Arquitectónicos Consolidados

Se ratificaron y consolidaron para futuros sprints (como Caja, Clientes y Créditos) los siguientes patrones:
1. **Existencias como Proyección Acumulativa**: No almacenar estados mutables directos para variables derivadas. El stock es siempre el balance neto histórico del agregado `MovimientoInventario`.
2. **Puertos de Integración Catalogados (`*Lookup`)**: Uso de interfaces de consulta de solo lectura para validar catálogos externos sin acoplamiento.
3. **Consistencia Transaccional Local Coordinada por Use Case**: El caso de uso abre la transacción SQLite, guarda el agregado y despacha eventos de forma síncrona en memoria, confirmando (`commit`) o abortando (`rollback`) todo en bloque.
4. **Desacoplamiento de Bounded Contexts por Conceptos del Negocio**: Los agregados solo referencian el origen de la transacción mediante enums abstractos del negocio (`ConceptoMovimiento`) e identificadores lógicos.

---

# 3. Deuda Técnica Identificada

* **Caché de Stock (Proyección de Lectura)**: Actualmente, la obtención del stock de un producto recalcula la suma cronológica de movimientos en cada consulta. Para bases de datos extensas, esto introduce ineficiencia.
  * *Acción futura:* Implementar una tabla de lectura optimizada (`stock_actual` o `existencia_disponible`) que se actualice síncronamente mediante event handlers ante cada movimiento (CQRS).
* **Mocks de Búsqueda Externos**: El módulo de Inventario sigue resolviendo `BoxLookup` y `CreditLookup` mediante mocks que retornan `True`. Deben conectarse cuando esos módulos existan.

---

# 4. Riesgos Futuros y Recomendaciones

### Riesgo 1: Condiciones de Carrera en SQLite en Operaciones Concurrentes
* **Descripción:** SQLite bloquea la base de datos a nivel de archivo durante escrituras concurrentes. Al calcular el stock de forma derivada leyendo movimientos, transacciones simultáneas de venta podrían calcular saldos desactualizados.
* **Recomendación:** Implementar bloqueos optimistas o utilizar base de datos PostgreSQL en el servidor cloud para manejar concurrencia avanzada, manteniendo SQLite estrictamente en el cliente offline.

### Riesgo 2: Sincronización Fuera de Orden (Offline-First)
* **Descripción:** Al operar offline, el orden de recepción de movimientos en el servidor podría diferir de la fecha física real en que ocurrió en el cliente.
* **Recomendación:** Forzar que la consolidación del balance en el servidor reconstruya el Kardex basándose en el campo `created_at` generado por el dispositivo cliente, garantizando la consistencia histórica.

---

# 5. Propuesta de Cierre Git

### Mensaje de Commit
```text
feat(inventory): implement inventory module, transactional unit of work and domain events

- Implement MovimientoInventario aggregate root with Merma and AjusteInventario internal entities
- Implement RegistrarMovimiento, RegistrarMerma, RegistrarAjuste, and ObtenerStockProducto use cases
- Maintain derived stock calculation from in-memory and database movements history (Kardex)
- Enforce negative stock prevention and controls_stock flags via ProductLookup port
- Re-use transaction coordination and repositories without autocommit (Unit of Work)
- Rename temporary database tables in Venta models to mock_* to resolve SQLAlchemy metadata duplication
- Add 6 new integration and rollback tests (all 31 project tests passing)
```

### Descripción de Pull Request (PR)
```markdown
## Descripción
Este PR introduce el módulo de **Inventario** completo para el backend de CajaFácil. La arquitectura se basa en Clean Architecture y DDD, homologando el estándar transaccional del módulo Ventas.

## Cambios Realizados
* **Domain:** Agregado `MovimientoInventario`, entidades `Merma` y `AjusteInventario`, excepciones específicas y eventos de dominio (`InventarioActualizado`, `MermaRegistrada`, `AjusteInventarioRegistrado`).
* **Application:** Casos de uso de registro de movimientos, descarte de mermas y auditoría de ajustes físicos con Unit of Work y dispatcher síncrono.
* **Infrastructure:** Modelos físicos de tablas en SQLAlchemy, Mapper de mapeo bidireccional y repositorio concreto.
* **Presentation:** Router FastAPI, validación sintáctica de DTOs y dependencias.
* **Integración:** Corrección de conflictos de metadatos de SQLAlchemy renombrando tablas de simulación del módulo de Ventas a `mock_*`.
* **Tests:** Suite de 6 pruebas unitarias e integración en SQLite en memoria (`pytest`).

## Deuda Técnica
* Consultas de stock recalculan el historial completo de movimientos. Se recomienda añadir una tabla caché de lectura optimizada en el futuro.
```
