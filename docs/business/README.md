# Categoría Documental: Business (Negocio y Producto)

## Propósito
Esta carpeta es el repositorio central del conocimiento comercial y operativo de CajaFácil. Contiene el manifiesto fundacional, las especificaciones funcionales generales del software, el diccionario del negocio (lenguaje ubicuo) y las especificaciones conceptuales de reglas de negocio transversales.

## Alcance
*   **Qué pertenece aquí:** Manifiesto, especificaciones de requisitos de negocio, diccionario de términos comerciales y reglas conceptuales de impuestos, existencias y caja.
*   **Qué NO pertenece aquí:** Especificaciones de bases de datos, código fuente, configuraciones técnicas de frameworks o detalles de desarrollo.

## Propietario
*   **Rol:** Product Owner / Business Analyst.

## Documentos Canónicos
*   `00_MANIFIESTO_CAJA_FACIL.md` (CF-DOC-005): Visión y principios estratégicos.
*   `01_ESPECIFICACION_FUNCIONAL.md` (CF-DOC-006): Alcance de funcionalidades del MVP.
*   `03_DICCIONARIO_DEL_NEGOCIO.md` (CF-DOC-007): Glosario de términos oficiales del dominio.
*   `04_DOMINIO_PRODUCTO.md` (CF-DOC-009): Catálogo maestro de productos y categorizaciones.
*   `06_REGLAS_DE_NEGOCIO.md` (CF-DOC-008): Especificación matemática y lógica de impuestos, existencias y ventas.
*   `07_DOMINIO_INVENTARIO.md` (CF-DOC-014): Especificación del dominio comercial de existencias y Kardex.
*   `08_DOMINIO_COMPRAS.md` (CF-DOC-015): Especificación del dominio comercial de adquisiciones y costos de proveedor.
*   `09_DOMINIO_VENTAS.md` (CF-DOC-011): Especificación del dominio comercial de ventas y cobros.
*   `10_DOMINIO_CAJA.md` (CF-DOC-010): Especificación del dominio comercial de aperturas, cierres y gaveta de efectivo.
*   `12_DOMINIO_SEGURIDAD.md` (CF-DOC-012): Reglas y requerimientos de autenticación y permisos.
*   `13_DOMINIO_EMPRESA.md` (CF-DOC-013): Reglas y requerimientos de tenencia multi-tenant y sucursales.

## Documentos Dependientes (Especificaciones de Negocio)
*   `26_ANALISIS_FUNCIONAL_INVENTARIO.md` (CF-DOC-026): Análisis funcional de stock, Kardex y mermas.
*   `27_DISENO_DOMINIO_INVENTARIO.md` (CF-DOC-027): Diseño de lógica del dominio de inventario.
*   `30_ANALISIS_FUNCIONAL_CAJA.md` (CF-DOC-030): Análisis funcional de arqueos, turnos y diferencias de efectivo.
*   `31_DISENO_DOMINIO_CAJA.md` (CF-DOC-031): Diseño de lógica del dominio de caja registradora.
*   `55_ANALISIS_FUNCIONAL_OPERACION_DIARIA.md` (CF-DOC-055): Análisis funcional de la capacidad Operación Diaria (flujo completo del POS).
*   `56_DESIGN_SYSTEM.md` (CF-DOC-056): Especificación oficial del Design System (colores, fuentes, componentes, tokens).
*   `57_ARQUITECTURA_UX_POS.md` (CF-DOC-057): Especificación oficial de la Arquitectura UX y Flujos de Foco del POS.
*   `58_WIREFRAME_FUNCIONAL_POS.md` (CF-DOC-058): Especificación oficial de la Distribución de Pantalla y Wireframe Funcional del POS.
*   `59_MOCKUP_POS.md` (CF-DOC-059): Especificación oficial de los Mockups y Apariencia Definitiva del POS.

## Documentos Relacionados
*   Diseño técnico en `docs/engineering/architecture/`.
*   Esquemas de persistencia en `docs/engineering/database/`.
