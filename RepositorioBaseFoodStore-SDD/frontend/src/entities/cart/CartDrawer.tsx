import React from 'react';
import { useCartStore } from './model/cartStore';

const CartDrawer = ({ open, onClose }: { open: boolean; onClose: () => void }) => {
  const { items, total, removeItem, updateQuantity, clearCart } = useCartStore();

  if (!open) return null;

  return (
    <div className="cart-drawer-overlay" onClick={onClose}>
      <div className="cart-drawer" onClick={(e) => e.stopPropagation()}>
        <h2>Carrito de Compras</h2>
        {items.length === 0 ? (
          <p>Tu carrito está vacío.</p>
        ) : (
          <>
            <ul>
              {items.map((item) => (
                <li key={item.id} className="cart-item">
                  <img src={item.imageUrl} alt={item.name} width={40} />
                  <span>{item.name}</span>
                  <span>${item.price}</span>
                  <input
                    type="number"
                    min={1}
                    value={item.quantity}
                    onChange={(e) => updateQuantity(item.id, parseInt(e.target.value, 10))}
                    style={{ width: '50px' }}
                  />
                  <button onClick={() => removeItem(item.id)}>Eliminar</button>
                </li>
              ))}
            </ul>
            <div className="cart-subtotal">
              <strong>Subtotal:</strong> ${total}
            </div>
            <button onClick={clearCart}>Vaciar carrito</button>
            <button className="checkout-btn">Finalizar compra</button>
          </>
        )}
        <button onClick={onClose} className="close-btn">Cerrar</button>
      </div>
    </div>
  );
};

export default CartDrawer;
