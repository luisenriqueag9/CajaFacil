---
id: CF-DOC-002
title: "Mapa Documental del Proyecto"
owner: "cto"
status: "approved"
last_reviewed: 2026-07-24
role: "canonical"
---

# Mapa Documental de CajaFácil

Este documento detalla la estructura física de carpetas y los índices de navegación temática para toda la documentación del proyecto CajaFácil.

---

## 1. Estructura de Directorios (Modelo Híbrido)

La documentación de CajaFácil se distribuye físicamente bajo la carpeta `/docs` en la siguiente estructura jerárquica:

```text
docs/
├── INDEX.md                         # Entrada general (CF-DOC-000)
├── PLAN_REORGANIZACION_DOCUMENTAL.md # Estrategia de gobernanza (CF-DOC-001)
├── MAPA_DOCUMENTAL.md                 # Este archivo: taxonomía e índices (CF-DOC-002)
├── MATRIZ_DE_DOCUMENTOS.md            # Estado de transición de archivos (CF-DOC-003)
├── REGLAS_DE_DOCUMENTACION.md         # Convenciones de redacción (CF-DOC-004)
├── PLAN_MIGRACION_DOCUMENTAL.md       # Hoja de ruta por dominios (CF-DOC-005)
│
├── business/                          # [NEGOCIO Y REGLAS CONCEPTUALES]
│   ├── README.md                      # Propósito e índice del área
│   ├── 00_MANIFIESTO_CAJA_FACIL.md    # Visión estratégica
│   ├── 01_ESPECIFICACION_FUNCIONAL.md # Alcance del MVP
│   ├── 03_DICCIONARIO_DEL_NEGOCIO.md  # Lenguaje ubicuo
│   ├── 04_DOMINIO_PRODUCTO.md         # Reglas del catálogo de productos
│   ├── 06_REGLAS_DE_NEGOCIO.md        # Reglas impositivas y de checkout
│   ├── 07_DOMINIO_INVENTARIO.md       # Reglas y Kardex de existencias
│   ├── 09_DOMINIO_VENTAS.md           # Reglas de cobros y facturación
│   ├── 10_DOMINIO_CAJA.md             # Reglas de aperturas, arqueos y cierres
│   ├── 12_DOMINIO_SEGURIDAD.md        # Reglas de autenticación y roles
│   ├── 13_DOMINIO_EMPRESA.md          # Aislamiento multi-tenant y sucursales
│   ├── 26_ANALISIS_FUNCIONAL_INVENTARIO.md # Casos de uso de control de existencias
│   ├── 27_DISENO_DOMINIO_INVENTARIO.md # Lógica pura de Kardex y mermas
│   ├── 30_ANALISIS_FUNCIONAL_CAJA.md  # Casos de uso de turnos y arqueos
│   └── 31_DISENO_DOMINIO_CAJA.md      # Lógica pura del turno de caja
│
├── engineering/                       # [INGENIERÍA Y DISEÑO DE SOFTWARE]
│   ├── README.md                      # Propósito y alcance de ingeniería
│   │
│   ├── architecture/                  # [DISEÑO DE ARQUITECTURA DETALLADA]
│   │   ├── README.md                  # Propósito y responsabilidades
│   │   ├── 02_ARQUITECTURA_GENERAL.md # Capas de backend/frontend y dependencias
│   │   ├── 05_MODELO_DEL_DOMINIO.md   # Bounded Contexts y agregados
│   │   ├── 14_REVISION_ARQUITECTONICA.md # Auditoría de diseño macro inicial
│   │   ├── 24_DISENO_ARQUITECTONICO_VENTAS.md # Capas y controladores de ventas
│   │   ├── 28_DISENO_ARQUITECTONICO_INVENTARIO.md # Capas y controladores de stock
│   │   └── 32_DISENO_ARQUITECTONICO_CAJA.md # Capas y controladores de caja
│   │
│   ├── database/                      # [PERSISTENCIA Y SQL]
│   │   ├── README.md                  # Propósito y convenciones de persistencia
│   │   ├── 15_MODELO_CONCEPTUAL_DE_DATOS.md # Esquema entidad-relación global
│   │   ├── 16_MODELO_LOGICO_EMPRESA_SEGURIDAD.md # Modelo lógico relacional multiempresa
│   │   ├── 17_MODELO_LOGICO_PRODUCTOS_INVENTARIO.md # Modelo lógico relacional de catálogo y stock
│   │   ├── 19_MODELO_LOGICO_VENTAS_CAJA.md # Modelo lógico de cobros y caja
│   │   └── 21_DISENO_BASE_DE_DATOS.md # Estructura física SQLite/PostgreSQL
│   │
│   ├── standards/                     # [ESTÁNDARES Y GUÍAS DE CODIFICACIÓN]
│   │   ├── README.md                  # Propósito y responsables técnicos
│   │   ├── 22_BACKEND_ARQUITECTURA.md # Convenciones de capas en FastAPI (Global)
│   │   ├── 23_FRONTEND_ARQUITECTURA.md # Convenciones de Flutter (Global)
│   │   ├── 34_ESTANDARES_DE_IMPLEMENTACION.md # Reglas de implementación y routers
│   │   ├── 35_ESTANDARES_DDD.md       # Invariantes en memoria y dataclasses
│   │   ├── 36_ESTANDARES_TRANSACCIONALES.md # Unit of Work y commits automáticos
│   │   ├── 37_ESTANDARES_OFFLINE_FIRST.md # Sincronización y bases de datos embebidas
│   │   └── 38_ESTANDARES_DE_PRUEBAS.md # pytest y bases de datos en memoria
│   │
│   └── adr/                           # [ARCHIVES DE DECISIONES DE DISEÑO]
│       ├── README.md                  # Bitácora histórica de ADRs
│       └── ADR-001_xxx.md             # Registro individual de decisión
│
├── reference/                         # [REFERENCIAS DE TERCEROS Y LEYES]
│   ├── README.md                      # Propósito e índice de material externo
│   └── ...                            # APIs de pago, leyes tributarias
│
├── templates/                         # [BLUEPRINTS Y PLANTILLAS]
│   ├── README.md                      # Catálogo de plantillas
│   ├── adr_template.md                # Plantilla base para redactar ADRs
│   ├── spec_template.md               # Plantilla para especificaciones técnicas
│   └── ESTANDAR_DOCUMENTAL_DOMINIO.md # Estándar de estructura y jerarquía de dominios
│
├── ai/                                # [ADAPTADOR DE CONTEXTO PARA IA]
│   ├── README.md                      # Propósito del adaptador
│   ├── 00_LEEME.md                    # Manifiesto y guía para agentes autónomos
│   ├── arquitectura/
│   │   └── 01_PATRON_MODULO_MAESTRO.md # Plantilla estructurada del módulo master
│   └── desarrollo/
│       ├── 02_ESTANDARES_DE_CODIGO.md # Nomenclatura, typing y precisión financiera
│       ├── 03_WORKFLOW_SPRINTS.md
│       ├── 04_CONVENCIONES_DE_PROYECTO.md
│       ├── 05_PLANTILLAS.md
│       └── 06_CHECKLIST_DE_REVISION.md
│
└── history/                           # [HISTORIAL Y AUDITORÍAS PASADAS]
    ├── README.md                      # Índice general de archivo
    ├── 25_CIERRE_SPRINT13_VENTAS.md   # Cierre Sprint 13 (Ventas)
    ├── 29_CIERRE_SPRINT14_INVENTARIO.md # Cierre Sprint 14 (Inventario)
    ├── 45_CIERRE_SPRINT17_CONFIGURACION_TRIBUTARIA.md # Cierre Sprint 17
    ├── 51_CIERRE_SPRINT19_GESTION_EXISTENCIAS.md # Cierre Sprint 19
    ├── 52_AUDITORIA_TRANSVERSAL_BACKEND.md # Auditoría transaccional backend
    ├── 53_PLAN_ACCION_AUDITORIA_BACKEND.md # Plan de acción
    ├── BITACORA_MIGRACION.md          # Bitácora histórica acumulada de migración
    └── 99_PROYECTO_CAJAFACIL_AI.md    # Monolito discontinuado
```

