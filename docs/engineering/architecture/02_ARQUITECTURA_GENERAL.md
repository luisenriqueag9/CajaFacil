# 02_ARQUITECTURA_GENERAL.md

**Versión:** 2.0  
**Estado:** Aprobado (Revisión Arquitectónica)  
**Última actualización:** 2026-07-19  
**Documento:** Arquitectura General

# Arquitectura General de CajaFácil

## Objetivo

Definir la arquitectura técnica oficial que gobernará el desarrollo de CajaFácil durante todo su ciclo de vida. Este documento es el contrato arquitectónico del proyecto y prevalece sobre cualquier decisión de implementación.

---

# Principios Arquitectónicos

- El negocio gobierna la tecnología.
- Arquitectura antes que implementación.
- Offline First.
- Multiempresa desde el diseño.
- Bajo acoplamiento.
- Alta cohesión.
- Separación estricta de responsabilidades.
- Escalabilidad.
- Mantenibilidad.
- Trazabilidad completa.
- No generar deuda técnica deliberadamente.

---

# Arquitectura por Capas

```text
Presentation
      │
      ▼
Application
      │
      ▼
Domain
      ▲
      │
Infrastructure (Data)
```

## Presentation

Responsable únicamente de:

- UI
- Navegación
- Estado de pantalla
- Widgets
- Validaciones de presentación

Nunca contiene reglas del negocio.

---

## Application

Coordina los casos de uso.

Incluye:

- Use Cases
- DTO
- Commands
- Queries
- Coordinación de transacciones

No contiene acceso directo a la base de datos.

---

## Domain

Es el corazón del sistema.

Contiene:

- Entidades
- Value Objects
- Servicios de dominio
- Interfaces de repositorios
- Reglas del negocio
- Excepciones del dominio

El dominio nunca depende de Infrastructure.

---

## Infrastructure (Data)

Implementa:

- SQLite
- PostgreSQL
- API
- Repositorios
- Datasources
- Mappers
- Persistencia

Nunca contiene reglas del negocio.

---

# Organización del Proyecto

```text
desktop_app/
│
├── docs/
├── lib/
│   ├── app/
│   │   ├── core/
│   │   ├── shared/
│   │   └── modules/
│   └── main.dart
```

---

# Organización de un Módulo

```text
productos/
│
├── application/
│   ├── dto/
│   ├── usecases/
│   ├── commands/
│   └── queries/
│
├── domain/
│   ├── entities/
│   ├── value_objects/
│   ├── repositories/
│   ├── services/
│   └── exceptions/
│
├── infrastructure/
│   ├── datasources/
│   ├── models/
│   ├── mappers/
│   └── repositories/
│
└── presentation/
    ├── controllers/
    ├── providers/
    ├── pages/
    └── widgets/
```

---

# Reglas de Dependencia

- Presentation depende únicamente de Application.
- Application depende únicamente de Domain.
- Infrastructure implementa interfaces definidas por Domain.
- Domain no conoce Flutter, SQLite, PostgreSQL ni FastAPI.

---

# Dependency Injection

Todas las dependencias deberán resolverse mediante un contenedor de inyección.

Ningún módulo podrá instanciar manualmente repositorios concretos.

---

# Comunicación entre Módulos

Los módulos no acceden a datos internos de otros módulos.

La comunicación se realiza mediante:

- Casos de uso
- Interfaces públicas
- Eventos de dominio cuando corresponda

---

# Eventos del Dominio

Eventos típicos:

- VentaConfirmada
- CompraRegistrada
- CajaAbierta
- CajaCerrada
- ProductoActualizado

Permiten desacoplar Inventario, Caja, Auditoría y Sincronización.

---

# Transacciones

Operaciones críticas deberán ser atómicas.

Ejemplo:

Registrar venta:

- Venta
- Movimiento de inventario
- Movimiento de caja
- Auditoría

Si cualquiera falla, toda la operación se revierte.

---

# Offline First

SQLite es la base operativa.

La aplicación nunca dependerá de Internet para vender.

---

# Sincronización

La sincronización será independiente de la operación.

Principios:

- Cola de sincronización
- Reintentos automáticos
- Idempotencia
- Resolución de conflictos
- Identificadores globales
- Marcas de tiempo

---

# Seguridad

Los permisos se validan tanto en UI como en Application y Domain.

Ocultar botones nunca constituye seguridad.

---

# Auditoría

Las operaciones críticas generan registros inmutables.

Nunca se elimina historial.

---

# Rendimiento

Prioridades:

- Ventas
- Búsquedas
- Inventario
- Apertura de pantallas

La experiencia del cajero tiene prioridad sobre efectos visuales.

---

# Convenciones

Ejemplos:

- Producto
- ProductoRepository
- ProductoRepositoryImpl
- CrearProductoUseCase
- ProductoDTO
- ProductoMapper
- ProductoPage
- ProductoController

---

# Registro de Decisiones Arquitectónicas (ADR)

Cada decisión incluirá:

- ID
- Fecha
- Contexto
- Decisión
- Consecuencias
- Estado
- Impacto
- Documentos relacionados

---

# Decisiones Vigentes

- A-001 Arquitectura Modular.
- A-002 Lógica del negocio en Domain.
- A-003 SQLite como base operativa.
- A-004 PostgreSQL para sincronización y nube.
- A-005 Offline First.
- A-006 Introducción de Application como capa de coordinación.
- A-007 Dependency Injection obligatoria.
- A-008 Comunicación mediante interfaces y eventos.
- A-009 Transacciones atómicas.
- A-010 ADR obligatorio para cambios arquitectónicos.

---

# Reglas para Antigravity

Toda generación automática de código deberá respetar:

- La estructura oficial de carpetas.
- Las convenciones de nombres.
- La separación por capas.
- Las dependencias permitidas.
- La prohibición de lógica de negocio fuera de Domain.
- La reutilización de componentes Shared.
- La independencia entre módulos.

---

# Observaciones Finales

Ninguna funcionalidad podrá incorporarse rompiendo estas reglas sin aprobar previamente una nueva Decisión Arquitectónica (ADR).

Este documento constituye la referencia técnica principal para la evolución de CajaFácil.