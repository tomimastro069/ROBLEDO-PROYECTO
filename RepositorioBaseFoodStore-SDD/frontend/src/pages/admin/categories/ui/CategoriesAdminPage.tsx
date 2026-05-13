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
      title="Gestión de Categorías"
      description="Administra las categorías de productos."
      helpContent={helpContent.categories}
      actions={
        <button onClick={() => modal.openCreate()} className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-lg font-medium transition shadow-md shadow-orange-200">
          + Nueva Categoría
        </button>
      }
    >
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        {isLoading ? (
          <div className="p-8 text-center text-gray-400 animate-pulse">Cargando...</div>
        ) : (
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-gray-50 border-b border-gray-100">
                <th className="px-6 py-4 font-semibold text-gray-600 text-sm">Nombre</th>
                <th className="px-6 py-4 font-semibold text-gray-600 text-sm">Descripción</th>
                <th className="px-6 py-4 font-semibold text-gray-600 text-sm text-right">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {categories?.map(cat => (
                <tr key={cat.id} className="hover:bg-gray-50 transition">
                  <td className="px-6 py-4 font-medium text-gray-800">{cat.name}</td>
                  <td className="px-6 py-4 text-gray-500">{cat.description || '-'}</td>
                  <td className="px-6 py-4 text-right">
                    <button onClick={() => modal.openEdit(cat, { name: cat.name, description: cat.description || '' })} className="text-orange-500 hover:bg-orange-50 p-2 rounded-lg transition mr-2">Editar</button>
                    <button onClick={() => deleteDialog.open(cat)} className="text-red-500 hover:bg-red-50 p-2 rounded-lg transition">Borrar</button>
                  </td>
                </tr>
              ))}
              {categories?.length === 0 && (
                <tr><td colSpan={3} className="px-6 py-8 text-center text-gray-400">No hay categorías.</td></tr>
              )}
            </tbody>
          </table>
        )}
      </div>

      {/* Modal Form */}
      {modal.isOpen && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/50 p-4">
          <div className="bg-white rounded-xl shadow-xl w-full max-w-md animate-in fade-in zoom-in-95 duration-200">
            <div className="flex justify-between items-center p-6 border-b border-gray-100">
              <h3 className="text-xl font-bold">{modal.selectedItem ? 'Editar Categoría' : 'Nueva Categoría'}</h3>
              <button onClick={modal.close} className="text-gray-400 hover:text-gray-600 text-2xl leading-none">&times;</button>
            </div>
            <form onSubmit={handleSubmit} className="p-6 space-y-4">
              <div className="flex items-center gap-2 mb-2 bg-blue-50 text-blue-800 p-3 rounded-lg text-sm">
                <HelpButton size="sm" content={<p>Ingresa el nombre y la descripción para organizar tus productos.</p>} />
                <span>Completa los datos de la categoría.</span>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Nombre</label>
                <input required type="text" value={modal.formData.name} onChange={e => modal.setFormData(prev => ({ ...prev, name: e.target.value }))} className="w-full border border-gray-300 rounded-lg px-3 py-2" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Descripción</label>
                <input type="text" value={modal.formData.description} onChange={e => modal.setFormData(prev => ({ ...prev, description: e.target.value }))} className="w-full border border-gray-300 rounded-lg px-3 py-2" />
              </div>
              <div className="pt-4 flex gap-3">
                <button type="button" onClick={modal.close} className="flex-1 bg-gray-100 text-gray-700 py-2 rounded-lg font-medium hover:bg-gray-200">Cancelar</button>
                <button type="submit" disabled={createMutation.isPending || updateMutation.isPending} className="flex-1 bg-orange-500 text-white py-2 rounded-lg font-medium hover:bg-orange-600 disabled:opacity-50">Guardar</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Delete Dialog */}
      {deleteDialog.isOpen && deleteDialog.item && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/50 p-4">
          <div className="bg-white rounded-xl shadow-xl w-full max-w-sm p-6 text-center animate-in zoom-in-95">
            <div className="w-16 h-16 bg-red-100 text-red-500 rounded-full flex items-center justify-center mx-auto mb-4 text-3xl">⚠️</div>
            <h3 className="text-xl font-bold mb-2">¿Eliminar categoría?</h3>
            <p className="text-gray-500 mb-6">Vas a borrar "{deleteDialog.item.name}". Esta acción no se puede deshacer.</p>
            <div className="flex gap-3">
              <button onClick={deleteDialog.close} className="flex-1 bg-gray-100 text-gray-700 py-2 rounded-lg font-medium">Cancelar</button>
              <button onClick={() => deleteMutation.mutate(deleteDialog.item!.id)} disabled={deleteMutation.isPending} className="flex-1 bg-red-500 text-white py-2 rounded-lg font-medium hover:bg-red-600">Eliminar</button>
            </div>
          </div>
        </div>
      )}
    </PageContainer>
  );
};
