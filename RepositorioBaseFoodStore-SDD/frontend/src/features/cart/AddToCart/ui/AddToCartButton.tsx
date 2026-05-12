import React from "react";
import { useCartStore, CartItem } from "@/entities/cart/model/cartStore";

interface AddToCartButtonProps {
  product: Omit<CartItem, "quantity">;
  initialQuantity?: number;
  children?: React.ReactNode;
}

/**
 * AddToCartButton feature: adds a product to the cart store.
 */
export const AddToCartButton: React.FC<AddToCartButtonProps> = ({ product, initialQuantity = 1, children }) => {
  const addItem = useCartStore((state) => state.addItem);
  return (
    <button
      className="add-to-cart-btn"
      onClick={() => addItem({ ...product, quantity: initialQuantity })}
    >
      {children ?? "Agregar al carrito"}
    </button>
  );
};
