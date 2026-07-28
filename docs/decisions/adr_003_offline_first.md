# ADR-003: Offline First

* **Estado:** Aceptado
* **Fecha:** 2026-07-28
* **Autor:** Principal Software Architect

## Contexto
CajaFácil es un punto de venta (POS) SaaS que se despliega en comercios donde la conectividad a internet puede ser inestable o nula durante horas.

## Problema
Si el sistema dependiera de una conexión a internet constante para validar stock, registrar ventas o cobrar, los comercios quedarían inoperativos durante las caídas de red, generando pérdidas económicas directas.

## Alternativas Consideradas
1. **Alternativa A**: Diseñar una arquitectura Cloud-Native tradicional con caché local de solo lectura.
2. **Alternativa B (Elegida)**: Adoptar una filosofía **Offline-First**. Toda la base de datos operativa se replica localmente y las escrituras se realizan sobre almacenamiento local síncrono, sincronizando de forma asíncrona hacia la nube cuando la red esté disponible.

## Decisión Tomada
Se eligió la **Alternativa B**. El sistema opera de forma local autónoma utilizando bases de datos empotradas (SQLite). El motor garantiza transaccionalidad local inmediata y propaga cambios a la nube mediante colas de sincronización asíncronas.

## Consecuencias
* **Positivas**:
  * Tolerancia absoluta a caídas de red; el comercio puede seguir vendiendo y cobrando.
  * Tiempos de respuesta inmediatos en el mostrador (latencia de red cero en base de datos).
* **Negativas**:
  * Incrementa la complejidad en el manejo de resolución de conflictos de sincronización y claves únicas concurrentes.
