import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { productsApi } from '@/shared/api/productsApi';
import { useCartStore } from '@/entities/cart/model/cartStore';

export const ProductDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { addItem } = useCartStore();

  const { data: product, isLoading, isError } = useQuery({
    queryKey: ['product', id],
    queryFn: () => productsApi.getById(Number(id)),
    enabled: !!id,
  });

  if (isLoading) return <div className="p-8 text-gray-500">Cargando...</div>;
  if (isError || !product) return <div className="p-8 text-red-500">Producto no encontrado.</div>;

  const allergens = product.allergens ?? [];
  const ingredients = product.ingredients ?? [];

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <button onClick={() => navigate(-1)} className="text-sm text-gray-500 hover:text-orange-500 mb-6 flex items-center gap-1">
        ← Volver al catálogo
      </button>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <div className="bg-gray-100 h-56 flex items-center justify-center">
          <span className="text-7xl">🍽️</span>
        </div>
        <div className="p-6">
          <h1 className="text-2xl font-bold text-gray-800">{product.name}</h1>
          <p className="text-3xl font-bold text-orange-500 mt-2">${Number(product.price).toFixed(2)}</p>

          {product.description && (
            <p className="text-gray-600 mt-3">{product.description}</p>
          )}

          <p className="text-sm text-gray-400 mt-2">
            {product.stock > 0 ? `✅ En stock (${product.stock} disponibles)` : '❌ Sin stock'}
          </p>

          {ingredients.length > 0 && (
            <div className="mt-5">
              <h2 className="font-semibold text-gray-700 mb-2">Ingredientes</h2>
              <div className="flex flex-wrap gap-2">
                {ingredients.map((ing) => (
                  <span key={ing.id} className="bg-gray-100 text-gray-600 text-xs px-3 py-1 rounded-full">
                    {ing.name}
                  </span>
                ))}
              </div>
            </div>
          )}

          {allergens.length > 0 && (
            <div className="mt-4">
              <h2 className="font-semibold text-gray-700 mb-2">⚠️ Alérgenos</h2>
              <div className="flex flex-wrap gap-2">
                {allergens.map((a) => (
                  <span key={a.id} className="bg-red-100 text-red-600 text-xs px-3 py-1 rounded-full font-medium">
                    {a.name}
                  </span>
                ))}
              </div>
            </div>
          )}

          <button
            onClick={() => addItem({ id: product.id, name: product.name, price: Number(product.price), quantity: 1 })}
            disabled={product.stock === 0}
            className="mt-6 w-full bg-orange-500 hover:bg-orange-600 text-white font-semibold py-3 rounded-lg transition disabled:opacity-40"
          >
            {product.stock === 0 ? 'Sin stock' : 'Agregar al carrito'}
          </button>
        </div>
      </div>
    </div>
  );
};
