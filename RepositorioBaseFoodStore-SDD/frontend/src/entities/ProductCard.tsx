import React from 'react';
import { AddToCartButton } from '@/features/cart/AddToCart/ui/AddToCartButton';

interface ProductCardProps {
  id: number;
  name: string;
  price: number;
  imageUrl?: string;
}

const ProductCard: React.FC<ProductCardProps> = ({ id, name, price, imageUrl }) => {
  return (
    <div className="product-card" style={{ border: '1px solid #ccc', padding: '1rem', borderRadius: '8px' }}>
      <img src={imageUrl || 'https://via.placeholder.com/100'} alt={name} width={100} height={100} style={{ objectFit: 'cover' }} />
      <h3>{name}</h3>
      <span>${price}</span>
      <div style={{ marginTop: '1rem' }}>
        <AddToCartButton product={{ id, name, price, imageUrl }} />
      </div>
    </div>
  );
};

export default ProductCard;
