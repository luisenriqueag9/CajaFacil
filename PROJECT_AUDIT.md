# PROJECT AUDIT: CajaFácil POS

**Rol:** Arquitecto de Software Senior  
**Fecha de Auditoría:** 2026-07-20  
**Estado General del Proyecto:** 🟡 En Desarrollo Inicial (Fase de Esqueleto y Prototipado)

---

## 1. Estructura del proyecto

A continuación, se detalla el árbol completo de carpetas y archivos clave del repositorio de **CajaFácil**:

```text
CajaFacil/
├── backend/
│   ├── app/
│   │   ├── common/
│   │   │   ├── exceptions.py
│   │   │   ├── filters.py
│   │   │   ├── pagination.py
│   │   │   ├── responses.py
│   │   │   ├── utils.py
│   │   │   ├── validators.py
│   │   │   └── __init__.py
│   │   ├── core/
│   │   │   ├── services/
│   │   │   │   └── __init__.py
│   │   │   ├── config.py
│   │   │   └── logger.py
│   │   ├── database/
│   │   │   ├── migrations/
│   │   │   │   ├── versions/
│   │   │   │   │   ├── 013925a578b3_create_unit_table.py
│   │   │   │   │   ├── 07587c453c53_create_product_table.py
│   │   │   │   │   ├── 0a914349279e_create_company_table.py
│   │   │   │   │   ├── 18012e53eca6_consolidate_product_table.py
│   │   │   │   │   ├── 60b36599d839_create_category_table.py
│   │   │   │   │   └── cbfe8faf79d5_create_brand_table.py
│   │   │   │   └── env.py
│   │   │   ├── models/
│   │   │   │   └── __init__.py
│   │   │   ├── repositories/
│   │   │   │   ├── base.py
│   │   │   │   └── __init__.py
│   │   │   ├── base.py
│   │   │   └── session.py
│   │   ├── modules/
│   │   │   ├── brand/
│   │   │   │   ├── data/
│   │   │   │   │   ├── models.py
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── domain/
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── presentation/
│   │   │   │   │   └── __init__.py
│   │   │   │   └── __init__.py
│   │   │   ├── category/
│   │   │   │   ├── data/
│   │   │   │   │   ├── models.py
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── domain/
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── presentation/
│   │   │   │   │   └── __init__.py
│   │   │   │   └── __init__.py
│   │   │   ├── company/
│   │   │   │   ├── data/
│   │   │   │   │   ├── models.py
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── domain/
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── presentation/
│   │   │   │   │   └── __init__.py
│   │   │   │   └── __init__.py
│   │   │   ├── product/
│   │   │   │   ├── data/
│   │   │   │   │   ├── models.py
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── domain/
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── presentation/
│   │   │   │   │   └── __init__.py
│   │   │   │   └── __init__.py
│   │   │   └── unit/
│   │   │       ├── data/
│   │   │       │   ├── models.py
│   │   │       │   └── __init__.py
│   │   │       ├── domain/
│   │   │       │   └── __init__.py
│   │   │       ├── presentation/
│   │   │       │   └── __init__.py
│   │   │       └── __init__.py
│   │   ├── main.py
│   │   └── __init__.py
│   ├── tests/
│   │   └── test_placeholder.py
│   ├── .env
│   ├── .env.example
│   ├── alembic.ini
│   ├── requirements.txt
│   └── caja_facil.db
├── desktop_app/
│   ├── lib/
│   │   ├── app/
│   │   │   ├── core/
│   │   │   │   ├── config/
│   │   │   │   │   └── app_config.dart
│   │   │   │   ├── database/
│   │   │   │   │   └── local_db.dart
│   │   │   │   ├── logger/
│   │   │   │   │   └── app_logger.dart
│   │   │   │   ├── router/
│   │   │   │   │   ├── app_router.dart
│   │   │   │   │   └── app_routes.dart
│   │   │   │   └── theme/
│   │   │   │       ├── app_colors.dart
│   │   │   │       ├── app_radius.dart
│   │   │   │       ├── app_shadows.dart
│   │   │   │       ├── app_spacing.dart
│   │   │   │       ├── app_text_styles.dart
│   │   │   │       └── app_theme.dart
│   │   │   ├── modules/
│   │   │   │   ├── auth/
│   │   │   │   │   └── presentation/
│   │   │   │   │       └── pages/
│   │   │   │   │           └── login_page.dart
│   │   │   │   └── dashboard/
│   │   │   │       └── presentation/
│   │   │   │           └── pages/
│   │   │   │               └── dashboard_page.dart
│   │   │   ├── shared/
│   │   │   │   ├── constants/
│   │   │   │   │   └── app_constants.dart
│   │   │   │   ├── extensions/
│   │   │   │   │   └── build_context_extensions.dart
│   │   │   │   ├── helpers/
│   │   │   │   │   └── formatters.dart
│   │   │   │   ├── layouts/
│   │   │   │   │   └── main_layout.dart
│   │   │   │   ├── pages/
│   │   │   │   │   └── module_placeholder_page.dart
│   │   │   │   └── widgets/
│   │   │   │       ├── app_button.dart
│   │   │   │       ├── app_card.dart
│   │   │   │       ├── app_sidebar.dart
│   │   │   │       ├── app_text_field.dart
│   │   │   │       └── custom_card.dart
│   │   │   └── app.dart
│   │   └── main.dart
│   ├── test/
│   │   └── app_test.dart
│   ├── pubspec.yaml
│   ├── pubspec.lock
│   └── analysis_options.yaml
└── docs/
    ├── 00_MANIFIESTO_CAJA_FACIL.md
    ├── 01_ESPECIFICACION_FUNCIONAL_V1.md
    ├── 02_ARQUITECTURA_GENERAL.md
    ├── ... (Resto de especificaciones funcionales y modelos lógicos 03 a 23)
```

