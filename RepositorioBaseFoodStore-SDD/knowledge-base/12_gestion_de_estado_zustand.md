# Dominio Especial: Gestión de Estado con Zustand

## Separación de Responsabilidades en el Cliente
El diseño arquitectónico del frontend restringe el uso de almacenes globales a cuatro dominios de cliente perfectamente acotados, aislando por completo la gestión del estado de la interfaz local frente al estado remoto del servidor (delegado enteramente a TanStack Query).

### 1. Store de Autenticación (`authStore.ts`)
- **Responsabilidad**: Retener el token de acceso opaco Bearer (`accessToken`), los metadatos públicos del usuario autenticado y el conmutador de sesión (`isAuthenticated`).
- **Métodos expuestos**: `login()`, `logout()`, `refreshToken()`, `hasRole(rol)`.
- **Estrategia de Persistencia**: Implementa el middleware `persist` configurado con la opción `partialize` para guardar de forma exclusiva en `localStorage` la cadena del `accessToken`. Al inicializarse la aplicación, un hook global consume el endpoint `/api/v1/auth/me` para reconstruir en memoria los datos del usuario de forma segura y actualizada.

### 2. Store del Carrito de Compras (`cartStore.ts`)
- **Responsabilidad**: Almacenar la lista de ítems seleccionados para la compra antes de su confirmación transaccional en el servidor.
- **Estructura del Ítem**: Cada elemento preserva el identificador primario del producto (`producto_id`), una instantánea temporal de `nombre` y `precio` para renderizado ágil en el *drawer*, la `cantidad` solicitada y el array de enteros con los IDs de los ingredientes excluidos (`personalizacion`).
- **Métodos expuestos**: `addItem()`, `removeItem()`, `updateCantidad()`, `clearCart()`, y selectores computados para `subtotal()`, `costoEnvio()` y `total()`.
- **Estrategia de Persistencia**: Almacenamiento íntegro persistente mediante `localStorage` para tolerar recargas accidentales o cierres de pestaña del navegador durante el proceso de compra.

### 3. Store de Estado de Pago (`paymentStore.ts`)
- **Responsabilidad**: Rastrear el progreso efímero de la interacción con el SDK de MercadoPago durante el *checkout*.
- **Estructura**: Mantiene el estado en curso (`status`: `idle` | `processing` | `approved` | `rejected` | `error`), el identificador de transacción devuelto por la pasarela (`mpPaymentId`) y detalles textuales de rechazo (`statusDetail`).
- **Estrategia de Persistencia**: **Sin persistencia**. Reside puramente en la memoria volátil de la sesión de React, reseteándose automáticamente ante recargas para forzar una reinicialización limpia del intento de pago.

### 4. Store de Interfaz de Usuario (`uiStore.ts`)
- **Responsabilidad**: Orquestar de forma declarativa la visibilidad de elementos superpuestos de navegación global.
- **Estructura**: Banderas booleanas simples (`cartOpen`, `sidebarOpen`, `confirmModalActive`).
- **Métodos expuestos**: `openCart()`, `closeCart()`, `toggleSidebar()`.
- **Estrategia de Persistencia**: **Sin persistencia**.

## Buenas Prácticas de Consumo
Para preservar el alto rendimiento y evitar renderizados en cascada innecesarios en la jerarquía de componentes de React, se establecen las siguientes normas de consumo:
- **Suscripción granular mediante selectores atómicos**: Se debe extraer cada valor atómico o función de forma individual:
  ```typescript
  // Correcto: Suscripción focalizada que re-renderiza solo si cambia el conteo
  const itemCount = useCartStore(state => state.itemCount());
  // Incorrecto: Suscribe el componente a la totalidad del estado
  const store = useCartStore();
  ```
- **Acceso imperativo externo**: Para consumir el token dentro de interceptores de Axios sin violar las reglas de los hooks de React, se utiliza el acceso estático directo:
  ```typescript
  const token = useAuthStore.getState().accessToken;
  ```
