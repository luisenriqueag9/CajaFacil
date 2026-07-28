# ADR-002: CommonSqlAlchemyUnitOfWork centralizado

* **Estado:** Aceptado
* **Fecha:** 2026-07-28
* **Autor:** Principal Software Architect

## Contexto
Cada módulo implementaba su propia infraestructura para la gestión de transacciones con SQLAlchemy (`SqlAlchemyUnitOfWork`).

## Problema
Esta duplicación de código en la capa de persistencia violaba el principio DRY y dificultaba el mantenimiento. Además, provocaba que el manejo de savepoints y transacciones anidadas (`begin_nested()`) fuera inconsistente entre distintos módulos.

## Alternativas Consideradas
1. **Alternativa A**: Mantener implementaciones aisladas de `SqlAlchemyUnitOfWork` por módulo.
2. **Alternativa B (Elegida)**: Normalizar la gestión transaccional extrayéndola del directorio de módulos a un componente de infraestructura común (`CommonSqlAlchemyUnitOfWork` en `app/database/unit_of_work.py`).

## Decisión Tomada
Se eligió la **Alternativa B**. Se centralizó el comportamiento transaccional en `CommonSqlAlchemyUnitOfWork`. Las implementaciones de UoW específicas de cada módulo ahora heredan de este componente común y de sus respectivas interfaces ports de aplicación, eliminando el código duplicado.

## Consecuencias
* **Positivas**:
  * Eliminación total de duplicación física de transacciones.
  * Consistencia garantizada en el manejo de rollback y savepoints.
  * Los casos de uso de la aplicación interactúan exclusivamente con la interfaz port `UnitOfWork` sin conocer detalles del ORM.
* **Negativas**:
  * Acoplamiento a un componente base transaccional compartido en la capa de infraestructura común.