---

## 2. Backend

### Módulos existentes
Los módulos definidos a nivel estructural (carpetas físicas) dentro de `backend/app/modules` son:
*   `brand` (Marca)
*   `category` (Categoría)
*   `company` (Empresa)
*   `product` (Producto)
*   `unit` (Unidad de Medida)

*(Nota: Solo cuentan con el esqueleto de directorios `data`, `domain` y `presentation` con sus respectivos archivos `__init__.py`, y los modelos SQLAlchemy. No contienen lógica de negocio o routers).*

### Configuración
*   **Archivo:** `backend/app/core/config.py`
*   **Tecnología:** Utiliza Pydantic Settings (`BaseSettings`) para gestionar la configuración de manera segura con tipado fuerte. Carga las variables de entorno de un archivo `.env` localizado en la raíz del backend.
*   **Variables clave:** `APP_NAME`, `ENV` (development/testing/production), `DEBUG`, `LOG_LEVEL`, `DB_PROVIDER` (sqlite/postgres), y configuraciones específicas para SQLite (`SQLITE_DB_PATH`) y PostgreSQL (`POSTGRES_USER`, `POSTGRES_PASSWORD`, etc.).

### SQLAlchemy
*   **Configuración centralizada:** `backend/app/database/session.py` y `backend/app/database/base.py`.
*   **Declarative Base:** Utiliza SQLAlchemy 2.0 (`DeclarativeBase`). Todos los modelos se importan explícitamente en `base.py` para consolidar sus metadatos y facilitar la autogeneración de Alembic.
*   **Sesiones:** Provee una factoría de sesiones sincrónica `SessionLocal` y una función generadora de dependencias (`get_db`) que implementa la inyección de dependencias para los endpoints de FastAPI, gestionando transacciones y cierres de sesión de manera segura.
*   **Soporte SQLite Fk:** Habilita el soporte para claves foráneas (`PRAGMA foreign_keys=ON`) en conexiones SQLite mediante escuchadores de eventos SQLAlchemy.

