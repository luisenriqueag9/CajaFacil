# Índice Maestro de Documentación - CajaFácil Core 1.0

Bienvenido al repositorio de conocimiento de **CajaFácil**. Este documento constituye el punto oficial de entrada y mapa general para desarrolladores, arquitectos y asistentes de Inteligencia Artificial (IA).

---

## 1. Propósito del Proyecto
CajaFácil es un punto de venta (POS) SaaS comercial multi-tenant y multi-sucursal, diseñado con capacidades **Offline-First** para garantizar que los comercios operen de forma ininterrumpida ante fallas de red. Su núcleo está estructurado bajo **Domain-Driven Design (DDD) Táctico** y **Clean Architecture** para asegurar la mantenibilidad y escalabilidad del producto a largo plazo.

---

## 2. Mapa Documental de Carpetas

La base de conocimiento está organizada bajo la siguiente topología estricta:

```text
docs/
├── INDEX.md                             # Este archivo: Entrada general
├── MAPA_DOCUMENTAL.md                   # Taxonomía e índices de dominios
├── MATRIZ_DE_DOCUMENTOS.md              # Plan y estado de migración de archivos
├── PLAN_REORGANIZACION_DOCUMENTAL.md    # Estrategia de gobernanza documental
├── PLAN_MIGRACION_DOCUMENTAL.md         # Fases de transición documental
├── REGLAS_DE_DOCUMENTACION.md           # Estándar y convenciones de redacción
│
├── business/                            # [NEGOCIO Y PRODUCTO]
│   ├── 00_MANIFIESTO_CAJA_FACIL.md      # Visión y misión de CajaFácil
│   ├── 01_ESPECIFICACION_FUNCIONAL_V1.md# Especificación general funcional
│   ├── 03_DICCIONARIO_DEL_NEGOCIO.md    # Glosario y lenguaje ubicuo
│   ├── 06_REGLAS_DE_NEGOCIO.md          # Listado canonical de reglas (RN-XXX)
│   ├── 55_ANALISIS_FUNCIONAL_OPERACION_DIARIA.md # Capacidad de Operación Diaria (POS)
│   ├── 56_DESIGN_SYSTEM.md              # Sistema de Diseño Visual y de Interacción (UX/UI)
│   └── dominios/                        # Bounded Contexts y reglas funcionales específicas:
│       ├── 04_DOMINIO_PRODUCTO.md
│       ├── 07_DOMINIO_INVENTARIO.md
│       ├── 08_DOMINIO_COMPRAS.md
│       ├── 09_DOMINIO_VENTAS.md
│       ├── 10_DOMINIO_CAJA.md
│       ├── 11_DOMINIO_CLIENTES_CREDITO.md
│       ├── 12_DOMINIO_SEGURIDAD.md
│       └── 13_DOMINIO_EMPRESA.md
│
├── engineering/                         # [INGENIERÍA Y DISEÑO TÉCNICO]
│   ├── architecture/                    # Macro arquitectura y diagramas
│   │   ├── 02_ARQUITECTURA_GENERAL.md
│   │   ├── 05_MODELO_DEL_DOMINIO.md
│   │   ├── 22_BACKEND_ARQUITECTURA.md
│   │   └── 23_FRONTEND_ARQUITECTURA.md
│   ├── database/                        # Diseños y modelos lógicos/físicos
│   │   ├── 15_MODELO_CONCEPTUAL_DE_DATOS.md
│   │   ├── 18_MODELO_LOGICO_COMPRAS.md
│   │   ├── 20_MODELO_LOGICO_CLIENTES_CREDITO.md
│   │   └── 21_DISENO_BASE_DE_DATOS.md
│   └── standards/                       # Estándares obligatorios de codificación
│       ├── 33_ESTANDAR_DE_IMPLEMENTACION.md
│       ├── 34_ESTANDARES_DE_IMPLEMENTACION.md
│       ├── 35_ESTANDARES_DDD.md
│       ├── 36_ESTANDARES_TRANSACCIONALES.md
│       ├── 37_ESTANDARES_OFFLINE_FIRST.md
│       ├── 38_ESTANDARES_DE_PRUEBAS.md
│       ├── 39_GUIA_DESARROLLO_CAJAFACIL.md
│       └── 40_GUIA_IA_CAJAFACIL.md
│
├── decisions/                           # [ARCHITECTURE DECISION RECORDS - ADR]
│   ├── adr_001_sesion_caja_aggregate_root.md
│   ├── adr_002_commonsqlalchemyunitofwork.md
│   ├── adr_003_offline_first.md
│   ├── adr_004_sqlite_postgresql.md
│   └── adr_005_dominio_propietario_datos.md
│
├── ai/                                  # [ADAPTADOR Y DIRECTRICES PARA IA]
│   └── ...
│
├── history/                             # [REPORTES DE CIERRE E SPRINTS COMPLETADOS]
│   └── ...
│
└── archive/                             # [DOCUMENTACIÓN REEMPLAZADA / OBSOLETA]
    └── ...
```

---

## 3. Guía de Inicio para Nuevos Desarrolladores

Para integrarse de forma efectiva al desarrollo de CajaFácil, siga el orden recomendado de lectura:

### Paso 1: Comprender el Negocio
*   Comience por el **[Manifiesto del Proyecto](file:///docs/business/00_MANIFIESTO_CAJA_FACIL.md)** para alinearse con los objetivos y filosofía del negocio.
*   Estudie el **[Diccionario del Negocio](file:///docs/business/03_DICCIONARIO_DEL_NEGOCIO.md)** para dominar el Lenguaje Ubicuo obligatorio en el código.
*   Revise las **[Reglas de Negocio](file:///docs/business/06_REGLAS_DE_NEGOCIO.md)** generales del sistema.

### Paso 2: Entender la Arquitectura
*   Lea la **[Arquitectura General](file:///docs/engineering/architecture/02_ARQUITECTURA_GENERAL.md)** para conocer las capas físicas y el flujo de dependencias.
*   Estudie las decisiones críticas de diseño documentadas en la sección **[decisions/](file:///docs/decisions/)** (ADR).

### Paso 3: Seguir los Estándares de Codificación
*   Es obligatorio revisar el **[Estándar de Implementación / Constitución Técnica](file:///docs/engineering/standards/33_ESTANDAR_DE_IMPLEMENTACION.md)** y las pautas de estilo en **[Estándares Oficiales](file:///docs/engineering/standards/34_ESTANDARES_DE_IMPLEMENTACION.md)**.
*   Asegure la correcta transaccionalidad revisando los **[Estándares Transaccionales](file:///docs/engineering/standards/36_ESTANDARES_TRANSACCIONALES.md)**.

### Paso 4: Asegurar Calidad
*   Toda modificación o adición de código debe incluir pruebas unitarias o de integración según se detalla en los **[Estándares de Pruebas](file:///docs/engineering/standards/38_ESTANDARES_DE_PRUEBAS.md)**.

---

## 4. Gobernanza de la Documentación

*   **Consistencia**: La documentación se trata como un activo de software.
*   **Actualización**: Si modifica el comportamiento de un caso de uso o regla de negocio, es obligatorio actualizar el archivo correspondiente en el mismo Pull Request.
