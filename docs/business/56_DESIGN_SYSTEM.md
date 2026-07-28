---
id: CF-DOC-056
title: "Especificación: Design System Oficial"
owner: "product-owner"
status: "approved"
last_reviewed: 2026-07-28
role: "canonical"
---

# Design System Oficial de CajaFácil

> [!NOTE]
> Este documento constituye la especificación definitiva y canónica de la identidad visual, el comportamiento de los componentes y las directrices de interacción (UX/UI) del producto CajaFácil. Es de cumplimiento obligatorio para todas las plataformas del ecosistema POS.

---

## 1. Filosofía Visual

La filosofía visual de CajaFácil está diseñada para responder a la realidad de su entorno operativo: mostradores comerciales de alto tráfico en América Latina (pulperías, ferreterías, farmacias, tiendas de conveniencia).

### A) Personalidad del Producto
CajaFácil debe proyectarse como una herramienta **profesional, confiable, ágil y limpia**. No es una aplicación decorativa ni de entretenimiento. Su diseño elimina todo ruido visual superfluo (degradados pesados, ilustraciones genéricas de relleno, sombras excesivas) para centrar la atención del usuario en los datos comerciales y de facturación.

### B) Sensación que Transmite
- **Agilidad**: El cajero debe sentir que el sistema responde de forma instantánea al teclado.
- **Control y Seguridad**: Estabilidad financiera y control de caja estricto mediante contrastes claros y tipografías legibles.
- **Confort Ocular**: Mitigación del cansancio visual durante jornadas laborales de más de 8 o 12 horas consecutivas frente a la pantalla.

### C) Perfil del Usuario
El operador del POS suele ser un cajero de tienda o el mismo dueño del negocio, cuyo rango de edad y alfabetización digital es sumamente amplio.
- **Cero fricción de inicio**: La interfaz debe requerir una capacitación mínima o nula.
- **Operación sin mouse**: El usuario experto operará mediante memoria muscular utilizando atajos de teclado.
- **Diseño táctil accesible**: En terminales táctiles, los objetivos de toque (touch targets) deben ser lo suficientemente amplios para evitar pulsaciones erróneas.

### D) Prioridades de Diseño (Jerarquía de Valor)
$$\text{Velocidad} > \text{Claridad de Datos} > \text{Simplicidad} > \text{Estética Decorativa}$$
Cualquier propuesta visual que ralentice el procesamiento de la venta o que consuma espacio de pantalla de forma improductiva queda descartada automáticamente.

---

## 2. Principios de Diseño

1. **Simplicidad Absoluta**: Cada pantalla debe mostrar únicamente los elementos necesarios para completar la tarea actual. El área del mostrador se limpia de banners o menús secundarios no relacionados con la facturación.
2. **Rapidez Extrema**: Los componentes visuales y transiciones de pantalla deben procesarse en milisegundos. Se prohíben animaciones complejas que dilaten la carga del POS.
3. **Consistencia Rígida**: Un botón de acción principal o un campo de texto debe verse y comportarse exactamente igual en el módulo de Ventas, de Inventario o de Clientes.
4. **Bajo Costo de Aprendizaje**: Los patrones de interacción deben ser estándar (ej. el color verde para confirmar/éxito, el rojo para cancelar/peligro).
5. **Accesibilidad Integrada**: Contraste de texto y elementos gráficos cumpliendo los estándares de legibilidad WCAG AA en todo momento.
6. **Prioridad al Teclado**: Todo componente interactivo expuesto en pantalla debe contar con un foco visible y un atajo de teclado asociado y rotulado de forma clara.

---

## 3. Sistema de Colores Oficial

El sistema de colores de CajaFácil utiliza la escala de grises para el 90% de la interfaz, reservando los tonos de color puro para estados críticos, acentos y llamadas a la acción (Call to Action - CTA).

