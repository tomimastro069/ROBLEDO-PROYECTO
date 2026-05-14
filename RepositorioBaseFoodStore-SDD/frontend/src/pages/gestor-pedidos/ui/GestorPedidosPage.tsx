import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { ordersApi, type OrderStatus } from '@/shared/api/ordersApi';
import { usePagination } from '@/shared/hooks/usePagination';
import { PageContainer } from '@/shared/ui/PageContainer';

const STATUS_LABELS: Record<OrderStatus, string> = {
  PENDIENTE: 'Pendiente',
  CONFIRMADO: 'Confirmado',
  EN_PREPARACION: 'En preparación',
  EN_CAMINO: 'En camino',
  ENTREGADO: 'Entregado',
  CANCELADO: 'Cancelado',
};

const STATUS_COLORS: Record<OrderStatus, string> = {
  PENDIENTE: 'bg-yellow-50 text-yellow-600 border-yellow-100',
  CONFIRMADO: 'bg-blue-50 text-blue-600 border-blue-100',
  EN_PREPARACION: 'bg-purple-50 text-purple-600 border-purple-100',
  EN_CAMINO: 'bg-indigo-50 text-indigo-600 border-indigo-100',
  ENTREGADO: 'bg-emerald-50 text-emerald-600 border-emerald-100',
  CANCELADO: 'bg-rose-50 text-rose-500 border-rose-100',
};

const NEXT_STATUS: Partial<Record<OrderStatus, OrderStatus>> = {
  CONFIRMADO: 'EN_PREPARACION',
  EN_PREPARACION: 'EN_CAMINO',
  EN_CAMINO: 'ENTREGADO',
};

const NEXT_LABELS: Partial<Record<OrderStatus, string>> = {
  CONFIRMADO: 'Preparar',
  EN_PREPARACION: 'Despachar',
  EN_CAMINO: 'Entregar',
};

const PAYMENT_LABELS: Record<string, string> = {
  MERCADOPAGO: '💳 MP',
  EFECTIVO: '💵 Efectivo',
  TRANSFERENCIA: '🏦 Transf.',
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
    if (filterStatus) return o.status === filterStatus;
    return showCancelled || o.status !== 'CANCELADO';
  });

  const { paginatedItems, currentPage, totalPages, setCurrentPage } = usePagination(filtered, 10);

  const counts = (orders ?? []).reduce<Record<string, number>>((acc, o) => {
    acc[o.status] = (acc[o.status] ?? 0) + 1;
    return acc;
  }, {});

  return (
    <PageContainer
      title="Gestor de Pedidos"
      description="Control en tiempo real de las órdenes."
      actions={
        <button
          onClick={() => setShowCancelled(!showCancelled)}
          className={`text-[10px] font-black uppercase tracking-[0.2em] px-6 py-2.5 rounded-xl border-2 transition-all active:scale-95 ${showCancelled
            ? 'bg-rose-50 border-rose-200 text-rose-600'
            : 'bg-white border-gray-100 text-gray-400 hover:border-orange-200 hover:text-orange-500'
            }`}
        >
          {showCancelled ? 'Ocultando Cancelados' : 'Mostrar Cancelados'}
        </button>
      }
    >
      {/* KPI chips premium */}
      {!isLoading && (
        <div className="flex flex-wrap gap-3 mb-10">
          <button onClick={() => setFilterStatus('')}
            className={`px-5 py-2 rounded-2xl text-xs font-black uppercase tracking-widest transition-all border ${filterStatus === '' ? 'bg-gray-900 text-white border-gray-900 shadow-lg shadow-gray-200' : 'bg-white border-gray-100 text-gray-400 hover:border-gray-300'}`}>
            Todos ({showCancelled ? orders?.length : (orders?.length ?? 0) - (counts['CANCELADO'] ?? 0)})
          </button>
          {(['PENDIENTE', 'CONFIRMADO', 'EN_PREPARACION', 'EN_CAMINO', 'ENTREGADO', 'CANCELADO'] as OrderStatus[]).map((s) => (
            counts[s] ? (
              <button key={s} onClick={() => setFilterStatus(s)}
                className={`px-5 py-2 rounded-2xl text-xs font-black uppercase tracking-widest transition-all border ${filterStatus === s ? 'bg-gray-900 text-white border-gray-900 shadow-lg shadow-gray-200' : `${STATUS_COLORS[s]} hover:brightness-95`}`}>
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
              <tbody className="divide-y divide-gray-50">
                {paginatedItems.map((order) => {
                  const nextStatus = NEXT_STATUS[order.status];
                  const canCancel = ['PENDIENTE', 'CONFIRMADO', 'EN_PREPARACION'].includes(order.status);
                  return (
                    <tr key={order.id} className="hover:bg-orange-50/30 transition-colors group">
                      <td className="px-8 py-5 font-black text-gray-900">#{order.id}</td>
                      <td className="px-8 py-5">
                        <div className="text-xs font-bold text-gray-800">
                          {new Date(order.created_at).toLocaleDateString('es-AR')}
                        </div>
                        <div className="text-[10px] text-gray-400 uppercase font-bold">
                          {new Date(order.created_at).toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit' })}
                        </div>
                      </td>
                      <td className="px-8 py-5">
                        <div className="text-xs font-bold text-gray-800 truncate max-w-[200px]">
                          {order.direccion_calle} {order.direccion_numero}
                        </div>
                        <div className="text-[10px] text-gray-400 font-bold uppercase tracking-wider">
                          {order.direccion_ciudad}
                        </div>
                      </td>
                      <td className="px-8 py-5 text-right font-black text-orange-600 text-lg">
                        ${Number(order.total).toLocaleString('es-AR', { minimumFractionDigits: 2 })}
                      </td>
                      <td className="px-5 py-4 font-bold text-orange-500">${Number(order.total).toFixed(2)}</td>
                      <td className="px-5 py-4">
                        <span className={`text-xs font-medium px-3 py-1 rounded-full ${STATUS_COLORS[order.status]}`}>
                          {STATUS_LABELS[order.status]}
                        </span>
                      </td>
                      <td className="px-8 py-5 text-right">
                        <div className="flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                          {nextStatus && (
                            <button
                              onClick={() => advanceMutation.mutate({ id: order.id, status: nextStatus })}
                              disabled={advanceMutation.isPending}
                              className="bg-gray-900 text-white text-[10px] font-black uppercase tracking-widest px-4 py-2 rounded-xl hover:bg-orange-600 transition-all active:scale-95"
                            >
                              {NEXT_LABELS[order.status]}
                            </button>
                          )}
                          {canCancel && (
                            <button
                              onClick={() => { if (confirm('¿Cancelar pedido?')) cancelMutation.mutate({ id: order.id }); }}
                              className="bg-white border border-rose-100 text-rose-500 text-[10px] font-black uppercase tracking-widest px-4 py-2 rounded-xl hover:bg-rose-50 transition-all active:scale-95"
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
          <button onClick={() => setCurrentPage(currentPage + 1)} disabled={currentPage === totalPages} className="w-10 h-10 flex items-center justify-center bg-white border border-gray-200 rounded-xl text-gray-500 hover:bg-gray-50 disabled:opacity-30 transition-all font-bold">
            &rarr;
          </button>
        </div>
      )}
    </PageContainer>
  );
};
