---
id: CF-DOC-058
title: "Especificación: Wireframe Funcional del POS"
owner: "product-owner"
status: "approved"
last_reviewed: 2026-07-28
role: "dependent"
---

# Wireframe Funcional del POS de CajaFácil

> [!NOTE]
> Este documento depende de las especificaciones de negocio de la capacidad de Operación Diaria, el Design System y la Arquitectura UX:
> - [Capacidad: Operación Diaria](file:///docs/business/55_ANALISIS_FUNCIONAL_OPERACION_DIARIA.md) (CF-DOC-055)
> - [Design System Oficial](file:///docs/business/56_DESIGN_SYSTEM.md) (CF-DOC-056)
> - [Arquitectura UX del POS](file:///docs/business/57_ARQUITECTURA_UX_POS.md) (CF-DOC-057)

---

## 1. Objetivos del Wireframe

El wireframe funcional de CajaFácil tiene como meta estructurar el espacio de pantalla del punto de venta (POS) para solucionar los siguientes problemas críticos detectados en la operación de mostrador minorista:

- **Reducción del Tiempo de Cobro**: Organizar las celdas y los totales de modo que el cajero identifique el monto a cobrar y calcule el cambio sin desviar la mirada del cliente.
- **Eliminación del Re-Foco Manual**: Situar la barra de escaneo/búsqueda en una posición fija y de foco permanente para evitar clics correctivos con el mouse.
- **Minimización de Fatiga Ocular y del Cuello**: Reducir el ángulo de giro de la cabeza del cajero agrupando los datos de alta frecuencia de lectura en el centro de su campo visual.
- **Facilidad de Lectura**: Proveer una densidad de información óptima donde el cliente y el cajero lean de un vistazo los productos agregados.

---

## 2. Jerarquía de Información

La distribución espacial de los elementos responde a una escala estricta de prioridad visual basada en la urgencia y frecuencia de lectura:

1. **Total a Pagar (Prioridad Máxima - Ultra destacado)**: Debe visualizarse de forma gigante en una zona exclusiva. Es el dato que el cajero lee en voz alta al cliente y que el cliente busca desesperadamente con la mirada.
2. **Buscador / Entrada de Escáner (Prioridad Alta - Foco principal)**: Campo de texto ancho y centrado en la pantalla que indica que el sistema está listo para registrar datos.
3. **Grilla del Carrito de Ventas (Prioridad Media - Control operativo)**: Muestra el listado de productos cargados. Permite al cajero verificar que los precios y cantidades escaneados coincidan con la mercadería física.
4. **Resumen e Información de Sesión (Prioridad Pasiva - Consulta)**: Datos como el cajero logueado, hora, estado de la red y del hardware. Se ubican en los márgenes de la pantalla.

---

## 3. Zonas de Atención

Clasificamos las zonas de la pantalla de la terminal en tres niveles de atención según el comportamiento esperado del operador:

```
+----------------------------------------------------------------------------------------------------+
| ZONAS DE ATENCIÓN EN LA INTERFAZ DEL POS                                                           |
+----------------------------------------------------------------------------------------------------+
| A) ATENCIÓN PERMANENTE (Campo de escaneo, grilla del carrito, total de venta).                     |
| B) ATENCIÓN OCASIONAL  (Favoritos/Buscador avanzado, panel de checkout, visor lateral consulta).   |
| C) ATENCIÓN PASIVA     (Usuario, caja, sincronización online, hora del sistema).                   |
+----------------------------------------------------------------------------------------------------+
```

- **A) Atención Permanente (Zona Central e Inferior Derecha)**:
  - *Elementos*: Grilla del carrito, barra de escaneo y cuadro de Total.
  - *Justificación*: El cajero pasa el 95% del tiempo de la jornada vigilando estas áreas para asegurar el ingreso correcto de productos y el cobro.
- **B) Atención Ocasional (Zonas Flotantes/Desplazables)**:
  - *Elementos*: Buscador avanzado (`F8`), visor lateral de precios (`F3`), cola de suspendidos (`F7`) y modal de checkout (`F12`).
  - *Justificación*: Solo demandan atención activa en momentos puntuales (ej. cuando se procesa el cobro o al resolver una consulta de precio).
- **C) Atención Pasiva (Márgenes Superior e Inferior)**:
  - *Elementos*: Identificador del cajero, caja activa, reloj del sistema y badges de red/hardware.
  - *Justificación*: Son metadatos de control y diagnóstico que el cajero solo mira en caso de fallas o para validar su turno.

