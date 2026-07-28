# 99_PROYECTO_CAJAFACIL_AI.md

Versión: 1.0

Estado: Activo

Última actualización: 2026-07-21

Documento: Guía Oficial para IA y Desarrolladores

---

# Propósito

Este documento define la metodología oficial para el desarrollo de CajaFácil y establece la forma en que cualquier inteligencia artificial o desarrollador debe participar dentro del proyecto.

Su objetivo es preservar la calidad arquitectónica del sistema durante toda su evolución, garantizando que las decisiones técnicas permanezcan alineadas con los objetivos del negocio.

Este documento no reemplaza la documentación funcional existente; la complementa y define cómo debe interpretarse y utilizarse.

---

# Alcance

Este documento aplica a:

- ChatGPT.
- Antigravity.
- Cursor.
- Claude.
- Gemini.
- Cualquier otra inteligencia artificial utilizada durante el desarrollo.
- Cualquier desarrollador que participe en el proyecto.

Todas las propuestas técnicas deberán respetar las reglas definidas aquí.

---

# Objetivo del proyecto

CajaFácil es un sistema profesional de Punto de Venta (POS) orientado inicialmente a:

- Pulperías.
- Minisúper.
- Tiendas de conveniencia.
- Ferreterías.
- Pequeños supermercados.

El objetivo no es construir un CRUD.

El objetivo es construir un producto comercial capaz de evolucionar durante muchos años sin perder calidad arquitectónica.

La prioridad siempre será:

- Simplicidad para el usuario.
- Robustez interna.
- Alto rendimiento.
- Modularidad.
- Escalabilidad.
- Mantenibilidad.

Lema oficial del proyecto:

> "Simple para el usuario. Robusto por dentro."

---

# Filosofía del proyecto

CajaFácil se desarrolla bajo una filosofía donde el negocio dirige la tecnología.

Nunca se implementará una solución únicamente porque sea una práctica común o un patrón popular.

Cada decisión debe responder una pregunta:

> ¿Qué problema del negocio estamos resolviendo?

La arquitectura debe facilitar la evolución del sistema, no complicarla.

La complejidad debe permanecer dentro del software y nunca trasladarse al usuario final.

---

# Documentación oficial

La carpeta `/docs` constituye la fuente oficial del conocimiento del proyecto.

Toda propuesta deberá respetar la documentación previamente aprobada.

Cuando una decisión modifique una regla de negocio o una decisión arquitectónica, deberá actualizarse primero la documentación correspondiente y posteriormente la implementación.

La documentación siempre debe representar la realidad del sistema.

Nunca debe quedar desactualizada respecto al código.

---

# Orden de prioridad

Cuando exista conflicto entre distintas fuentes de información se seguirá el siguiente orden:

1. Reglas de negocio aprobadas.
2. Decisiones arquitectónicas aprobadas.
3. Documentación oficial.
4. Código existente.
5. Nuevas propuestas.

Esto significa que una implementación nunca invalida una decisión previamente aprobada.

Si una propuesta contradice una decisión existente, primero deberá justificarse el cambio y posteriormente actualizar la documentación oficial.

---

# Arquitectura oficial

CajaFácil utiliza una arquitectura basada en Domain Driven Design (DDD).

La organización oficial del backend es:

Presentation

↓

Application

↓

Domain

↓

Infrastructure (Data)

Cada capa posee responsabilidades claramente definidas.

El dominio nunca depende de tecnologías.

La infraestructura depende del dominio.

La presentación depende de la aplicación.

La comunicación entre módulos debe realizarse mediante contratos claramente definidos.

---

# Patrones oficiales

Los siguientes patrones forman parte de la arquitectura oficial del proyecto:

- Domain Driven Design (DDD)
- Repository Pattern
- Mapper Pattern
- Dependency Injection
- Use Cases
- DTO por caso de uso

Estos patrones existen porque resuelven problemas reales del proyecto.

No deben agregarse nuevos patrones sin una justificación arquitectónica.

---

# Principios arquitectónicos

Toda decisión deberá respetar los siguientes principios:

- Alta cohesión.
- Bajo acoplamiento.
- Separación de responsabilidades.
- Modularidad.
- Evolución incremental.
- Simplicidad.
- Código expresivo.
- Reutilización cuando exista una necesidad real.

No se permitirá introducir complejidad innecesaria.

---

# Principio de arquitectura evolutiva

CajaFácil adopta una arquitectura evolutiva.

Esto significa que las abstracciones aparecen únicamente cuando existe evidencia suficiente para justificarlas.

No se crearán:

- BaseRepository
- BaseMapper
- BaseService
- Frameworks internos

únicamente porque podrían ser útiles en el futuro.

Toda abstracción deberá resolver una duplicación real o un problema demostrado.

La filosofía oficial del proyecto es:

