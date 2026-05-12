import React from "react";
import { useCartStore } from "@/entities/cart/model/cartStore";

interface QuantityControlsProps {
  itemId: number;
  quantity: number;
  min?: number;
  max?: number;
}

/**
 * QuantityControls feature: updates the quantity of an item in the cart store.
 */
export const QuantityControls: React.FC<QuantityControlsProps> = ({ itemId, quantity, min = 1, max = 99 }) => {
  const updateQuantity = useCartStore((state) => state.updateQuantity);
  return (
    <span className="quantity-controls">
      <button
        onClick={() => updateQuantity(itemId, Math.max(min, quantity - 1))}
        aria-label="Disminuir"
        disabled={quantity <= min}
      >
        -
      </button>
      <span className="quantity-number">{quantity}</span>
      <button
        onClick={() => updateQuantity(itemId, Math.min(max, quantity + 1))}
        aria-label="Aumentar"
        disabled={quantity >= max}
      >
        +
      </button>
    </span>
  );
};
