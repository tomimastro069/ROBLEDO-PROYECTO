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
  MERCADOPAGO: 'MP',
  EFECTIVO: 'Efectivo',
  TRANSFERENCIA: 'Transf.',
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
            : 'bg-white border-gray-100 text-gray-400 hover:border-red-200 hover:text-red-600'
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
        <div className="space-y-4">
          {Array.from({ length: 5 }).map((_, i) => <div key={i} className="bg-gray-100/50 rounded-[2rem] h-24 animate-pulse" />)}
        </div>
      ) : filtered.length === 0 ? (
        <div className="text-center py-24 glass-card rounded-[2.5rem] border-white/60">
          <div className="text-5xl mb-6 opacity-20 italic font-black">?</div>
          <p className="text-gray-400 font-bold uppercase tracking-[0.2em] text-xs">No hay pedidos con ese estado</p>
        </div>
      ) : (
        <div className="space-y-10">
          {/* Tabla desktop */}
          <div className="hidden lg:block glass-card rounded-[2.5rem] border-white/60 overflow-hidden shadow-xl">
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-gray-50/50 border-b border-gray-100">
                    <th className="px-8 py-5 font-black text-[10px] text-gray-400 uppercase tracking-[0.2em]">ID</th>
                    <th className="px-8 py-5 font-black text-[10px] text-gray-400 uppercase tracking-[0.2em]">Fecha / Hora</th>
                    <th className="px-8 py-5 font-black text-[10px] text-gray-400 uppercase tracking-[0.2em]">Cliente / Dirección</th>
                    <th className="px-8 py-5 font-black text-[10px] text-gray-400 uppercase tracking-[0.2em]">Pago</th>
                    <th className="px-8 py-5 font-black text-[10px] text-gray-400 uppercase tracking-[0.2em] text-right">Total</th>
                    <th className="px-8 py-5 font-black text-[10px] text-gray-400 uppercase tracking-[0.2em]">Estado</th>
                    <th className="px-8 py-5 font-black text-[10px] text-gray-400 uppercase tracking-[0.2em] text-right">Acciones</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-50">
                  {paginatedItems.map((order) => {
                    const nextStatus = NEXT_STATUS[order.status];
                    const canCancel = ['PENDIENTE', 'CONFIRMADO', 'EN_PREPARACION'].includes(order.status);
                    return (
                      <tr key={order.id} className="hover:bg-red-50/30 transition-colors group">
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
                          <div className="text-xs font-bold text-gray-800 truncate max-w-[180px]">
                            {order.direccion_calle} {order.direccion_numero}
                          </div>
                          <div className="text-[10px] text-gray-400 font-bold uppercase tracking-wider">
                            {order.direccion_ciudad}
                          </div>
                        </td>
                        <td className="px-8 py-5">
                          <span className="text-[10px] font-black uppercase tracking-widest bg-gray-100/50 px-2.5 py-1 rounded-lg text-gray-500">
                            {order.forma_pago_codigo ? (PAYMENT_LABELS[order.forma_pago_codigo] || order.forma_pago_codigo) : 'N/A'}
                          </span>
                        </td>
                        <td className="px-8 py-5 text-right font-black text-[#d32f2f] text-lg">
                          ${Number(order.total).toLocaleString('es-AR', { minimumFractionDigits: 2 })}
                        </td>
                        <td className="px-8 py-5">
                          <span className={`inline-block px-3 py-1 rounded-xl text-[10px] font-black uppercase tracking-wider border ${STATUS_COLORS[order.status]}`}>
                            {STATUS_LABELS[order.status]}
                          </span>
                        </td>
                        <td className="px-8 py-5 text-right">
                          <div className="flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                            {nextStatus && (
                              <button
                                onClick={() => advanceMutation.mutate({ id: order.id, status: nextStatus })}
                                disabled={advanceMutation.isPending}
                                className="bg-gray-900 text-white text-[10px] font-black uppercase tracking-widest px-4 py-2 rounded-xl hover:bg-red-600 transition-all active:scale-95"
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
          </div>

          {/* Cards mobile */}
          <div className="lg:hidden space-y-4">
            {paginatedItems.map((order) => {
              const nextStatus = NEXT_STATUS[order.status];
              const canCancel = ['PENDIENTE', 'CONFIRMADO', 'EN_PREPARACION'].includes(order.status);
              return (
                <div key={order.id} className="glass-card rounded-[2rem] p-6 border-white/60 shadow-lg">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <p className="font-black text-gray-900 text-lg">#{order.id}</p>
                      <p className="text-[10px] text-gray-400 font-bold uppercase tracking-widest">
                        {new Date(order.created_at).toLocaleString('es-AR')}
                      </p>
                    </div>
                    <span className={`px-3 py-1 rounded-xl text-[10px] font-black uppercase tracking-wider border ${STATUS_COLORS[order.status]}`}>
                      {STATUS_LABELS[order.status]}
                    </span>
                  </div>

                  <div className="space-y-4 mb-6">
                    <div className="text-xs text-gray-600 font-medium">
                      <p className="font-bold text-gray-900">{order.direccion_calle} {order.direccion_numero}</p>
                      <p className="uppercase tracking-widest text-[10px] text-gray-400">{order.direccion_ciudad}</p>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-[10px] font-black uppercase tracking-widest bg-gray-100/50 px-2 py-1 rounded-lg text-gray-500">
                        {order.forma_pago_codigo ? (PAYMENT_LABELS[order.forma_pago_codigo] || order.forma_pago_codigo) : 'N/A'}
                      </span>
                      <span className="font-black text-[#d32f2f] text-xl">
                        ${Number(order.total).toLocaleString('es-AR', { minimumFractionDigits: 2 })}
                      </span>
                    </div>
                  </div>

                  <div className="flex gap-2">
                    {nextStatus && (
                      <button onClick={() => advanceMutation.mutate({ id: order.id, status: nextStatus })}
                        className="flex-1 bg-gray-900 text-white text-[10px] font-black uppercase tracking-widest py-3 rounded-2xl hover:bg-red-600 transition-all">
                        {NEXT_LABELS[order.status]}
                      </button>
                    )}
                    {canCancel && (
                      <button onClick={() => { if (confirm('¿Cancelar?')) cancelMutation.mutate({ id: order.id }); }}
                        className="flex-1 bg-white border border-rose-100 text-rose-500 text-[10px] font-black uppercase tracking-widest py-3 rounded-2xl hover:bg-rose-50 transition-all">
                        Cancelar
                      </button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Paginación premium */}
          {totalPages > 1 && (
            <div className="flex items-center justify-center gap-4 pt-4">
              <button onClick={() => setCurrentPage(currentPage - 1)} disabled={currentPage === 1} className="w-12 h-12 flex items-center justify-center bg-white border border-gray-200 rounded-2xl text-gray-500 hover:bg-gray-50 disabled:opacity-30 transition-all font-bold shadow-sm">
                &larr;
              </button>
              <div className="bg-white border border-gray-200 px-6 py-3 rounded-2xl text-sm font-black text-gray-900 shadow-sm">
                {currentPage} <span className="text-gray-300 mx-2">/</span> {totalPages}
              </div>
              <button onClick={() => setCurrentPage(currentPage + 1)} disabled={currentPage === totalPages} className="w-12 h-12 flex items-center justify-center bg-white border border-gray-200 rounded-2xl text-gray-500 hover:bg-gray-50 disabled:opacity-30 transition-all font-bold shadow-sm">
                &rarr;
              </button>
            </div>
          )}
        </div>
      )}
    </PageContainer>
  );
};