### Alembic
*   **Archivos:** `backend/alembic.ini` y `backend/app/database/migrations/env.py`.
*   **Mecanismo:** Alembic está configurado para leer dinámicamente la URL de conexión del objeto `settings` de Pydantic. Cuenta con soporte de migración por lotes (`render_as_batch=True`) para sortear las limitaciones de alteración de tablas en SQLite.
*   **Migraciones existentes:** Posee 6 versiones de migración lineal:
    1.  `07587c453c53_create_product_table` (Crea tabla producto sin restricciones FK físicas inicialmente).
    2.  `013925a578b3_create_unit_table` (Crea tabla unidad de medida).
    3.  `60b36599d839_create_category_table` (Crea tabla categorías).
    4.  `0a914349279e_create_company_table` (Crea tabla empresa/tenant).
    5.  `cbfe8faf79d5_create_brand_table` (Crea tabla marcas).
    6.  `18012e53eca6_consolidate_product_table` (Modifica la tabla de productos aplicando los tipos UUID correspondientes y agregando las restricciones FK físicas `RESTRICT`).

### Autenticación
*   **Estado:** ❌ **No existe**.
*   A pesar de estar declarada como parte fundamental en `docs/22_BACKEND_ARQUITECTURA.md` (JWT, Passlib, BCrypt), no se encuentra implementado ningún tipo de middleware de seguridad, lógica de hash de contraseñas o generación de tokens en el código del backend.

### Rutas
*   **Archivo:** `backend/app/main.py`
*   **Endpoints activos:** Únicamente `/health` (GET), que valida el estado del servicio core.
*   **Módulos:** No hay rutas registradas ni routers modulares para los productos, unidades, marcas, etc. El archivo incluye comentarios indicando dónde deben registrarse en el futuro.

### Servicios
*   **Estado:** ❌ **No existe**.
*   Solo se encuentra el archivo vacío `backend/app/core/services/__init__.py`. No hay servicios de negocio compartidos implementados.

### Repositorios
*   **Clase Base:** `backend/app/database/repositories/base.py` contiene `BaseRepository[ModelType]`, una interfaz genérica que provee esqueletos CRUD (Create, Read, Update, Delete) utilizando SQLAlchemy.
*   **Repositorios de dominio:** ❌ **No existen** implementaciones concretas para ningún módulo maestro en el backend.

### Casos de uso
*   **Estado:** ❌ **No existe**.
*   Las carpetas `domain` en los módulos se encuentran vacías (solo contienen archivos `__init__.py` vacíos).

### Pruebas
*   **Archivo:** `backend/tests/test_placeholder.py`
*   **Cobertura:** Solo contiene un test de integración (`test_app_settings_initialization`) para validar la carga de configuraciones con Pydantic. No existen pruebas para lógica de dominio o persistencia.

---

## 3. Frontend

### Módulos
Los módulos presentes físicamente dentro de `desktop_app/lib/app/modules` son:
1.  `auth` (Autenticación / Login)
2.  `dashboard` (Panel principal de control)

*(Nota: Otros módulos de negocio como `clientes`, `productos`, `inventario`, `ventas`, `reportes` y `configuración` no están estructurados como módulos físicos en el código del frontend).*

### Pantallas
1.  `LoginPage` (`desktop_app/lib/app/modules/auth/presentation/pages/login_page.dart`): Interfaz visual de inicio de sesión de doble panel (banner institucional + formulario). Contiene lógica dummy para el botón "Ingresar", el cual solo despliega un mensaje (SnackBar) indicando que la funcionalidad estará disponible próximamente.
2.  `DashboardPage` (`desktop_app/lib/app/modules/dashboard/presentation/pages/dashboard_page.dart`): Vista de bienvenida vacía.
3.  `ModulePlaceholderPage` (`desktop_app/lib/app/shared/pages/module_placeholder_page.dart`): Pantalla genérica reutilizable para representar los módulos que están "en construcción".