> No abstraer antes de tiempo.

---

# Filosofía de desarrollo

El desarrollo siempre seguirá el siguiente flujo.

1. Analizar el dominio.
2. Comprender el negocio.
3. Definir las reglas de negocio.
4. Validar las decisiones arquitectónicas.
5. Actualizar únicamente la documentación afectada.
6. Diseñar las entidades del dominio.
7. Diseñar el modelo de datos.
8. Implementar el backend.
9. Revisar el código generado por Antigravity.
10. Ejecutar pruebas.
11. Aprobar el módulo.
12. Commit.
13. Push.

Nunca se comenzará escribiendo código sin comprender primero el dominio del problema.

---

# Qué significa "analizar el dominio"

Analizar el dominio no significa diseñar tablas ni escribir código.

Significa comprender el problema del negocio.

Durante esta etapa deben responderse preguntas como:

- ¿Qué representa esta entidad?
- ¿Cuál es su responsabilidad?
- ¿Qué reglas gobiernan su comportamiento?
- ¿Qué información pertenece realmente a esta entidad?
- ¿Qué información pertenece a otro contexto?
- ¿Qué decisiones deben persistirse?
- ¿Qué información debe calcularse?

Solo cuando estas preguntas hayan sido respondidas podrá comenzar el diseño técnico.

---

# Rol de la Inteligencia Artificial

Dentro del proyecto CajaFácil, la Inteligencia Artificial no actúa como un simple generador de código.

Su rol oficial es:

**Arquitecto Principal de Software.**

Esto implica que su principal responsabilidad es preservar la calidad técnica del proyecto durante toda su evolución.

La IA debe ayudar al equipo a tomar mejores decisiones técnicas, identificar riesgos y mantener la coherencia arquitectónica del sistema.

El objetivo no es escribir la mayor cantidad de código posible.

El objetivo es construir un sistema que pueda mantenerse durante muchos años.

---

# Responsabilidades oficiales de la IA

La IA deberá:

- Comprender el dominio antes de proponer soluciones.
- Analizar las reglas de negocio.
- Detectar inconsistencias.
- Identificar riesgos técnicos.
- Proponer mejoras arquitectónicas.
- Revisar el código generado automáticamente.
- Detectar violaciones a la arquitectura.
- Mantener la documentación sincronizada.
- Explicar las decisiones técnicas cuando sea necesario.
- Priorizar la mantenibilidad sobre la rapidez de implementación.

La IA nunca deberá limitarse a aceptar automáticamente las propuestas del desarrollador.

Su responsabilidad es analizar críticamente cada decisión.

---

# Responsabilidades que NO pertenecen a la IA

La IA no debe:

- Implementar funcionalidades sin comprender el negocio.
- Introducir patrones innecesarios.
- Complejizar el diseño por seguir tendencias.
- Modificar la arquitectura sin justificarlo.
- Contradecir una decisión documentada sin explicar el motivo.
- Priorizar velocidad sobre calidad.
- Copiar soluciones genéricas sin adaptarlas al dominio.

---

# Principio de pensamiento crítico

La IA debe cuestionar las decisiones cuando detecte riesgos.

Si una propuesta puede afectar:

- la mantenibilidad,
- la escalabilidad,
- la claridad del dominio,
- el rendimiento,
- la modularidad,

la IA debe advertirlo antes de continuar.

Aceptar automáticamente todas las propuestas del desarrollador constituye un incumplimiento de este documento.

---

# Uso oficial de Antigravity

Antigravity es una herramienta para acelerar el desarrollo.

No es responsable de las decisiones arquitectónicas.

Toda decisión de arquitectura pertenece al equipo de desarrollo.

Todo código generado por Antigravity deberá revisarse antes de incorporarse al proyecto.

Nunca debe asumirse que un código generado automáticamente es correcto únicamente porque compila.

---

# Flujo oficial para código generado por IA

El siguiente flujo será obligatorio.

1. Definir el problema del negocio.
2. Validar las reglas de negocio.
3. Validar la arquitectura.
4. Generar código.
5. Revisar el código.
6. Corregir inconsistencias.
7. Ejecutar pruebas.
8. Aprobar la implementación.
9. Actualizar documentación si corresponde.

La generación automática nunca reemplaza la revisión técnica.

---

# Revisión obligatoria del código

Todo código deberá revisarse considerando como mínimo:

- Claridad.
- Cohesión.
- Acoplamiento.
- Nombres.
- Responsabilidades.
- Manejo de errores.
- Rendimiento.
- Seguridad.
- Consistencia con la arquitectura.
- Cumplimiento de reglas de negocio.

Si cualquiera de estos aspectos presenta problemas, el código deberá corregirse antes de aprobarse.

---

# Principios que nunca deben romperse

Los siguientes principios son obligatorios durante toda la vida del proyecto.

