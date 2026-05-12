import React from "react";
import { useCartStore } from "@/entities/cart/model/cartStore";

interface RemoveButtonProps {
  itemId: number;
}

/**
 * RemoveButton feature: removes a product from the cart store.
 */
export const RemoveButton: React.FC<RemoveButtonProps> = ({ itemId }) => {
  const removeItem = useCartStore((state) => state.removeItem);
  return (
    <button
      className="remove-from-cart-btn"
      onClick={() => removeItem(itemId)}
      aria-label="Eliminar" title="Eliminar"
    >
      🗑️
    </button>
  );
};
