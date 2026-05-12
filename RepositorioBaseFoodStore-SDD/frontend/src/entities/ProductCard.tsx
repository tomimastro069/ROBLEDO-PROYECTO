import React from 'react';
import { useCartStore } from './cart/model/cartStore';

interface ProductCardProps {
  id: number;
  name: string;
  price: number;
  imageUrl?: string;
}

const ProductCard: React.FC<ProductCardProps> = ({ id, name, price, imageUrl }) => {
  const addItem = useCartStore((state) => state.addItem);
  return (
    <div className="product-card">
      <img src={imageUrl} alt={name} width={100} />
      <h3>{name}</h3>
      <span>${price}</span>
      <button
        onClick={() => addItem({ id, name, price, imageUrl, quantity: 1 })}
      >
        Agregar al carrito
      </button>
    </div>
  );
};

export default ProductCard;
