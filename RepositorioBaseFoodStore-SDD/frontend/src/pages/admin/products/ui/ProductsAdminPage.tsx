import React from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { PageContainer } from '@/shared/ui/PageContainer';
import { helpContent } from '@/shared/utils/helpContent';
import { useFormModal } from '@/shared/hooks/useFormModal';
import { useConfirmDialog } from '@/shared/hooks/useConfirmDialog';
import { usePagination } from '@/shared/hooks/usePagination';
import { productsApi, Product } from '@/shared/api/productsApi';
import { categoriesApi } from '@/shared/api/categoriesApi';
import { HelpButton } from '@/shared/ui/HelpButton';
import { handleError } from '@/shared/utils/logger';

export const ProductsAdminPage = () => {
  const queryClient = useQueryClient();
  const { data: productsData, isLoading } = useQuery({ queryKey: ['products-admin'], queryFn: () => productsApi.list({ limit: 100 }) });
  const { data: categories } = useQuery({ queryKey: ['categories'], queryFn: categoriesApi.list });

  const products = productsData?.items || [];
  const { paginatedItems, currentPage, totalPages, setCurrentPage } = usePagination(products, 10);

  const modal = useFormModal<{ name: string; description: string; price: number; stock: number; category_id: number | null }, Product>({
    name: '', description: '', price: 0, stock: 0, category_id: null
  });
  const deleteDialog = useConfirmDialog<Product>();

  const createMutation = useMutation({
    mutationFn: productsApi.create,
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['products-admin'] }); modal.close(); },
    onError: (err) => alert(handleError(err, 'Create Product'))
  });

  const updateMutation = useMutation({
    mutationFn: (args: { id: number; payload: any }) => productsApi.update(args.id, args.payload),
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['products-admin'] }); modal.close(); },
    onError: (err) => alert(handleError(err, 'Update Product'))
  });

  const deleteMutation = useMutation({
    mutationFn: productsApi.remove,
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['products-admin'] }); deleteDialog.close(); },
    onError: (err) => alert(handleError(err, 'Delete Product'))
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
      title="Gestión de Productos"
      description="Administra el catálogo, precios y stock."
      helpContent={helpContent.products}
      actions={
        <button onClick={() => modal.openCreate()} className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-lg font-medium transition shadow-md shadow-orange-200">
          + Nuevo Producto
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
                <th className="px-6 py-4 font-semibold text-gray-600 text-sm">Categoría</th>
                <th className="px-6 py-4 font-semibold text-gray-600 text-sm text-right">Precio</th>
                <th className="px-6 py-4 font-semibold text-gray-600 text-sm text-right">Stock</th>
                <th className="px-6 py-4 font-semibold text-gray-600 text-sm text-right">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {paginatedItems.map(prod => (
                <tr key={prod.id} className="hover:bg-gray-50 transition">
                  <td className="px-6 py-4 font-medium text-gray-800">{prod.name}</td>
                  <td className="px-6 py-4 text-gray-500">{categories?.find(c => c.id === prod.category_id)?.name || '-'}</td>
                  <td className="px-6 py-4 text-gray-800 font-medium text-right">${Number(prod.price).toFixed(2)}</td>
                  <td className="px-6 py-4 text-right">
                    <span className={`px-2 py-1 rounded-md text-xs font-bold ${prod.stock > 0 ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                      {prod.stock}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button onClick={() => modal.openEdit(prod, { name: prod.name, description: prod.description || '', price: prod.price, stock: prod.stock, category_id: prod.category_id })} className="text-orange-500 hover:bg-orange-50 p-2 rounded-lg transition mr-2">Editar</button>
                    <button onClick={() => deleteDialog.open(prod)} className="text-red-500 hover:bg-red-50 p-2 rounded-lg transition">Borrar</button>
                  </td>
                </tr>
              ))}
              {paginatedItems.length === 0 && (
                <tr><td colSpan={5} className="px-6 py-8 text-center text-gray-400">No hay productos.</td></tr>
              )}
            </tbody>
          </table>
        )}
      </div>

      {totalPages > 1 && (
        <div className="flex items-center justify-center gap-2 mt-6">
          <button onClick={() => setCurrentPage(currentPage - 1)} disabled={currentPage === 1} className="px-4 py-2 border border-gray-200 rounded-lg text-sm disabled:opacity-40">Anterior</button>
          <span className="text-sm text-gray-600">{currentPage} / {totalPages}</span>
          <button onClick={() => setCurrentPage(currentPage + 1)} disabled={currentPage === totalPages} className="px-4 py-2 border border-gray-200 rounded-lg text-sm disabled:opacity-40">Siguiente</button>
        </div>
      )}

      {/* Modal Form */}
      {modal.isOpen && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/50 p-4">
          <div className="bg-white rounded-xl shadow-xl w-full max-w-md animate-in fade-in zoom-in-95 duration-200">
            <div className="flex justify-between items-center p-6 border-b border-gray-100">
              <h3 className="text-xl font-bold">{modal.selectedItem ? 'Editar Producto' : 'Nuevo Producto'}</h3>
              <button type="button" onClick={modal.close} className="text-gray-400 hover:text-gray-600 text-2xl leading-none">&times;</button>
            </div>
            <form onSubmit={handleSubmit} className="p-6 space-y-4">
              <div className="flex items-center gap-2 mb-2 bg-blue-50 text-blue-800 p-3 rounded-lg text-sm">
                <HelpButton size="sm" content={<p>Define el producto, su precio y stock. Si el stock llega a 0, no se podrá comprar.</p>} />
                <span>Datos del producto.</span>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Nombre</label>
                <input required type="text" value={modal.formData.name} onChange={e => modal.setFormData(prev => ({ ...prev, name: e.target.value }))} className="w-full border border-gray-300 rounded-lg px-3 py-2" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Precio ($)</label>
                  <input required type="number" min="0" step="0.01" value={modal.formData.price} onChange={e => modal.setFormData(prev => ({ ...prev, price: parseFloat(e.target.value) || 0 }))} className="w-full border border-gray-300 rounded-lg px-3 py-2" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Stock</label>
                  <input required type="number" min="0" value={modal.formData.stock} onChange={e => modal.setFormData(prev => ({ ...prev, stock: parseInt(e.target.value) || 0 }))} className="w-full border border-gray-300 rounded-lg px-3 py-2" />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Categoría</label>
                <select value={modal.formData.category_id || ''} onChange={e => modal.setFormData(prev => ({ ...prev, category_id: e.target.value ? parseInt(e.target.value) : null }))} className="w-full border border-gray-300 rounded-lg px-3 py-2">
                  <option value="">Sin categoría</option>
                  {categories?.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
                </select>
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
            <h3 className="text-xl font-bold mb-2">¿Eliminar producto?</h3>
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
