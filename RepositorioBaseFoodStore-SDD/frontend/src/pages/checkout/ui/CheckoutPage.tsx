import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery, useMutation } from '@tanstack/react-query';
import { direccionesApi } from '@/shared/api/direccionesApi';
import { ordersApi } from '@/shared/api/ordersApi';
import { useCartStore } from '@/entities/cart/model/cartStore';

export const CheckoutPage = () => {
  const navigate = useNavigate();
  const { items, total, clearCart } = useCartStore();
  const [selectedAddressId, setSelectedAddressId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const { data: addresses, isLoading: loadingAddr } = useQuery({
    queryKey: ['direcciones'],
    queryFn: direccionesApi.list,
  });

  const createOrder = useMutation({
    mutationFn: ordersApi.create,
    onSuccess: (order) => { clearCart(); navigate(`/pedidos/${order.id}`); },
    onError: () => setError('Error al crear el pedido. Verificá el stock disponible.'),
  });

  if (items.length === 0) {
    return (
      <div className="max-w-xl mx-auto px-4 py-20 text-center">
        <p className="text-xl text-gray-400">Tu carrito está vacío.</p>
        <button onClick={() => navigate('/catalogo')} className="mt-4 text-orange-500 hover:underline">
          Ir al catálogo
        </button>
      </div>
    );
  }

  const selected = addresses?.find((a) => a.id === selectedAddressId);

  const handleConfirm = () => {
    if (!selected) { setError('Seleccioná una dirección de entrega.'); return; }
    setError(null);

    // El payload ahora coincide con el esquema seguro del backend
    createOrder.mutate({
      items: items.map((i) => ({
        product_id: i.id,
        quantity: i.quantity
        // Ya no enviamos el precio (el backend lo busca en DB por seguridad)
        // Ni la dirección manual (enviamos el ID)
      })),
      shipping_address_id: selected.id,
    });
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-2xl sm:text-3xl font-bold text-gray-800 mb-8">Confirmar pedido</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

        {/* Columna izquierda — Dirección */}
        <div className="space-y-6">
          <div className="bg-white border border-gray-200 rounded-xl p-6">
            <h2 className="font-semibold text-gray-800 text-lg mb-4">Dirección de entrega</h2>
            {loadingAddr ? (
              <p className="text-sm text-gray-400">Cargando...</p>
            ) : addresses?.length === 0 ? (
              <p className="text-sm text-gray-500">
                No tenés direcciones.{' '}
                <button onClick={() => navigate('/direcciones')} className="text-orange-500 hover:underline">
                  Agregar una
                </button>
              </p>
            ) : (
              <div className="space-y-3">
                {addresses?.map((addr) => (
                  <label key={addr.id}
                    className={`flex items-start gap-3 border rounded-xl p-4 cursor-pointer transition ${selectedAddressId === addr.id ? 'border-orange-400 bg-orange-50' : 'border-gray-200 hover:border-gray-300'}`}>
                    <input
                      type="radio" name="address"
                      checked={selectedAddressId === addr.id}
                      onChange={() => setSelectedAddressId(addr.id)}
                      className="mt-0.5 accent-orange-500"
                    />
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-800">
                        {addr.street} {addr.numero}{addr.piso ? `, piso ${addr.piso}` : ''}
                      </p>
                      <p className="text-xs text-gray-500 mt-0.5">{addr.city}, {addr.state} — {addr.zip_code}</p>
                      {addr.is_default && (
                        <span className="text-xs text-orange-500 font-medium mt-1 inline-block">★ Predeterminada</span>
                      )}
                    </div>
                  </label>
                ))}
                <button onClick={() => navigate('/direcciones')} className="text-sm text-orange-500 hover:underline mt-1">
                  + Agregar nueva dirección
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Columna derecha — Resumen + confirmar */}
        <div className="space-y-6">
          <div className="bg-white border border-gray-200 rounded-xl p-6">
            <h2 className="font-semibold text-gray-800 text-lg mb-4">Resumen del pedido</h2>
            <ul className="divide-y divide-gray-100">
              {items.map((item) => (
                <li key={item.id} className="py-3 flex justify-between items-center">
                  <div>
                    <p className="text-sm font-medium text-gray-800">{item.name}</p>
                    <p className="text-xs text-gray-400">x{item.quantity} · ${Number(item.price).toFixed(2)} c/u</p>
                  </div>
                  <span className="text-sm font-semibold text-gray-700">
                    ${(Number(item.price) * item.quantity).toFixed(2)}
                  </span>
                </li>
              ))}
            </ul>
            <div className="border-t border-gray-200 pt-4 mt-4 flex justify-between">
              <span className="font-bold text-gray-800">Total</span>
              <span className="font-bold text-xl text-orange-500">${Number(total).toFixed(2)}</span>
            </div>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-xl px-4 py-3">
              <p className="text-sm text-red-600">{error}</p>
            </div>
          )}

          <button
            onClick={handleConfirm}
            disabled={createOrder.isPending}
            className="w-full bg-orange-500 hover:bg-orange-600 text-white font-bold py-4 rounded-xl text-lg transition disabled:opacity-50 shadow-sm"
          >
            {createOrder.isPending ? 'Creando pedido...' : '✓ Confirmar pedido'}
          </button>

          <button onClick={() => navigate(-1)} className="w-full text-gray-400 hover:text-gray-600 text-sm transition">
            ← Volver al carrito
          </button>
        </div>
      </div>
    </div>
  );
};
