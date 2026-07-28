# 54_ANALISIS_FUNCIONAL_ENDURECIMIENTO_RC_V0_1_0.md

**Versión:** 1.1  
**Estado:** 📜 En Proceso de Auditoría  
**Última actualización:** 2026-07-24  
**Documento:** Análisis Funcional del Endurecimiento del Backend RC v0.1.0  

---

# 1. Introducción y Contexto del Negocio

Durante la consolidación de la primera versión del backend, se identificaron dos prioridades funcionales críticas para la consistencia y operatividad de CajaFácil:
* **H1: Política de Control de Existencias**: Definición clara del comportamiento esperado del sistema cuando un operador intenta vender un producto cuyo inventario lógico es insuficiente.
* **H5: Consulta Consolidada de Existencias**: Necesidad de disponer de una visualización unificada y ágil del inventario de todos los artículos para apoyar la toma de decisiones operativas y la reposición en mostrador.

Este documento establece el análisis funcional y las reglas operativas desde la perspectiva del negocio para ambas funcionalidades.

---

# 2. Política de Control de Existencias (H1)

## 2.1. Definición Funcional de la Política
La Política de Control de Existencias establece las reglas del negocio para el comportamiento del punto de venta (POS) y el inventario cuando la cantidad de unidades solicitada en una venta supera el saldo lógico registrado en el sistema. 

El sistema debe proveer una delimitación clara sobre si el checkout se detiene (bloqueo operativo) o si se permite la facturación bajo registro de discrepancias.

## 2.2. Política Oficial para el MVP: Inventario Estricto
Para el lanzamiento del MVP de CajaFácil, la política oficial y única activa es el **Inventario Estricto**. 

Bajo esta modalidad:
* El sistema **no permite confirmar una venta** si la disponibilidad lógica registrada es insuficiente para cubrir los ítems solicitados.
* El operador de caja recibirá un bloqueo inmediato al intentar añadir o facturar unidades excedentes, previniendo inconsistencias físicas e impositivas y obligando a mantener una disciplina rigurosa en el registro de entradas y salidas.

## 2.3. Capacidad de Arquitectura Futura: Inventario Flexible
Se contempla el **Inventario Flexible** únicamente como una capacidad futura prevista por la arquitectura del sistema, mas **no constituirá un requisito operativo para el MVP**.

Esta futura capacidad prevé:
* Permitir la facturación de artículos con saldo lógico insuficiente para evitar detener la fila del mostrador ante desfases temporales de ingreso de facturas.
* Generar registros de discrepancia y alertas de regularización para control administrativo.

## 2.4. Propiedad de la Configuración y Alcance
* **Propietario de la Regla**: El contexto de **Catálogo de Productos** define la ficha de cada artículo y sus flags generales (por ejemplo, si el artículo está sujeto a control de stock o si es un servicio exento).
* **Consumo de la Regla**: El módulo de **Inventario** evalúa las existencias en cada salida de mercancía, y el módulo de **Ventas** las consulta para validar y guiar las interacciones en la pantalla de facturación de caja.

## 2.5. Impacto en los Procesos de Negocio

### Ventas (Checkout)
* En el checkout de mostrador, el sistema verifica la disponibilidad lógica neta. Si las unidades a vender superan el saldo del sistema, la venta se bloquea y se solicita la intervención de un supervisor o la regularización previa del inventario.

### Compras (Recepción de Mercancía)
* Al registrarse la recepción física de mercancía a través de una compra, el balance disponible del producto se incrementa proporcionalmente con las unidades ingresadas, habilitando nuevamente su venta en mostrador.

### Inventario (Control y Auditoría)
* El comportamiento estricto asegura que los reportes de inventario coincidan estrechamente con el stock físico disponible en el comercio, facilitando arqueos, conciliaciones y el control de mermas directas.

---

# 3. Consulta Consolidada de Existencias (H5)

## 3.1. Requisitos de Información del Frontend
Para que el operador del mostrador o el administrador visualicen de forma efectiva el estado de su inventario, la pantalla de consulta requiere acceder a una vista unificada que proporcione:
* **Identificación del Artículo**: Código interno y código de barras.
* **Descripción**: Nombre del producto.
* **Existencia Disponible**: Cantidad neta pre-calculada lista para la venta.
* **Metadatos Operativos**: Indicadores que señalen si el producto requiere control de stock y si tiene políticas específicas activas.

## 3.2. Proyección y Necesidades Futuras del Negocio

El diseño de la consulta consolidada de stock debe estructurarse con la flexibilidad necesaria para admitir la evolución del negocio en fases posteriores del producto:

1. **Estructura Multibodega**:
   * Posibilidad de filtrar y segmentar el saldo de existencias según la sucursal, bodega o almacén físico desde el cual se realiza la consulta (por ejemplo: stock disponible en góndola exhibida frente a existencias en bodega secundaria).
2. **Existencia Física vs. Disponibilidad Comercial (Reservas)**:
   * Diferenciación funcional entre las existencias físicamente presentes en la tienda y la disponibilidad real para la venta (restando preventas pendientes de entrega, pedidos futuros o mercancía comprometida para canales digitales).
3. **Paginación y Filtrado Dinámico**:
   * Soporte para catálogos extensos con miles de artículos, garantizando la búsqueda por texto y la entrega de datos en bloques optimizados.

---

# 4. Reglas del Negocio Clave (Invariantes Funcionales)

* **Regla 1: Prevalencia de Servicios y Artículos Sin Control**: Si un producto está definido en el catálogo como no sujeto a control de stock, se asume con disponibilidad comercial ilimitada; las operaciones de validación de saldos y decrementos se omiten por completo.
* **Regla 2: Unicidad del Saldo por Empresa**: Cada artículo posee únicamente un saldo operativo pre-calculado por empresa inquilina (tenant), asegurando coherencia en las consultas masivas.
