# 🎥 Guía de Demostración y Guion de Voz IA — Food Store v5.0

Esta guía está diseñada para que grabes un video impecable, mostrando la robustez de la arquitectura SDD y la fluidez del sistema. EL OBJETIVO ES QUE SE NOTE LA CALIDAD DEL SOFTWARE QUE CONSTRUISTE.

---

## 🛠 PARTE 1: Experiencia del Cliente (Lado Cliente)

### 📋 Guía de Pasos (Checklist para grabar)
1.  **Inicio**: Mostrá el Menú de Inicio, hacé scroll para que se vea el diseño responsivo y el catálogo inicial.
2.  **Registro**: Abrí el modal de registro. Completá datos de prueba rápidos.
3.  **Login**: Salí y entrá con la cuenta recién creada. Que se vea el toast de éxito.
4.  **Catálogo y Carrito**:
    *   Filtrá por categoría.
    *   Agregá un producto (ej. Hamburguesa).
    *   Personalizalo (quitá un ingrediente si tenés la opción visible).
    *   Abrí el carrito y modificá cantidades.
5.  **Checkout y Pago**:
    *   Andá al Checkout.
    *   **Dirección**: Creá una dirección nueva (ej. "Mi Casa"). Elegila como principal.
    *   **Método de Pago**: Elegí MercadoPago.
    *   **Simulación**: Usá la tarjeta de prueba (Visa Approved) que tenés en la documentación.
    *   **Finalización**: Confirmá el pago y mostrá la pantalla de "Pedido Recibido" o el Timeline de estado en PENDIENTE/CONFIRMADO.

### 🎙 Guion para Voz IA (Parte Cliente)
"Bienvenido a Food Store. Vamos a comenzar viendo la experiencia desde la perspectiva del cliente. Como pueden observar, contamos con una interfaz moderna y fluida, diseñada con Atomic Design y Tailwind CSS.

Empezamos registrando un nuevo usuario. El sistema valida los datos en tiempo real y gestiona la sesión mediante JWT con almacenamiento seguro en authStore de Zustand. Una vez logueados, exploramos el catálogo. Noten la velocidad de respuesta gracias a TanStack Query y su sistema de caché.

Agregamos productos al carrito y procedemos al checkout. Aquí, el cliente puede gestionar sus direcciones de forma dinámica. Para el pago, integramos la SDK oficial de MercadoPago. Utilizamos una tarjeta de prueba para simular una transacción real PCI-compliant. Una vez procesado, el sistema nos redirige al historial, donde el pedido inicia su ciclo de vida en estado Confirmado gracias a la integración del Webhook IPN que actualiza el estado de forma asíncrona."

---

## ⚙️ PARTE 2: Gestión y Administración (Lado Admin)

### 📋 Guía de Pasos (Checklist para grabar)
1.  **Login Admin**: Entrá con las credenciales de administrador.
2.  **Dashboard**: Mostrá brevemente los gráficos de Recharts (KPIs).
3.  **Gestión de Pedidos**:
    *   Buscá el pedido que hiciste recién.
    *   Cambiá el estado: `CONFIRMADO` ➡️ `EN PREPARACIÓN` ➡️ `EN CAMINO` ➡️ `ENTREGADO`.
    *   Mostrá el historial (Timeline) del pedido para que se vea el Audit Trail.
4.  **Cancelación**: Agarrá otro pedido y cancelalo poniendo un motivo (ej. "Falta de stock").
5.  **Catálogo (CRUDs)**:
    *   **Categoría**: Creá una nueva (ej. "Postres").
    *   **Ingrediente**: Creá uno nuevo (ej. "Chocolate") y marcalo como alérgeno.
    *   **Producto**: Creá un producto nuevo usando la categoría e ingrediente creados.
    *   **Edición**: Editá un producto existente (cambiá precio o stock).
6.  **Usuarios**:
    *   Creá un nuevo usuario con rol `PEDIDOS` o `STOCK`.
    *   Editá un usuario existente (cambiá el nombre o rol).

### 🎙 Guion para Voz IA (Parte Admin)
"Ahora pasamos al panel de administración, el corazón del sistema. Aquí el personal puede visualizar métricas clave en tiempo real.

En el módulo de pedidos, gestionamos el ciclo de vida de cada orden. La máquina de estados FSM garantiza que las transiciones sean válidas y queden registradas en un Audit Trail inmutable. Observen cómo avanzamos el pedido de 'Confirmado' a 'Entregado' con un solo click, manteniendo la trazabilidad completa. También es posible cancelar pedidos, requiriendo siempre un motivo para la auditoría.

En la sección de catálogo, el administrador tiene control total. Podemos crear categorías jerárquicas, gestionar ingredientes con alertas de alérgenos y dar de alta nuevos productos con snapshots de precios para proteger la integridad histórica de las ventas. 

Finalmente, el módulo de usuarios permite una gestión robusta de roles basada en RBAC, asegurando que cada empleado acceda solo a las funciones que le corresponden. Food Store no es solo una app de comida, es una plataforma de gestión integral diseñada para escalar."

---

> [!TIP]
> **CONSEJO DE ARQUITECTO:** Asegurate de que se vean los TOASTS de éxito y error. Eso demuestra que te importó la experiencia de usuario (UX). ¡DALE CON TODO A ESA GRABACIÓN!
