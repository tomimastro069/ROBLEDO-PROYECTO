import React from "react";
import { useCartStore } from "@/entities/cart/model/cartStore";

export const CartButton: React.FC<{ onClick: () => void }> = ({ onClick }) => {
  const items = useCartStore((state) => state.items);
  const totalItems = items.reduce((sum, i) => sum + i.quantity, 0);
  return (
    <button 
      className="relative p-2 text-gray-500 hover:text-[#d32f2f] transition-colors" 
      onClick={onClick} 
      aria-label="Abrir carrito"
    >
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
      </svg>
      {totalItems > 0 && (
        <span className="absolute top-0 right-0 bg-[#d32f2f] text-white text-[8px] font-black w-4 h-4 flex items-center justify-center rounded-full">
          {totalItems}
        </span>
      )}
    </button>
  );
};
