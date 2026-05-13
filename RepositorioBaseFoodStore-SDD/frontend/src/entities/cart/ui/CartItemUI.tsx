import React from 'react';
import type { CartItem } from '../model/cartStore';

export interface CartItemUIProps {
  item: CartItem;
  actions?: React.ReactNode;
}

/**
 * Pure UI component for a cart item row. FSD: entities must be dumb, no store hooks!
 * Actions are injected from the parent via props (e.g., Remove, ChangeQuantity, etc).
 */
export const CartItemUI: React.FC<CartItemUIProps> = ({ item, actions }) => {
  return (
    <div className="flex items-start gap-4">
      <img
        src={item.imageUrl}
        alt={item.name}
        className="w-16 h-16 object-cover rounded-md border border-gray-200"
      />
      <div className="flex-1 flex flex-col">
        <div className="flex justify-between font-medium text-gray-900">
          <h3>{item.name}</h3>
          <p className="ml-4">${Number(item.price).toFixed(2)}</p>
        </div>
        <div className="mt-2 flex-1 flex items-end justify-between text-sm">
          {actions}
        </div>
      </div>
    </div>
  );
};
