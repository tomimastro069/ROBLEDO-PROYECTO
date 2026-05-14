import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
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

const PAYMENT_LABELS: Record<string, string> = {
  MERCADOPAGO: '💳 MP',
  EFECTIVO: '💵 Efectivo',
  TRANSFERENCIA: '🏦 Transf.',
};

export const OrdersPage = () => {
  const { data: orders, isLoading } = useQuery({
    queryKey: ['orders'],
    queryFn: () => ordersApi.list(),
  });

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-2xl sm:text-3xl font-bold text-gray-800 mb-6">Mis Pedidos</h1>

      {isLoading ? (
        <div className="space-y-3">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="bg-gray-100 rounded-xl h-20 animate-pulse" />
          ))}
        </div>
      ) : orders?.length === 0 ? (
        <div className="text-center py-20 bg-white rounded-xl border border-gray-100">
          <p className="text-gray-400 text-lg mb-3">Todavía no realizaste ningún pedido.</p>
          <Link to="/catalogo" className="bg-[#d32f2f] hover:bg-[#b71c1c] text-white px-6 py-2 rounded-lg text-sm font-medium transition inline-block">
            Ver catálogo
          </Link>
        </div>
      ) : (
        <>
          {/* Tabla en desktop */}
          <div className="hidden md:block bg-white rounded-xl border border-gray-200 overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Pedido</th>
                  <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Fecha</th>
                  <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Ítems</th>
                  <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Total</th>
                  <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Método Pago</th>
                  <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Estado</th>
                  <th className="px-6 py-3" />
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {orders?.map((order) => (
                  <tr key={order.id} className="hover:bg-gray-50 transition">
                    <td className="px-6 py-4 font-semibold text-gray-800">#{order.id}</td>
                    <td className="px-6 py-4 text-gray-500">
                      {new Date(order.created_at).toLocaleDateString('es-AR', { day: '2-digit', month: 'short', year: 'numeric' })}
                    </td>
                    <td className="px-6 py-4 text-gray-600">{order.items?.length ?? 0}</td>
                    <td className="px-6 py-4 font-bold text-[#d32f2f]">${Number(order.total).toFixed(2)}</td>
                    <td className="px-6 py-4 text-xs text-gray-600 font-medium">
                      {order.forma_pago_codigo ? PAYMENT_LABELS[order.forma_pago_codigo] || order.forma_pago_codigo : 'N/A'}
                    </td>
                    <td className="px-6 py-4">
                      <span className={`text-xs font-medium px-3 py-1 rounded-full ${STATUS_COLORS[order.status]}`}>
                        {STATUS_LABELS[order.status]}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <Link to={`/pedidos/${order.id}`} className="text-[#d32f2f] hover:underline text-xs font-medium">
                        Ver detalle →
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Cards en mobile */}
          <div className="md:hidden space-y-3">
            {orders?.map((order) => (
              <Link key={order.id} to={`/pedidos/${order.id}`}
                className="block bg-white border border-gray-200 rounded-xl p-4 hover:border-red-300 transition">
                <div className="flex justify-between items-start mb-2">
                  <p className="font-semibold text-gray-800">Pedido #{order.id}</p>
                  <span className={`text-xs font-medium px-2 py-1 rounded-full ${STATUS_COLORS[order.status]}`}>
                    {STATUS_LABELS[order.status]}
                  </span>
                </div>
                <p className="text-xs text-gray-400">{new Date(order.created_at).toLocaleDateString('es-AR')}</p>
                <div className="flex justify-between mt-2">
                  <span className="text-sm text-gray-500">{order.items?.length ?? 0} ítems</span>
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-[#d32f2f]">${Number(order.total).toFixed(2)}</span>
                    {order.forma_pago_codigo && (
                      <span className="text-xs font-medium text-gray-500 bg-gray-100 px-2 py-0.5 rounded-md">
                        {PAYMENT_LABELS[order.forma_pago_codigo] || order.forma_pago_codigo}
                      </span>
                    )}
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </>
      )}
    </div>
  );
};