```
+-----------------------------------------------------------------------------------+
| PALETA DE COLORES SEMÁNTICOS (HSL / HEX)                                          |
+-----------------------------------------------------------------------------------+
|  [Primario Slate]       HEX #1E293B  | HSL 215, 25%, 17% | Cabeceras y Textos    |
|  [Secundario Slate]     HEX #475569  | HSL 215, 16%, 34% | Sub-bordes e Iconos   |
|  [Acento/Acción]        HEX #3B82F6  | HSL 217, 91%, 60% | Botón Principal / Foco|
|                                                                                   |
|  [Estado: Éxito]        HEX #10B981  | HSL 162, 76%, 41% | Ventas Completadas    |
|  [Estado: Error]        HEX #EF4444  | HSL   0, 84%, 60% | Alertas y Cancelación |
|  [Estado: Advertencia]  HEX #F59E0B  | HSL  38, 92%, 50% | Stock Bajo / Offline  |
|  [Estado: Información]  HEX #06B6D4  | HSL 188, 86%, 43% | Guías / Ayudas        |
|                                                                                   |
|  [Fondo Principal]      HEX #F8FAFC  | HSL 210, 40%, 98% | Fondo Pantalla POS    |
|  [Fondo Tarjeta/Grid]   HEX #FFFFFF  | HSL   0,  0%,100% | Grilla del Carrito    |
|  [Bordes / Divisores]   HEX #E2E8F0  | HSL 212, 33%, 89% | Líneas de División    |
+-----------------------------------------------------------------------------------+
```

### Justificación de la Paleta
- **Primario Slate (Charcoal Deep)**: Un gris pizarra profundo en lugar de negro puro. Reduce el destello de la pantalla en entornos cerrados y proporciona una estética de software empresarial moderna y neutral.
- **Acento Azul (Blue Accent)**: El azul es el color universal para representar acción sin los sesgos de peligro (rojo) o éxito (verde). Guía el ojo del cajero hacia el botón de cobro.
- **Gris de Fondo (Slate White/F8FAFC)**: Mantiene las tarjetas blancas elevadas con excelente contraste sin fatigar el ojo del operador.
- **Rojo/Verde Semánticos**: Alineados con la memoria cognitiva habitual del operador (Verde = Dinero que ingresa; Rojo = Alerta de error o salida de efectivo).

---

## 4. Tipografía y Jerarquía

La tipografía debe asegurar una lectura rápida a una distancia de **$60\text{ a }80\text{ cm}$** del monitor del mostrador.

- **Fuente Oficial**: **Inter** (o en su defecto, Outfit). Una tipografía sans-serif de geometría limpia y excelente legibilidad en pantallas digitales medianas y pequeñas.
- **Fuente para Números e Importes**: **JetBrains Mono** (o Roboto Mono). Tipografía monoespaciada obligatoria para grillas de ventas, precios, subtotales y cantidades.
  - *Justificación*: Los caracteres con ancho idéntico garantizan que las comas decimales y los dígitos se alineen perfectamente de forma vertical en las columnas de las tablas, facilitando la suma visual rápida del cajero.

### Escala de Textos (Jerarquía)

| Nivel de Jerarquía | Tamaño | Peso (Weight) | Uso Recomendado | Fuente |
| :--- | :--- | :--- | :--- | :--- |
| **Título Gigante (Total)** | 32 sp | Bold (700) | Monto Total de Pago (Checkout/Mostrador) | JetBrains Mono |
| **Título Principal (Sección)**| 20 sp | SemiBold (600)| Título de Paneles y Modales | Inter |
| **Cabecera de Tabla** | 12 sp | Medium (500) | Columnas de la Grilla de Ventas | Inter |
| **Contenido de Tabla (Texto)** | 14 sp | Regular (400) | Nombre del Producto en Carrito | Inter |
| **Contenido de Tabla (Número)**| 14 sp | Regular (400) | Precios, Cantidades y Subtotales | JetBrains Mono |
| **Etiqueta de Botón** | 14 sp | SemiBold (600)| Texto de Botones y Acciones de Teclado | Inter |
| **Texto de Toast/Notificación**| 12 sp | Regular (400) | Alertas informativas auto-desvanecibles | Inter |
| **Badge / Indicador** | 10 sp | Bold (700) | Etiquetas de estado (Offline, Sincronizado)| Inter |

---

## 5. Sistema de Espaciado (Spacing Scale)

