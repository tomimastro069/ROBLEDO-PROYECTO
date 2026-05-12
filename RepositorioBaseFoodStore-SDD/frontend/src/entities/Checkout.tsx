import React, { useState } from 'react';
import { useCartStore } from './cart/model/cartStore';

const Checkout = () => {
  const items = useCartStore((state) => state.items);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleCheckout = async () => {
    setLoading(true);
    setError(null);
    setSuccess(false);
    try {
      const res = await fetch('/api/cart/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ items }),
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || 'Error al validar el carrito');
      }
      setSuccess(true);
      // Redirigir al siguiente paso, por ejemplo: pago
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Confirmar Compra</h2>
      <button onClick={handleCheckout} disabled={loading}>
        {loading ? 'Validando...' : 'Validar y pagar'}
      </button>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {success && <div style={{ color: 'green' }}>Validación exitosa, avanzando a pago.</div>}
    </div>
  );
};

export default Checkout;
