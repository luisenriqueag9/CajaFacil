# 38_ESTANDARES_DE_PRUEBAS.md

**Versión:** 1.0  
**Estado:** 📜 Aprobado (Sprint 16)  
**Última actualización:** 2026-07-23  
**Documento:** Estándares Oficiales de Pruebas de Calidad  

---

# 1. Organización y Nomenclatura de Pruebas

En CajaFácil, la calidad y estabilidad de la arquitectura modular se garantiza mediante una pirámide de pruebas robusta ejecutada de forma automatizada.

### Ubicación
* Todas las pruebas del backend se ubican en la carpeta `backend/tests/`.
* Nombre del archivo: `snake_case` con prefijo `test_` seguido del nombre del módulo o componente.
  * **Ejemplo:** `backend/tests/test_caja_use_cases.py`

### Nomenclatura de Funciones de Prueba
* Las funciones de test deben comenzar con `test_` seguido de una descripción clara en formato `snake_case` que identifique el escenario y resultado esperado.
  * **Ejemplo:** `test_cerrar_caja_and_block_mutations()`
  * **Ejemplo:** `test_registrar_movimiento_insufficient_stock()`

---

# 2. Qué se debe Probar (Alcance Obligatorio)

Todo nuevo módulo de negocio debe incorporar pruebas automatizadas que verifiquen al menos las siguientes cinco dimensiones:

### A. Invariantes del Dominio
* Probar que el constructor de la entidad o agregado lanza excepciones ante datos inválidos.
* **Ejemplo:** Pasar cantidad negativa al movimiento de inventario debe levantar `CantidadInvalidaException`.

### B. Flujos de Casos de Uso (Happy Path y Alternativos)
* Probar el éxito de la operación llamando al use case con Commands válidos.
* Probar el comportamiento esperado ante excepciones del negocio (ej. denegar ventas si no hay stock).

### C. Despacho de Eventos
* Suscribirse en memoria al dispatcher de eventos en el test y validar que, tras ejecutar el caso de uso, el evento se emite con los datos correctos del payload.

### D. Persistencia y Mapeo en SQLite
* Probar que el mapper traduce correctamente a modelos ORM y que el repositorio inserta y actualiza los registros en base de datos.

### E. Rollback Transaccional (Unit of Work)
* Montar una base de datos en memoria (`sqlite:///:memory:`) con la metadata cargada.
* Forzar una falla (ej. inyectar un error en el despachador de eventos).
* Confirmar mediante una consulta directa al SQLite que la base de datos no persistió ningún cambio (la transacción se revirtió en su totalidad).

---

# 3. Cobertura Mínima y Ejecución

* **Cobertura Funcional Mínima:** 100% de los casos de uso críticos (procesamiento de ventas, cobros, existencias) y 100% de las invariantes lógicas del dominio.
* **Comando de Ejecución:** `python -m pytest` desde el directorio `backend`.
* **Regla de Integración Continua (CI):** Ningún PR puede ser aprobado si existe una sola prueba fallida en la suite.