Para mantener una consistencia matemática en los layouts y evitar el apiñamiento visual, CajaFácil adopta una escala de espaciado basada en múltiplos de **$4\text{ px}$**.

```
+---------------------------------------------------------------------------------+
| ESCALA DE ESPACIADO OFICIAL                                                     |
+---------------------------------------------------------------------------------+
|  4 px  | Spacing-XXS | Relleno interno de badges, micro-separaciones.           |
|  8 px  | Spacing-XS  | Relleno de botones pequeños, espacio entre label e input. |
| 12 px  | Spacing-S   | Margen interno de celdas de tabla (padding denso).       |
| 16 px  | Spacing-M   | Padding estándar de tarjetas y contenedores de panel.   |
| 24 px  | Spacing-L   | Separación de columnas de Grid y paneles estructurales.  |
| 32 px  | Spacing-XL  | Margen externo de pantallas principales.                 |
| 48 px  | Spacing-XXL | Separación entre bloques de checkout de alto impacto.    |
+---------------------------------------------------------------------------------+
```

---

## 6. Sistema de Grid y Alineación

CajaFácil utiliza una rejilla (grid) de **12 columnas** flexible para estructurar la interfaz.

### Reglas de Alineación de Datos (Mandatorias)
1. **Alineación a la Izquierda**:
   - Descripciones de productos, categorías, nombres de clientes y textos informativos descriptivos.
2. **Alineación a la Derecha**:
   - **Todos los valores numéricos y monetarios** (cantidades, precios unitarios, porcentajes de descuento, subtotales, totales).
   - *Justificación*: El ojo lee cifras numéricas alineadas a la derecha de forma natural de acuerdo al orden decimal.
3. **Alineación al Centro**:
   - Códigos de barra, códigos internos, folios de facturas, fechas de creación y estados de sincronización.

---

## 7. Componentes Oficiales y sus Estados

Todos los componentes deben reaccionar visualmente a las interacciones del cajero. Se definen a continuación las guías de comportamiento e identidad visual por estado:

### A) Botones (Buttons)
- **Estados Requeridos**:
  - *Normal*: Color sólido de fondo.
  - *Hover*: Aumento de brillo/oscuridad en un 10%. Cursor cambia a pointer.
  - *Focus*: Borde de acento exterior de 2px de grosor (color azul `#3B82F6` con separación de 2px).
  - *Disabled*: Opacidad del 40%, fondo gris plano (`#E2E8F0`), cursor no-allowed. El atajo de teclado asociado deja de responder.
  - *Loading*: Reemplaza el texto por un spinner circular concéntrico sin alterar el tamaño del botón.
- **Tipos de Botones**:
  - *Primary (Cobro/F12)*: Fondo azul acento, letras blancas.
  - *Secondary (Acciones comunes)*: Fondo gris suave, letras oscuras slate.
  - *Destructive (Cancelar/Anular)*: Fondo rojo error, letras blancas.

### B) Campos de Texto / Inputs
- **Estados Requeridos**:
  - *Normal*: Fondo blanco, borde de 1px gris suave (`#CBD5E1`).
  - *Hover*: Borde gris medio.
  - *Focus*: **Borde azul acento de 2px de grosor**. El foco debe ser sumamente llamativo visualmente.
  - *Error*: Borde rojo de 2px con texto de ayuda de error inferior en el mismo color.
  - *Disabled*: Fondo gris sólido (`#F1F5F9`), texto gris suave.
- **Comportamiento**: Al enfocarse en un input numérico (ej. Cantidad), el valor existente debe autoseleccionarse completo para permitir la sobreescritura rápida sin necesidad de presionar borrar de forma manual.

### C) Tablas (Grillas de Ventas)
- **Estructura**: Cabecera en gris Slate, filas con fondo blanco alternado con gris claro (`#F8FAFC`) para diferenciar líneas.
- **Estados**:
  - *Fila Seleccionada*: Resaltada con un fondo azul claro suave (`#EFF6FF`) y borde izquierdo de 4px color azul acento. Indica de forma inequívoca qué producto se modificará al presionar `F5` o `DEL`.

