# Preguntas Abiertas

## Dudas y dependencias no resueltas
Al consolidar la base de conocimiento canónica a partir de los documentos fuente de la versión 5.0, se identificaron los siguientes puntos que requerirán definición por parte del equipo de arquitectura o producto en futuras iteraciones:

1. **Estrategia de reintento de Webhooks fallidos**: Si el servidor de Food Store se encuentra temporalmente inactivo o retorna un error 5xx ante una notificación IPN entrante de MercadoPago, ¿cuál es el tiempo máximo de espera (*timeout*) y la política de reintentos exponenciales configurada del lado del PSP antes de marcar la orden como permanentemente no sincronizada?
2. **Límite de ítems distintos en un único carrito**: Las validaciones actuales exigen `cantidad >= 1` por ítem de pedido, pero no especifican un límite superior estricto sobre el tamaño del array de ítems o la cantidad máxima de un mismo producto para prevenir bloqueos abusivos de inventario.
3. **Manejo de zonas geográficas de entrega**: El campo `costo_envio` se asume fijo en $\$50.00$. ¿Se prevé una integración futura con APIs de geocodificación para calcular tarifas dinámicas basadas en la distancia desde el local comercial hacia las coordenadas de la `DireccionEntrega`?
4. **Rotación manual anticipada de Secret Keys**: Ante una eventual vulneración de la `SECRET_KEY` de JWT, ¿cuál es el procedimiento operativo estándar para invalidar de forma global e instantánea todas las sesiones activas emitidas previamente sin requerir un vaciado completo de la tabla `RefreshToken`?
