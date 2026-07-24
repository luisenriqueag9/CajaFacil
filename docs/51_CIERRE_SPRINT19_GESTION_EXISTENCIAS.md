# 51_CIERRE_SPRINT19_GESTION_EXISTENCIAS.md

**Versión:** 1.0  
**Estado:** 📜 Aprobado e Inmutable  
**Última actualización:** 2026-07-24  
**Documento:** Acta de Cierre del Sprint 19 (Gestión de Existencias)  

---

# 1. Objetivo del Sprint

El Sprint 19 tuvo como objetivo modelar, diseñar e implementar el módulo de **Gestión de Existencias (Stock Disponible)** en el backend de CajaFácil. La meta funcional consistió en dotar al sistema de una consulta de existencias de alta velocidad y consistencia transaccional absoluta en el punto de venta (POS) mostrador, protegiendo las invariantes del negocio en escenarios con y sin soporte de inventarios negativos (sobreventa).

---

# 2. Problema del Negocio Resuelto

En sistemas de facturación para comercios minoristas, la lentitud en la consulta de inventarios ralentiza la fila de cobro, provocando pérdida de clientes. Por otro lado, calcular el stock disponible en tiempo real sumando recursivamente todo el historial de movimientos de inventario (Kardex) tiene un costo de consulta exponencial $O(N)$ inviable a escala.

Este sprint resuelve el dilema aplicando una arquitectura de **Proyección Rápida y Co-localizada (CQRS)**:
* **Lecturas a velocidad de memoria $O(1)$**: Disponibilidad comercial de consulta prácticamente instantánea a través de una tabla balance (`ExistenciaProducto`).
* **Consistencia e Invariabilidad**: Escrituras seguras de movimientos de inventario que actualizan el balance rápido bajo una misma transacción relacional relámpago (Unit of Work).

---

# 3. Resumen del Análisis Funcional

* **Física vs. Comercial**: Para el alcance del MVP, la Existencia Física y la Disponibilidad Comercial se consideran equivalentes (sin reservas complejas ni integraciones de e-commerce simultáneas).
* **Propiedad de la Información**: El control de stock y balances rápidos reside en el contexto de **Inventario**, pero interactúa estrechamente con el contexto de **Ventas** durante la facturación.
* **Control de Inventario Negativo**: Configurable a nivel de producto. Si está desactivado, el sistema bloquea transacciones que superen el saldo disponible. Si está activado, permite la venta y registra las existencias negativas para su posterior conciliación física.

---

# 4. Resumen del Diseño del Dominio