---

## 2. Índices de Navegación Temática (Cross-Linking)

Para permitir una comprensión integral de un módulo sin tener que buscar aleatoriamente por carpetas, se establecen los siguientes índices temáticos oficiales:

### 2.1. Índice Temático: Módulo Ventas (Sales)
*   **Negocio (Rules):** [09_DOMINIO_VENTAS.md](file:///docs/business/09_DOMINIO_VENTAS.md)
*   **Base de Datos (Schema):** [19_MODELO_LOGICO_VENTAS_CAJA.md](file:///docs/engineering/database/19_MODELO_LOGICO_VENTAS_CAJA.md) (Compartido con Caja)
*   **Diseño Técnico:** [24_DISENO_ARQUITECTONICO_VENTAS.md](file:///docs/engineering/architecture/24_DISENO_ARQUITECTONICO_VENTAS.md)
*   **Transaccionalidad:** [36_ESTANDARES_TRANSACCIONALES.md](file:///docs/engineering/standards/36_ESTANDARES_TRANSACCIONALES.md)
*   **Historial:** [25_CIERRE_SPRINT13_VENTAS.md](file:///docs/history/25_CIERRE_SPRINT13_VENTAS.md)

### 2.2. Índice Temático: Módulo Inventario (Inventory)
*   **Negocio (Rules):** [07_DOMINIO_INVENTARIO.md](file:///docs/business/07_DOMINIO_INVENTARIO.md)
*   **Análisis Funcional:** [26_ANALISIS_FUNCIONAL_INVENTARIO.md](file:///docs/business/26_ANALISIS_FUNCIONAL_INVENTARIO.md)
*   **Base de Datos (Schema):** [17_MODELO_LOGICO_PRODUCTOS_INVENTARIO.md](file:///docs/engineering/database/17_MODELO_LOGICO_PRODUCTOS_INVENTARIO.md) (Compartido con Producto)
*   **Diseño Técnico (Kardex):** [28_DISENO_ARQUITECTONICO_INVENTARIO.md](file:///docs/engineering/architecture/28_DISENO_ARQUITECTONICO_INVENTARIO.md)
*   **Offline-First & Caché:** [37_ESTANDARES_OFFLINE_FIRST.md](file:///docs/engineering/standards/37_ESTANDARES_OFFLINE_FIRST.md)
*   **Historial:** [29_CIERRE_SPRINT14_INVENTARIO.md](file:///docs/history/29_CIERRE_SPRINT14_INVENTARIO.md)

### 2.3. Índice Temático: Módulo Caja (Cash Box)
*   **Negocio (Rules):** [10_DOMINIO_CAJA.md](file:///docs/business/10_DOMINIO_CAJA.md)
*   **Análisis Funcional:** [30_ANALISIS_FUNCIONAL_CAJA.md](file:///docs/business/30_ANALISIS_FUNCIONAL_CAJA.md)
*   **Diseño de Dominio:** [31_DISENO_DOMINIO_CAJA.md](file:///docs/business/31_DISENO_DOMINIO_CAJA.md)
*   **Base de Datos (Schema):** [19_MODELO_LOGICO_VENTAS_CAJA.md](file:///docs/engineering/database/19_MODELO_LOGICO_VENTAS_CAJA.md) (Compartido con Ventas)
*   **Diseño Técnico:** [32_DISENO_ARQUITECTONICO_CAJA.md](file:///docs/engineering/architecture/32_DISENO_ARQUITECTONICO_CAJA.md)

### 2.4. Índice Temático: Configuración Tributaria (Taxes)
*   **Análisis Funcional:** [42_ANALISIS_FUNCIONAL_CONFIGURACION_TRIBUTARIA.md](file:///docs/business/42_ANALISIS_FUNCIONAL_CONFIGURACION_TRIBUTARIA.md)
*   **Diseño de Dominio:** [43_DISENO_DOMINIO_CONFIGURACION_TRIBUTARIA.md](file:///docs/business/43_DISENO_DOMINIO_CONFIGURACION_TRIBUTARIA.md)
*   **Diseño Arquitectónico:** [44_DISENO_ARQUITECTONICO_CONFIGURACION_TRIBUTARIA.md](file:///docs/engineering/standards/44_DISENO_ARQUITECTONICO_CONFIGURACION_TRIBUTARIA.md)
*   **Historial:** [45_CIERRE_SPRINT17_CONFIGURACION_TRIBUTARIA.md](file:///docs/history/45_CIERRE_SPRINT17_CONFIGURACION_TRIBUTARIA.md)

### 2.5. Índice Temático: Gestión de Existencias (Stock)
*   **Análisis Funcional:** [48_ANALISIS_FUNCIONAL_GESTION_EXISTENCIAS.md](file:///docs/business/48_ANALISIS_FUNCIONAL_GESTION_EXISTENCIAS.md)
*   **Diseño de Dominio:** [49_DISENO_DOMINIO_GESTION_EXISTENCIAS.md](file:///docs/business/49_DISENO_DOMINIO_GESTION_EXISTENCIAS.md)
*   **Diseño Arquitectónico:** [50_DISENO_ARQUITECTONICO_GESTION_EXISTENCIAS.md](file:///docs/engineering/standards/50_DISENO_ARQUITECTONICO_GESTION_EXISTENCIAS.md)
*   **Historial:** [51_CIERRE_SPRINT19_GESTION_EXISTENCIAS.md](file:///docs/history/51_CIERRE_SPRINT19_GESTION_EXISTENCIAS.md)

---

## 3. Control de Modificaciones del Mapa

Cualquier cambio físico en la estructura de carpetas (crear directorios, mover archivos) debe registrarse primero en la matriz oficial y posteriormente reflejarse en este documento.