### Providers
Usa Riverpod como gestor de estado. Los únicos providers declarados son:
*   `appConfigProvider` (`lib/app/core/config/app_config.dart`): Entrega la instancia de configuración actual.
*   `localDatabaseProvider` (`lib/app/core/database/local_db.dart`): Provee el esqueleto de base de datos local SQLite.
*   `routerProvider` (`lib/app/core/router/app_router.dart`): Provee el objeto de enrutamiento GoRouter.

No existen providers de estado para lógica de negocio de módulos.

### Repositories
*   **Estado:** ❌ **No existe**.
*   No hay repositorios definidos para interactuar con la base de datos local o con APIs HTTP.

### Widgets
Ubicados en `desktop_app/lib/app/shared/widgets/`:
*   `AppButton`: Botón estilizado con soporte de carga (`isLoading`).
*   `AppCard`: Contenedor estilizado con bordes y sombras basadas en tokens de diseño.
*   `AppSidebar`: Barra lateral de navegación principal con ítems dinámicos según ruta activa.
*   `AppTextField`: Campo de entrada de texto personalizado con soporte de iconos de prefijo/sufijo y validación.
*   `CustomCard`: Widget duplicado para tarjetas (con lógica de elevación al hacer hover).

### Layouts
*   `MainLayout` (`desktop_app/lib/app/shared/layouts/main_layout.dart`): Disposición general de la pantalla dividida en dos partes: el sidebar a la izquierda y el contenido del módulo actual a la derecha.

### Router
*   **Archivo:** `desktop_app/lib/app/core/router/app_router.dart` y `app_routes.dart`.
*   **Definición:** Configurado mediante GoRouter. Cuenta con las siguientes rutas registradas:
    *   `/login` -> Muestra `LoginPage`
    *   `/dashboard` -> Muestra `DashboardPage`
    *   `/clientes` -> Muestra `ModulePlaceholderPage`
    *   `/productos` -> Muestra `ModulePlaceholderPage`
    *   `/inventario` -> Muestra `ModulePlaceholderPage`
    *   `/ventas` -> Muestra `ModulePlaceholderPage`
    *   `/reportes` -> Muestra `ModulePlaceholderPage`
    *   `/configuracion` -> Muestra `ModulePlaceholderPage`
*   **Lógica de inicio:** Si `AppConfig.developmentMode` es verdadero, el enrutador puentea el login y entra directamente al `/dashboard`.

### Theme
Implementado bajo tokens de diseño en `desktop_app/lib/app/core/theme/`:
*   `AppColors`: Paleta estática basada en colores corporativos (Teal, Emerald, etc.).
*   `AppRadius`, `AppSpacing`, `AppShadows`, `AppTextStyles`: Definiciones constantes y abstractas para bordes, sombras, espaciado y tipografía consistente.
*   `AppTheme`: Expone `darkTheme` (tema por defecto configurado de forma rígida), `lightTheme` (tema claro corporativo Indigo) y `light` (tema claro corporativo Teal heredado).

---

## 4. Dependencias

Las librerías de importancia que sustentan el proyecto son:

### Backend (`requirements.txt`)
*   `fastapi >= 0.110.0` (Framework API REST principal)
*   `uvicorn >= 0.28.0` (Servidor web ASGI para ejecución del backend)
*   `pydantic >= 2.6.0` y `pydantic-settings >= 2.2.0` (Modelado y validación de tipos y configuraciones)
*   `sqlalchemy >= 2.0.28` (ORM de persistencia relacional SQL)
*   `alembic >= 1.13.1` (Gestor de migraciones del esquema de BD)
*   `psycopg2-binary >= 2.9.9` (Driver PostgreSQL para almacenamiento en la nube)
*   `python-dotenv >= 1.0.1` (Utilidad para cargar variables de entorno locales)
*   `pytest >= 8.0.0` (Librería de pruebas de software)

### Frontend (`pubspec.yaml`)
*   `flutter_riverpod: ^3.3.2` (Gestor de estado oficial)
*   `go_router: ^17.2.3` (Gestor de navegación estructurada)
*   `flutter_lints: ^5.0.0` (Reglas de buenas prácticas de código de Flutter)