### D) Badges / Etiquetas de Estado
- **Comportamiento**: Contenedores pequeños y redondeados para mostrar estados breves.
- **Semántica**:
  - *Offline*: Fondo amarillo claro, texto amber.
  - *Sincronizado*: Fondo verde claro, texto éxito.
  - *Bloqueado/Inactivo*: Fondo gris claro, texto gris.

### E) Toasts (Notificaciones Emergentes)
- **Comportamiento**: Aparecen en la esquina superior derecha, duran **3 segundos** y se desvanecen automáticamente. Tienen un botón "X" para cierre manual inmediato.
- **Semántica**: Éxito (ingreso correcto), Error (acción no autorizada), Información (ayudas de teclado).

### F) Diálogos / Ventanas Modales
- **Comportamiento**: Superpuestos con un fondo oscurecido translúcido (overlay de 50% opacidad negra). Bloquean la interacción inferior.
- **Regla**: Deben contener un botón claro de confirmación (derecha) y de cancelación (izquierda), mapeados por teclado a `Enter` y `ESC` respectivamente.

### G) Tarjetas (Cards)
- **Comportamiento**: Fondo blanco puro, bordes redondeados y una sombra de elevación muy sutil (`0 1px 3px rgba(0,0,0,0.05)`).
- **Uso**: Agrupador de paneles lógicos (resumen de totales, catálogo rápido).

### H) Barras de Búsqueda
- **Comportamiento**: Ocupa el foco primario de la pantalla. Cuenta con un icono de lupa a la izquierda y un badge de atajo rotulado a la derecha (ej. `F8` o `Enter`).

---

## 8. Iconografía Oficial

CajaFácil adopta un estilo de iconos de **línea delgada y minimalista** (Lucide Icons o Feather Icons).

- **Reglas de Uso**:
  - **No usar iconos huérfanos**: Las acciones de control (ej. guardar, borrar, arqueo) no deben mostrar únicamente un icono sin texto aclaratorio de su atajo o nombre.
  - **Tamaño Estándar**: **24 dp** para la interfaz general, **20 dp** para tablas densas de datos.
  - **Color**: Deben heredar el color semántico de su estado (ej. un icono de advertencia debe ser ámbar).

---

## 9. Animaciones y Transiciones

La velocidad operativa es el valor supremo de la interfaz. Las animaciones se restringen a micro-interacciones sutiles para dar retroalimentación de estado:

- **Transición de Foco**: Desvanecido de borde de input (fade) de **100 ms**.
- **Entrada de Toasts**: Desplazamiento lateral rápido desde la derecha de **150 ms** con curva de facilidad de salida (ease-out).
- **Apertura de Modales**: Escalado sutil del 95% al 100% de **150 ms** (ease-out).

### Cuándo NO usar animaciones (Prohibición)
- **Grilla de Ventas**: Los productos escaneados deben aparecer instantáneamente en el carrito. Queda prohibido cualquier efecto de desvanecimiento o animación de entrada para los ítems de la grilla.
- **Checkout**: El panel de checkout debe superponerse de inmediato al presionar la tecla rápida, sin retardos de desplazamiento o animaciones dramáticas.

---

## 10. Layout y Distribución Estructural de Pantallas

La pantalla del POS Desktop/Laptop se divide de forma predecible en las siguientes 5 áreas principales:

```
+-----------------------------------------------------------------------------------+
| 1. BARRA SUPERIOR (Info del sistema, usuario, sucursal, estado de sincronización) |
+------------------------------------------------------------------+----------------+
|                                                                  |                |
|                                                                  | 3. PANEL       |
|                                                                  |    LATERAL     |
|                                                                  |    ACCIONES /  |
| 2. CONTENIDO PRINCIPAL (Grilla del carrito activo)               |    FAVORITOS   |
|    (Ocupa el 70% del ancho de pantalla)                          |    (30% ancho) |
|                                                                  |                |
|                                                                  |                |
|                                                                  |                |
+------------------------------------------------------------------+----------------+
| 4. PANEL INFERIOR DE ACCIONES RÁPIDAS (Atajos de teclado, F1..F12)                |
+-----------------------------------------------------------------------------------+
| 5. AREA DE TOTALES Y COBRO (F12)                                                  |
+-----------------------------------------------------------------------------------+
```

