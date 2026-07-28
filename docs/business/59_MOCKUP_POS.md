---
id: CF-DOC-059
title: "Especificación: Mockups Oficiales del POS"
owner: "product-owner"
status: "approved"
last_reviewed: 2026-07-28
role: "dependent"
---

# Mockups Oficiales del POS de CajaFácil

> [!NOTE]
> Este documento depende de las especificaciones de la capacidad de Operación Diaria, el Design System, la Arquitectura UX y el Wireframe Funcional:
> - [Capacidad: Operación Diaria](file:///docs/business/55_ANALISIS_FUNCIONAL_OPERACION_DIARIA.md) (CF-DOC-055)
> - [Design System Oficial](file:///docs/business/56_DESIGN_SYSTEM.md) (CF-DOC-056)
> - [Arquitectura UX del POS](file:///docs/business/57_ARQUITECTURA_UX_POS.md) (CF-DOC-057)
> - [Wireframe Funcional del POS](file:///docs/business/58_WIREFRAME_FUNCIONAL_POS.md) (CF-DOC-058)

---

## 1. Introducción

Esta especificación constituye el Mockup Oficial del POS de CajaFácil. Transpone de manera fiel e integrada las pautas del Design System, la lógica secuencial de la Arquitectura UX y la distribución ergonómica del Wireframe Funcional. Su objetivo es servir como la guía visual definitiva de alta fidelidad para el equipo de desarrollo frontend de la aplicación de escritorio (`desktop_app` en Flutter), eliminando cualquier margen de improvisación visual en la etapa de codificación.

De acuerdo con las directrices de producto, los activos de diseño visual de alta fidelidad generados no se incrustan como imágenes directas en el cuerpo de este texto, sino que se almacenan como archivos independientes en el directorio de activos del proyecto (`docs/assets/`), quedando referenciados formalmente en cada sección por su ruta física correspondiente.

---

## 2. Catálogo Oficial de Componentes Nombrados

Para facilitar el mapeo de la interfaz en widgets reutilizables de Flutter, se definen los siguientes nombres conceptuales oficiales para cada componente de la pantalla principal del POS:

1. **`POSTopBar` (Barra Superior de Control)**: Cabecera fija que expone los metadatos contextuales (empresa, sucursal, caja, cajero, estado de sincronización y estado de periféricos).
2. **`ProductSearchField` (Campo de Búsqueda Principal)**: Input de texto ancho de foco persistente en la parte superior-izquierda del área de trabajo.
3. **`SaleGrid` (Grilla de Compra / Carrito)**: Tabla interactiva que lista los productos cargados, precios, cantidades, descuentos y totales por línea.
4. **`FavoritesPanel` (Botonera de Favoritos)**: Cuadrícula lateral derecha de botones rápidos para registrar productos sin código de barras (favoritos del mostrador).
5. **`TotalsPanel` (Panel de Resumen e Importes)**: Contenedor gigante en la esquina inferior derecha que detalla el Subtotal, Descuentos, Impuesto y el Total a Pagar en tipografía de alto impacto.
6. **`QuickActionsBar` (Barra de Atajos Rápidos)**: Franja horizontal en la base de la pantalla que enlista la guía de teclas de función (`F1` a `F12`, `ESC`, `DEL`).
7. **`CheckoutDialog` (Ventana de Cobro / Checkout)**: Panel modal superpuesto que aparece al cobrar, bloqueando el carrito de forma pasiva a la izquierda.
8. **`QuerySidebar` (Visor de Consulta Lateral)**: Panel deslizante desde el lateral derecho que sustituye temporalmente a `FavoritesPanel` para verificar stock e impuestos.
9. **`SuspendedQueuePanel` (Visor de Cola Suspendida)**: Lista emergente local que despliega los tickets suspendidos en espera para reanudar el cobro.
10. **`ToastNotification` (Notificación Flotante Toast)**: Mensaje no intrusivo auto-desvanecible para avisos informativos (ej. producto inexistente, atasco de papel).
11. **`ConfirmDialog` (Diálogo de Confirmación Destructiva)**: Ventana emergente con overlay de fondo negro opaco para autorizaciones críticas o cancelación del carrito.
12. **`StatusBar` (Barra de Estados Técnicos)**: Sub-sección en el `POSTopBar` que dibuja los badges de red, sincronización y conexión de hardware.

---

## 3. Mockup 1: Vista Principal (`pos_main_view`)

- **Archivo de Activo Visual (Alta Fidelidad)**: [docs/assets/pos_main_view.jpg](file:///c:/Users/User/Desktop/CajaFacil/docs/assets/pos_main_view.jpg)
- **Objetivo**: Diseñar la interfaz principal de facturación diaria optimizada para uso continuo.
- **Escenario**: Cajero registrando un carrito activo con tres artículos (leche, pan, tomate a granel). El foco del cursor se encuentra en `ProductSearchField`.
- **Decisiones de Diseño**:
  - **Distribución de Columnas**: Relación horizontal 70% para el flujo crítico de facturación (`ProductSearchField` y `SaleGrid`) y 30% a la derecha para `FavoritesPanel`. Esto mantiene el foco de atención del operador en la mitad izquierda-centro de la pantalla.
  - **SaleGrid Compacta**: Celdas con espaciado de 12px (`spacing_s`) para mostrar la descripción y detalles completos del producto sin necesidad de scroll horizontal.
  - **Visualización de Totales**: El cuadro `TotalsPanel` utiliza el gris pizarra profundo (`#1E293B`) como fondo para contrastar fuertemente las letras blancas de la cifra total en tamaño 32sp, convirtiéndolo en el punto de mayor peso visual de la interfaz.
- **Relación con Design System y Arquitectura UX**:
  - Aplica los tokens `font_family_numeric` (JetBrains Mono) en la grilla para la alineación decimal de precios y totales.
  - Garantiza que la fila activa seleccionada en `SaleGrid` se visualice en fondo azul claro (`#EFF6FF`) con un borde izquierdo acentuado.

---

## 4. Mockup 2: Vista de Checkout (`pos_checkout_view`)

- **Archivo de Activo Visual (Alta Fidelidad)**: [docs/assets/pos_checkout_view.jpg](file:///c:/Users/User/Desktop/CajaFacil/docs/assets/pos_checkout_view.jpg)
- **Objetivo**: Diseñar el modal superpuesto de cobros multimétodo.
- **Escenario**: Proceso de cobro de un ticket por un total de L 159.00 liquidándose con L 200.00 en efectivo, mostrando un cambio de L 41.00.
- **Decisiones de Diseño**:
  - **Superposición No Destructiva**: El componente `CheckoutDialog` cubre el 40% derecho de la pantalla, sustituyendo `FavoritesPanel` y superponiéndose a `TotalsPanel`. Sin embargo, `SaleGrid` a la izquierda permanece 100% visible con una opacidad reducida al 50%. Esto permite que el cajero confirme visualmente los ítems cobrados ante una duda de último segundo del cliente.
  - **Foco de Entrada**: El foco se sitúa de forma automática en el input numérico "Efectivo Recibido".
  - **Cambio Gigante**: El vuelto/cambio calculado se proyecta en color verde éxito (`#10B981`) con tamaño 32sp para facilitar su lectura inmediata a $80\text{ cm}$.
- **Relación con Design System y Arquitectura UX**:
  - Utiliza los botones de atajo rápidos (`F1` para Efectivo, `F2` para Tarjeta, etc.) debidamente etiquetados en la cabecera del input.
  - Aplica la escala de grises suave (`#F8FAFC` y `#E2E8F0`) en el modal para no competir con el brillo del total a cobrar.

---

## 5. Mockup 3: Vista de Consulta Lateral (`pos_query_view`)

- **Archivo de Activo Visual (Alta Fidelidad)**: [docs/assets/pos_query_view.jpg](file:///c:/Users/User/Desktop/CajaFacil/docs/assets/pos_query_view.jpg)
- **Objetivo**: Diseñar el visor lateral deslizante de precios y existencias en caliente.
- **Escenario**: Cajero verifica el precio de "Leche Sula 1L" y consulta stock disponible en sucursales vecinas sin salir del carrito activo de ventas.
- **Decisiones de Diseño**:
  - **Deslizamiento Lateral**: El componente `QuerySidebar` se desliza desde el lateral derecho cubriendo `FavoritesPanel`. `SaleGrid` y el buscador principal a la izquierda no se modifican ni se ocultan.
  - **Desglose de Stock**: Muestra de forma legible el stock local en la sucursal actual (45 un) y un desglose de las sucursales del tenant (Sucursal Norte: 12 un, Sucursal Sur: 8 un) utilizando tipografía monoespaciada para alineación rápida.
- **Relación con Design System y Arquitectura UX**:
  - Al presionar `ESC` el panel se oculta y el foco regresa de forma inmediata al `ProductSearchField` de la venta activa sin clics.
  - Respeta el token `spacing_m` (16px) como padding general de separación de campos del panel.

---

## 6. Vista de Venta Suspendida (UI / Comportamiento)

- **Objetivo**: Visualizar y recuperar tickets suspendidos de forma ágil.
- **Escenario**: El cajero presiona `F7` y se despliega `SuspendedQueuePanel`.
- **Decisión de Diseño Visual**:
  - El panel se despliega como una lista emergente (popover) justo debajo de la barra de búsqueda `ProductSearchField`.
  - Cada fila de la cola suspendida muestra el número correlativo local (ej. *Ticket #01*), el subtotal, la hora de suspensión y la cantidad de artículos.
  - El primer ticket de la lista se resalta por defecto en fondo gris suave. El cajero navega la cola con las flechas del teclado y presiona `Enter` para cargarlo, borrando la ventana emergente e inyectando los ítems en `SaleGrid` instantáneamente.

---

## 7. Vista de Venta Masiva (UI / Comportamiento)

- **Objetivo**: Mantener el ritmo del cajero y la visibilidad de datos durante ventas extensas (más de 30 productos).
- **Escenario**: Carrito saturado que excede el alto físico de `SaleGrid`.
- **Decisión de Diseño Visual**:
  - La cabecera de `SaleGrid` permanece fija. Solo el cuerpo de la grilla tiene scroll vertical.
  - Se añade un scrollbar táctil ancho de color gris medio (`#CBD5E1`) a la derecha de la grilla que se hace visible de forma permanente al superar las 8 líneas de venta.
  - Cuando se escanea un producto número 9, la lista hace autoscroll hacia abajo de forma instantánea. La fila del producto recién agregado se posiciona en la penúltima línea visible y parpadea en color azul suave `#EFF6FF` durante 200ms para confirmar la recepción visual.

---

## 8. Vista de Error Recuperable (UI / Comportamiento)

- **Objetivo**: Emitir advertencias sin romper el flujo de escaneo del cajero.
- **Escenario**: El lector escanea un producto no registrado en la base local o la impresora se queda sin papel térmico.
- **Decisión de Diseño Visual**:
  - Para código inexistente: No se abren popups centrales. Se dibuja una alerta tipo Toast en la esquina superior derecha (`ToastNotification`) con fondo rojo suave y letras blancas, acompañada de un bip sonoro corto. El foco del teclado **se mantiene** en `ProductSearchField`. El cajero puede seguir escaneando.
  - Para impresora desconectada: Se activa un badge amarillo permanente en el `StatusBar` (Barra de Estados) de la cabecera `POSTopBar`. El cajero factura normalmente y la factura se almacena en la cola local de spooler en segundo plano.

---

## 9. Validación Ergonómica del Diseño

La combinación de colores neutrales de la paleta Slate y la distribución espacial de los componentes optimiza la ergonomía del cajero:
- **Reducción de Fatiga Ocular**: Al evitar el color negro puro en el fondo y favorecer un tema claro de bajo contraste (`#F8FAFC` de fondo y `#1E293B` de texto), se previene el cansancio de la pupila por variaciones drásticas de luz ambiental.
- **Movimiento de Cuello $0^\circ$**: El agrupamiento del buscador principal y el carrito a la izquierda del monitor asegura que el operador realice el control visual utilizando la visión fóvea central sin necesidad de rotar el cuello durante el día.

---

## 10. Validación del Mockup en Resoluciones Adaptativas

### A) Resolución Desktop Full HD (1920x1080)
- **Estructura**: Visualización óptima de 5 áreas completas.
- **Grilla**: `SaleGrid` expone con comodidad las 8 columnas del detalle y permite ver hasta 12 líneas de productos al mismo tiempo sin necesidad de hacer scroll. `FavoritesPanel` muestra una botonera de hasta 16 favoritos con espaciado de 16px.

### B) Resolución Laptop (1366x768)
- **Estructura**: El ancho se optimiza de forma automática reduciendo la separación interna.
- **Adaptabilidad**:
  - `FavoritesPanel` colapsa su ancho un 10% y el padding de la botonera disminuye a 8px (`spacing_xs`) para evitar desbordes.
  - `SaleGrid` oculta la columna "Código Interno" si el ancho del monitor es crítico, conservando visibles únicamente los datos comerciales esenciales (Nombre, Cantidad, Precio, Descuento, Total).
  - La tipografía general se escala automáticamente en 2 puntos (ej. cuerpo pasa de 14sp a 12sp) para mantener la consistencia sin desbordamientos de cajas.

---

## 11. Validación del Mockup por Tipo de Negocio

El mockup se adapta a cada perfil de comercio minorista modificando la composición de la botonera lateral `FavoritesPanel` y la grilla `SaleGrid`:

1. **Minisúper / Tienda de Conveniencia**:
   - `FavoritesPanel` se destina a productos de alta rotación sin código (hielo, recargas telefónicas rápidas).
   - `SaleGrid` opera en modo de cantidad unitaria estándar y escaneo continuo veloz.
2. **Ferretería**:
   - `FavoritesPanel` se desactiva por completo o se minimiza para priorizar el ancho de `SaleGrid`.
   - `SaleGrid` muestra campos de cantidad con soporte decimal (ej. clavos en libras o metros de alambre) y precios fraccionados.
3. **Farmacia**:
   - `FavoritesPanel` se reemplaza por el panel lateral de consultas `QuerySidebar` fijo, que solicita obligatoriamente el Lote y Fecha de Vencimiento de cada producto agregado a `SaleGrid`.
4. **Pulpería**:
   - `FavoritesPanel` muestra una rejilla de botones grandes de los productos cotidianos de refrigerador y panadería para registrar ventas rápidas de 1 clic táctil.
   - El cobro rápido de efectivo se resalta en el panel inferior.
