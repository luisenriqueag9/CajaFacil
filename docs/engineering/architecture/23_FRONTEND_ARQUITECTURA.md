# 23_FRONTEND_ARQUITECTURA.md

Versión: 1.0

Estado: Aprobado

Última actualización: 2026-07-20

Documento: Arquitectura Frontend

---

# Objetivo

Definir la arquitectura oficial del Frontend de CajaFácil.

Este documento establece la organización del proyecto Flutter Desktop, las responsabilidades de cada capa, las convenciones de desarrollo y las tecnologías utilizadas para construir una interfaz rápida, modular, reutilizable y preparada para crecer durante muchos años.

---

# Tecnologías

Framework

- Flutter Desktop

Lenguaje

- Dart

Estado

- Riverpod

Navegación

- GoRouter

Persistencia Local

- SQLite
- Drift (o SQLite mediante la capa de persistencia definida)

Comunicación Backend

- HTTP REST

Serialización

- JSON

---

# Objetivos de Diseño

El Frontend debe ser:

- Muy rápido.
- Fácil de aprender.
- Modular.
- Consistente.
- Escalable.
- Reutilizable.
- Adaptado para pantallas táctiles y teclado.
- Preparado para trabajo Offline First.

---

# Arquitectura General

La aplicación se organizará de la siguiente manera:

desktop_app/

lib/

app/

core/

shared/

modules/

main.dart

---

# Organización del proyecto

## core

Contendrá toda la infraestructura compartida.

Ejemplos

config/

database/

network/

router/

theme/

logger/

services/

constants/

---

## shared

Componentes reutilizables.

Ejemplos

widgets/

layouts/

dialogs/

extensions/

helpers/

validators/

formatters/

---

## modules

Cada funcionalidad del sistema será un módulo independiente.

Ejemplos

empresa/

usuarios/

productos/

compras/

ventas/

clientes/

creditos/

reportes/

configuracion/

---

# Organización de cada módulo

Cada módulo tendrá la misma estructura.

Ejemplo

productos/

controllers/

providers/

models/

repositories/

services/

views/

widgets/

---

# Responsabilidades

## Controllers

Coordinan las acciones de la pantalla.

No contienen reglas del negocio.

---

## Providers

Administran el estado utilizando Riverpod.

---

## Models

Representan los datos que consume el frontend.

Corresponden a los DTO enviados por la API.

---

## Repositories

Son responsables de comunicarse con el Backend.

Nunca las vistas realizarán llamadas HTTP directamente.

---

## Services

Encapsulan funcionalidades compartidas.

Ejemplos

Exportar PDF.

Escáner de código de barras.

Impresión.

Sincronización.

---

## Views

Representan las pantallas del sistema.

Solo contienen lógica de presentación.

---

## Widgets

Componentes reutilizables.

Ejemplos

Botones.

Tablas.

Cuadros de búsqueda.

Campos de texto.

Tarjetas.

Diálogos.

---

# Navegación

Toda la navegación utilizará GoRouter.

No se utilizará Navigator directamente.

---

# Gestión del Estado

Riverpod será la única solución oficial.

Se evitará el uso de variables globales.

---

# Comunicación con el Backend

Toda comunicación seguirá este flujo:

Vista

↓

Provider

↓

Repository

↓

HTTP Client

↓

FastAPI

↓

Respuesta

---

# Persistencia Local

El frontend almacenará únicamente información necesaria para el funcionamiento Offline First.

Ejemplos

Configuración.

Sesión.

Cola de sincronización.

Catálogos.

Datos temporales.

---

# Manejo de Errores

Los errores deberán mostrarse mediante componentes reutilizables.

Ejemplos

SnackBar.

Dialog.

Banner.

Nunca mediante print().

---

# Tema Visual

Existirá un único ThemeData.

Se utilizarán colores corporativos.

Toda la aplicación reutilizará el mismo sistema de estilos.

---

# Diseño de Pantallas

Principios

- Interfaces limpias.
- Pocos clics.
- Botones grandes.
- Tipografía legible.
- Alto contraste.
- Operación rápida.

---

# Componentes Compartidos

Se desarrollarán widgets reutilizables para:

Botones.

Campos de texto.

Tablas.

Buscadores.

Tarjetas.

Diálogos.

Indicadores de carga.

Mensajes vacíos.

Selector de fechas.

Selector de moneda.

---

# Convenciones

Archivos

snake_case.dart

Clases

PascalCase

Variables

camelCase

Constantes

UPPER_CASE

---

# Rendimiento

No reconstruir widgets innecesariamente.

Utilizar const siempre que sea posible.

Separar widgets grandes.

Lazy loading para listas.

Paginación cuando sea necesaria.

---

# Seguridad

Nunca almacenar contraseñas.

Nunca almacenar tokens sin cifrado.

Cerrar automáticamente sesiones expiradas.

---

# Escalabilidad

La arquitectura permitirá agregar nuevos módulos sin modificar los existentes.

Ejemplos

Facturación electrónica.

Bodegas.

Inventario por ubicación.

Promociones.

Aplicación móvil.

---

# Flujo de una acción

Usuario

↓

Pantalla

↓

Provider

↓

Repository

↓

Backend

↓

Respuesta

↓

Actualización de la interfaz

---

# Pruebas

Cada módulo deberá incluir:

Pruebas de widgets.

Pruebas de providers.

Pruebas de repositorios.

Pruebas de integración.

---

# Conclusión

El Frontend de CajaFácil estará basado en una arquitectura modular orientada a componentes reutilizables, utilizando Flutter Desktop, Riverpod y GoRouter como base tecnológica.

Esta arquitectura permitirá mantener un código organizado, fácil de mantener y preparado para el crecimiento futuro del sistema.