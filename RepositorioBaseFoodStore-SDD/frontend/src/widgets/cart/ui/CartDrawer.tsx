import React from 'react';
import { useNavigate } from 'react-router-dom';
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
  const navigate = useNavigate();

  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex justify-end">
      {/* Fondo oscuro */}
      <div className="fixed inset-0 bg-black/50" onClick={onClose} />

      {/* Panel del carrito (a la derecha) */}
      <div className="relative w-full max-w-md h-full bg-white shadow-2xl flex flex-col animate-slide-in-right">
        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gray-50">
          <h2 className="text-xl font-bold text-gray-800">Carrito 🛒</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-red-500 text-3xl">&times;</button>
        </div>

        {/* Lista de items */}
        <div className="flex-1 overflow-y-auto px-6 py-4">
          {items.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-gray-400">
              <span className="text-4xl mb-2">🛍️</span>
              <p>Tu carrito está vacío</p>
            </div>
          ) : (
            <ul className="divide-y divide-gray-100">
              {items.map(item => (
                <li key={item.id} className="py-4">
                  <CartItemUI
                    item={item}
                    actions={
                      <div className="flex justify-between items-center w-full mt-3 bg-gray-50 p-2 rounded-lg">
                        <QuantityControls itemId={item.id} quantity={item.quantity} />
                        <RemoveButton itemId={item.id} />
                      </div>
                    }
                  />
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* Footer */}
        {items.length > 0 && (
          <div className="border-t border-gray-200 p-6 bg-gray-50">
            <div className="flex justify-between text-lg font-bold text-gray-900 mb-4">
              <span>Total</span>
              <span className="text-orange-500">${Number(total).toFixed(2)}</span>
            </div>
            <div className="flex flex-col gap-2">
              <button
                onClick={() => { onClose(); navigate('/checkout'); }}
                className="w-full bg-orange-500 text-white font-bold py-3 rounded-lg hover:bg-orange-600 transition shadow-lg shadow-orange-200"
              >
                Finalizar Compra
              </button>
              <button
                onClick={clearCart}
                className="w-full bg-white text-red-500 font-bold py-3 rounded-lg hover:bg-red-50 border border-red-100 transition"
              >
                Vaciar Carrito
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CartDrawer;
