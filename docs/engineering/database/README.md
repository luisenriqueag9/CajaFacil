# Categoría Documental: Engineering / Database (Persistencia y Modelado de Datos)

## Propósito
Esta carpeta documenta los modelos relacionales conceptuales, lógicos y físicos de CajaFácil para las bases de datos SQLite (offline local) y PostgreSQL (nube).

## Alcance
*   **Qué pertenece aquí:** Modelos conceptuales y lógicos de datos por módulo, diseños físicos de tablas, restricciones de llaves foráneas y especificaciones de versionado con Alembic.
*   **Qué NO pertenece aquí:** Modelos de negocio o diagramas funcionales sin impacto en el almacenamiento físico.

## Propietario
*   **Rol:** Lead Architect.

## Documentos Canónicos
*   `15_MODELO_CONCEPTUAL_DE_DATOS.md` (CF-DOC-020): Esquema relacional global y cardinalidades.
*   `21_DISENO_BASE_DE_DATOS.md` (CF-DOC-021): Configuración física de SQLite y PostgreSQL.

## Documentos Dependientes (Modelos Lógicos por Módulo)
*   `16_MODELO_LOGICO_EMPRESA_SEGURIDAD.md` (CF-DOC-016)
*   `17_MODELO_LOGICO_PRODUCTOS_INVENTARIO.md` (CF-DOC-017)
*   `18_MODELO_LOGICO_COMPRAS.md` (CF-DOC-024)
*   `19_MODELO_LOGICO_VENTAS_CAJA.md` (CF-DOC-019)
*   `20_MODELO_LOGICO_CLIENTES_CREDITO.md` (CF-DOC-020)

## Documentos Relacionados
*   Estándares transaccionales y offline-first en `docs/engineering/standards/`.
