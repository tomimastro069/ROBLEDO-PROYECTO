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
    <div className="cart-item-row">
      <img
        src={item.imageUrl}
        alt={item.name}
        className="cart-item-img"
        style={{ width: 64, height: 64, objectFit: 'cover' }}
      />
      <div className="cart-item-details">
        <div className="cart-item-title">{item.name}</div>
        <div className="cart-item-price">${item.price.toFixed(2)}</div>
      </div>
      <div className="cart-item-actions">{actions}</div>
    </div>
  );
};