1. **Barra Superior**: Fija en todo momento. Muestra el logo, el nombre de la empresa/sucursal activa, el nombre del cajero logueado, y el estado de sincronización (Online/Offline).
2. **Contenido Principal (Área de Trabajo)**: Muestra la grilla de productos en el carrito de compras en curso. Debe tener scroll independiente y scrollbar visible.
3. **Panel Lateral**: Panel modular de doble comportamiento:
   - *Modo Catálogo*: Grid de botones rápidos para productos favoritos sin código de barras.
   - *Modo Resumen*: Muestra detalles de la última venta, el saldo disponible del cliente nominado o la cola de tickets suspendidos en espera.
4. **Panel Inferior de Acciones**: Muestra de forma constante la leyenda de atajos de teclado disponibles en la pantalla activa para guiar visualmente al operador.
5. **Área de Totales**: Caja gigante en la esquina inferior derecha que resalta el Subtotal, Impuestos, Descuentos y el **Total a Pagar** en tipografía JetBrains Mono de 32sp.

---

## 11. Responsive y Adaptabilidad

El POS de CajaFácil debe garantizar la ergonomía operativa en diferentes formatos de visualización física:

- **POS Desktop (1920x1080 / 1080p)**: Distribución estándar completa de 5 áreas con panel lateral y grid de favoritos desplegado simultáneamente.
- **Laptop (1366x768)**: El panel lateral se colapsa automáticamente en un menú flotante para priorizar la visibilidad de las columnas de la grilla del carrito de ventas. El tamaño de la fuente se ajusta de forma adaptativa.
- **Pantallas Táctiles (POS Integrados/Tablets)**:
  - Los botones interactivos aumentan su tamaño a un área mínima de **$48\text{ px } \times 48\text{ px}$** (tamaño de toque ergonómico mínimo).
  - Se habilitan áreas de scroll táctil más generosas y se auto-despliega el teclado numérico en pantalla al enfocar campos de cantidades o cobros.
- **Móviles (Futura app de inventario/ventas rápidas)**: El layout se reduce a una sola columna vertical. El carrito se visualiza en formato de lista simplificada y el checkout se despliega como una pantalla de paso completo en lugar de un modal superpuesto.

---

## 12. Accesibilidad (WCAG AA)

- **Contraste de Color**: La relación de contraste para el texto principal y los elementos interactivos debe ser de al menos **$4.5:1$** sobre el fondo del contenedor.
- **Navegación por Teclado Silenciosa**: El uso de las teclas de tabulación (`Tab` / `Shift+Tab`) no debe quedar atrapado en bucles infinitos dentro de los paneles.
- **Indicador de Foco Inequívoco**: Todo elemento enfocado activamente por teclado debe resaltar con un anillo de borde de color azul acento de 2px de grosor. El foco nunca debe ser invisible.
- **Compatibilidad con Escala de Fuentes**: El POS debe tolerar la escala de fuentes del sistema operativo (hasta un 150%) sin desbordar los textos de las celdas de las tablas o encimarse sobre las etiquetas de los botones.

---

## 13. Catálogo Conceptual de Design Tokens

Los tokens de diseño son las variables abstractas e independientes de la tecnología de programación que definen la coherencia visual de CajaFácil.

### Tokens de Color
- `color_primary`: `#1E293B` (Gris profundo Slate para textos principales y cabeceras)
- `color_secondary`: `#475569` (Gris medio para textos descriptivos y bordes activos)
- `color_accent`: `#3B82F6` (Azul para foco y llamadas a la acción)
- `color_success`: `#10B981` (Verde para ventas e ingresos confirmados)
- `color_error`: `#EF4444` (Rojo para alertas, cancelaciones y egresos)
- `color_warning`: `#F59E0B` (Ámbar para stock bajo y offline)
- `color_bg_main`: `#F8FAFC` (Fondo gris claro del POS)
- `color_bg_card`: `#FFFFFF` (Fondo blanco de elementos elevados)
- `color_border`: `#E2E8F0` (Gris muy suave para bordes y divisores)

