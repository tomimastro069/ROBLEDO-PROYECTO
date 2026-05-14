import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { ordersApi, type OrderStatus } from '@/shared/api/ordersApi';

const STATUS_LABELS: Record<OrderStatus, string> = {
  PENDIENTE: 'Pendiente',
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

const NEXT_STATUS: Partial<Record<OrderStatus, OrderStatus>> = {
  CONFIRMADO: 'EN_PREPARACION',
  EN_PREPARACION: 'EN_CAMINO',
  EN_CAMINO: 'ENTREGADO',
};

const NEXT_LABELS: Partial<Record<OrderStatus, string>> = {
  CONFIRMADO: 'Iniciar preparación',
  EN_PREPARACION: 'Marcar en camino',
  EN_CAMINO: 'Entregado',
};

export const GestorPedidosPage = () => {
  const qc = useQueryClient();
  const [filterStatus, setFilterStatus] = useState<OrderStatus | ''>('');
  const [showCancelled, setShowCancelled] = useState(false);

  const { data: orders, isLoading } = useQuery({
    queryKey: ['admin-orders'],
    queryFn: () => ordersApi.listAll(),
    refetchInterval: 15000,
  });

  const advanceMutation = useMutation({
    mutationFn: ({ id, status }: { id: number; status: OrderStatus }) =>
      ordersApi.updateStatus(id, status, 'Avance de estado por gestor'),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin-orders'] }),
  });

  const cancelMutation = useMutation({
    mutationFn: ({ id }: { id: number }) => ordersApi.cancel(id, 'Cancelado por gestor'),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin-orders'] }),
  });

  const filtered = (orders ?? []).filter((o) => {
    // Si el usuario eligió específicamente un estado en los chips, manda ese
    if (filterStatus) return o.status === filterStatus;

    // Si está en "Todos", respetamos el botón de mostrar/ocultar cancelados
    return showCancelled || o.status !== 'CANCELADO';
  });

  const counts = (orders ?? []).reduce<Record<string, number>>((acc, o) => {
    acc[o.status] = (acc[o.status] ?? 0) + 1;
    return acc;
  }, {});

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
        <h1 className="text-2xl sm:text-3xl font-bold text-gray-800">Panel de Pedidos</h1>

        <button
          onClick={() => setShowCancelled(!showCancelled)}
          className={`text-[10px] font-bold uppercase tracking-widest px-4 py-2 border-2 transition-all ${showCancelled
            ? 'bg-red-50 border-red-200 text-red-600'
            : 'bg-white border-gray-100 text-gray-400 hover:border-gray-200'
            }`}
        >
          {showCancelled ? '🚫 Ocultando Cancelados' : '👁️ Mostrar Cancelados'}
        </button>
      </div>

      {/* KPI chips */}
      {!isLoading && (
        <div className="flex flex-wrap gap-2 mb-6">
          <button onClick={() => setFilterStatus('')}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition border ${filterStatus === '' ? 'bg-gray-800 text-white border-gray-800' : 'border-gray-300 text-gray-600 hover:bg-gray-50'}`}>
            Todos ({showCancelled ? orders?.length : (orders?.length ?? 0) - (counts['CANCELADO'] ?? 0)})
          </button>
          {(['PENDIENTE', 'CONFIRMADO', 'EN_PREPARACION', 'EN_CAMINO', 'ENTREGADO', 'CANCELADO'] as OrderStatus[]).map((s) => (
            counts[s] ? (
              <button key={s} onClick={() => setFilterStatus(s)}
                className={`px-4 py-1.5 rounded-full text-sm font-medium transition border ${filterStatus === s ? 'bg-gray-800 text-white border-gray-800' : `${STATUS_COLORS[s]} border-transparent`}`}>
                {STATUS_LABELS[s]} ({counts[s]})
              </button>
            ) : null
          ))}
        </div>
      )}

      {isLoading ? (
        <div className="space-y-3">
          {Array.from({ length: 5 }).map((_, i) => <div key={i} className="bg-gray-100 rounded-xl h-20 animate-pulse" />)}
        </div>
      ) : filtered.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-xl border border-gray-100">
          <p className="text-gray-400">No hay pedidos con ese estado.</p>
        </div>
      ) : (
        <>
          {/* Tabla desktop */}
          <div className="hidden lg:block bg-white rounded-xl border border-gray-200 overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase">Pedido</th>
                  <th className="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase">Fecha</th>
                  <th className="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase">Dirección</th>
                  <th className="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase">Total</th>
                  <th className="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase">Estado</th>
                  <th className="px-5 py-3 text-xs font-semibold text-gray-500 uppercase text-right">Acciones</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {filtered.map((order) => {
                  const nextStatus = NEXT_STATUS[order.status];
                  const canCancel = ['PENDIENTE', 'CONFIRMADO', 'EN_PREPARACION'].includes(order.status);
                  return (
                    <tr key={order.id} className="hover:bg-gray-50 transition">
                      <td className="px-5 py-4 font-bold text-gray-800">#{order.id}</td>
                      <td className="px-5 py-4 text-gray-500 text-xs">
                        {new Date(order.created_at).toLocaleString('es-AR', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' })}
                      </td>
                      <td className="px-5 py-4 text-gray-600 text-xs">
                        {order.direccion_calle} {order.direccion_numero}, {order.direccion_ciudad}
                      </td>
                      <td className="px-5 py-4 font-bold text-orange-500">${Number(order.total).toFixed(2)}</td>
                      <td className="px-5 py-4">
                        <span className={`text-xs font-medium px-3 py-1 rounded-full ${STATUS_COLORS[order.status]}`}>
                          {STATUS_LABELS[order.status]}
                        </span>
                      </td>
                      <td className="px-5 py-4">
                        <div className="flex gap-2 justify-end">
                          {nextStatus && (
                            <button
                              onClick={() => advanceMutation.mutate({ id: order.id, status: nextStatus })}
                              disabled={advanceMutation.isPending}
                              className="bg-blue-500 hover:bg-blue-600 text-white text-xs px-3 py-1.5 rounded-lg transition whitespace-nowrap"
                            >
                              {NEXT_LABELS[order.status]}
                            </button>
                          )}
                          {canCancel && (
                            <button
                              onClick={() => { if (confirm('¿Cancelar pedido?')) cancelMutation.mutate({ id: order.id }); }}
                              className="border border-red-200 text-red-500 hover:bg-red-50 text-xs px-3 py-1.5 rounded-lg transition"
                            >
                              Cancelar
                            </button>
                          )}
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {/* Cards mobile/tablet */}
          <div className="lg:hidden space-y-3">
            {filtered.map((order) => {
              const nextStatus = NEXT_STATUS[order.status];
              const canCancel = ['PENDIENTE', 'CONFIRMADO', 'EN_PREPARACION'].includes(order.status);
              return (
                <div key={order.id} className="bg-white border border-gray-200 rounded-xl p-4">
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <p className="font-bold text-gray-800">Pedido #{order.id}</p>
                      <p className="text-xs text-gray-400 mt-0.5">{new Date(order.created_at).toLocaleString('es-AR')}</p>
                      <p className="text-xs text-gray-500 mt-1">{order.direccion_calle} {order.direccion_numero}, {order.direccion_ciudad}</p>
                    </div>
                    <span className={`text-xs font-medium px-3 py-1 rounded-full ${STATUS_COLORS[order.status]}`}>
                      {STATUS_LABELS[order.status]}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-orange-500">${Number(order.total).toFixed(2)}</span>
                    <div className="flex gap-2">
                      {nextStatus && (
                        <button onClick={() => advanceMutation.mutate({ id: order.id, status: nextStatus })}
                          className="bg-blue-500 hover:bg-blue-600 text-white text-xs px-3 py-1.5 rounded-lg transition">
                          {NEXT_LABELS[order.status]}
                        </button>
                      )}
                      {canCancel && (
                        <button onClick={() => { if (confirm('¿Cancelar?')) cancelMutation.mutate({ id: order.id }); }}
                          className="border border-red-200 text-red-500 text-xs px-3 py-1.5 rounded-lg transition">
                          Cancelar
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </>
      )}
    </div>
  );
};
