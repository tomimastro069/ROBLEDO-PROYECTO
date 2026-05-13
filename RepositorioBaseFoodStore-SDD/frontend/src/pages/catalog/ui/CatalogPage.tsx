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
          placeholder="Buscar producto..."
          value={search}
          onChange={(e) => { setSearch(e.target.value); setPage(0); }}
          className="border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400 sm:w-72"
        />
        <select
          value={categoryId ?? ''}
          onChange={(e) => { setCategoryId(e.target.value ? Number(e.target.value) : undefined); setPage(0); }}
          className="border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400 sm:w-56"
        >
          <option value="">Todas las categorías</option>
          {categories?.map((c) => (
            <option key={c.id} value={c.id}>{c.name}</option>
          ))}
        </select>
        {(search || categoryId) && (
          <button
            onClick={() => { setSearch(''); setCategoryId(undefined); setPage(0); }}
            className="text-sm text-orange-500 hover:underline self-center"
          >
            Limpiar filtros
          </button>
        )}
      </div>

      {isLoading ? (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
          {Array.from({ length: 12 }).map((_, i) => (
            <div key={i} className="bg-gray-100 rounded-xl h-64 animate-pulse" />
          ))}
        </div>
      ) : data?.items.length === 0 ? (
        <div className="text-center py-20">
          <p className="text-gray-400 text-lg">No se encontraron productos.</p>
          <button onClick={() => { setSearch(''); setCategoryId(undefined); }} className="mt-3 text-orange-500 hover:underline text-sm">
            Ver todos
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
          {data?.items.map((product) => (
            <div key={product.id}
              className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-lg hover:-translate-y-1 transition-all duration-200 flex flex-col group cursor-pointer"
              onClick={() => setSelectedProductId(product.id)}
            >
              <div className="bg-orange-50 h-36 flex items-center justify-center relative overflow-hidden">
                <span className="text-5xl transition-transform duration-300 group-hover:scale-110">🍽️</span>
                <div className="absolute inset-0 bg-orange-500/0 group-hover:bg-orange-500/5 transition-colors duration-200" />
              </div>
              <div className="p-3 flex flex-col flex-1">
                <p className="font-semibold text-gray-800 group-hover:text-orange-500 text-sm leading-tight line-clamp-2 mb-1 transition-colors">
                  {product.name}
                </p>
                <p className="text-orange-500 font-bold text-sm mt-auto">
                  ${Number(product.price).toFixed(2)}
                </p>
                <p className={`text-xs mt-0.5 ${product.stock > 0 ? 'text-gray-400' : 'text-red-400'}`}>
                  {product.stock > 0 ? `Stock: ${product.stock}` : 'Sin stock'}
                </p>
                <button
                  onClick={(e) => { e.stopPropagation(); handleAdd(product); }}
                  disabled={product.stock === 0}
                  className="mt-2 w-full bg-orange-500 hover:bg-orange-600 disabled:bg-gray-200 disabled:text-gray-400 text-white text-xs py-1.5 rounded-lg transition font-medium"
                >
                  {product.stock === 0 ? 'Sin stock' : '+ Agregar'}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {totalPages > 1 && (
        <div className="flex items-center justify-center gap-2 mt-10">
          <button onClick={() => setPage(p => Math.max(0, p - 1))} disabled={page === 0}
            className="px-4 py-2 border border-gray-200 rounded-lg text-sm disabled:opacity-40 hover:bg-gray-50 transition">
            ← Anterior
          </button>
          <span className="px-4 py-2 text-sm text-gray-600 bg-white border border-gray-200 rounded-lg">
            {page + 1} / {totalPages}
          </span>
          <button onClick={() => setPage(p => Math.min(totalPages - 1, p + 1))} disabled={page >= totalPages - 1}
            className="px-4 py-2 border border-gray-200 rounded-lg text-sm disabled:opacity-40 hover:bg-gray-50 transition">
            Siguiente →
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