---

## 5. Estado de implementación

A continuación, se presenta la matriz de cobertura y nivel de completitud de los módulos core descritos en el manifiesto de CajaFácil:

| Módulo del Sistema | Persistencia BD (Backend) | Lógica/Servicios (Backend) | Endpoints API | Interfaz de Usuario (Frontend) | Estado General |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Empresa (Tenant Management)** | ✅ Completo | ❌ No existe | ❌ No existe | ❌ No existe | 🟡 **Parcial** |
| **Seguridad y Autenticación** | ❌ No existe | ❌ No existe | ❌ No existe | 🟡 Parcial (Dummy Login) | ❌ **No existe** |
| **Productos y Catálogo** | ✅ Completo | ❌ No existe | ❌ No existe | ❌ No existe (Placeholder) | 🟡 **Parcial** |
| **Inventario (Stock y Movimientos)** | ❌ No existe | ❌ No existe | ❌ No existe | ❌ No existe (Placeholder) | ❌ **No existe** |
| **Compras y Proveedores** | ❌ No existe | ❌ No existe | ❌ No existe | ❌ No existe | ❌ **No existe** |
| **Ventas y Facturación** | ❌ No existe | ❌ No existe | ❌ No existe | ❌ No existe (Placeholder) | ❌ **No existe** |
| **Caja (Flujos de Efectivo)** | ❌ No existe | ❌ No existe | ❌ No existe | ❌ No existe | ❌ **No existe** |
| **Clientes y Crédito** | ❌ No existe | ❌ No existe | ❌ No existe | ❌ No existe (Placeholder) | ❌ **No existe** |

---

## 6. Problemas encontrados

### Arquitectura
1.  **Inconsistencia de restricciones físicas en base de datos:** El modelo de productos (`Product`) posee claves foráneas reales a nivel de base de datos (`ForeignKey("company.id")`, `ForeignKey("category.id")`, etc.). Sin embargo, otros modelos como `Category`, `Brand` y `Unit` almacenan `company_id` simplemente como un campo tipo `SqlUUID`, prescindiendo de claves foráneas físicas. Si la arquitectura promueve desacoplamiento por agregados sin llaves físicas (como sugiere la nota en `Category.parent_id`), la restricción fuerte en `Product` viola este principio. Si se requiere consistencia fuerte, se deben añadir las llaves físicas en el resto de los catálogos.
2.  **Mocks de persistencia en el Frontend:** La clase `SQLiteLocalDatabase` (`lib/app/core/database/local_db.dart`) simplemente cambia una bandera en memoria a `_initialized = true` sin interactuar con un motor real, ya que no existen librerías de persistencia locales instaladas (`sqflite`, `drift` o `sqlite3` no constan en `pubspec.yaml`).
3.  **Falta de cliente HTTP en el Frontend:** No existe ninguna librería HTTP (como `dio` o `http`) declarada en `pubspec.yaml`, lo cual imposibilita la comunicación real entre las pantallas y el backend REST de FastAPI.
4.  **Uso de Tema Estático y Mismatch de Paleta Color:**
    *   La aplicación fuerza rígidamente el modo oscuro mediante la propiedad `themeMode: ThemeMode.dark` en `CajaFacilApp` (`lib/app/app.dart`), impidiendo que el usuario cambie a modo claro.
    *   El sidebar y el login importan `AppColors` de forma estática para pintar fondos con la constante `AppColors.primary` (que equivale al color Teal `0xFF0F766E`), mientras que el tema activo (`AppTheme.darkTheme`) asigna el color Indigo `0xFF6366F1` a la propiedad `primary` del esquema de colores. Esto produce incoherencia visual en el diseño.

