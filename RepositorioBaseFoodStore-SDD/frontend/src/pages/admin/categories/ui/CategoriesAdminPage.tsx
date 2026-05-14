import React, { useMemo } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { PageContainer } from '@/shared/ui/PageContainer';
import { helpContent } from '@/shared/utils/helpContent';
import { useFormModal } from '@/shared/hooks/useFormModal';
import { useConfirmDialog } from '@/shared/hooks/useConfirmDialog';
import { categoriesApi, Category } from '@/shared/api/categoriesApi';
import { HelpButton } from '@/shared/ui/HelpButton';
import { handleError } from '@/shared/utils/logger';

export const CategoriesAdminPage = () => {
  const queryClient = useQueryClient();
  const { data: categories, isLoading } = useQuery({ queryKey: ['categories'], queryFn: categoriesApi.list });

  const modal = useFormModal<{ name: string; description: string }, Category>({ name: '', description: '' });
  const deleteDialog = useConfirmDialog<Category>();

  const createMutation = useMutation({
    mutationFn: categoriesApi.create,
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['categories'] }); modal.close(); },
    onError: (err) => alert(handleError(err, 'Create Category'))
  });

  const updateMutation = useMutation({
    mutationFn: (args: { id: number; payload: any }) => categoriesApi.update(args.id, args.payload),
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['categories'] }); modal.close(); },
    onError: (err) => alert(handleError(err, 'Update Category'))
  });

  const deleteMutation = useMutation({
    mutationFn: categoriesApi.remove,
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['categories'] }); deleteDialog.close(); },
    onError: (err) => alert(handleError(err, 'Delete Category'))
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (modal.selectedItem) {
      updateMutation.mutate({ id: modal.selectedItem.id, payload: modal.formData });
    } else {
      createMutation.mutate(modal.formData);
    }
  };

  return (
    <PageContainer
      title="Categorías"
      description="Organizá tu catálogo de productos."
      actions={
        <button onClick={() => modal.openCreate()} className="btn-premium py-2 px-6 text-sm">
          + Nueva Categoría
        </button>
      }
    >
      <div className="glass-card rounded-[2rem] border-white/60 overflow-hidden shadow-xl">
        {isLoading ? (
          <div className="p-12 text-center text-gray-400 animate-pulse font-medium">Cargando categorías...</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-gray-50/50 border-b border-gray-100">
                  <th className="px-8 py-5 font-black text-[10px] text-gray-400 uppercase tracking-[0.2em]">Nombre</th>
                  <th className="px-8 py-5 font-black text-[10px] text-gray-400 uppercase tracking-[0.2em]">Descripción</th>
                  <th className="px-8 py-5 font-black text-[10px] text-gray-400 uppercase tracking-[0.2em] text-right">Acciones</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {categories?.map(cat => (
                  <tr key={cat.id} className="hover:bg-orange-50/30 transition-colors group">
                    <td className="px-8 py-5 font-bold text-gray-900">{cat.name}</td>
                    <td className="px-8 py-5 text-gray-500 font-medium">{cat.description || '—'}</td>
                    <td className="px-8 py-5 text-right">
                      <div className="flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button onClick={() => modal.openEdit(cat, { name: cat.name, description: cat.description || '' })} className="bg-white border border-gray-200 text-gray-600 hover:text-orange-600 hover:border-orange-200 px-4 py-1.5 rounded-xl text-xs font-bold transition-all">
                          Editar
                        </button>
                        <button onClick={() => deleteDialog.open(cat)} className="bg-white border border-gray-200 text-rose-400 hover:text-rose-600 hover:border-rose-200 px-4 py-1.5 rounded-xl text-xs font-bold transition-all">
                          Borrar
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
                {categories?.length === 0 && (
                  <tr>
                    <td colSpan={3} className="px-8 py-20 text-center">
                      <p className="text-gray-400 font-bold uppercase tracking-widest text-xs">No hay categorías registradas</p>
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Modal Form */}
      {modal.isOpen && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/40 backdrop-blur-sm p-4 animate-in fade-in duration-300">
          <div className="glass-card rounded-[2.5rem] w-full max-w-md border-white/60 shadow-2xl animate-in zoom-in-95 duration-300 overflow-hidden">
            <div className="flex justify-between items-center p-8 border-b border-gray-100 bg-white/50">
              <h3 className="text-2xl font-bold text-gray-900">{modal.selectedItem ? 'Editar Categoría' : 'Nueva Categoría'}</h3>
              <button onClick={modal.close} className="w-10 h-10 flex items-center justify-center rounded-full hover:bg-gray-100 text-gray-400 transition-colors">&times;</button>
            </div>
            <form onSubmit={handleSubmit} className="p-8 space-y-6 bg-white/30">
              <div className="space-y-2">
                <label className="block text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Nombre</label>
                <input required type="text" value={modal.formData.name} onChange={e => modal.setFormData(prev => ({ ...prev, name: e.target.value }))} className="input-premium" placeholder="Ej: Hamburguesas" />
              </div>
              <div className="space-y-2">
                <label className="block text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Descripción</label>
                <textarea value={modal.formData.description} onChange={e => modal.setFormData(prev => ({ ...prev, description: e.target.value }))} className="input-premium h-24 resize-none" placeholder="Breve descripción..." />
              </div>
              <div className="pt-4 flex gap-4">
                <button type="submit" disabled={createMutation.isPending || updateMutation.isPending} className="flex-[2] btn-premium py-3">
                  {modal.selectedItem ? 'Guardar Cambios' : 'Crear Categoría'}
                </button>
                <button type="button" onClick={modal.close} className="flex-1 bg-white border border-gray-200 text-gray-500 font-bold py-3 rounded-2xl hover:bg-gray-50 transition-all">
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Delete Dialog */}
      {deleteDialog.isOpen && deleteDialog.item && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/40 backdrop-blur-sm p-4 animate-in fade-in duration-300">
          <div className="glass-card rounded-[2.5rem] w-full max-w-sm p-10 text-center border-white/60 shadow-2xl animate-in zoom-in-95 duration-300">
            <div className="w-20 h-20 bg-rose-50 text-rose-500 rounded-3xl flex items-center justify-center mx-auto mb-6 text-4xl shadow-inner italic">!</div>
            <h3 className="text-2xl font-bold text-gray-900 mb-2">¿Eliminar categoría?</h3>
            <p className="text-gray-500 font-medium mb-8 leading-relaxed">Vas a borrar <span className="text-gray-900 font-bold">"{deleteDialog.item.name}"</span>. Esta acción es permanente.</p>
            <div className="flex gap-4">
              <button onClick={() => deleteMutation.mutate(deleteDialog.item!.id)} disabled={deleteMutation.isPending} className="flex-1 bg-rose-500 hover:bg-rose-600 text-white py-3 rounded-2xl font-bold transition-all active:scale-95 shadow-lg shadow-rose-100">
                Eliminar
              </button>
              <button onClick={deleteDialog.close} className="flex-1 bg-gray-100 text-gray-500 py-3 rounded-2xl font-bold hover:bg-gray-200 transition-all">
                Cancelar
              </button>
            </div>
          </div>
        </div>
      )}
    </PageContainer>
  );
};