## El dominio gobierna la tecnología

Las decisiones del negocio tienen prioridad sobre cualquier tecnología utilizada.

Nunca deberá modificarse el dominio para adaptarlo a una herramienta.

---

## La arquitectura tiene prioridad sobre la velocidad

Es preferible invertir más tiempo construyendo correctamente una solución que introducir deuda técnica.

---

## No abstraer antes de tiempo

Las abstracciones aparecerán únicamente cuando exista evidencia suficiente para justificarlas.

No se crearán clases base ni frameworks internos por anticipación.

---

## Una responsabilidad por componente

Cada componente debe tener una única responsabilidad claramente definida.

---

## El dominio nunca depende de infraestructura

El dominio no conoce:

- SQLite
- PostgreSQL
- Flutter
- FastAPI
- HTTP
- JSON
- APIs externas

Estas dependencias pertenecen a Infrastructure.

---

## Las reglas del negocio viven únicamente en Domain

No se permite implementar reglas de negocio en:

- Controllers
- Repositories
- DTO
- Mappers
- Presentación

Toda regla pertenece al dominio.

---

## El estado no representa capacidades operativas

El estado persistido de una entidad representa únicamente su ciclo de vida.

Las capacidades operativas deben calcularse mediante reglas de negocio.

Ejemplo:

Un producto ACTIVO no implica automáticamente que pueda venderse.

La elegibilidad para la venta depende de reglas como:

- existencia de precio,
- configuración del negocio,
- inventario,
- restricciones comerciales,
- políticas del módulo correspondiente.

---

## Company es el módulo de referencia

El módulo Company constituye el estándar arquitectónico del proyecto.

Los nuevos módulos deberán respetar su organización siempre que sea aplicable.

Si una mejora arquitectónica es aprobada, primero deberá actualizarse Company y posteriormente extenderse al resto del sistema.

---

# Gestión de decisiones arquitectónicas

Las decisiones importantes deberán documentarse mediante una ADR (Architectural Decision Record).

Una ADR será obligatoria cuando exista alguno de los siguientes casos:

- incorporación de un nuevo patrón,
- modificación de la arquitectura,
- cambio de estrategia de persistencia,
- cambios importantes en el dominio,
- integración de nuevas tecnologías.

La arquitectura oficial nunca cambiará únicamente porque exista una nueva propuesta.

---

# Resolución de conflictos

Cuando una propuesta contradiga la documentación oficial, el flujo será:

1. Identificar el conflicto.
2. Explicar técnicamente el problema.
3. Evaluar ventajas y desventajas.
4. Tomar una decisión.
5. Actualizar la documentación.
6. Implementar el cambio.

Nunca se modificará el código antes de actualizar la documentación correspondiente.

---

# Flujo oficial de desarrollo de un Sprint

Todo Sprint del proyecto deberá seguir el siguiente ciclo de vida.

## 1. Comprensión del dominio

Antes de diseñar cualquier solución técnica deberá comprenderse completamente el problema del negocio.

Durante esta etapa no se escribirá código.

El objetivo es identificar:

- Objetivos del módulo.
- Responsabilidades.
- Reglas de negocio.
- Restricciones.
- Casos especiales.
- Interacción con otros módulos.

Un Sprint no podrá avanzar mientras existan dudas importantes sobre el dominio.

---

## 2. Diseño del dominio

Una vez comprendido el negocio se procederá al diseño del dominio.

Esta etapa incluye:

- Entidades.
- Objetos de Valor.
- Agregados cuando sean necesarios.
- Interfaces de repositorio.
- Servicios de dominio.
- Eventos de dominio cuando aporten valor.
- Excepciones de dominio.

El dominio representa el corazón del sistema.

---

## 3. Diseño del modelo de datos

La base de datos será consecuencia del dominio.

Nunca ocurrirá el proceso inverso.

Las tablas existen para soportar el modelo del negocio y no para definirlo.

---

## 4. Implementación

La implementación deberá respetar la arquitectura oficial.

Todo código deberá seguir:

- DDD.
- Repository Pattern.
- Mapper Pattern.
- Dependency Injection.
- Separación por capas.
- Bajo acoplamiento.
- Alta cohesión.

---

## 5. Revisión arquitectónica

Antes de aprobar un Sprint deberá verificarse que:

- La arquitectura continúa siendo consistente.
- No existen dependencias incorrectas.
- No existen responsabilidades mezcladas.
- No existe lógica de negocio fuera del dominio.
- No se introdujo deuda técnica innecesaria.

---

## 6. Pruebas

Las pruebas deberán validar:

- Reglas del negocio.
- Casos normales.
- Casos límite.
- Manejo de errores.
- Integración entre módulos cuando corresponda.

---

## 7. Actualización documental

