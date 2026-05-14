import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { productsApi } from '@/shared/api/productsApi';
import { categoriesApi } from '@/shared/api/categoriesApi';
import { useCartStore } from '@/entities/cart/model/cartStore';
import { ProductQuickViewModal } from '@/shared/ui/ProductQuickViewModal';

export const CatalogPage = () => {
  const [search, setSearch] = useState('');
  const [categoryId, setCategoryId] = useState<number | undefined>();
  const [page, setPage] = useState(0);
  const [selectedProductId, setSelectedProductId] = useState<number | null>(null);
  const limit = 12;

  const { data: categories } = useQuery({ queryKey: ['categories'], queryFn: categoriesApi.list });

  const { data, isLoading } = useQuery({
    queryKey: ['products', { search, categoryId, page }],
    queryFn: () => productsApi.list({
      search: search || undefined,
      category_id: categoryId,
      skip: page * limit,
      limit,
    }),
  });

  const { addItem } = useCartStore();

  const handleAdd = (p: { id: number; name: string; price: number }) =>
    addItem({ id: p.id, name: p.name, price: p.price, quantity: 1 });

  const totalPages = data ? Math.ceil(data.total / limit) : 0;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-2xl sm:text-3xl font-bold text-gray-800 mb-6">Catálogo</h1>

      <div className="flex flex-col sm:flex-row gap-3 mb-8">
        <input
          type="text"
          placeholder="BUSCAR PRODUCTO..."
          value={search}
          onChange={(e) => { setSearch(e.target.value); setPage(0); }}
          className="border-2 border-gray-100 bg-white px-4 py-2 text-xs font-bold uppercase tracking-widest focus:outline-none focus:border-[#d32f2f] sm:w-72 transition-colors"
        />
        <select
          value={categoryId ?? ''}
          onChange={(e) => { setCategoryId(e.target.value ? Number(e.target.value) : undefined); setPage(0); }}
          className="border-2 border-gray-100 bg-white px-4 py-2 text-xs font-bold uppercase tracking-widest focus:outline-none focus:border-[#d32f2f] sm:w-56 transition-colors cursor-pointer"
        >
          <option value="">TODAS LAS CATEGORÍAS</option>
          {categories?.map((c) => (
            <option key={c.id} value={c.id}>{c.name.toUpperCase()}</option>
          ))}
        </select>
        {(search || categoryId) && (
          <button
            onClick={() => { setSearch(''); setCategoryId(undefined); setPage(0); }}
            className="text-[10px] font-bold text-[#d32f2f] uppercase tracking-widest hover:underline self-center"
          >
            LIMPIAR FILTROS
          </button>
        )}
      </div>

      {isLoading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {Array.from({ length: 8 }).map((_, i) => (
            <div key={i} className="bg-gray-100 h-80 animate-pulse" />
          ))}
        </div>
      ) : data?.items.length === 0 ? (
        <div className="text-center py-20 border-2 border-dashed border-gray-100">
          <p className="text-gray-400 text-sm font-bold uppercase tracking-widest">No se encontraron productos.</p>
          <button onClick={() => { setSearch(''); setCategoryId(undefined); }} className="mt-4 text-[#d32f2f] font-bold uppercase tracking-widest text-xs hover:underline">
            Ver todos
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
          {data?.items.map((product) => (
            <div key={product.id}
              className="bg-white border-b-2 border-transparent hover:border-[#d32f2f] shadow-sm hover:shadow-xl transition-all duration-300 flex flex-col group cursor-pointer"
              onClick={() => setSelectedProductId(product.id)}
            >
              <div className="bg-gray-50 h-52 flex items-center justify-center relative overflow-hidden">
                {/* Imagen del producto o fallback sobrio */}
                <div className="text-[10px] font-black text-gray-200 uppercase tracking-[0.5em] select-none">
                  FOOD STORE / PREMIUM
                </div>
                <div className="absolute inset-0 bg-[#d32f2f]/0 group-hover:bg-[#d32f2f]/5 transition-colors duration-300" />
              </div>
              <div className="p-6 flex flex-col flex-1">
                <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-2">
                  {categories?.find(c => c.id === product.category_id)?.name ?? 'General'}
                </p>
                <h3 className="font-bold text-[#1a1a1a] text-lg uppercase tracking-tight mb-2 group-hover:text-[#d32f2f] transition-colors">
                  {product.name}
                </h3>
                <div className="flex justify-between items-end mt-auto pt-4 border-t border-gray-50">
                  <div>
                    <p className="text-[#d32f2f] font-black text-xl">
                      ${Number(product.price).toFixed(2)}
                    </p>
                    <p className={`text-[10px] font-bold uppercase tracking-widest mt-1 ${product.stock > 0 ? 'text-gray-400' : 'text-red-500'}`}>
                      {product.stock > 0 ? `In Stock: ${product.stock}` : 'Agotado'}
                    </p>
                  </div>
                  <button
                    onClick={(e) => { e.stopPropagation(); handleAdd(product); }}
                    disabled={product.stock === 0}
                    className="bg-gray-900 hover:bg-[#d32f2f] disabled:bg-gray-100 disabled:text-gray-300 text-white p-3 transition-colors"
                    title="Añadir al carrito"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {totalPages > 1 && (
        <div className="flex items-center justify-center gap-4 mt-16">
          <button onClick={() => setPage(p => Math.max(0, p - 1))} disabled={page === 0}
            className="text-[10px] font-bold uppercase tracking-[0.3em] disabled:opacity-20 hover:text-[#d32f2f] transition-colors">
            PREV
          </button>
          <div className="h-4 w-px bg-gray-200" />
          <span className="text-[10px] font-bold text-gray-400">
            {page + 1} / {totalPages}
          </span>
          <div className="h-4 w-px bg-gray-200" />
          <button onClick={() => setPage(p => Math.min(totalPages - 1, p + 1))} disabled={page >= totalPages - 1}
            className="text-[10px] font-bold uppercase tracking-[0.3em] disabled:opacity-20 hover:text-[#d32f2f] transition-colors">
            NEXT
          </button>
        </div>
      )}

      <ProductQuickViewModal
        productId={selectedProductId}
        onClose={() => setSelectedProductId(null)}
      />
    </div>
  );
};
