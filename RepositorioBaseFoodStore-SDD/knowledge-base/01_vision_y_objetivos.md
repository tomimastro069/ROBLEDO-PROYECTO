# Visión y Objetivos

## Propósito del sistema
Food Store es un sistema de comercio electrónico full-stack diseñado específicamente para la venta de productos alimenticios y la gestión integral de un negocio de comidas. Su propósito fundamental es ofrecer una plataforma robusta y completa que permita a los clientes explorar un catálogo de productos con información detallada sobre ingredientes y alérgenos, gestionar un carrito de compras persistente, realizar pedidos personalizables y pagar de forma segura a través de la pasarela integrada de MercadoPago. De forma paralela, provee un conjunto completo de herramientas de administración y tableros de control para gestionar el inventario, procesar pedidos en tiempo real con trazabilidad total y analizar métricas clave del negocio.

## Objetivos por actor
| Actor | Objetivo principal | Objetivos secundarios |
| :--- | :--- | :--- |
| **Cliente** | Navegar el catálogo, gestionar carrito, pagar de forma segura con MercadoPago y rastrear sus pedidos con trazabilidad completa. | Gestionar múltiples direcciones de entrega (definiendo una principal), visualizar alérgenos y personalizar productos excluyendo ingredientes. |
| **Administrador (Admin)** | Poseer control total sobre el sistema, gestionando categorías, productos, stock, usuarios y el ciclo de vida completo de pedidos desde el panel centralizado. | Asignar roles RBAC, acceder al dashboard de métricas clave (recharts), configurar formas de pago y forzar transiciones o cancelaciones especiales. |
| **Gestor de Stock** | Controlar la disponibilidad y mantener actualizadas las cantidades de inventario de cada producto en el catálogo. | Gestionar ingredientes (identificando explícitamente alérgenos) y administrar las categorías jerárquicas. |
| **Gestor de Pedidos** | Visualizar y gestionar el flujo operativo de los pedidos avanzando sus estados a través de la máquina de estados finitos (FSM) definida. | Cancelar pedidos cuando las reglas de negocio lo permitan y auditar historiales. |
| **Sistema** | Procesar notificaciones automatizadas (webhooks IPN de MercadoPago) y garantizar la trazabilidad completa e inmutable de transiciones de estado. | Actualizar pagos atómicamente, disparar avances de estado por cobros aprobados y rotar/revocar refresh tokens. |

## Alcance v5.0
- Autenticación y autorización robusta basada en JWT de doble token (Access de 30 min y Refresh de 7 días) con rotación automática e invalidación en base de datos.
- Modelo de control de acceso basado en roles (RBAC) con 4 roles predefinidos (ADMIN, STOCK, PEDIDOS, CLIENT).
- Catálogo de productos completo con soporte para categorías jerárquicas de profundidad arbitraria (consultadas vía Common Table Expressions CTE recursivas en PostgreSQL).
- Gestión granular de ingredientes asociados a productos, destacando visualmente aquellos marcados con el flag `es_alergeno`.
- Carrito de compras puramente en el cliente con persistencia garantizada en `localStorage` a través del middleware de Zustand, soportando cierres de navegador y recargas.
- Flujo de creación de pedidos 100% atómico bajo el patrón Unit of Work (UoW), aplicando el patrón Snapshot para preservar inmutables precios y direcciones históricas.
- Soporte para personalización de productos en pedidos, permitiendo la exclusión de ingredientes almacenada nativamente en arrays de enteros (`INTEGER[]`).
- Máquina de estados finitos (FSM) de 6 estados (PENDIENTE, CONFIRMADO, EN_PREPARACIÓN, EN_CAMINO, ENTREGADO, CANCELADO) con transiciones estrictamente validadas.
- Audit trail inmutable y append-only en la tabla `HistorialEstadoPedido` para registrar cada cambio de estado con timestamp y responsable.
- Pasarela de pagos integrada vía MercadoPago Checkout API (Orders) cumpliendo con el estándar PCI DSS SAQ-A mediante tokenización de tarjetas en el navegador.
- Recepción asíncrona de webhooks IPN de MercadoPago con protección de claves de idempotencia (`idempotency_key`) para confirmación y actualización automática de inventario.
- Módulo completo de direcciones de entrega con definición de dirección predeterminada única por cliente.
- Panel de administración avanzado con visualización de métricas en gráficos dinámicos utilizando `recharts`.
- Seguridad perimetral con Rate Limiting implementado vía `slowapi` protegiendo endpoints críticos (máximo 5 intentos fallidos en 15 minutos en login).
- Carga obligatoria de datos semilla (Seed Data) estables e idempotentes para roles, estados de pedido, formas de pago y cuenta de superadministrador.

## Fuera de alcance
- Logística de despacho automatizada o asignación a repartidores externos de terceros mediante GPS en tiempo real.
- Facturación fiscal electrónica directa con AFIP u organismos impositivos (se gestionan comprobantes internos de venta).
- Soporte multi-tenant para múltiples comercios o sucursales independientes en el mismo despliegue.
- Gestión de compras a proveedores de insumos o cálculo de mermas de ingredientes por peso/volumen.

## Métricas de éxito
- **Tasa de conversión de pedidos**: Porcentaje de carritos persistidos que finalizan exitosamente en un pedido confirmado y pagado.
- **Tiempo medio de preparación y entrega**: Medición exacta extraída de los timestamps inmutables del audit trail entre los estados `CONFIRMADO` y `ENTREGADO`.
- **Incidencia de errores transaccionales**: Verificación de fallas de stock en checkout, garantizando 0% de inconsistencias gracias a transacciones atómicas UoW.
- **Disponibilidad de la pasarela**: Porcentaje de webhooks IPN procesados exitosamente y respondidos con HTTP 200 al primer intento gracias a la clave de idempotencia.
