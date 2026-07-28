# 22_BACKEND_ARQUITECTURA.md

Versión: 1.0

Estado: Aprobado

Última actualización: 2026-07-20

Documento: Arquitectura Backend

---

# Objetivo

Definir la arquitectura oficial del Backend de CajaFácil.

Este documento establece la organización del proyecto, responsabilidades de cada capa, convenciones de desarrollo y lineamientos técnicos para garantizar un sistema modular, mantenible, escalable y preparado para trabajar tanto en modo local como sincronizado con la nube.

---

# Tecnologías

Backend

- Python 3.14
- FastAPI

Persistencia

- SQLAlchemy 2.0
- Alembic

Base de datos

- SQLite (Local)
- PostgreSQL (Nube)

Seguridad

- JWT
- Passlib
- BCrypt

Validaciones

- Pydantic v2

Documentación

- OpenAPI
- Swagger

Pruebas

- Pytest

---

# Principios de Arquitectura

El backend seguirá los siguientes principios:

- Arquitectura por capas.
- Modularidad.
- Separación de responsabilidades.
- Alta cohesión.
- Bajo acoplamiento.
- Inyección de dependencias.
- Código reutilizable.
- Programación orientada al dominio.
- Principios SOLID.

---

# Arquitectura General

El proyecto se organizará de la siguiente manera:

backend/

app/

common/

core/

database/

modules/

tests/

---

# Organización por capas

Cada módulo seguirá exactamente la misma estructura.

Ejemplo

modules/

producto/

cliente/

venta/

compra/

empresa/

usuario/

etc.

---

Dentro de cada módulo existirá la siguiente estructura:

domain/

application/

infrastructure/

presentation/

---

# Capa Domain

Responsabilidades

- Entidades del dominio.
- Interfaces.
- Reglas del negocio.
- Objetos de valor.
- Enumeraciones.

La capa Domain no conoce FastAPI ni SQLAlchemy.

---

# Capa Application

Responsabilidades

- Casos de uso.
- Servicios de aplicación.
- Coordinación del dominio.
- Validaciones de negocio.

Ejemplos

CrearProducto

ActualizarProducto

EliminarProducto

BuscarProducto

RegistrarVenta

CerrarCaja

---

# Capa Infrastructure

Responsabilidades

- SQLAlchemy.
- Repositorios.
- Persistencia.
- Acceso a datos.
- Adaptadores externos.

Aquí viven

Repositories

ORM Models

Database

Migrations

---

# Capa Presentation

Responsabilidades

- Endpoints FastAPI.
- DTOs.
- Schemas.
- Dependencias.
- Respuestas HTTP.

Nunca contendrá reglas del negocio.

---

# Estructura de módulos

Ejemplo

modules/

producto/

domain/

entities/

value_objects/

repositories/

enums/

application/

use_cases/

services/

dtos/

infrastructure/

models/

repositories/

presentation/

routes/

schemas/

dependencies/

---

# Casos de uso

Cada acción importante será un caso de uso independiente.

Ejemplos

CrearProducto

EditarProducto

EliminarProducto

CrearVenta

CerrarCaja

RegistrarCompra

RegistrarAbono

LoginUsuario

---

# Repositorios

Cada Aggregate Root tendrá su propio repositorio.

Ejemplo

ProductoRepository

VentaRepository

CompraRepository

ClienteRepository

UsuarioRepository

---

Los casos de uso nunca accederán directamente a SQLAlchemy.

Siempre utilizarán interfaces de repositorio.

---

# ORM

SQLAlchemy será el único ORM permitido.

No se permitirá SQL embebido en los casos de uso.

---

# Alembic

Toda modificación del esquema deberá realizarse mediante migraciones.

Nunca se modificará una tabla manualmente en producción.

---

# Configuración

Toda configuración se almacenará mediante variables de entorno.

Ejemplos

DATABASE_URL

JWT_SECRET

JWT_EXPIRE_MINUTES

LOG_LEVEL

SYNC_ENABLED

---

# Logging

Se implementará un sistema centralizado de logs.

Tipos

INFO

WARNING

ERROR

CRITICAL

---

# Manejo de errores

Se utilizarán excepciones personalizadas.

Ejemplos

ProductoNoExiste

ClienteNoExiste

CajaCerrada

CreditoCancelado

StockInsuficiente

---

# Transacciones

Se utilizarán transacciones para

Registrar ventas.

Registrar compras.

Registrar créditos.

Cerrar caja.

Sincronización.

---

# Validaciones

Las validaciones se dividirán en:

Validaciones HTTP

Pydantic.

Validaciones de negocio

Casos de uso.

Validaciones de persistencia

Base de datos.

---

# Seguridad

Autenticación mediante JWT.

Las contraseñas utilizarán BCrypt.

Nunca se almacenarán contraseñas en texto plano.

---

# Dependencias

FastAPI Dependency Injection será el único mecanismo permitido para resolver servicios.

No se crearán objetos manualmente dentro de los endpoints.

---

# API REST

La API seguirá convenciones REST.

Ejemplos

GET

POST

PUT

DELETE

PATCH

---

# Convenciones de código

Clases

PascalCase

Variables

snake_case

Constantes

UPPER_CASE

Archivos

snake_case.py

---

# Pruebas

Cada módulo deberá incluir:

Pruebas unitarias.

Pruebas de integración.

Pruebas de repositorios.

Pruebas de casos de uso.

---

# Escalabilidad

La arquitectura permitirá agregar nuevos módulos sin modificar los existentes.

Ejemplos

Facturación electrónica.

Bodegas.

Promociones.

Aplicación móvil.

API pública.

---

# Flujo de una solicitud

Cliente

↓

FastAPI Route

↓

Schema

↓

Caso de Uso

↓

Repositorio

↓

SQLAlchemy

↓

SQLite / PostgreSQL

↓

Respuesta

---

# Conclusión

El backend de CajaFácil estará basado en una arquitectura modular por capas, orientada al dominio y preparada para crecer durante muchos años sin comprometer la mantenibilidad ni el rendimiento del sistema.