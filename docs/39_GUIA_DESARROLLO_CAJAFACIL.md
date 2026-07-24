# 39_GUIA_DESARROLLO_CAJAFACIL.md

**Versión:** 1.0  
**Estado:** 📜 Aprobado (Sprint 16)  
**Última actualización:** 2026-07-23  
**Documento:** Guía de Desarrollo del Proyecto CajaFácil  

---

# 1. Filosofía del Proyecto

CajaFácil es un ecosistema POS/ERP diseñado bajo la premisa de **confiabilidad absoluta en el punto de venta offline y consistencia modular**. Toda decisión arquitectónica sigue una prioridad inalterable:

$$\text{NEGOCIO} \longrightarrow \text{DOMINIO} \longrightarrow \text{ARQUITECTURA} \longrightarrow \text{IMPLEMENTACIÓN}$$

* **El Dominio es el Rey:** El código que describe las reglas de venta, inventario y caja no debe depender de bases de datos, APIs REST o frameworks.
* **Aislamiento Multi-Tenant:** Cada dato pertenece a una empresa (`company_id`). El cruce de información entre empresas está estrictamente prohibido a nivel lógico y de base de datos.
* **Offline-First:** El sistema debe continuar facturando y cobrando en el local comercial aunque no haya conexión a internet, garantizando sincronización retardada consistente.

---

# 2. Cómo Crear un Nuevo Módulo (Paso a Paso)

Para incorporar un nuevo Bounded Context (ej. *Crédito*, *Clientes*, *Reportes*), se debe seguir rigurosamente esta secuencia de pasos:

1. **Fase 1: Análisis Funcional:** Responder las preguntas esenciales del negocio en un documento en `docs/`. Definir el alcance y responsabilidades del contexto.
2. **Fase 2: Diseño del Dominio:** Especificar el Agregado Raíz, entidades internas, value objects, invariantes del negocio y eventos de dominio. Registrar en `docs/`.
3. **Fase 3: Diseño Arquitectónico:** Especificar contratos de repositorio, casos de uso, flujos transaccionales y matriz de comunicación permitida y prohibida. Registrar en `docs/`.
4. **Fase 4: Implementación:**
   * Crear la carpeta del módulo en `app/modules/<modulo>/`.
   * Implementar `domain/` (Python puro).
   * Implementar `application/` (Commands, Use Cases).
   * Implementar `data/` (Modelos SQLAlchemy, Mapper, Repositorio físico).
   * Implementar `presentation/` (FastAPI Routers, DTO Pydantic).
   * Registrar modelos en `app/database/base.py` y el router en `app/main.py`.
5. **Fase 5: Pruebas y Validación:** Crear suite en `backend/tests/` cubriendo invariantes, casos de uso y rollback transaccional en SQLite.

---

# 3. Buenas Prácticas y Prohibiciones

### Buenas Prácticas
* **Use Dataclasses Puras:** Defina agregados y entidades sin métodos que dependan de infraestructura.
* **Mantenga Repositorios Limpios:** El repositorio solo agrega registros y ejecuta `flush()`. El commit lo maneja el caso de uso.
* **Calcule Variables Derivadas:** Las variables acumulativas (como existencias y saldos de efectivo) se calculan a partir del Kardex histórico para mantener la trazabilidad.

### Acciones Prohibidas (Criterio de Rechazo de PR)
* ❌ **PROHIBIDO:** Importar modelos ORM o clases de persistencia en la capa de dominio.
* ❌ **PROHIBIDO:** Usar `db.commit()` dentro de las implementaciones de repositorios.
* ❌ **PROHIBIDO:** Realizar consultas cruzadas JOIN entre tablas de distintos módulos. Toda integración se realiza mediante puertos de lectura (`*Lookup`) y payloads de eventos de dominio.
* ❌ **PROHIBIDO:** Dejar de probar el rollback transaccional ante fallos.