---

## 4. Zonas Permanentes (Layout Fijo)

- **Barra Superior (Estructura de Control)**: Ubicada en el tope de la pantalla. Contiene datos de auditoría (`RN-001`, `RN-002`, `RN-003`). Su posición arriba a la izquierda y derecha sigue el estándar de cabeceras de sistemas operativos.
- **Área Central Izquierda (Grilla del Carrito)**: Ocupa el 70% del ancho de la pantalla y el 70% del alto. Es el bloque más grande.
  - *Justificación*: Permite visualizar hasta 10 o 12 líneas de productos simultáneamente sin hacer scroll.
- **Área Central Derecha (Favoritos / Panel Modular)**: Ocupa el 30% del ancho de pantalla.
  - *Justificación*: Ubicado a la derecha para facilitar la interacción rápida (por ser la mano derecha la dominante en la mayoría de los usuarios).
- **Barra de Entrada de Productos**: Situada justo encima de la grilla del carrito de ventas.
  - *Justificación*: Es el primer elemento de lectura al desplazar la mirada de arriba hacia abajo.
- **Caja de Totales (Monto de Pago)**: Ubicada en la esquina inferior derecha.
  - *Justificación*: Es el final natural del flujo visual en "Z" de lectura occidental.
- **Barra Inferior de Atajos**: Ubicada en la base. Funciona como un recordatorio visual de las teclas rápidas (`F1`-`F12`) para el cajero.

---

## 5. Zonas Dinámicas (Paneles Temporales)

Las zonas dinámicas se superponen o deslizan sobre las permanentes para evitar la navegación destructiva de pantallas:

- **Panel de Checkout (`F12` / `+`)**: Cubre de forma modal el panel central de favoritos y la caja de totales, pero **mantiene parcialmente visible el carrito de compras a la izquierda** con opacidad reducida (50%).
  - *Activación*: Se despliega al presionar `F12` o `+` con el carrito activo.
  - *Desactivación*: Se oculta presionando `ESC` o al confirmar el pago con `Enter`.
- **Visor Lateral de Consulta (`F3`)**: Desliza desde el lateral derecho cubriendo el panel de favoritos.
  - *Activación*: Al presionar `F3`.
  - *Desactivación*: Al presionar `ESC` o `F3` de nuevo.
- **Buscador Avanzado de Productos (`F8`)**: Modal centrado de tamaño mediano que cubre la grilla.
  - *Activación*: Al presionar `F8`.
  - *Desactivación*: Al presionar `ESC` o seleccionar un producto con `Enter`.
- **Cola de Suspendidas (`F7`)**: Panel modular flotante que aparece abajo de la barra de búsqueda.
  - *Activación*: Al presionar `F7`.
  - *Desactivación*: Al presionar `ESC` o seleccionar un ticket con `Enter`.

---

## 6. Distribución del Espacio y Proporciones

Para pantallas estándar de escritorio (relación de aspecto 16:9), la proporción del espacio de trabajo se divide de la siguiente manera:

- **Estructural Horizontal (Ancho)**:
  - **70%**: Área de Grilla de Venta, Barra de Búsqueda y Totales (flujo crítico).
  - **30%**: Área de Botonera de Favoritos o Paneles de Consulta Lateral.
  - *Justificación*: Maximiza el espacio horizontal para que los nombres de los productos no se trunquen en la grilla.
- **Estructural Vertical (Alto)**:
  - **8%**: Barra Superior de Control.
  - **77%**: Área de Grilla y Botonera.
  - **10%**: Área de Totales y Cobro.
  - **5%**: Barra Inferior de Atajos de Teclado.

### Proximidad y Separación
- **Cercanía del Buscador y la Grilla**: La barra de búsqueda de productos se ubica inmediatamente arriba de la grilla de ventas.
  - *Justificación*: El cajero escribe o escanea e inmediatamente baja la mirada al carrito para confirmar la inserción de la línea, minimizando la distancia de movimiento ocular.
- **Lejanía de Totales de la Zona de Registro**: Los botones de operaciones auxiliares (cierre, depósitos) se ubican lejos del área de totales y cobro.
  - *Justificación*: Evita pulsaciones erróneas de cierre de caja durante el cobro de un cliente.

---

## 7. Ergonomía Visual (Reducción de Fatiga)

Para garantizar la salud laboral del cajero durante turnos prolongados de 8 a 12 horas, CajaFácil define estas tres reglas de ergonomía visual en el wireframe:

