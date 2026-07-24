# 36_ESTANDARES_TRANSACCIONALES.md

**Versión:** 1.0  
**Estado:** 📜 Aprobado (Sprint 16)  
**Última actualización:** 2026-07-23  
**Documento:** Estándares Transaccionales y de Unidad de Trabajo  

---

# 1. Reglas del Patrón Unit of Work

Para garantizar la atomicidad en CajaFácil (especialmente en transacciones críticas que involucran caja, ventas e inventario bajo consistencia local), se aplica estrictamente el patrón **Unit of Work (UoW)**.

```text
       Capa de Aplicación (Caso de Uso)
     ┌───────────────────────────────────┐
     │ 1. Iniciar db.begin_nested()      │
     │ 2. Ejecutar Repo.save() (flush)   │
     │ 3. Despachar Eventos en memoria   │
     │ 4. Confirmar db.commit()          │
     └───────────────────────────────────┘
```

### Regla 1: El Repositorio NO hace Commit
* Ninguna implementación de repositorio (`*RepositoryImpl`) bajo la capa de datos puede invocar a `self.db.commit()`.
* Su única responsabilidad de escritura es agregar la entidad a la sesión (`self.db.add()`) y forzar la sincronización de IDs con la base de datos (`self.db.flush()`).

### Regla 2: Coordinación Centralizada en la Capa de Aplicación
* La confirmación (`commit`) o reversión (`rollback`) de la transacción es potestad exclusiva del caso de uso en la capa de aplicación.
* Se debe usar `begin_nested()` para soportar transacciones anidadas seguras en SQLite.

---

# 2. Flujo de Ejecución y Orden de Operaciones

Todo caso de uso mutador en la aplicación debe ejecutar las fases en este orden secuencial estricto:

1. **Fase de Validación Preliminar:** Recuperación de entidades y chequeo de invariantes lógicas (ej: validar que la caja esté abierta).
2. **Fase de Mutación:** Modificación del Aggregate Root o agregado de registros en memoria.
3. **Fase de Apertura de Transacción:** Iniciar bloque con `begin_nested()`.
4. **Fase de Persistencia Parcial:** Guardar en repositorio (ejecuta `flush()` internamente).
5. **Fase de Despacho de Eventos:** Lanzar los eventos a los subscriptores locales síncronos. Si un event handler falla, lanzará una excepción que aborta el bloque.
6. **Fase de Confirmación:** Ejecutar `db.commit()`.
7. **Fase de Manejo de Excepciones:** Ante cualquier error en los pasos 3 a 6, se captura, se ejecuta `db.rollback()` y se propaga el error al cliente.

### Ejemplo de Referencia (Homologado):
```python
def execute(self, command: RegistrarMovimientoCommand) -> MovimientoInventario:
    # 1. Validaciones lógicas
    product_details = self.product_lookup.get_details(command.company_id, command.product_id)
    if not product_details.exists:
        raise ProductoNotFoundException(command.product_id)

    # 2. Creación del Agregado
    movimiento = MovimientoInventario(...)

    # 3. Transacción (Unit of Work)
    try:
        with self.db.begin_nested():
            # A. Guardado (solo flush)
            saved_mov = self.repository.save(movimiento)
            
            # B. Dispatching de eventos
            event = InventarioActualizado(
                product_id=saved_mov.product_id,
                new_balance=calculated_balance,
                occurred_at=saved_mov.created_at
            )
            self.event_dispatcher.dispatch(event)
            
        # C. Commit final
        self.db.commit()
        return saved_mov
    except Exception as e:
        self.db.rollback()
        raise e
```

---

# 3. Manejo de Errores y Atomicidad

* Si un oyente de eventos (Event Handler) falla al actualizar un saldo, el bloque transaccional se interrumpe y la base de datos se revierte completamente a su estado previo.
* Esto previene que se registre una venta en el sistema si el cobro en caja no se guardó, o si el movimiento de salida física de inventario falló.
* **Consistencia Offline:** Al correr localmente en SQLite, este comportamiento garantiza que la base de datos local nunca quede corrupta o parcialmente grabada tras fallos repentinos.
