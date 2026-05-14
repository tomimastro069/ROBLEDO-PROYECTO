# Registro de Fallos y Mejoras Pendientes — Frontend Checkout

**Fecha de relevamiento**: 2026-05-14
**Módulo afectado**: Pantalla final de Confirmación de Pago / Checkout (`Confirmar pedido` paso final).

## Descripción del Problema
Al avanzar desde el carrito hacia la confirmación final, el backend procesa exitosamente la creación del pedido (`POST /orders/`) y la generación de la preferencia en Sandbox (`POST /pagos/crear`), pero la vista React presenta graves fallos de sincronización y de experiencia de usuario (UX):

1. **Pérdida de Estado y Monto Total**: El componente de la pasarela final renderiza un **Total de $0.00**, perdiendo el estado global/local con el resumen real de las líneas de pedido ($5000.00 en la prueba).
2. **Ausencia de Interfaz de Selección**: No existen controles de formulario (radios, selectores) para alternar entre las formas de pago nativas (`EFECTIVO`, `TRANSFERENCIA`) y `MERCADOPAGO`.
3. **Bloqueo del Flujo (Dead-end)**: No se despliega el botón de acción para redirigir al usuario al `init_point` retornado por la preferencia ni para simular la acreditación en entorno de desarrollo. La pantalla queda estática e incompleta.

## Causa Raíz Conceptual
El componente presentacional no está consumiendo correctamente la respuesta del hook de mutación de pagos (`pagosApi.crear`), o bien dispara la petición de forma prematura al montar la vista sin pasar el estado inmutable de la orden recién creada.

## Solución Propuesta (Para próxima iteración)
- Refactorizar la vista final para que reciba el `pedido_id` y el `total` real desde el estado de enrutamiento o la store global.
- Añadir un selector visual para elegir la forma de pago antes de disparar el `POST /pagos/crear`.
- Renderizar dinámicamente un botón o enlace con el `init_point` devuelto por el backend para completar la redirección al flujo Sandbox/Local.

## Fallos en Sección "Mis Pedidos" y Detalle
1. **Falta de Nombres de Producto**: En la lista de ítems del detalle del pedido, el frontend renderiza el string hardcodeado `"Producto #" + id` (ej. `Producto #6 x2`) en lugar de extraer y mostrar la propiedad `product.name` proveniente del payload anidado del backend.
2. **Enrutamiento Roto (404 Not Found)**: Al hacer clic en el botón **"Pagar ahora"** para reanudar el pago de un pedido pendiente, la aplicación navega a una ruta inexistente o mal construida, desembocando en la pantalla de error `404 — Página no encontrada`.
