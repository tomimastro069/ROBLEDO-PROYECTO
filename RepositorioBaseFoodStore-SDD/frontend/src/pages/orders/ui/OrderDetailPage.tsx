import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { ordersApi, type OrderStatus } from '@/shared/api/ordersApi';

const STATUS_LABELS: Record<OrderStatus, string> = {
  PENDIENTE: 'Pendiente de pago',
  CONFIRMADO: 'Confirmado',
  EN_PREPARACION: 'En preparación',
  EN_CAMINO: 'En camino',
  ENTREGADO: 'Entregado',
  CANCELADO: 'Cancelado',
};

const STATUS_COLORS: Record<OrderStatus, string> = {
  PENDIENTE: 'bg-yellow-100 text-yellow-700',
  CONFIRMADO: 'bg-blue-100 text-blue-700',
  EN_PREPARACION: 'bg-purple-100 text-purple-700',
  EN_CAMINO: 'bg-indigo-100 text-indigo-700',
  ENTREGADO: 'bg-green-100 text-green-700',
  CANCELADO: 'bg-red-100 text-red-700',
};

export const OrderDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const qc = useQueryClient();

  const { data: order, isLoading } = useQuery({
    queryKey: ['order', id],
    queryFn: () => ordersApi.getById(Number(id)),
    enabled: !!id,
  });

  const cancelMutation = useMutation({
    mutationFn: () => ordersApi.cancel(Number(id), 'Cancelado por el cliente'),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['order', id] }),
  });

  if (isLoading) return <div className="p-8 text-gray-500">Cargando...</div>;
  if (!order) return <div className="p-8 text-red-500">Pedido no encontrado.</div>;

  const canCancel = order.status === 'PENDIENTE' || order.status === 'CONFIRMADO';

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <button onClick={() => navigate('/pedidos')} className="text-sm text-gray-500 hover:text-orange-500 mb-6">
        ← Mis pedidos
      </button>

      <div className="flex justify-between items-start mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">Pedido #{order.id}</h1>
          <p className="text-sm text-gray-400 mt-1">{new Date(order.created_at).toLocaleString('es-AR')}</p>
        </div>
        <span className={`text-sm font-medium px-3 py-1 rounded-full ${STATUS_COLORS[order.status]}`}>
          {STATUS_LABELS[order.status]}
        </span>
      </div>

      {/* Ítems */}
      <div className="bg-white border border-gray-200 rounded-xl p-5 mb-4">
        <h2 className="font-semibold text-gray-700 mb-3">Ítems</h2>
        <ul className="divide-y divide-gray-100">
          {order.items?.map((item, i) => (
            <li key={i} className="py-2 flex justify-between text-sm">
              <span>Producto #{item.product_id} <span className="text-gray-400">x{item.quantity}</span></span>
              <span className="font-medium">${(Number(item.price) * item.quantity).toFixed(2)}</span>
            </li>
          ))}
        </ul>
        <div className="border-t pt-3 mt-3 flex justify-between font-bold">
          <span>Total</span>
          <span className="text-orange-500">${Number(order.total).toFixed(2)}</span>
        </div>
      </div>

      {/* Dirección */}
      <div className="bg-white border border-gray-200 rounded-xl p-5 mb-4">
        <h2 className="font-semibold text-gray-700 mb-2">Dirección de entrega</h2>
        <p className="text-sm text-gray-600">{order.direccion_calle} {order.direccion_numero}</p>
        <p className="text-sm text-gray-500">{order.direccion_ciudad}</p>
      </div>

      {/* Pagar si está pendiente */}
      {order.status === 'PENDIENTE' && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-5 mb-4">
          <p className="text-sm text-yellow-700 mb-3">Tu pedido está esperando el pago.</p>
          <button
            onClick={() => navigate(`/pago/iniciar/${order.id}`)}
            className="bg-orange-500 hover:bg-orange-600 text-white px-5 py-2 rounded-lg text-sm font-semibold transition"
          >
            Pagar ahora
          </button>
        </div>
      )}

      {/* Cancelar */}
      {canCancel && (
        <button
          onClick={() => { if (confirm('¿Cancelar este pedido?')) cancelMutation.mutate(); }}
          disabled={cancelMutation.isPending}
          className="w-full border border-red-300 text-red-500 hover:bg-red-50 py-2 rounded-lg text-sm transition mt-2"
        >
          {cancelMutation.isPending ? 'Cancelando...' : 'Cancelar pedido'}
        </button>
      )}
    </div>
  );
};
