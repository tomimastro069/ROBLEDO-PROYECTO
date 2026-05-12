import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { CartButton } from '@/widgets/cart/ui/CartButton';
import CartDrawer from '@/widgets/cart/ui/CartDrawer';

export const MainLayout = () => {
  const [isCartOpen, setIsCartOpen] = useState(false);

  return (
    <div className="main-layout">
      <header className="main-header" style={{ display: 'flex', justifyContent: 'space-between', padding: '1rem', borderBottom: '1px solid #ccc' }}>
        <h2>FoodStore</h2>
        <CartButton onClick={() => setIsCartOpen(true)} />
      </header>
      <main className="main-content" style={{ padding: '1rem' }}>
        <Outlet />
      </main>
      <CartDrawer open={isCartOpen} onClose={() => setIsCartOpen(false)} />
    </div>
  );
};