### Tokens de Tipografía
- `font_family_base`: `"Inter", sans-serif`
- `font_family_numeric`: `"JetBrains Mono", monospace`
- `font_size_title_lg`: `32sp`
- `font_size_title_md`: `20sp`
- `font_size_body`: `14sp`
- `font_size_caption`: `12sp`
- `font_weight_regular`: `400`
- `font_weight_semibold`: `600`
- `font_weight_bold`: `700`

### Tokens de Espaciado y Estructura
- `spacing_xxs`: `4px`
- `spacing_xs`: `8px`
- `spacing_s`: `12px`
- `spacing_m`: `16px`
- `spacing_l`: `24px`
- `spacing_xl`: `32px`
- `border_radius_s`: `4px` (Esquinas de botones e inputs)
- `border_radius_m`: `8px` (Esquinas de tarjetas y diálogos modales)
- `elevation_low`: `0 1px 3px rgba(0,0,0,0.05)` (Sombra para separar elementos en grilla)

---

## 14. Tema Oscuro (Dark Theme)

### Beneficios
- **Reducción de Fatiga Ocular**: En turnos nocturnos o en comercios con poca luz natural (ej. bares, bodegas de abarrotes cerradas), las pantallas blancas emiten un exceso de luz azul que cansa la vista rápidamente.
- **Ahorro de Energía**: En terminales POS portátiles o tablets con pantallas OLED, el tema oscuro reduce el consumo de batería de forma considerable.

### Riesgos y Desafíos
- **Efecto Halación (Borrosidad)**: En personas con astigmatismo, el texto blanco brillante sobre fondo negro puro tiende a difuminarse (halación), dificultando la lectura rápida.
- **Pérdida de Contraste en Impuestos/Cifras**: Si no se eligen adecuadamente los grises de fondo, los colores semánticos (rojo y verde) pierden legibilidad.

### Recomendación Oficial de CajaFácil
**El Tema Oscuro es Opcional**. El sistema operará en **Tema Claro (Light Mode) por defecto**, ya que la mayoría de los negocios minoristas operan de día con luz ambiental alta. 
Sin embargo, el sistema **debe implementar la capacidad de Tema Oscuro** a través de un switch rápido de interfaz. El Tema Oscuro de CajaFácil **no utilizará fondo negro puro (#000000)**; en su lugar, se configurará un gris pizarra muy oscuro (`#0F172A`) como color de fondo y textos en gris claro (`#F1F5F9`) para mitigar completamente el efecto de halación y mantener el contraste WCAG AA.

---

## 15. Anexo: Recomendaciones de Implementación para Flutter

Para el equipo de desarrollo de la app de escritorio (`desktop_app`), se especifican las siguientes pautas de traducción técnica del Design System:

1. **Configuración de ThemeData**:
   - Mapear los tokens en el objeto `ThemeData` global de la aplicación.
   - Definir el `ColorScheme` utilizando la paleta HSL/HEX especificada:
     ```dart
     ColorScheme.light(
       primary: Color(0xFF1E293B),
       secondary: Color(0xFF475569),
       error: Color(0xFFEF4444),
       surface: Colors.white,
       background: Color(0xFFF8FAFC),
     )
     ```
2. **Tipografía Integrada**:
   - Utilizar el paquete `google_fonts` para cargar Inter de forma local (offline-first).
   - Crear un sub-estilo específico en el TextTheme para los valores monetarios utilizando `google_fonts` con JetBrains Mono o Roboto Mono.
3. **Componentes Custom Reutilizables**:
   - Crear clases de botones personalizadas (`AppButton.primary()`, `AppButton.destructive()`) encapsulando los paddings de la escala de espaciado y los estados de foco.
   - Evitar el uso de valores numéricos de espaciado directamente en el código de las vistas (ej. `SizedBox(width: 12)`); en su lugar, crear constantes centralizadas basadas en los tokens (`AppSpacing.s = 12.0`).
4. **Manejo del Foco**:
   - Personalizar el `FocusDecoration` en los inputs para renderizar el borde de 2px azul cuando tengan el foco de entrada del teclado, y garantizar que al pulsar `ESC` se active el Listener de re-foco sobre el input de búsqueda general de forma automática.
