# Decisiones y Supuestos

## Decisiones técnicas (ADRs)
### ADR-01: Uso de Common Table Expressions (CTE) para jerarquía de Categorías
- **Contexto**: El catálogo de productos requiere organizar sus ítems en categorías que pueden poseer subcategorías con un nivel de profundidad arbitrario e ilimitado.
- **Decisión**: Se implementa una relación autoreferencial simple en `Categoria` (`parent_id`) resuelta a nivel de persistencia mediante consultas SQL recursivas utilizando `WITH RECURSIVE` (CTE) en PostgreSQL, encapsulando la complejidad enteramente dentro de `CategoriaRepository`.
- **Consecuencias**: Permite recuperar el árbol jerárquico completo en una única consulta ultrarrápida a la base de datos, evitando el problema de consultas $N+1$ o la sobrecarga de transportar tablas adyacentes pesadas al servidor de aplicaciones.

### ADR-02: Almacenamiento nativo de personalizaciones con PostgreSQL Arrays (`INTEGER[]`)
- **Contexto**: Los clientes pueden excluir ingredientes específicos de un producto al añadirlo a su pedido.
- **Decisión**: En lugar de crear una tabla relacional adicional extra (ej. `DetallePedidoExclusionIngrediente`) con millones de filas de cruce de bajo valor, se optó por almacenar los identificadores de los ingredientes excluidos nativamente en la columna `personalizacion` de tipo `INTEGER[]` en la tabla `DetallePedido`.
- **Consecuencias**: Reducción drástica del tamaño de la base de datos y simplificación en la inserción/consulta de las líneas de pedido, manteniendo al mismo tiempo un tipado estricto a nivel motor.

### ADR-03: Separación estricta del estado frontend (Zustand vs TanStack Query)
- **Contexto**: El frontend en React maneja datos remotos asíncronos en constante cambio (catálogo, métricas) y datos locales de sesión en el dispositivo del cliente.
- **Decisión**: Se prohíbe terminantemente mezclar ambos tipos de datos en un único almacén global. Se confina el estado del cliente (carrito, tokens, modales UI) a **Zustand** (con persistencia selectiva en `localStorage`) y el estado del servidor a **TanStack Query** (con revalidación en segundo plano y almacenamiento en caché en memoria).
- **Consecuencias**: Evita la desincronización de datos del servidor, simplifica el código de los componentes y optimiza las recargas de página.

## Supuestos del negocio
- **Disponibilidad continua de PostgreSQL**: Se asume que la base de datos relacional opera con un esquema de replicación o copias de seguridad continuas (Point-in-Time Recovery), justificando que la tabla `HistorialEstadoPedido` sea la única fuente de verdad inmutable (audit trail) para la facturación y disputas de entrega.
- **Conectividad de red para IPN**: Se asume que el servidor expone una URL pública HTTPS estable accesible por los servidores de MercadoPago para la entrega confiable de notificaciones push (Webhooks), mitigando la necesidad de implementar rutinas de *polling* intensivo desde el backend.
- **Costo de envío fijo inicial**: Para la versión 5.0, se asume un costo de envío fijo predeterminado de $\$50.00$ para todas las zonas de entrega locales, documentado como un valor base de partida para la lógica de liquidación en el `Service`.
