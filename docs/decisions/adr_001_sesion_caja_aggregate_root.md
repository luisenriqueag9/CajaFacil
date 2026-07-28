# ADR-001: SesionCaja como Aggregate Root

* **Estado:** Aceptado
* **Fecha:** 2026-07-28
* **Autor:** Principal Software Architect

## Contexto
El módulo Caja administra la contabilidad del dinero en mostrador y los turnos de caja de los cajeros. Anteriormente, la entidad `Caja` se usaba tanto para representar la caja registradora física como la sesión transaccional de turno.

## Problema
El uso de una única entidad `Caja` para ambos propósitos impedía soportar múltiples turnos secuenciales en un mismo terminal físico de forma paralela o independiente. Además, presentaba problemas de concurrencia cuando se querían consultar saldos en terminales físicos mientras un cajero tenía una sesión abierta.

## Alternativas Consideradas
1. **Alternativa A**: Mantener `Caja` como la raíz agregada y guardar el historial de turnos en un listado interno mutable.
2. **Alternativa B (Elegida)**: Separar las responsabilidades físicas de las transaccionales. Definir `Caja` como una entidad física inmutable operativa y `SesionCaja` como la raíz agregada (Aggregate Root) transaccional que gobierna el ciclo de vida del turno y custodia los movimientos.

## Decisión Tomada
Se eligió la **Alternativa B**. La raíz agregada (Aggregate Root) del módulo es `SesionCaja`, la cual gestiona directamente los agregados de `MovimientoCaja` y `ArqueoCaja`. La entidad `Caja` representa únicamente el recurso o terminal físico de cobro.

## Consecuencias
* **Positivas**:
  * Desacoplamiento total entre las cajas registradoras físicas (terminales) y los turnos de cajeros.
  * Soporte limpio para múltiples cajas por empresa y múltiples turnos secuenciales.
  * Mayor consistencia en las invariantes de bloqueo de movimientos tras el cierre de turno.
* **Negativas**:
  * Requiere mapeo de relaciones un poco más complejo (`Caja` 1 -> N `SesionCaja`).
