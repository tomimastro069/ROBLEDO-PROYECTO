# Arquitectura Propuesta

## Opciones analizadas
Durante el diseño de la capa de acceso a datos y la orquestación de transacciones en el backend con FastAPI y SQLModel, se contemplaron tres enfoques arquitectónicos alternativos:

1. **Active Record Puro (Inyección Directa de Sesión en Routers)**
   - **Mecánica**: El controlador HTTP recibe la sesión de base de datos como una dependencia (`Depends(get_session)`) y ejecuta directamente consultas y `session.commit()` en el cuerpo de la función.
   - **Trade-offs**: Extremadamente veloz de codificar para prototipos rápidos. Sin embargo, acopla la lógica de negocio al transporte HTTP, imposibilita la reutilización de transacciones entre múltiples servicios y vuelve el testing unitario sumamente frágil al requerir bases de datos en memoria o complejas intercepciones.
2. **Service Layer con Inyección Manual de Repositorios**
   - **Mecánica**: Se crean clases de servicio que reciben instancias individuales de repositorios por constructor. Cada servicio maneja llamadas aisladas a repositorios.
   - **Trade-offs**: Desacopla el acceso a datos, pero la responsabilidad de la transacción (el límite de cuándo confirmar o revertir) recae de forma difusa o requiere que los repositorios expongan métodos transaccionales propensos a interbloqueos en operaciones compuestas.
3. **Hexagonal-Lite: Unit of Work (UoW) + Repositorios Genéricos (Opción Seleccionada)**
   - **Mecánica**: Implementación de un director de transacción centralizado (`UnitOfWork`) expuesto como un gestor de contexto (`context manager`) que inicializa y provee de forma controlada todos los repositorios concretos inyectando una única sesión compartida.

## Decisión y justificación
Se optó sin reservas por el patrón **Unit of Work junto con Repositorios Genéricos** (Opción 3) como el estándar fundacional para todo el desarrollo del backend.

```
+---------------------------------------------------------------------------------+
|                                 CAPA DE NEGOCIO                                 |
|                                                                                 |
|   +-------------------------------------------------------------------------+   |
|   | Service Layer (Lógica stateless, validaciones FSM, cálculos financieros)|   |
|   +------------------------------------+------------------------------------+   |
|                                        |                                        |
|         +------------------------------+------------------------------+         |
|         | with UnitOfWork() as uow:                                   |         |
|         |                                                             |         |
|         |    uow.productos.get_by_id(...)                             |         |
|         |    uow.pedidos.create(...)                                  |         |
|         |    uow.historial.create(...)                                |         |
|         +------------------------------+------------------------------+         |
|                                        |                                        |
+----------------------------------------|----------------------------------------+
                                         v
+----------------------------------------|----------------------------------------+
|                               CAPA DE PERSISTENCIA                              |
|                                                                                 |
|   +------------------------------------+------------------------------------+   |
|   | Unit of Work (Abre/cierra Session, inyecta dependencias, commit/rollback)|  |
|   +---+--------------------------------+--------------------------------+---+   |
|       |                                |                                |       |
|       v                                v                                v       |
| +------------+                  +------------+                  +------------+  |
| | Producto   |                  | Pedido     |                  | Historial  |  |
| | Repository |                  | Repository |                  | Repository |  |
| +------------+                  +------------+                  +------------+  |
|       |                                |                                |       |
|       +--------------------------------+--------------------------------+       |
|                                        |                                        |
|                                        v                                        |
|                     +------------------------------------+                      |
|                     | BaseRepository[T] (CRUD Genérico)  |                      |
|                     +------------------------------------+                      |
+---------------------------------------------------------------------------------+
```

### Ventajas clave
- **Límite Transaccional Explícito**: Toda operación de negocio que involucre múltiples pasos de escritura tiene garantizado su comportamiento atómico. El `commit` ocurre de manera transparente, unificada y diferida exclusivamente al salir del bloque `with` sin excepciones.
- **Aislamiento de Responsabilidades**:
  - `Router`: HTTP puro (parseo, serialización, autenticación perimetral).
  - `Service`: Lógica pura independiente del almacenamiento físico.
  - `BaseRepository[T]`: Encapsulamiento de sentencias SQL/SQLModel (evita duplicación de código en métodos como `get_by_id`, `create`, `soft_delete`).
- **Testabilidad Insuperable**: Permite someter la capa de servicio a pruebas exhaustivas inyectando una implementación simulada (`MockUnitOfWork`) que expone diccionarios en memoria en lugar de repositorios de base de datos, logrando tiempos de ejecución de milisegundos en las suites de CI/CD.
