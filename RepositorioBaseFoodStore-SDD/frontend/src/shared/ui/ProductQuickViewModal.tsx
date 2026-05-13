import { useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { productsApi } from '@/shared/api/productsApi';
import { useCartStore } from '@/entities/cart/model/cartStore';

interface Props {
  productId: number | null;
  onClose: () => void;
}

export const ProductQuickViewModal = ({ productId, onClose }: Props) => {
  const { addItem } = useCartStore();

  const { data: product, isLoading } = useQuery({
    queryKey: ['product', productId],
    queryFn: () => productsApi.getById(productId!),
    enabled: productId !== null,
  });

  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose(); };
    document.addEventListener('keydown', handleKey);
    return () => document.removeEventListener('keydown', handleKey);
  }, [onClose]);

  useEffect(() => {
    if (productId !== null) document.body.style.overflow = 'hidden';
    return () => { document.body.style.overflow = ''; };
  }, [productId]);

  if (productId === null) return null;

  const ingredientesList = product?.ingredientes ?? [];
  const allergens = ingredientesList.filter((i) => i.es_alergeno);
  const ingredients = ingredientesList.filter((i) => !i.es_alergeno);

  const handleAddToCart = () => {
    if (!product) return;
    addItem({ id: product.id, name: product.name, price: Number(product.price), quantity: 1 });
    onClose();
  };

  return (
    <>
      <style>{`
        @keyframes qv-fade-in  { from { opacity: 0 } to { opacity: 1 } }
        @keyframes qv-slide-up { from { transform: translateY(100%); opacity: 0 } to { transform: translateY(0); opacity: 1 } }
        @keyframes qv-zoom-in  { from { transform: scale(0.95); opacity: 0 } to { transform: scale(1); opacity: 1 } }
        .qv-overlay  { animation: qv-fade-in 0.2s ease both; }
        .qv-panel    { animation: qv-slide-up 0.3s cubic-bezier(.22,1,.36,1) both; }
        @media (min-width: 640px) { .qv-panel { animation: qv-zoom-in 0.25s cubic-bezier(.22,1,.36,1) both; } }
      `}</style>

      <div
        className="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-0 sm:p-4"
        onClick={onClose}
        role="dialog"
        aria-modal="true"
        aria-label="Detalle del producto"
      >
        <div className="qv-overlay absolute inset-0 bg-black/60 backdrop-blur-sm" />

        <div
          className="qv-panel relative w-full sm:max-w-lg bg-white rounded-t-3xl sm:rounded-2xl shadow-2xl overflow-hidden"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Pill mobile */}
          <div className="flex justify-center pt-3 pb-1 sm:hidden">
            <div className="w-10 h-1 bg-gray-300 rounded-full" />
          </div>

          {/* Cerrar */}
          <button
            onClick={onClose}
            aria-label="Cerrar"
            className="absolute top-4 right-4 z-10 w-8 h-8 flex items-center justify-center bg-white/80 backdrop-blur-sm rounded-full text-gray-500 hover:text-gray-800 hover:bg-white shadow-sm transition-all duration-150"
          >
            ✕
          </button>

          {/* Hero */}
          <div className="bg-gradient-to-br from-orange-50 to-amber-100 h-52 flex items-center justify-center">
            <span className="text-8xl drop-shadow-md select-none">🍽️</span>
          </div>

          {/* Body */}
          <div className="px-6 py-5">
            {isLoading || !product ? (
              <div className="space-y-3 animate-pulse">
                <div className="h-6 bg-gray-200 rounded w-3/4" />
                <div className="h-8 bg-orange-100 rounded w-1/3" />
                <div className="h-4 bg-gray-100 rounded w-full" />
                <div className="h-4 bg-gray-100 rounded w-5/6" />
              </div>
            ) : (
              <>
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <h2 className="text-xl font-bold text-gray-900 leading-tight">{product.name}</h2>
                    <p className="text-2xl font-extrabold text-orange-500 mt-1">
                      ${Number(product.price).toLocaleString('es-AR', { minimumFractionDigits: 2 })}
                    </p>
                  </div>
                  <span className={`shrink-0 text-xs font-semibold px-2.5 py-1 rounded-full mt-1 ${product.stock > 0 ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-600'}`}>
                    {product.stock > 0 ? `✅ ${product.stock} en stock` : '❌ Sin stock'}
                  </span>
                </div>

                {product.description && (
                  <p className="text-gray-500 text-sm mt-3 leading-relaxed">{product.description}</p>
                )}

                {ingredients.length > 0 && (
                  <div className="mt-4">
                    <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Ingredientes</p>
                    <div className="flex flex-wrap gap-1.5">
                      {ingredients.map((ing) => (
                        <span key={ing.id} className="bg-gray-100 text-gray-600 text-xs px-2.5 py-1 rounded-full">
                          {ing.nombre}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {allergens.length > 0 && (
                  <div className="mt-3">
                    <p className="text-xs font-semibold text-amber-500 uppercase tracking-wider mb-2">⚠️ Alérgenos</p>
                    <div className="flex flex-wrap gap-1.5">
                      {allergens.map((a) => (
                        <span key={a.id} className="bg-red-50 text-red-600 text-xs px-2.5 py-1 rounded-full font-medium border border-red-100">
                          {a.nombre}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                <div className="flex gap-3 mt-6">
                  <button
                    onClick={handleAddToCart}
                    disabled={product.stock === 0}
                    className="flex-1 bg-orange-500 hover:bg-orange-600 active:scale-95 disabled:bg-gray-200 disabled:text-gray-400 text-white font-semibold py-3 rounded-xl transition-all duration-150 shadow-sm shadow-orange-200"
                  >
                    {product.stock === 0 ? 'Sin stock' : '🛒 Agregar al carrito'}
                  </button>
                  <Link
                    to={`/producto/${product.id}`}
                    onClick={onClose}
                    className="px-4 py-3 border border-gray-200 rounded-xl text-gray-600 hover:bg-gray-50 text-sm font-medium transition-colors duration-150 flex items-center gap-1 whitespace-nowrap"
                  >
                    Ver más →
                  </Link>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </>
  );
};
