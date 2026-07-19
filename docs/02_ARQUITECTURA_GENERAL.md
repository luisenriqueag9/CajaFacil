# 02_ARQUITECTURA_GENERAL.md

Versión: 1.0
Estado: Aprobado
Última actualización: 2026-07-18
Documento: Arquitectura General

# Arquitectura General de CajaFácil

## Objetivo

Definir la arquitectura técnica que gobernará el desarrollo de CajaFácil, estableciendo la organización del sistema, las responsabilidades de cada componente y las reglas que deberán respetarse durante todo el ciclo de vida del proyecto.

Este documento será la referencia principal para cualquier decisión de arquitectura.

---

# Principios de Arquitectura

Toda decisión técnica deberá respetar los siguientes principios:

- Modularidad.
- Bajo acoplamiento.
- Alta cohesión.
- Escalabilidad.
- Mantenibilidad.
- Rendimiento.
- Seguridad.
- Simplicidad para el usuario.
- Código reutilizable.
- Separación de responsabilidades.

---

# Arquitectura General

CajaFácil estará dividido en módulos independientes.

Cada módulo será responsable únicamente de su propio dominio del negocio.

Los módulos no deberán contener lógica perteneciente a otros módulos.

---

# Estructura General

La aplicación estará organizada de la siguiente manera:

```
desktop_app/
│
├── lib/
│   ├── app/
│   │   ├── core/
│   │   ├── modules/
│   │   └── shared/
│   │
│   └── main.dart
│
├── docs/
│
└── ...
```

---

# Core

El directorio **core** contendrá los componentes globales del sistema.

Ejemplos:

- Configuración.
- Tema.
- Colores.
- Navegación.
- Base de datos.
- Servicios globales.
- Seguridad.
- Sincronización.
- Constantes.
- Utilidades generales.

El código ubicado en Core podrá ser utilizado por cualquier módulo.

---

# Shared

Shared contendrá componentes reutilizables.

Ejemplos:

- Botones.
- TextFields.
- Diálogos.
- Tablas.
- Widgets reutilizables.
- Validadores comunes.
- Helpers.

Shared nunca contendrá reglas del negocio.

---

# Modules

Cada módulo representará un dominio del negocio.

Ejemplos:

- Productos.
- Compras.
- Inventario.
- Ventas.
- Caja.
- Clientes.
- Crédito.
- Reportes.

Cada módulo deberá ser independiente.

---

# Arquitectura interna de un módulo

Todos los módulos seguirán exactamente la misma estructura.

```
module/
│
├── data/
│
├── domain/
│
└── presentation/
    ├── controllers/
    ├── pages/
    └── widgets/
```

---

# Data

Responsabilidades:

- SQLite.
- PostgreSQL.
- API.
- Repositorios.
- Modelos.
- Mappers.
- Persistencia.

Data nunca contendrá reglas del negocio.

---

# Domain

Es el corazón del sistema.

Aquí vivirán:

- Entidades.
- Casos de uso.
- Interfaces.
- Reglas del negocio.
- Validaciones del dominio.

Todo el comportamiento del negocio deberá implementarse aquí.

---

# Presentation

Responsable de la interfaz gráfica.

Incluye:

- Pantallas.
- Widgets.
- Controladores.
- Estados.
- Navegación del módulo.

Presentation nunca accederá directamente a la base de datos.

---

# Comunicación entre capas

La comunicación será únicamente en un sentido.

```
Presentation
      ↓
Domain
      ↓
Data
```

Nunca deberá ocurrir lo contrario.

---

# Comunicación entre módulos

Un módulo no podrá modificar directamente la información interna de otro módulo.

Toda comunicación deberá realizarse mediante servicios, casos de uso o interfaces públicas.

---

# Base de datos

CajaFácil utilizará dos bases de datos.

## Local

SQLite.

Responsable de:

- Operación diaria.
- Funcionamiento sin Internet.
- Alto rendimiento.

---

## Nube

PostgreSQL.

Responsable de:

- Respaldo.
- Sincronización.
- Multiempresa.
- Administración remota.

---

# Funcionamiento Offline

La aplicación deberá funcionar completamente utilizando SQLite.

La sincronización con PostgreSQL será un proceso independiente.

Una falla de Internet nunca deberá impedir registrar una venta.

---

# Seguridad

Toda operación deberá respetar permisos.

No bastará con ocultar botones.

Las validaciones deberán realizarse también en la lógica del negocio.

---

# Auditoría

Las operaciones críticas deberán generar registros de auditoría.

Ejemplos:

- Cambios de precio.
- Ajustes.
- Eliminaciones lógicas.
- Aperturas de caja.
- Cierres.
- Anulaciones.

---

# Rendimiento

El rendimiento tendrá prioridad sobre efectos visuales innecesarios.

Toda operación frecuente deberá optimizarse.

Especialmente:

- Búsquedas.
- Ventas.
- Inventario.
- Apertura de pantallas.

---

# Escalabilidad

La arquitectura deberá permitir incorporar nuevos módulos sin modificar los existentes.

Ejemplos futuros:

- Restaurante.
- Facturación electrónica.
- Comercio electrónico.
- Programa de puntos.
- Aplicación móvil.

---

# Reglas Arquitectónicas

Siempre:

- Un módulo = una responsabilidad.
- Una pantalla = una responsabilidad.
- Una clase = una responsabilidad.

Nunca:

- Lógica del negocio en la interfaz.
- Consultas SQL desde la UI.
- Widgets con reglas de negocio.
- Código duplicado.
- Dependencias circulares.

---

# Decisiones Arquitectónicas

## A-001

CajaFácil utilizará una arquitectura modular organizada por dominios.

Estado:

Aprobada.

---

## A-002

La lógica del negocio vivirá exclusivamente en Domain.

Estado:

Aprobada.

---

## A-003

SQLite será la base principal de operación.

Estado:

Aprobada.

---

## A-004

PostgreSQL será utilizado para sincronización y servicios en la nube.

Estado:

Aprobada.

---

## A-005

El sistema deberá funcionar sin Internet.

Estado:

Aprobada.

---

# Observaciones

Toda nueva funcionalidad deberá respetar esta arquitectura.

Si una funcionalidad requiere romper alguna de estas reglas, primero deberá modificarse este documento y aprobarse la nueva decisión arquitectónica.