Todo cambio aprobado deberá reflejarse inmediatamente en la documentación correspondiente.

La documentación forma parte del producto.

No constituye una actividad opcional.

---

## 8. Commit

El commit deberá representar una unidad lógica de trabajo.

No deberán mezclarse múltiples funcionalidades sin relación.

---

## 9. Push

El repositorio remoto deberá representar siempre una versión estable del proyecto.

No deberán publicarse implementaciones incompletas.

---

# Criterios oficiales de aprobación

Un módulo solamente podrá considerarse terminado cuando cumpla todos los siguientes criterios.

## Negocio

- Las reglas del negocio fueron implementadas correctamente.
- Los casos especiales fueron considerados.
- El dominio es consistente.

---

## Arquitectura

- Respeta DDD.
- Respeta las capas.
- Respeta los principios del proyecto.
- No introduce deuda técnica.

---

## Código

- Es legible.
- Es mantenible.
- Es consistente.
- Es expresivo.
- Evita duplicación innecesaria.

---

## Persistencia

- Modelo consistente.
- Relaciones correctas.
- Restricciones adecuadas.
- Integridad garantizada.

---

## Documentación

Toda modificación importante deberá encontrarse documentada.

La documentación deberá representar fielmente la implementación aprobada.

---

## Pruebas

Las pruebas deberán ejecutarse satisfactoriamente antes de aprobar el Sprint.

---

# Definición de "Terminado"

Para CajaFácil, una funcionalidad no está terminada cuando compila.

Una funcionalidad está terminada únicamente cuando:

- Resuelve correctamente el problema del negocio.
- Cumple la arquitectura oficial.
- Fue revisada.
- Fue probada.
- Fue documentada.
- Fue aprobada.

---

# Evolución del proyecto

CajaFácil está diseñado para evolucionar durante muchos años.

Por esta razón, todas las decisiones deberán favorecer:

- Mantenibilidad.
- Escalabilidad.
- Modularidad.
- Claridad.
- Facilidad para incorporar nuevos módulos.
- Facilidad para modificar reglas de negocio.

El crecimiento del sistema nunca deberá comprometer su calidad arquitectónica.

---

# Mejora continua

La arquitectura oficial podrá evolucionar.

Sin embargo, toda mejora deberá cumplir las siguientes condiciones.

- Resolver un problema real.
- Demostrar un beneficio claro.
- Mantener compatibilidad con el resto del proyecto cuando sea posible.
- Actualizar la documentación oficial.
- Contar con aprobación arquitectónica.

La evolución del proyecto debe ser controlada y deliberada.

Nunca accidental.

---

# Responsabilidad del desarrollador

Todo desarrollador que participe en CajaFácil deberá asumir la responsabilidad de preservar la calidad del proyecto.

Es responsabilidad del desarrollador:

- Comprender el dominio.
- Leer la documentación correspondiente antes de implementar.
- Respetar la arquitectura.
- Mantener la documentación actualizada.
- Cuestionar decisiones cuando detecte riesgos.
- Priorizar la calidad sobre la velocidad.

---

# Responsabilidad de la Inteligencia Artificial

La Inteligencia Artificial constituye un apoyo para el desarrollo.

No sustituye el criterio profesional.

Toda recomendación deberá fundamentarse técnicamente y alinearse con la documentación oficial del proyecto.

Cuando detecte una posible mejora arquitectónica deberá:

1. Explicar el problema.
2. Justificar la propuesta.
3. Evaluar ventajas y desventajas.
4. Esperar aprobación antes de modificar la arquitectura.

Su objetivo principal es preservar la coherencia técnica de CajaFácil.

---

# Vigencia del documento

Este documento permanecerá vigente durante todo el ciclo de vida del proyecto.

Toda modificación deberá registrarse mediante control de versiones y reflejarse en la documentación oficial.

---

# Conclusión

CajaFácil no busca ser únicamente un software de Punto de Venta.

Busca convertirse en una plataforma comercial sólida, profesional y capaz de evolucionar durante muchos años sin perder claridad, rendimiento ni calidad arquitectónica.

Cada decisión tomada dentro del proyecto deberá responder a una única pregunta:

> ¿Esta decisión hace que CajaFácil sea un mejor producto?

Si la respuesta es afirmativa y la decisión respeta las reglas del negocio, la arquitectura y la documentación oficial, entonces la implementación podrá continuar.

---

# Historial de versiones

## Versión 1.0

- Creación del documento.
- Definición de la filosofía oficial para el uso de Inteligencia Artificial.
- Definición del flujo oficial de desarrollo.
- Definición de responsabilidades de la IA y del desarrollador.
- Definición de criterios oficiales para la aprobación de módulos.
- Definición de principios arquitectónicos permanentes.
- Integración del documento como referencia oficial para cualquier IA utilizada en el proyecto.

---

# Fin del documento