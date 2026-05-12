import React from 'react';
import ProductCard from '@/entities/ProductCard';

const MOCK_PRODUCTS = [
  { id: 1, name: 'Hamburguesa Clasica', price: 10, imageUrl: 'https://via.placeholder.com/150' },
  { id: 2, name: 'Papas Fritas', price: 5, imageUrl: 'https://via.placeholder.com/150' },
  { id: 3, name: 'Refresco', price: 3, imageUrl: 'https://via.placeholder.com/150' },
];

export const HomePage = () => {
  return (
    <div>
      <h1>Bienvenido a FoodStore</h1>
      <div style={{ display: 'flex', gap: '1rem', marginTop: '2rem', flexWrap: 'wrap' }}>
        {MOCK_PRODUCTS.map((product) => (
          <ProductCard key={product.id} {...product} />
        ))}
      </div>
    </div>
  );
};