* **Aggregate Root**: `ExistenciaProducto` ([existencia.py](file:///c:/Users/User/Desktop/CajaFacil/backend/app/modules/inventario/domain/entities/existencia.py)), responsable de mantener el balance rápido operativo y asegurar la integridad de las existencias.
* **Métodos Clave**:
  * `incrementar(quantity)`: Aumenta el stock.
  * `decrementar(quantity, allows_negative)`: Reduce el stock verificando que no se alcancen valores negativos si la regla del catálogo lo prohíbe, arrojando la excepción `StockInsuficienteException`.
  * `ajustar(physical_quantity)`: Modifica directamente el stock para que coincida con una auditoría o conteo físico.
* **Invariantes**: El balance no puede caer por debajo de cero a menos que `allows_negative` sea verdadero para ese producto específico. Las existencias deben actualizarse atómicamente con los movimientos de Kardex.

---

# 5. Resumen del Diseño Arquitectónico

* **CQRS Transaccional Co-localizado**: Segregación de la escritura (historial detallado de `MovimientoInventario`) y la lectura (balance rápido pre-calculado `ExistenciaProducto`), pero persistiendo ambos de manera atómica bajo una única transacción de base de datos SQLite (Unit of Work).
* **Puerto de Integración Desacoplado**: Definición de la interfaz `StockCheckerPort` ([stock_checker.py](file:///c:/Users/User/Desktop/CajaFacil/backend/app/modules/inventario/application/ports/stock_checker.py)) que permite a Ventas interrogar el stock disponible en mostrador de forma desacoplada de la infraestructura impositiva o de catálogos.
* **Recálculo Excepcional Administrativo**: El caso de uso `RecalcularExistenciaDesdeKardexUseCase` es una utilidad administrativa reservada exclusivamente para auditorías, migraciones, corrección por corrupción física o recuperación ante desastres. No participa en el flujo de facturación.
* **Offline-First**: La actualización local en SQLite es inmediata, garantizando la continuidad operativa en la terminal sin requerir latencia de red.

---

# 6. Resumen de la Implementación

* **Dominio**: Definición del agregado `ExistenciaProducto` y la interfaz del repositorio `ExistenciaRepository` ([existencia_repository.py](file:///c:/Users/User/Desktop/CajaFacil/backend/app/modules/inventario/domain/repositories/existencia_repository.py)).
* **Persistencia**: Mapeador de datos `ExistenciaMapper` ([existencia_mapper.py](file:///c:/Users/User/Desktop/CajaFacil/backend/app/modules/inventario/data/mappers/existencia_mapper.py)) y repositorio relacional SQLAlchemy `ExistenciaRepositoryImpl` ([existencia_repository_impl.py](file:///c:/Users/User/Desktop/CajaFacil/backend/app/modules/inventario/data/repositories/existencia_repository_impl.py)) sin autocommit para flujos unitarios coordinados.
* **Casos de Uso**:
  * `ConsultarExistenciaUseCase` para lecturas directas $O(1)$.
  * `RecalcularExistenciaDesdeKardexUseCase` para auditorías técnicas y restauraciones.
  * Refactorización de `RegistrarMovimientoUseCase`, `RegistrarMermaUseCase` y `RegistrarAjusteUseCase` para consolidar el balance de forma transaccional.
* **Enrutadores y Dependencias**:
  * Registro de `/productos/{product_id}/recalcular` y actualización de `/productos/{product_id}/stock` en `inventario_router.py`.
  * Saneamiento de los archivos `__init__.py` del nivel de paquete eliminando enrutadores circulares.

---

# 7. Integraciones Realizadas

* **Ventas (Sales)**: Integrado indirectamente a través del puerto `StockCheckerPort` y su implementación `StockCheckerImpl` ([stock_checker_impl.py](file:///c:/Users/User/Desktop/CajaFacil/backend/app/modules/inventario/application/ports/stock_checker_impl.py)), logrando un flujo de cobro inmune a acoplamientos rígidos entre módulos.
* **Compañía (Company)**: Aislamiento estricto multi-tenant por `company_id` integrado en consultas y llaves compuestas `UniqueConstraint("company_id", "product_id")` a nivel base de datos.
* **Catálogo de Productos**: Consumo del catálogo mediante `ProductLookup` para verificar dinámicamente si los productos controlan inventario (`controls_stock`) o permiten stock negativo (`allows_negative`).

---

# 8. Riesgos Identificados y Mitigaciones

* **Riesgo 1: Concurrencia Conectada Offline (Sobreventa)**: Terminales desconectadas que venden simultáneamente el último producto en existencia física (donde `allows_negative` es falso).
  * *Mitigación*: El servidor central acepta y procesa ambas facturas (para no rechazar retroactivamente ventas cobradas al cliente), registra el balance en stock negativo temporal, crea una entrada de alerta en `conflict_stock_log` y dispara una notificación urgente al administrador para conciliación manual.
* **Riesgo 2: Inconsistencias de Eventos de Aplicación**: Excepciones lanzadas por escuchadores (listeners) de eventos después de guardar el movimiento de Kardex, dejando el balance y los movimientos históricos desalineados.
  * *Mitigación*: La base relacional y los casos de uso utilizan bloques transaccionales coordinados (`begin_nested()` y `rollback()`). Si falla el disparo o dispatch de cualquier evento, se revierte la transacción relacional de inmediato (garantizando consistencia fuerte).

---

# 9. Resultados Obtenidos

* Balance de existencias disponible a nivel operativo y persistido con respuesta $O(1)$.
* Aislamiento total de los paquetes del módulo que previene la corrupción por importaciones circulares en el backend.
* Casos de uso robustos y mapeadores relacionales totalmente funcionales en SQLite.

---

# 10. Cobertura de Pruebas

Se diseñó e implementó un conjunto específico de pruebas de integración ([test_existencia_integration.py](file:///c:/Users/User/Desktop/CajaFacil/backend/tests/test_existencia_integration.py)) y unitarias ([test_inventario_use_cases.py](file:///c:/Users/User/Desktop/CajaFacil/backend/tests/test_inventario_use_cases.py)), validando:
* Transacciones felices (Entradas/Salidas/Mermas).
* Excepciones de stock insuficiente con reversión de datos.
* Transacciones con existencias negativas permitidas.
* Ajustes físicos correctivos tras inventarios de auditoría.
* Restauración de balances corruptos mediante recálculo masivo de Kardex.
* Verificación desacoplada mediante `StockCheckerPort`.
* **Resultados**: **50 pruebas aprobadas exitosamente (100% de éxito)**.

---

# 11. Beneficios para el Negocio

* **Filas rápidas**: Los cajeros consultan stock disponible instantáneamente, agilizando el checkout y mejorando la satisfacción del cliente.
* **Control de Mermas**: Registro inmediato con justificación técnica (rotura, robo, vencimiento) reduciendo pérdidas invisibles.
* **Flexibilidad Operativa**: Capacidad para operar de forma flexible permitiendo stock negativo en tiendas con reposición continua o forzando rigidez impositiva y de inventario en productos de alto valor impositivo/comercial.

---

# 12. Beneficios Técnicos

* **Consulta Eficiente**: Se elimina el cuello de botella $O(N)$ del cálculo dinámico del Kardex por una lectura indexada $O(1)$ sin comprometer la consistencia física e inmutable del Kardex.
* **Desacoplamiento Limpio**: El POS interactúa con la interfaz de puerto, impidiendo dependencias directas entre capas de dominio de distintos contextos delimitados.
* **Integridad Transaccional**: La integración de la persistencia de existencias bajo la transacción actual de SQLAlchemy garantiza consistencia fuerte sin caídas de red o desalineaciones en base de datos local.

---

# 13. Lecciones Aprendidas

* **Aislamiento de la Inicialización de Paquetes**: Las referencias cruzadas se exacerban si las carpetas raíz del módulo (`__init__.py`) cargan y exportan componentes pesados como enrutadores de presentación de FastAPI. Mantener los archivos `__init__.py` de los módulos limpios de lógica acoplante es crucial en arquitecturas de backend desacopladas.
* **Afinidad de Columnas en SQLite**: Al testear bases de datos relacionales SQLite en memoria, UUIDs numéricos puros (por ejemplo, aquellos formados puramente por dígitos hexadecimales `1` o `2` sin letras como `a-f`) pueden ser convertidos dinámicamente a números decimales (floats) debido a la afinidad de tipos de SQLite, provocando fallas imprevistas. El uso de UUIDs realistas con caracteres alfanuméricos resuelve este comportamiento.

---

# 14. Decisiones Arquitectónicas Relevantes

* **ExistenciaProducto como Aggregate Root Operativo**: Justificado conceptualmente por la velocidad requerida en el POS y para desacoplar transacciones de inventario del catálogo de productos general, protegiendo al mismo tiempo las invariantes operativas.
* **CQRS Co-localizado**: Elección de una estructura híbrida de consulta y escritura compartiendo la misma transacción en disco, alcanzando alta velocidad de lectura sin la latencia e inconsistencia temporal de bases de datos de lectura no relacionales en el MVP.

---

# 15. Estado Final del Módulo

* **Domain**: 100% Implementado y verificado.
* **Application**: 100% Implementado y verificado.
* **Infrastructure**: 100% Implementado y verificado.
* **Presentation**: 100% Enrutadores API actualizados y dependencias inyectadas mediante FastAPI.

---

# 16. Preparación para Futuros Sprints

El diseño conceptual y los modelos de datos de este sprint sientan las bases para las siguientes capacidades planeadas para la hoja de ruta extendida:
* **Disponibilidad Comercial vs. Existencia Física**: Soportará deducciones temporales por mercancías en tránsito, apartados de preventa o carritos de compra e-commerce, restando la disponibilidad sin alterar la existencia física persistida.
* **Estructura Multibodega**: La llave primaria compuesta y el modelo podrán escalarse hacia `(company_id, product_id, warehouse_id)` para soportar múltiples almacenes físicos, transferencias internas y sucursales distribuidas en sprints subsecuentes.
