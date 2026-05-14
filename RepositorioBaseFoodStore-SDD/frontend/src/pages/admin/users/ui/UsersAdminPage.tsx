import React from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { adminApi, AdminUser } from '@/shared/api/adminApi';
import { PageContainer } from '@/shared/ui/PageContainer';
import { useFormModal } from '@/shared/hooks/useFormModal';
import { usePagination } from '@/shared/hooks/usePagination';
import { handleError } from '@/shared/utils/logger';

export const UsersAdminPage = () => {
  const queryClient = useQueryClient();
  const { data: users = [], isLoading } = useQuery({
    queryKey: ['admin-users'],
    queryFn: () => adminApi.listUsers()
  });
  const { data: roles = [] } = useQuery({
    queryKey: ['admin-roles'],
    queryFn: () => adminApi.listRoles()
  });

  const { paginatedItems, currentPage, totalPages, setCurrentPage } = usePagination(users, 10);

  const modal = useFormModal<{ name: string; email: string; password?: string; role_id: number; is_active: boolean }, AdminUser>({
    name: '', email: '', password: '', role_id: 0, is_active: true
  });

  const createMutation = useMutation({
    mutationFn: adminApi.createUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-users'] });
      modal.close();
    },
    onError: (err) => alert(handleError(err, 'Crear Usuario'))
  });

  const updateMutation = useMutation({
    mutationFn: (args: { id: number; payload: any }) => adminApi.updateUser(args.id, args.payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-users'] });
      modal.close();
    },
    onError: (err) => alert(handleError(err, 'Actualizar Usuario'))
  });

  const toggleMutation = useMutation({
    mutationFn: (args: { id: number; active: boolean }) => adminApi.toggleUserActive(args.id, args.active),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['admin-users'] }),
    onError: (err) => alert(handleError(err, 'Cambiar Estado'))
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (modal.selectedItem) {
      const { password, ...payload } = modal.formData;
      updateMutation.mutate({ id: modal.selectedItem.id, payload });
    } else {
      createMutation.mutate(modal.formData);
    }
  };

  return (
    <PageContainer
      title="Gestión de Usuarios"
      description="Crea y administra accesos al sistema."
      actions={
        <button
          onClick={() => modal.openCreate()}
          className="bg-[#d32f2f] hover:bg-[#b71c1c] text-white px-8 py-3 text-xs font-black uppercase tracking-widest transition shadow-lg"
        >
          + Nuevo Usuario
        </button>
      }
    >
      <div className="bg-white border-2 border-gray-100 overflow-hidden shadow-sm">
        {isLoading ? (
          <div className="p-20 text-center text-[10px] font-bold text-gray-300 uppercase tracking-widest animate-pulse">
            Sincronizando Usuarios...
          </div>
        ) : (
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-gray-50 border-b-2 border-gray-100">
                <th className="px-8 py-5 text-[10px] font-black text-gray-400 uppercase tracking-widest">Nombre / Email</th>
                <th className="px-8 py-5 text-[10px] font-black text-gray-400 uppercase tracking-widest text-center">Rol</th>
                <th className="px-8 py-5 text-[10px] font-black text-gray-400 uppercase tracking-widest text-center">Estado</th>
                <th className="px-8 py-5 text-[10px] font-black text-gray-400 uppercase tracking-widest text-right">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {paginatedItems.map(u => (
                <tr key={u.id} className="hover:bg-gray-50/50 transition-colors group">
                  <td className="px-8 py-5">
                    <p className="text-sm font-black text-gray-900 uppercase tracking-tight group-hover:text-[#d32f2f] transition-colors">{u.name}</p>
                    <p className="text-[10px] font-bold text-gray-400 mt-1">{u.email}</p>
                  </td>
                  <td className="px-8 py-5 text-center">
                    <span className="text-[10px] font-black text-gray-500 bg-gray-100 px-3 py-1 uppercase tracking-widest">
                      {roles.find(r => r.id === u.role_id)?.name.replace('_', ' ') || 'Sin Rol'}
                    </span>
                  </td>
                  <td className="px-8 py-5 text-center">
                    <button
                      onClick={() => toggleMutation.mutate({ id: u.id, active: !u.is_active })}
                      className={`text-[9px] font-black px-3 py-1 uppercase tracking-widest transition ${u.is_active ? 'text-green-600 bg-green-50' : 'text-red-600 bg-red-50'}`}
                    >
                      {u.is_active ? 'Activo' : 'Inactivo'}
                    </button>
                  </td>
                  <td className="px-8 py-5 text-right">
                    <button
                      onClick={() => modal.openEdit(u, {
                        name: u.name || '',
                        email: u.email,
                        role_id: u.role_id || 0,
                        is_active: u.is_active
                      })}
                      className="text-[10px] font-black text-gray-400 hover:text-[#d32f2f] uppercase tracking-widest transition"
                    >
                      [ Editar ]
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {totalPages > 1 && (
        <div className="flex items-center justify-center gap-4 mt-12">
          <button onClick={() => setCurrentPage(currentPage - 1)} disabled={currentPage === 1} className="text-[10px] font-black uppercase tracking-widest disabled:opacity-20">Anterior</button>
          <span className="text-[10px] font-bold text-gray-400">{currentPage} / {totalPages}</span>
          <button onClick={() => setCurrentPage(currentPage + 1)} disabled={currentPage === totalPages} className="text-[10px] font-black uppercase tracking-widest disabled:opacity-20">Siguiente</button>
        </div>
      )}

      {modal.isOpen && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <div className="bg-white border-t-8 border-[#d32f2f] w-full max-w-md shadow-2xl">
            <div className="flex justify-between items-center p-8 border-b border-gray-100">
              <h3 className="text-xl font-black uppercase tracking-tighter">
                {modal.selectedItem ? 'Editar Usuario' : 'Nuevo Usuario'}
              </h3>
              <button onClick={modal.close} className="text-gray-300 hover:text-red-500 text-3xl font-light">&times;</button>
            </div>
            <form onSubmit={handleSubmit} className="p-8 space-y-6">
              <div>
                <label className="block text-[10px] font-black text-gray-400 uppercase tracking-widest mb-2">Nombre Completo</label>
                <input required type="text" value={modal.formData.name} onChange={e => modal.setFormData(prev => ({ ...prev, name: e.target.value }))} className="w-full border-2 border-gray-100 px-4 py-3 text-sm focus:outline-none focus:border-[#d32f2f] transition-colors font-bold" />
              </div>
              <div>
                <label className="block text-[10px] font-black text-gray-400 uppercase tracking-widest mb-2">Email de Acceso</label>
                <input required type="email" value={modal.formData.email} onChange={e => modal.setFormData(prev => ({ ...prev, email: e.target.value }))} className="w-full border-2 border-gray-100 px-4 py-3 text-sm focus:outline-none focus:border-[#d32f2f] transition-colors font-bold" />
              </div>
              {!modal.selectedItem && (
                <div>
                  <label className="block text-[10px] font-black text-gray-400 uppercase tracking-widest mb-2">Contraseña Inicial</label>
                  <input required type="password" value={modal.formData.password} onChange={e => modal.setFormData(prev => ({ ...prev, password: e.target.value }))} className="w-full border-2 border-gray-100 px-4 py-3 text-sm focus:outline-none focus:border-[#d32f2f] transition-colors font-bold" />
                </div>
              )}
              <div>
                <label className="block text-[10px] font-black text-gray-400 uppercase tracking-widest mb-2">Rol del Sistema</label>
                <select required value={modal.formData.role_id || ''} onChange={e => modal.setFormData(prev => ({ ...prev, role_id: parseInt(e.target.value) }))} className="w-full border-2 border-gray-100 px-4 py-3 text-sm focus:outline-none focus:border-[#d32f2f] transition-colors font-bold uppercase tracking-widest">
                  <option value="">Seleccionar Rol</option>
                  {roles
                    .filter(r => r.name !== 'sistema')
                    .map(r => <option key={r.id} value={r.id}>{r.name.replace('_', ' ')}</option>)}
                </select>
              </div>
              <div className="pt-6 flex gap-4">
                <button type="button" onClick={modal.close} className="flex-1 text-[10px] font-black uppercase tracking-widest text-gray-400 hover:text-gray-900 transition-colors">Cancelar</button>
                <button type="submit" disabled={createMutation.isPending || updateMutation.isPending} className="flex-1 bg-gray-900 hover:bg-[#d32f2f] text-white py-4 text-xs font-black uppercase tracking-widest transition">
                  {modal.selectedItem ? 'Guardar Cambios' : 'Crear Usuario'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </PageContainer>
  );
};
