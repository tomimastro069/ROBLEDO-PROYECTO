import React from 'react';
import { useCartStore } from '@/entities/cart/model/cartStore';
import { CartItemUI } from '@/entities/cart/ui/CartItemUI';
import { RemoveButton } from '@/features/cart/RemoveFromCart/ui/RemoveButton';
import { QuantityControls } from '@/features/cart/ChangeQuantity/ui/QuantityControls';

interface CartDrawerProps {
  open: boolean;
  onClose: () => void;
}

const CartDrawer: React.FC<CartDrawerProps> = ({ open, onClose }) => {
  const { items, total, clearCart } = useCartStore();

  if (!open) return null;

  return (
    <div className="cart-drawer-overlay" onClick={onClose}>
      <div className="cart-drawer" onClick={e => e.stopPropagation()}>
        <h2>Carrito de Compras</h2>
        {items.length === 0 ? (
          <p>Tu carrito está vacío.</p>
        ) : (
          <>
            <ul>
              {items.map(item => (
                <li key={item.id} className="cart-item">
                  <CartItemUI
                    item={item}
                    actions={
                      <>
                        <QuantityControls itemId={item.id} quantity={item.quantity} />
                        <RemoveButton itemId={item.id} />
                      </>
                    }
                  />
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
