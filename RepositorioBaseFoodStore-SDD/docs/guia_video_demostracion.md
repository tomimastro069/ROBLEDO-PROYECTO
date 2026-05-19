# 🎥 Guía de Demostración y Guion de Voz IA — Food Store v5.0

Esta guía está diseñada para que grabes un video impecable, mostrando la robustez de la arquitectura SDD y la fluidez del sistema. EL OBJETIVO ES QUE SE NOTE LA CALIDAD DEL SOFTWARE QUE CONSTRUISTE.

---

## 🛠 PARTE 1: Experiencia del Cliente (Lado Cliente)

### 📋 Guía de Pasos (Checklist para grabar)

1.  **Inicio**: Mostrá el Menú de Inicio, hacé scroll para que se vea el diseño responsivo y el catálogo inicial.
2.  **Registro**: Abrí el modal de registro. Completá datos de prueba rápidos.
3.  **Login**: Salí y entrá con la cuenta recién creada. Que se vea el toast de éxito.
4.  **Catálogo y Carrito**:
    - Filtrá por categoría.
    - Agregá un producto (ej. Hamburguesa).
    - Personalizalo (quitá un ingrediente si tenés la opción visible).
    - Abrí el carrito y modificá cantidades.
5.  **Checkout y Pago**:
    - Andá al Checkout.
    - **Dirección**: Creá una dirección nueva (ej. "Mi Casa"). Elegila como principal.
    - **Método de Pago**: Elegí MercadoPago.
    - **Simulación**: Usá la tarjeta de prueba (Visa Approved) que tenés en la documentación.
    - **Finalización**: Confirmá el pago y mostrá la pantalla de "Pedido Recibido" o el Timeline de estado en PENDIENTE/CONFIRMADO.

### 🎙 Guion para Voz IA (Parte Cliente)

"Bienvenido a Food Store. Vamos a comenzar viendo la experiencia desde la perspectiva del cliente. Como pueden observar, contamos con una interfaz moderna y fluida, diseñada con Atomic Design y Tailwind CSS.

Empezamos registrando un nuevo usuario. El sistema valida los datos en tiempo real y gestiona la sesión mediante JWT con almacenamiento seguro en authStore de Zustand. Una vez logueados, exploramos el catálogo. Noten la velocidad de respuesta gracias a TanStack Query y su sistema de caché.

Agregamos productos al carrito y procedemos al checkout. Aquí, el cliente puede gestionar sus direcciones de forma dinámica. Para el pago, integramos la SDK oficial de MercadoPago. Utilizamos una tarjeta de prueba para simular una transacción real PCI-compliant. Una vez procesado, el sistema nos redirige al historial, donde el pedido inicia su ciclo de vida en estado Confirmado gracias a la integración del Webhook IPN que actualiza el estado de forma asíncrona."

Empezamos registrando un nuevo usuario. El sistema valida los datos en tiempo real y gestiona la sesión mediante JWT con almacenamiento seguro en authStore de Zustand. Una vez logueados, exploramos el catálogo. Noten la velocidad de respuesta gracias a TanStack Query y su sistema de caché.
Agregamos productos al carrito y procedemos al checkout. Aquí, el cliente puede gestionar sus direcciones de forma dinámica. Una vez procesado el pago, el sistema nos redirige al historial, donde el pedido inicia su ciclo de vida en estado Confirmado y ahora dependera del apartado administrador para cambiar el estado del pedido

-

## ⚙️ PARTE 2: Gestión y Administración (Lado Admin)

### 📋 Guía de Pasos (Checklist para grabar)

1.  **Gestión de Categorías**: Creá una nueva categoría ingresando su nombre, seleccionando una categoría superior/padre y cargando su descripción.
2.  **Gestión de Ingredientes**: Creá un nuevo ingrediente, poné su nombre, marcalo como alérgeno y dale de alta.
3.  **Gestión de Productos (CRUD Completo)**:
    - **Alta**: Creá un producto nuevo asignando nombre, precio, stock inicial y su categoría. Usá la barra de búsqueda interactiva de ingredientes para agregar 3 ingredientes, demostrá el borrado de uno (badge con cruz), completá la descripción y crealo.
    - **Edición**: Editá un producto existente modificando algunos valores al azar para verificar la actualización en vivo.
    - **Eliminación**: Seleccioná un producto para borrar, confirmá su eliminación en el modal de advertencia de seguridad.
4.  **Flujo de Pedidos y Filtros**: Entrá a pedidos y cambiá los estados de las órdenes activas secuencialmente (`Confirmado` ➡️ `En Preparación` ➡️ `En Camino` ➡️ `Entregado`). Utilizá los filtros rápidos de estado para alternar vistas y visualizar solo un estado a la vez.
5.  **Módulo de Usuarios**: Desactivá un usuario de la lista, editá otro para cambiarle el rol de cliente a Gestor de Pedidos, y creá un nuevo usuario asignándole el rol de Gestor de Stock.
6.  **Eliminaciones y Edición de Catálogo**: Eliminá una categoría existente, eliminá un ingrediente y editá otro ingrediente modificando su nombre y estado de alérgeno.
7.  **Verificación Final**: Volvé a la vista de la tienda principal del cliente y mostrá la tarjeta responsiva entera del producto recién creado.

### 🎙 Guion para Voz IA (Parte Admin)

"Ahora pasamos al panel de administración, el corazón del sistema. Aquí el personal puede visualizar métricas clave en tiempo real.

Comenzamos en el módulo de categorías para dar de alta una nueva y asignarle un elemento superior, vinculándola directamente con otra existente para estructurar el menú. De ahí pasamos a ingredientes para dar de alta uno nuevo señalando si posee alérgenos.
En el panel de productos, vamos a dar de alta una nueva hamburguesa. En este formulario completamos todos los detalles generales como su nombre, el precio, el stock disponible y le asignamos su categoría correspondiente para indexarla en el catálogo.

Luego, implementamos la carga de insumos mediante el nuevo buscador interactivo: a medida que tipeamos los ingredientes, el sistema nos sugiere coincidencias; los vamos seleccionando con autofocus inmediato y, si nos equivocamos con alguno, podemos removerlo al instante haciendo click en su badge. Para cerrar la sección del catálogo, editamos valores de un artículo existente y eliminamos otro confirmando la acción de forma segura.

Luego pasamos a la sección de pedidos, donde podemos gestionar y modificar los estados de cada orden en tiempo real: avanzamos el flujo de un pedido desde que está Confirmado, a En Preparación, en camino de ser entregado y finalmente en estado Entregado. Además, el administrador cuenta con filtros rápidos que le permiten agrupar y visualizar todos los pedidos que compartan un mismo estado en común. En la sección de usuarios, desactivamos una cuenta, reasignamos roles mediante RBAC para nombrar un Gestor de Pedidos y creamos un Gestor de Stock desde cero. Finalmente, limpiamos categorías e ingredientes redundantes, editamos alérgenos y regresamos a la tienda principal para verificar que nuestra nueva hamburguesa luzca perfecta en el catálogo responsivo del cliente. Con esto finalizamos la presentación de Food Store. ¡Muchas gracias por su tiempo!"

---

> [!TIP]
> **CONSEJO DE ARQUITECTO:** Asegurate de que se vean los TOASTS de éxito y error. Eso demuestra que te importó la experiencia de usuario (UX). ¡DALE CON TODO A ESA GRABACIÓN!