1. **Agrupación en el Campo Visual Central (Fóvea)**: La línea activa del carrito (último producto escaneado) siempre debe hacer autoscroll hacia el centro o la parte superior visible de la grilla, evitando que el cajero deba forzar la mirada hacia la base física del monitor de forma repetitiva.
2. **Minimización de Giros de Cabeza**: El monitor debe estar centrado al cajero. El wireframe agrupa la barra de búsqueda, la lista de compra y los subtotales en la zona izquierda-centro para que el operador realice el control visual con un movimiento ocular de menos de **$15^\circ$** sin requerir giros del cuello.
3. **Contraste de Foco Activo**: El anillo de foco sobre el input activo debe poseer un grosor mínimo de 2px en azul acento, permitiendo que la visión periférica del cajero identifique la posición del cursor sin requerir escrutinio activo.

---

## 8. Flujo Visual (El Recorrido de la Mirada)

El recorrido natural de la mirada del cajero sigue una secuencia en forma de **"Z" modificada** adaptada al checkout rápido:

```
Paso 1: Barra Superior (Check de Estado) ------> Paso 2: Buscador Principal (Listo)
                                                        |
                                                        | (Escanear)
                                                        v
Paso 4: Total & Cobro (Confirmar) <------------- Paso 3: Grilla Carrito (Verificar)
```

1. **Inicio de venta (Paso 1)**: La mirada inicia arriba en la barra de búsqueda/escaneo para confirmar foco.
2. **Registro de Ítems (Paso 2)**: Al escanear, la mirada desciende a la grilla para verificar el precio y nombre del producto. Este ciclo (Paso 1 -> Paso 2) se repite por cada producto del carrito.
3. **Cobro (Paso 3)**: Al completar el registro, la mirada se desplaza a la esquina inferior derecha para leer el Total a pagar.
4. **Checkout (Paso 4)**: La mirada se enfoca en el modal de cobro superpuesto para registrar el efectivo y cambio, completando el flujo de venta.

---

## 9. Escaneo Continuo (Mantenimiento del Ritmo)

Durante secuencias largas de escaneo de productos (ej. un cliente con 30 artículos de supermercado), la interfaz se comporta de la siguiente manera para mantener el ritmo del cajero:

- **Scrollbar Automático Inteligente**: Si la grilla se llena, el POS desplaza la lista automáticamente hacia abajo para que el último producto escaneado permanezca visible en la penúltima fila de la grilla.
- **Indicador de Registro Exitoso**: Al escanear, la celda del producto insertado parpadea brevemente en un tono azul muy suave (`#EFF6FF`) durante **$200\text{ ms}$**. Esto da una confirmación visual pasiva de inserción sin interrumpir el foco.
- **Sin Popups de Alerta**: Las contingencias menores se resuelven de forma silenciosa (ej. si el stock está bajo, el badge de cantidad de la fila cambia a color ámbar de advertencia, pero no interrumpe el escaneo).

---

## 10. Densidad de Información

Para evitar la fatiga cognitiva, CajaFácil equilibra el espacio en pantalla:

- **Padding Ergonómico**: Las celdas de la grilla de ventas tienen un padding interno de **$12\text{ px}$** (`spacing_s`). Esto evita que los textos se toquen y permite una lectura rápida a $80\text{ cm}$ de distancia.
- **Monocromía de Control**: El 90% de las filas del carrito usan color de texto gris slate oscuro sobre fondo blanco. Solo se permiten colores para destacar estados críticos (rojo en descuentos o verde en pagos).
- **Prohibición de Espacio Vacío Inútil**: La grilla del carrito se expande verticalmente para ocupar todo el alto disponible de su zona. Si hay pocos ítems, se muestran filas vacías con líneas de división tenues (`#E2E8F0`) para mantener la estructura visual estable.

---

## 11. Información Persistente

Los siguientes datos son obligatorios y **jamás deben ser cubiertos** por ningún panel dinámico en el POS:

- **Cajero Activo (Auditoría)**: Identifica quién está operando (`RN-002`). Evita fraudes de suplantación en caja.
- **Caja y Sucursal Activas (Contexto)**: Ubicación del dinero físico.
- **Monto Total a Pagar**: Es la cifra guía de la venta. Debe permanecer visible incluso en checkout.
- **Cantidad de Productos/Unidades**: Suma total de unidades agregadas (ej. 3 productos, 5 unidades). Sirve para que el cajero compare la cantidad de productos físicos en el mostrador con los registrados en el sistema.
- **Estado de Sincronización (Online/Offline)**: Indica si las facturas se están guardando localmente o subiendo a la nube (`RN-802`).
- **Estado de Dispositivos (Impresora/Balanza)**: Permite alertar proactivamente antes de intentar imprimir.
- **Hora del Sistema**: Para control de turnos y arqueos.