### Duplicación
1.  **Layout y Espaciados:** El archivo `app_constants.dart` declara constantes de diseño para espaciado (`paddingXS`, `paddingSM`, etc.) y bordes (`radiusSM`, `radiusMD`, etc.), los cuales duplican e introducen conflictos menores con los definidos en `app_spacing.dart` y `app_radius.dart` (ejemplo: `AppConstants.radiusSM` es 8.0, mientras que `AppRadius.small` es 6.0).
2.  **Widgets de Tarjetas:** `AppCard` y `CustomCard` son estructuralmente el mismo widget de contenedor decorado con soporte de eventos táctiles.

### Código muerto
1.  **CustomCard:** Widget declarado en `desktop_app/lib/app/shared/widgets/custom_card.dart` que no se utiliza en ninguna vista.
2.  **AppTheme.light:** El getter `light` definido en `desktop_app/lib/app/core/theme/app_theme.dart` (línea 93) está en desuso debido a que `app.dart` utiliza `AppTheme.lightTheme`.

### TODO
*   **Línea 9 de `desktop_app/windows/flutter/CMakeLists.txt`:** `# TODO: Move the rest of this into files in ephemeral. See` (Código autogenerado por Flutter).

### FIXME
*   No se encontraron comentarios FIXME en el proyecto.

### Warnings
1.  **Control de punteros a conexión en SQLite:** En `backend/app/database/session.py` (líneas 26-34), la función `set_sqlite_pragma` realiza un control `if not hasattr(dbapi_connection, "cursor")` y registra un log de error en caso de fallo, pero inmediatamente después ejecuta `dbapi_connection.cursor()`, lo cual causará un error de atributo (`AttributeError`) e interrumpirá el flujo si el atributo no existe.

---

## 7. Recomendaciones

A continuación, se sugieren las acciones del arquitecto ordenadas por prioridad de adopción:

### Qué reutilizar
*   **Diseño estructural del Backend:** La separación de módulos con directorios diferenciados (`data`, `domain`, `presentation`) es una buena base de Clean Architecture y debe conservarse para los módulos faltantes.
*   **Mapeadores Pydantic y Respuestas Genéricas:** Los modelos estandarizados definidos en `backend/app/common/responses.py` y `pagination.py` son ideales para homogeneizar todas las respuestas HTTP de la aplicación.
*   **Tokens de Diseño del Frontend:** Las definiciones de tipografía y espaciados de `AppTheme` deben continuar gobernando el desarrollo de la interfaz de usuario.

### Qué corregir
*   **Instalación de dependencias críticas en Frontend:** Se debe enriquecer `pubspec.yaml` integrando paquetes esenciales como `http` o `dio` para las llamadas HTTP, y `drift` o `sqlite3` para dar vida a la capa de base de datos offline.
*   **Instalación de dependencias de seguridad en Backend:** Agregar a `requirements.txt` los paquetes `passlib[bcrypt]` y `pyjwt` o `python-jose` para poder implementar los flujos de seguridad del token JWT.
*   **Sincronización de estilos de widgets:** Reemplazar el uso estático de constantes como `AppColors.primary` por llamadas dinámicas a los estilos activos del contexto mediante `Theme.of(context).colorScheme.primary`.
*   **Consolidación de constantes de diseño:** Eliminar las métricas de espaciado y radio presentes en `AppConstants.dart` y migrar todas las referencias hacia `AppSpacing` y `AppRadius`.
*   **Unificación de criterios de llaves foráneas:** Homogeneizar si el sistema SaaS operará con Foreign Keys lógicas (a nivel de aplicación) para máxima modularidad y aislamiento entre módulos, o si operará con restricciones físicas en todas las bases de datos para salvaguardar la integridad referencial de forma estricta.

### Qué eliminar
*   **Eliminar `CustomCard`:** Remover el widget huérfano de `desktop_app/lib/app/shared/widgets/custom_card.dart` y estandarizar el uso de `AppCard` con soporte dinámico de elevaciones al hacer hover si es necesario.
*   **Eliminar tema legacy `AppTheme.light`:** Remover la función en desuso de `desktop_app/lib/app/core/theme/app_theme.dart` para simplificar la mantenibilidad del diseño estético claro y oscuro.
