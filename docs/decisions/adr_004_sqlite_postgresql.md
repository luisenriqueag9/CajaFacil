# ADR-004: SQLite + PostgreSQL

* **Estado:** Aceptado
* **Fecha:** 2026-07-28
* **Autor:** Principal Software Architect

## Contexto
El POS se ejecuta tanto de forma local (en la terminal del comercio) como en un backend central en la nube.

## Problema
Necesitamos un motor de base de datos ultraligero y de cero administración para las terminales locales (SQLite), pero requerimos un motor robusto y escalable para el entorno web multi-tenant centralizado (PostgreSQL).

## Alternativas Consideradas
1. **Alternativa A**: Utilizar PostgreSQL en contenedores locales en cada terminal física del comercio.
2. **Alternativa B (Elegida)**: Utilizar un ORM común (SQLAlchemy) con dialectos cruzados: **SQLite** localmente (modo batch para Alembic) y **PostgreSQL** en la nube.

## Decisión Tomada
Se seleccionó la **Alternativa B**. La base de datos local corre sobre SQLite para asegurar portabilidad y ligereza, mientras que la nube usa PostgreSQL. Las migraciones de Alembic se configuran en modo batch para que SQLite pueda procesar modificaciones complejas de Foreign Keys.

## Consecuencias
* **Positivas**:
  * SQLite no requiere administración y es idóneo para terminales de bajos recursos.
  * PostgreSQL provee robustez para el SaaS centralizado.
* **Negativas**:
  * Hay diferencias sintácticas entre dialectos (por ejemplo, SQLite no valida tipos de datos tan estrictamente ni soporta nativamente ciertas operaciones concurrentes), requiriendo escribir consultas estándar ANSI-SQL compatibles.
