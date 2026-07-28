# 37_ESTANDARES_OFFLINE_FIRST.md

**Versión:** 1.0  
**Estado:** 📜 Aprobado (Sprint 16)  
**Última actualización:** 2026-07-23  
**Documento:** Estándares de Operación Offline-First  

---

# 1. Arquitectura de Datos Offline (SQLite Local)

CajaFácil está diseñado para garantizar la continuidad del negocio en el mostrador del comercio, incluso ante fallas de internet.
* El cliente (dispositivo terminal) opera contra un motor relacional local **SQLite** estructurado idénticamente a la base de datos central PostgreSQL en la nube.
* La persistencia de transacciones (ventas, arqueos, caja) se graba localmente en SQLite con confirmación transaccional inmediata.

---

# 2. Protocolo de Sincronización y Reintentos

### Sincronización de Cola de Sucesos (Outbox Pattern)
* Todo caso de uso que altera estados genera eventos de integración registrados localmente en una tabla de auditoría `outbox` en la misma transacción SQLite.
* Un proceso en segundo plano (Worker) sondea la tabla `outbox` e intenta enviar las transacciones al backend en la nube mediante peticiones HTTP idempotentes.

### Reintentos con Backoff Exponencial
* Si el servidor no responde o hay falla de red:
  * El worker suspende el envío y programa un reintento utilizando **Backoff Exponencial con Jitter** para no saturar el servidor al recuperar la conexión.
  * Los registros permanecen seguros localmente y la interfaz de usuario continúa respondiendo en modo offline.

---

# 3. Resolución de Conflictos y Consistencia Temporal

### Conflicto de Concurrencia de Stock
* **Regla de Consistencia Temporal:** Los movimientos físicos de inventario y caja no se consolidan en la nube utilizando la fecha de recepción del servidor, sino la marca de tiempo de creación local `created_at` generada por el dispositivo del cliente.
* **Reconstrucción del Kardex:** Al ingresar movimientos tardíos a la nube, el sistema recalcula retrospectivamente la sumatoria acumulativa para reflejar el stock histórico correcto.

### Conflicto de Sesiones de Caja
* SQLite local bloquea la apertura de una nueva sesión de caja si el dispositivo local posee una sesión activa no cerrada.
* Una sesión de caja abierta offline no puede cerrarse en la nube si existen movimientos offline pendientes de sincronización para esa misma sesión.

---

# 4. Recuperación tras Apagones Inesperados

* La base de datos local SQLite tiene habilitado el modo **WAL (Write-Ahead Logging)** y transacciones ACID nativas.
* Si el terminal se apaga bruscamente durante una venta o arqueo:
  * Al encender el equipo, SQLite ejecuta su autorecovery descartando transacciones incompletas o consolidando las confirmadas.
  * La aplicación lee el estado de la sesión de caja; si quedó en base de datos local como `ABIERTA`, la sesión continúa activa y recupera de forma transparente el control. No se requiere intervención técnica.
