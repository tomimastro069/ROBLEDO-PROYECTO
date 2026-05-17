import React from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { PageContainer } from '@/shared/ui/PageContainer';
import { helpContent } from '@/shared/utils/helpContent';
import { useFormModal } from '@/shared/hooks/useFormModal';
import { useConfirmDialog } from '@/shared/hooks/useConfirmDialog';
import { usePagination } from '@/shared/hooks/usePagination';
import { productsApi, Product } from '@/shared/api/productsApi';
import { categoriesApi } from '@/shared/api/categoriesApi';
import { ingredientesApi } from '@/shared/api/ingredientesApi';
import { HelpButton } from '@/shared/ui/HelpButton';
import { handleError } from '@/shared/utils/logger';

export const ProductsAdminPage = () => {
  const queryClient = useQueryClient();
  const { data: productsData, isLoading } = useQuery({ queryKey: ['products-admin'], queryFn: () => productsApi.list({ limit: 100 }) });
  const { data: categories } = useQuery({ queryKey: ['categories'], queryFn: categoriesApi.list });
  const { data: ingredients } = useQuery({ queryKey: ['ingredients'], queryFn: ingredientesApi.list });

  const products = productsData?.items || [];
  const { paginatedItems, currentPage, totalPages, setCurrentPage } = usePagination(products, 10);

  const modal = useFormModal<{
    name: string;
    description: string;
    price: number;
    stock: number;
    category_id: number | null;
    ingredient_ids: number[];
  }, Product>({
    name: '', description: '', price: 0, stock: 0, category_id: null, ingredient_ids: []
  });
  const deleteDialog = useConfirmDialog<Product>();

  const [ingredienteSearch, setIngredienteSearch] = React.useState('');
  const searchInputRef = React.useRef<HTMLInputElement>(null);

  const sugerencias = React.useMemo(() => {
    if (!ingredienteSearch.trim()) return [];
    return (ingredients || []).filter(ing =>
      ing.nombre.toLowerCase().includes(ingredienteSearch.toLowerCase()) &&
      !modal.formData.ingredient_ids.includes(ing.id)
    );
  }, [ingredienteSearch, ingredients, modal.formData.ingredient_ids]);

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

  const handleOpenEdit = async (prod: Product) => {
    try {
      const detail = await productsApi.getById(prod.id);
      modal.openEdit(prod, {
        name: detail.name,
        description: detail.description || '',
        price: detail.price,
        stock: detail.stock,
        category_id: detail.category_id,
        ingredient_ids: detail.ingredientes ? detail.ingredientes.map(i => i.id) : []
      });
    } catch (err) {
      alert(handleError(err, 'Cargar Detalles de Producto'));
    }
  };

  return (
    <PageContainer
      title="Productos"
      description="Administrá tu catálogo, precios y disponibilidad."
      actions={
        <button onClick={() => modal.openCreate()} className="btn-premium py-2 px-6 text-sm">
          + Nuevo Producto
        </button>
      }
    >
      <div className="glass-card rounded-[2rem] border-white/60 overflow-hidden shadow-xl">
        {isLoading ? (
          <div className="p-12 text-center text-gray-400 animate-pulse font-medium">Cargando productos...</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-gray-50/50 border-b border-gray-100">
                  <th className="px-8 py-5 font-black text-[10px] text-gray-400 uppercase tracking-[0.2em]">Producto</th>
                  <th className="px-8 py-5 font-black text-[10px] text-gray-400 uppercase tracking-[0.2em]">Categoría</th>
                  <th className="px-8 py-5 font-black text-[10px] text-gray-400 uppercase tracking-[0.2em] text-right">Precio</th>
                  <th className="px-8 py-5 font-black text-[10px] text-gray-400 uppercase tracking-[0.2em] text-right">Stock</th>
                  <th className="px-8 py-5 font-black text-[10px] text-gray-400 uppercase tracking-[0.2em] text-right">Acciones</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {paginatedItems.map(prod => (
                  <tr key={prod.id} className="hover:bg-red-50/30 transition-colors group">
                    <td className="px-8 py-5">
                      <div className="font-bold text-gray-900">{prod.name}</div>
                      <div className="text-[10px] text-gray-400 truncate max-w-[200px]">{prod.description || 'Sin descripción'}</div>
                    </td>
                    <td className="px-8 py-5">
                      {prod.category_id ? (
                        <div className="flex flex-col">
                          <span className="text-[10px] font-black uppercase tracking-widest text-[#d32f2f]">
                            {categories?.find(c => c.id === prod.category_id)?.name}
                          </span>
                          {categories?.find(c => c.id === prod.category_id)?.parent_id && (
                            <span className="text-[8px] font-bold text-gray-400 uppercase tracking-tighter">
                              En: {categories.find(c => c.id === categories.find(sub => sub.id === prod.category_id)?.parent_id)?.name}
                            </span>
                          )}
                        </div>
                      ) : (
                        <span className="text-[10px] font-bold text-gray-300 uppercase tracking-widest">Sin categoría</span>
                      )}
                    </td>
                    <td className="px-8 py-5 text-right font-black text-gray-900">${Number(prod.price).toLocaleString('es-AR', { minimumFractionDigits: 2 })}</td>
                    <td className="px-8 py-5 text-right">
                      <span className={`inline-block px-3 py-1 rounded-xl text-[10px] font-black uppercase tracking-wider ${prod.stock > 0 ? 'bg-emerald-50 text-emerald-600 border border-emerald-100' : 'bg-rose-50 text-rose-600 border border-rose-100'}`}>
                        {prod.stock > 0 ? `${prod.stock} disp.` : 'Agotado'}
                      </span>
                    </td>
                    <td className="px-8 py-5 text-right">
                      <div className="flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button onClick={() => handleOpenEdit(prod)} className="bg-white border border-gray-200 text-gray-600 hover:text-red-600 hover:border-red-200 px-4 py-1.5 rounded-xl text-xs font-bold transition-all">
                          Editar
                        </button>
                        <button onClick={() => deleteDialog.open(prod)} className="bg-white border border-gray-200 text-rose-400 hover:text-rose-600 hover:border-rose-200 px-4 py-1.5 rounded-xl text-xs font-bold transition-all">
                          Borrar
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {totalPages > 1 && (
        <div className="flex items-center justify-center gap-4 mt-10">
          <button onClick={() => setCurrentPage(currentPage - 1)} disabled={currentPage === 1} className="w-10 h-10 flex items-center justify-center bg-white border border-gray-200 rounded-xl text-gray-500 hover:bg-gray-50 disabled:opacity-30 transition-all font-bold">
            &larr;
          </button>
          <div className="bg-white border border-gray-200 px-4 py-2 rounded-xl text-sm font-black text-gray-900 shadow-sm">
            {currentPage} <span className="text-gray-300 mx-1">/</span> {totalPages}
          </div>
          <button onClick={() => setCurrentPage(currentPage + 1)} disabled={currentPage === totalPages} className="w-10 h-10 flex items-center justify-center bg-white border border-gray-200 rounded-xl text-gray-500 hover:bg-gray-50 disabled:opacity-30 transition-all font-bold">
            &rarr;
          </button>
        </div>
      )}

      {/* Modal Form */}
      {modal.isOpen && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/40 backdrop-blur-sm p-4 animate-in fade-in duration-300">
          <div className="glass-card rounded-[2.5rem] w-full max-w-lg border-white/60 shadow-2xl animate-in zoom-in-95 duration-300 overflow-hidden">
            <div className="flex justify-between items-center p-8 border-b border-gray-100 bg-white/50">
              <h3 className="text-2xl font-bold text-gray-900">{modal.selectedItem ? 'Editar Producto' : 'Nuevo Producto'}</h3>
              <button onClick={modal.close} className="w-10 h-10 flex items-center justify-center rounded-full hover:bg-gray-100 text-gray-400 transition-colors">&times;</button>
            </div>
            <form onSubmit={handleSubmit} className="p-8 space-y-6 bg-white/30">
              <div className="space-y-2">
                <label className="block text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Nombre del Producto</label>
                <input required type="text" value={modal.formData.name} onChange={e => modal.setFormData(prev => ({ ...prev, name: e.target.value }))} className="input-premium" placeholder="Ej: Hamburguesa VIP" />
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="block text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Precio ($)</label>
                  <input required type="number" min="0" step="0.01" value={modal.formData.price} onChange={e => modal.setFormData(prev => ({ ...prev, price: parseFloat(e.target.value) || 0 }))} onFocus={e => e.target.select()} className="input-premium" />
                </div>
                <div className="space-y-2">
                  <label className="block text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Stock Inicial</label>
                  <input required type="number" min="0" value={modal.formData.stock} onChange={e => modal.setFormData(prev => ({ ...prev, stock: parseInt(e.target.value) || 0 }))} onFocus={e => e.target.select()} className="input-premium" />
                </div>
              </div>

              <div className="space-y-2">
                <label className="block text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Categoría</label>
                <select value={modal.formData.category_id || ''} onChange={e => modal.setFormData(prev => ({ ...prev, category_id: e.target.value ? parseInt(e.target.value) : null }))} className="input-premium appearance-none">
                  <option value="">Sin categoría</option>
                  {categories?.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
                </select>
              </div>

              <div className="space-y-2 relative">
                <label className="block text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Ingredientes</label>
                <input
                  ref={searchInputRef}
                  type="text"
                  value={ingredienteSearch}
                  onChange={e => setIngredienteSearch(e.target.value)}
                  className="input-premium"
                  placeholder="Buscar y agregar ingrediente... (ej: Cheddar)"
                />
                
                {/* Floating Suggestions List */}
                {sugerencias.length > 0 && (
                  <div className="absolute left-0 right-0 mt-1 bg-white/95 border border-gray-150 rounded-2xl z-[150] shadow-lg max-h-32 overflow-y-auto divide-y divide-gray-50/50 backdrop-blur-sm animate-in fade-in slide-in-from-top-2 duration-150">
                    {sugerencias.map(ing => (
                      <button
                        key={ing.id}
                        type="button"
                        onClick={() => {
                          modal.setFormData(prev => ({
                            ...prev,
                            ingredient_ids: [...prev.ingredient_ids, ing.id]
                          }));
                          setIngredienteSearch('');
                          setTimeout(() => searchInputRef.current?.focus(), 0);
                        }}
                        className="w-full text-left px-4 py-2 hover:bg-red-50/50 text-xs font-bold text-gray-700 transition-colors flex items-center justify-between"
                      >
                        <span className="truncate flex-1">{ing.nombre}</span>
                        <div className="flex items-center gap-2">
                          {ing.es_alergeno && (
                            <span className="text-[10px] text-amber-500 font-black uppercase tracking-tighter bg-amber-50 px-2 py-0.5 rounded border border-amber-100 flex items-center gap-1">
                              ⚠️ Alérgeno
                            </span>
                          )}
                          <span className="text-[9px] text-[#d32f2f] uppercase tracking-wider font-black">
                            + Agregar
                          </span>
                        </div>
                      </button>
                    ))}
                  </div>
                )}
              </div>

              {/* Selected Ingredients Badges */}
              <div className="space-y-2">
                <label className="block text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Ingredientes Seleccionados</label>
                <div className="flex flex-wrap gap-2 p-3.5 bg-gray-50/50 border border-gray-100 rounded-2xl max-h-24 overflow-y-auto shadow-inner">
                  {modal.formData.ingredient_ids.length > 0 ? (
                    modal.formData.ingredient_ids.map(id => {
                      const ing = ingredients?.find(i => i.id === id);
                      if (!ing) return null;
                      return (
                        <div
                          key={ing.id}
                          className="flex items-center gap-1.5 px-3 py-1 bg-red-50 text-red-700 hover:bg-red-100/50 border border-red-100 rounded-full text-xs font-black transition-all select-none shadow-sm"
                        >
                          <span className="truncate max-w-[120px]">{ing.nombre}</span>
                          {ing.es_alergeno && (
                            <span className="text-[9px] text-amber-500" title="Contiene alérgenos">⚠️</span>
                          )}
                          <button
                            type="button"
                            onClick={() => {
                              modal.setFormData(prev => ({
                                ...prev,
                                ingredient_ids: prev.ingredient_ids.filter(x => x !== id)
                              }));
                            }}
                            className="w-4 h-4 flex items-center justify-center rounded-full hover:bg-red-200 text-red-500 hover:text-red-700 text-[10px] transition-colors font-black"
                          >
                            &times;
                          </button>
                        </div>
                      );
                    })
                  ) : (
                    <div className="w-full text-center py-2 text-xs font-semibold text-gray-400 italic">
                      Ningún ingrediente seleccionado.
                    </div>
                  )}
                </div>
              </div>

              <div className="space-y-2">
                <label className="block text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Descripción</label>
                <textarea value={modal.formData.description} onChange={e => modal.setFormData(prev => ({ ...prev, description: e.target.value }))} className="input-premium h-24 resize-none" placeholder="Ingredientes, peso, etc..." />
              </div>

              <div className="pt-4 flex gap-4">
                <button type="submit" disabled={createMutation.isPending || updateMutation.isPending} className="flex-[2] btn-premium py-3">
                  {modal.selectedItem ? 'Guardar Cambios' : 'Crear Producto'}
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
            <h3 className="text-2xl font-bold text-gray-900 mb-2">¿Eliminar producto?</h3>
            <p className="text-gray-500 font-medium mb-8 leading-relaxed">Vas a borrar <span className="text-gray-900 font-bold">"{deleteDialog.item.name}"</span>. Esta acción no se puede deshacer.</p>
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
