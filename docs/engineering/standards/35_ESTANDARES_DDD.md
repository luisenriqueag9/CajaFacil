# 35_ESTANDARES_DDD.md

**Versión:** 1.0  
**Estado:** 📜 Aprobado (Sprint 16)  
**Última actualización:** 2026-07-23  
**Documento:** Estándares de Diseño Guiado por el Dominio (DDD)  

---

# 1. Glosario de Conceptos de Dominio

En CajaFácil, la lógica del negocio está protegida de la infraestructura mediante la aplicación estricta de patrones de Domain-Driven Design (DDD).

### Aggregate Root (Agregado Raíz)
* **Definición:** Es el punto de entrada principal del dominio para un grupo de objetos asociados (entidades y objetos de valor). La raíz es la única entidad que puede ser consultada y persistida directamente por la infraestructura externa.
* **Cuándo usarlo:** Cuando un concepto del negocio controla y encapsula la consistencia y transaccionalidad de múltiples entidades relacionadas.
* **Ejemplo:** `Venta` es el Aggregate Root que contiene la lista de `DetalleVenta` y `VentaPayment`. `MovimientoInventario` es el Aggregate Root de Inventario.

### Entity (Entidad)
* **Definición:** Objeto que tiene una identidad única sostenida en el tiempo (habitualmente un ID UUID), independientemente de que sus atributos cambien.
* **Cuándo usarlo:** Cuando la identidad del objeto importa para el negocio y debe ser rastreado individualmente.
* **Ejemplo:** `Merma` dentro del agregado `MovimientoInventario`.

### Value Object (Objeto de Valor)
* **Definición:** Objeto inmutable que no posee una identidad propia. Se define exclusivamente por el valor de sus atributos. Dos objetos de valor con idénticos valores son considerados iguales.
* **Cuándo usarlo:** Para medir, describir o cuantificar conceptos del negocio que no requieren trazabilidad individual de identidad.
* **Ejemplo:** `Monto` (Decimal), `MetodoPago` (tarjeta, efectivo).

### Domain Service (Servicio del Dominio)
* **Definición:** Lógica o cálculo de negocio puro que no pertenece de forma natural a una única entidad o agregado, ya que involucra múltiples conceptos o requiere interactuar con varios agregados.
* **Cuándo usarlo:** Únicamente cuando la regla de validación o cálculo excede el alcance de una sola raíz. Debe ser puro (sin acceso a base de datos).

### Domain Event (Evento de Dominio)
* **Definición:** Hecho histórico inmutable que ya ocurrió en el negocio y que es de interés para otros Bounded Contexts.
* **Cuándo usarlo:** Para notificar cambios de estado (aperturas, cierres, registros) y permitir que otros módulos reaccionen asíncronamente o dentro de la misma transacción de forma desacoplada.
* **Ejemplo:** `InventarioActualizado`, `CajaCerrada`.

### Repository (Repositorio)
* **Definición:** Interfaz abstracta (puerto) que declara las operaciones de persistencia del Aggregate Root. Aísla el dominio de los detalles físicos del driver de base de datos (SQLAlchemy, SQLite, etc.).
* **Cuándo usarlo:** Exclusivamente para Aggregate Roots. Las entidades internas no tienen repositorios.

### Bounded Context (Contexto Acotado)
* **Definición:** Límite explícito dentro del cual un modelo de dominio y su lenguaje ubicuo son válidos. Cada módulo de CajaFácil (`venta`, `inventario`, `caja`) es un Bounded Context aislado.

---

# 2. Errores Comunes a Evitar

* **ERROR 1: Modificar entidades internas directamente por fuera de la raíz.**
  * *Consecuencia:* Se rompen las invariantes lógicas.
  * *Solución:* Todo cambio debe ejecutarse llamando a un método en el Aggregate Root (ej. `caja.agregar_movimiento()`).
* **ERROR 2: Crear repositorios para entidades internas.**
  * *Consecuencia:* Acoplamiento físico y pérdida de consistencia transaccional.
  * *Solución:* Persistir y consultar únicamente a través del repositorio de la raíz.
* **ERROR 3: Contaminar el dominio con SQLAlchemy o Pydantic.**
  * *Consecuencia:* El dominio pierde su pureza y portabilidad (imposibilita correrlo offline puro en Flutter o Python embebido sin librerías).
  * *Solución:* Mantener `domain/` estrictamente en Python plano (`@dataclass`).
* **ERROR 4: Acoplar contextos mediante importación de repositorios.**
  * *Consecuencia:* Spaghettización de bases de datos y bloqueos en cascada.
  * *Solución:* Integrar mediante lookups (interfaces de solo lectura) o despachando eventos de dominio.
* **ERROR 5: Almacenar valores derivados mutables como maestros.**
  * *Consecuencia:* Pérdida de trazabilidad de auditoría y descuadres irreparables.
  * *Solución:* El stock de inventario y el saldo de caja deben derivarse históricamente a partir de sumatorias algebraicas de movimientos.
