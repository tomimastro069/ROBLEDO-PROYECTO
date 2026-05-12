import React from "react";
import { useCartStore } from "@/entities/cart/model/cartStore";

export const CartButton: React.FC<{ onClick: () => void }> = ({ onClick }) => {
  const items = useCartStore((state) => state.items);
  const totalItems = items.reduce((sum, i) => sum + i.quantity, 0);
  return (
    <button className="cart-header-btn" onClick={onClick} aria-label="Abrir carrito">
      🛒
      {totalItems > 0 && <span className="cart-badge">{totalItems}</span>}
    </button>
  );
};