---

## 12. Preparación para Múltiples Monitores

CajaFácil está diseñado para soportar configuraciones de doble pantalla en el mostrador:

1. **Pantalla Principal (Cajero)**: Muestra el wireframe estándar con todas las herramientas de edición, arqueo, favoritos y controles de checkout.
2. **Pantalla Secundaria (Visor de Cliente - Customer Display)**:
   - **Comportamiento**: Un hilo secundario del frontend proyecta una vista de lectura optimizada para el cliente.
   - **Estructura**:
     - *Lado Izquierdo*: Lista simplificada de compras (nombre, cantidad, total).
     - *Lado Derecho*: Caja gigante con el **Total a Pagar** y los impuestos desglosados. En la zona inferior, muestra el **Cambio (Vuelto)** calculado.
     - *Área de Reposo*: Si no hay venta activa, proyecta ofertas de la empresa o un mensaje de bienvenida.
     - *Seguridad*: Esta pantalla del cliente jamás muestra datos del cajero, alertas de error del sistema, botones de configuración, ni información de arqueo de caja.

---

## 13. Wireframes Conceptuales (Esquemas ASCII)

### A) Modo Venta (Estructura de Trabajo Principal)

```
+----------------------------------------------------------------------------------------------------+
| [Logo] CajaFácil POS | Sucursal: Principal | Caja: #1 | Cajero: Luis E.      [Online] [Imp: OK] 13:45|
+----------------------------------------------------------------------------------------------------+
|  CLIENTE: Consumidor Final (F2)          | BUSCAR PRODUCTO: [ 75010012                  ] (F8/Enter)|
+------------------------------------------+---------------------------------------------------------+
|  GRILLA DEL CARRITO DE VENTAS (70% Ancho)| BOTONERA FAVORITOS (30% Ancho)                          |
|  #   CODIGO    PRODUCTO        CANT  P.U.   DESC   TOTAL  | +-----------------+ +-----------------+ |
|  1   750100    Leche Sula 1L   2.0   32.00  0.00   64.00  | | [F4-1]          | | [F4-2]          | |
|  2   981240    Pan Bimbo 450g  1.0   48.00  2.00   46.00  | | Hielo Bolsa     | | Pan Blanco      | |
|  3   *BAL-03   Tomate (Granel) 1.25  24.00  0.00   30.00  | +-----------------+ +-----------------+ |
|  4                                                        | +-----------------+ +-----------------+ |
|  5                                                        | | [F4-3]          | | [F4-4]          | |
|  6                                                        | | Recarga L 50    | | Bolsa Kraft     | |
|  7                                                        | +-----------------+ +-----------------+ |
|  8                                                        |                                         |
|  9                                                        |                                         |
+-----------------------------------------------------------+-----------------------------------------+
|  Líneas: 3 | Unidades: 4.250                              | SUBTOTAL:                      L 140.00 |
|                                                           | IMPUESTOS (15%):                L 21.00 |
|  [DEL] Borrar Línea  | [F6] Suspender | [F7] Recuperar    | DESCUENTOS:                      L 2.00 |
|  [F3]  Consulta L.   | [F11] Caja     | [ESC] Cancelar    | TOTAL A PAGAR:                 L 159.00 |
+-----------------------------------------------------------+-----------------------------------------+
|  [F12] O [+] PROCEDER AL CHECKOUT (COBRAR) --------------------------------------------------------|
+----------------------------------------------------------------------------------------------------+
```

### B) Modo Cobro (Checkout Superpuesto - F12)

