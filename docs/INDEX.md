---
id: CF-DOC-000
title: "Índice Maestro de Documentación"
owner: "cto"
status: "approved"
last_reviewed: 2026-07-24
role: "canonical"
---

# Índice Maestro de Documentación - CajaFácil

Bienvenido al repositorio de conocimiento de **CajaFácil**. Este documento constituye el punto oficial de entrada y mapa general para desarrolladores, arquitectos y asistentes de Inteligencia Artificial (IA).

---

## 1. Misión de la Documentación

En CajaFácil, la documentación es tratada como un activo de software. Su propósito es describir con precisión las reglas del negocio, la arquitectura del sistema y las directrices de ingeniería, garantizando la consistencia y mantenibilidad del producto durante su ciclo de vida a 10 años.

---

## 2. Estructura y Categorías Principales

La documentación está organizada bajo una estructura híbrida de carpetas que divide el conocimiento de negocio de las especificaciones y estándares de ingeniería de software:

```text
docs/
├── INDEX.md                         # Este archivo: Entrada general
├── PLAN_REORGANIZACION_DOCUMENTAL.md # Estrategia de gobernanza
├── MAPA_DOCUMENTAL.md                 # Taxonomía e índices de dominio
├── MATRIZ_DE_DOCUMENTOS.md            # Plan de transición de archivos
├── REGLAS_DE_DOCUMENTACION.md         # Estándar y convenciones de redacción
├── PLAN_MIGRACION_DOCUMENTAL.md       # Hoja de ruta para la ejecución
│
├── business/                          # [NEGOCIO Y PRODUCTO]
│
├── engineering/                       # [INGENIERÍA DE SOFTWARE]
│   ├── architecture/                  # Arquitectura macro y DDD
│   ├── database/                      # Esquemas relacionales y físicos
│   ├── standards/                     # Estándares de desarrollo y testing
│   └── adr/                           # Architecture Decision Records
│
├── reference/                         # [REFERENCIAS EXTERNAS]
├── ai/                                # [ADAPTADOR PARA IA]
├── templates/                         # [PLANTILLAS Y BLUEPRINTS]
└── history/                           # [HISTORIAL Y SPRINTS CERRADOS]
```
---

## 3. Estado de la Reorganización (Control de Migración Parcial)

El proyecto se encuentra en medio de un proceso de reorganización documental incremental por dominios funcionales. A continuación se detalla el estado oficial y la ubicación de la información para evitar confusiones de lectura:

| Dominio Funcional | Estado | Ubicación Oficial del Conocimiento |
| :--- | :---: | :--- |
| **Empresa (Tenant) y Seguridad** | ✅ MIGRADO | `docs/business/13_DOMINIO_EMPRESA.md`, `docs/business/12_DOMINIO_SEGURIDAD.md` y `docs/engineering/database/16_MODELO_LOGICO_EMPRESA_SEGURIDAD.md`. |
| **Producto (Catalog)** | ✅ MIGRADO | `docs/business/04_DOMINIO_PRODUCTO.md` y `docs/engineering/database/17_MODELO_LOGICO_PRODUCTOS_INVENTARIO.md`. |
| **Ventas (Sales)** | ✅ MIGRADO | `docs/business/09_DOMINIO_VENTAS.md`, `docs/engineering/database/19_MODELO_LOGICO_VENTAS_CAJA.md` y `docs/engineering/architecture/24_DISENO_ARQUITECTONICO_VENTAS.md`. |
| **Inventario (Stock)** | ✅ MIGRADO | `docs/business/07_DOMINIO_INVENTARIO.md`, `docs/engineering/database/17_MODELO_LOGICO_PRODUCTOS_INVENTARIO.md` y `docs/engineering/architecture/28_DISENO_ARQUITECTONICO_INVENTARIO.md`. |
| **Caja (Cash Box)** | ✅ MIGRADO | `docs/business/10_DOMINIO_CAJA.md`, `docs/engineering/database/19_MODELO_LOGICO_VENTAS_CAJA.md` y `docs/engineering/architecture/32_DISENO_ARQUITECTONICO_CAJA.md`. |
| **Configuración Tributaria** | 🔄 MIGRANDO | En proceso de traslado en la Fase 6 (ver matriz y plan de migración). |
| **Clientes y Crédito** | ⏳ PENDIENTE | Ubicado en el directorio raíz de `docs/`. |
| **Compras y Proveedores** | ✅ MIGRADO | `docs/business/08_DOMINIO_COMPRAS.md` y `docs/engineering/database/18_MODELO_LOGICO_COMPRAS.md`. |

---
## 4. Navegación Temática Rápida

Si deseas profundizar en un dominio de negocio específico, puedes seguir nuestros índices de dominio cruzados definidos en [MAPA_DOCUMENTAL.md](file:///docs/MAPA_DOCUMENTAL.md):
*   **Ventas:** Reglas, base de datos y arquitectura del checkout de cobro.
*   **Inventario:** Kardex, movimientos de stock y caché en terminales locales.
*   **Configuración Tributaria:** Tasas de impuesto y motores impositivos.
*   **Gestión de Existencias:** Auditoría física y balance de stock del inquilino (Tenant).

---

## 5. Clasificación Numérica Oficial

Para preservar la trazabilidad histórica de los documentos y evitar roturas de enlaces relacionales en Git, CajaFácil adopta un **Glosario Numérico de Rangos** oficial:
*   **`00 - 09`:** Reglas del Negocio y Manifiesto (Business Core).
*   **`10 - 14`:** Diseño de Dominio y Arquitectura Conceptual.
*   **`15 - 21`:** Modelos y Diseños de Persistencia (Base de Datos).
*   **`22 - 39`:** Guías de Implementación y Estándares Técnicos.
*   **`40 - 54`:** Especificaciones Funcionales por Módulo MVP.
*   **`55 - 90`:** Reportes de Cierre de Sprint y Auditoría de Saneamiento.
*   **`99`:** Guía y Adaptador de Contexto para Inteligencia Artificial.

---

## 6. Cómo Utilizar y Mantener esta Documentación

*   **Principio Canónico:** Cada concepto tiene una única fuente oficial. No dupliques contenido; usa enlaces directos de markdown.
*   **Antes de Codificar:** Revisa siempre los estándares en `docs/engineering/standards/` y las reglas en `docs/business/`.
*   **Actualización Obligatoria:** Si modificas el código de un módulo y esto altera su comportamiento arquitectónico o regla de negocio, debes actualizar el documento canónico en la misma rama (Pull Request) y actualizar la propiedad `last_reviewed` del Frontmatter.
