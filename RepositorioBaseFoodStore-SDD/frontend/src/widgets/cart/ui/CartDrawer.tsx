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
        <div className="px-6 py-6 border-b-2 border-[#d32f2f] flex justify-between items-center bg-white">
          <h2 className="text-sm font-black text-gray-900 uppercase tracking-[0.3em]">Carrito de Compras</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-[#d32f2f] transition-colors text-2xl font-light">&times;</button>
        </div>

        {/* Lista de items */}
        <div className="flex-1 overflow-y-auto px-6 py-4 bg-white">
          {items.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-gray-300">
              <p className="text-[10px] font-bold uppercase tracking-[0.4em]">Sin productos seleccionados</p>
            </div>
          ) : (
            <ul className="divide-y divide-gray-50">
              {items.map(item => (
                <li key={item.id} className="py-6">
                  <CartItemUI
                    item={item}
                    actions={
                      <div className="flex justify-between items-center w-full mt-4 border border-gray-100 p-2">
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
          <div className="border-t border-gray-100 p-8 bg-gray-50">
            <div className="flex justify-between items-end mb-8">
              <span className="text-[10px] font-black uppercase tracking-widest text-gray-400">Total</span>
              <span className="text-3xl font-black text-[#d32f2f]">${Number(total).toFixed(2)}</span>
            </div>
            <div className="flex flex-col gap-3">
              <button
                onClick={() => { onClose(); navigate('/checkout'); }}
                className="w-full bg-[#d32f2f] hover:bg-[#b71c1c] text-white font-black py-4 uppercase tracking-[0.2em] text-xs transition"
              >
                Continuar al Pago
              </button>
              <button
                onClick={clearCart}
                className="w-full text-gray-400 font-bold py-2 uppercase tracking-widest text-[8px] hover:text-red-600 transition"
              >
                [ VACIAR CARRITO ]
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CartDrawer;