```
+----------------------------------------------------------------------------------------------------+
| [Logo] CajaFácil POS | Sucursal: Principal | Caja: #1 | Cajero: Luis E.      [Online] [Imp: OK] 13:46|
+----------------------------------------------------------------------------------------------------+
|  CLIENTE: Consumidor Final (F2)          | BUSCAR PRODUCTO: [                                      ]|
+------------------------------------------+---------------------------------------------------------+
|  GRILLA DEL CARRITO DE VENTAS (Opaco)    | +-----------------------------------------------------+ |
|  #   CODIGO    PRODUCTO        CANT      | | CHECKOUT DE PAGO - TOTAL: L 159.00                  | |
|  1   750100    Leche Sula 1L   2.0       | +-----------------------------------------------------+ |
|  2   981240    Pan Bimbo 450g  1.0       | | 1. EFECTIVO [F1] ---------------------------------  | |
|  3   *BAL-03   Tomate (Granel) 1.25      | |    Recibido: [ L 200.00         ]                   | |
|  4                                       | |    Cambio / Vuelto: L 41.00                         | |
|  5                                       | |    Sugeridos: [ L 159.00 ]  [ L 200.00 ]  [ L 500.00]  | |
|  6                                       | |                                                     | |
|  7                                       | | 2. TARJETA [F2] | 3. TRANSFERENCIA [F3]             | |
|  8                                       | | 4. CREDITO [F4]                                     | |
|  9                                       | +-----------------------------------------------------+ |
+------------------------------------------+ | COBERTURA: 100% (L 159.00 / L 159.00)                 | |
|  Líneas: 3 | Unidades: 4.250              | +-----------------------------------------------------+ |
|                                          | | [Enter] Confirmar Factura  | [ESC] Volver al Carrito| |
|  [DEL] Borrar Línea  | [ESC] Cancelar    | +-----------------------------------------------------+ |
+------------------------------------------+---------------------------------------------------------+
|  [F12] COBRANDO FACTURA ACTUAL...                                                                  |
+----------------------------------------------------------------------------------------------------+
```

### C) Modo Consulta Lateral (F3)

```
+----------------------------------------------------------------------------------------------------+
| [Logo] CajaFácil POS | Sucursal: Principal | Caja: #1 | Cajero: Luis E.      [Online] [Imp: OK] 13:47|
+----------------------------------------------------------------------------------------------------+
|  CLIENTE: Consumidor Final (F2)          | BUSCAR PRODUCTO: [ Leche                         ] (F3) |
+------------------------------------------+---------------------------------------------------------+
|  GRILLA DEL CARRITO DE VENTAS (Activo)   | PANEL DE CONSULTA DE PRECIOS Y STOCK (F3)               |
|  #   CODIGO    PRODUCTO        CANT  P.U.| +-----------------------------------------------------+ |
|  1   750100    Leche Sula 1L   2.0   32.0| | Producto: Leche Entera Sula 1L                      | |
|  2   981240    Pan Bimbo 450g  1.0   48.0| | Código: 75010012                                    | |
|                                          | | Precio Público: L 32.00                             | |
|                                          | | Impuesto: 15% (L 4.17 incluido)                     | |
|                                          | +-----------------------------------------------------+ |
|                                          | | Existencias locales: 45 unidades                    | |
|                                          | | Sucursal Norte: 12 unidades                         | |
|                                          | | Sucursal Sur: 8 unidades                           | |
|                                          | +-----------------------------------------------------+ |
|                                          | | [ESC] Cerrar Consulta y regresar al carrito         | |
+------------------------------------------+---------------------------------------------------------+
|  Líneas: 2 | Unidades: 3.0               | TOTAL A PAGAR:                                 L 110.00 |
+------------------------------------------+---------------------------------------------------------+
|  [F12] O [+] PROCEDER AL CHECKOUT (COBRAR) --------------------------------------------------------|
+----------------------------------------------------------------------------------------------------+
```

---

## 14. Validación por Escenarios

1. **Venta Rápida**: El cajero escanea continuamente. La mirada se fija en la barra de búsqueda y en el parpadeo azul de confirmación en la grilla. No hay modales interactivos. Distribución 100% eficiente.
2. **Venta Masiva**: El carrito supera los 30 productos. El autoscroll mantiene el foco visual en el penúltimo ítem agregado. La barra de totales se conserva fija abajo a la derecha sin desbordes.
3. **Checkout**: El panel de pago cubre la botonera de favoritos (área no crítica en este estado), pero deja visible el carrito de compras a la izquierda para resolver dudas finales del cliente sobre los productos facturados.
4. **Consulta**: Al presionar `F3`, el panel de consulta reemplaza la botonera de favoritos. El cajero responde existencias en otras sucursales al cliente sin perder los 5 productos que ya tenía escaneados en la grilla principal.
5. **Venta Suspendida**: Al presionar `F7`, se abre un panel flotante de suspendidas abajo de la barra de búsqueda. El cajero selecciona el ticket anterior usando el teclado y el carrito se repuebla de inmediato, manteniendo el total visible.
6. **Error de Hardware**: Si falla la ticketera, se despliega una alerta Toast pequeña en la esquina superior derecha sin bloquear el total o el buscador. El cajero continúa facturando.
