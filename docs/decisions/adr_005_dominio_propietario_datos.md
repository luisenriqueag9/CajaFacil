# ADR-005: Dominio propietario de sus datos

* **Estado:** Aceptado
* **Fecha:** 2026-07-28
* **Autor:** Principal Software Architect

## Contexto
En arquitecturas monolíticas modulares, los módulos a menudo consultan o modifican directamente las tablas de otros contextos mediante sentencias SQL (JOINs) cruzados.

## Problema
El acceso directo de un módulo (como Ventas) a los modelos de base de datos de otro módulo (como Caja o Crédito) acopla de manera irreversible los esquemas físicos. Si un módulo cambia su base de datos, rompe a los demás, impidiendo separar o micro-serviciar los módulos en el futuro.

## Alternativas Consideradas
1. **Alternativa A**: Permitir llaves foráneas y consultas cruzadas directas de base de datos a nivel de infraestructura para simplificar la codificación.
2. **Alternativa B (Elegida)**: Prohibir consultas cruzadas directas. Cada módulo es el **dueño único y absoluto de sus datos**. Toda integración inter-contextos debe realizarse a través de puertos (Interfaces/Lookups) o mediante la publicación y consumo de **Eventos de Dominio**.

## Decisión Tomada
Se eligió la **Alternativa B**. Ningún módulo puede importar modelos SQLAlchemy de otro módulo ni realizar consultas SQL directas a tablas ajenas. Los datos cruzados se consultan a través de adaptadores concretos que se instancian en la capa de dependencias e interactúan únicamente con repositorios o puertos.

## Consecuencias
* **Positivas**:
  * Autonomía total de base de datos por Bounded Context.
  * Facilidad para migrar módulos específicos a bases de datos distintas o microservicios independientes.
  * Mantenimiento de límites limpios.
* **Negativas**:
  * Requiere escribir adaptadores e interfaces de puertos adicionales para comunicación inter-contexto.
