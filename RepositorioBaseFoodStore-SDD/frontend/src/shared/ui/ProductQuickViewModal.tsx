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
        @keyframes qv-backdrop { from { opacity: 0; backdrop-filter: blur(0px); } to { opacity: 1; backdrop-filter: blur(8px); } }
        @keyframes qv-content { from { transform: scale(0.95) translateY(20px); opacity: 0; } to { transform: scale(1) translateY(0); opacity: 1; } }
        .qv-overlay { animation: qv-backdrop 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        .qv-content { animation: qv-content 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
      `}</style>

      <div
        className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6"
        onClick={onClose}
        role="dialog"
        aria-modal="true"
      >
        <div className="qv-overlay absolute inset-0 bg-black/40" />

        <div
          className="qv-content relative w-full max-w-4xl glass-card rounded-[3rem] border-white/40 shadow-[0_32px_64px_-15px_rgba(0,0,0,0.2)] overflow-hidden flex flex-col md:flex-row max-h-[90vh]"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Botón cerrar premium */}
          <button
            onClick={onClose}
            className="absolute top-6 right-6 z-20 w-10 h-10 flex items-center justify-center rounded-full bg-white/20 hover:bg-white/40 text-white md:text-gray-900 border border-white/30 transition-all duration-300"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M6 18L18 6M6 6l12 12" /></svg>
          </button>

          {/* Imagen / Hero side */}
          <div className="md:w-1/2 bg-gradient-to-br from-orange-100 via-rose-50 to-orange-200 relative p-12 flex items-center justify-center">
            <div className="absolute top-12 left-12">
               <span className="text-[10px] font-black tracking-[0.4em] text-orange-500/50 uppercase">FoodStore / Premium</span>
            </div>
            <span className="text-9xl drop-shadow-2xl transform hover:scale-110 transition-transform duration-500 cursor-default">
               {product?.category_id === 1 ? '🍔' : product?.category_id === 2 ? '🍕' : '🍽️'}
            </span>
          </div>

          {/* Info side */}
          <div className="md:w-1/2 p-8 md:p-12 overflow-y-auto bg-white/80">
            {isLoading || !product ? (
              <div className="space-y-6 animate-pulse">
                <div className="h-4 bg-gray-100 rounded-full w-24" />
                <div className="h-10 bg-gray-200 rounded-2xl w-3/4" />
                <div className="h-6 bg-orange-100 rounded-full w-1/3" />
                <div className="space-y-3 pt-4">
                   <div className="h-4 bg-gray-100 rounded-full w-full" />
                   <div className="h-4 bg-gray-100 rounded-full w-5/6" />
                </div>
              </div>
            ) : (
              <div className="flex flex-col h-full">
                <div className="mb-8">
                  <span className="inline-block text-[10px] font-bold text-orange-600 uppercase tracking-widest bg-orange-50 px-3 py-1 rounded-lg mb-4">
                    Detalle del Producto
                  </span>
                  <h2 className="text-4xl font-bold text-gray-900 tracking-tight leading-none mb-3">
                    {product.name}
                  </h2>
                  <div className="flex items-baseline gap-4">
                    <p className="text-3xl font-bold text-orange-600">
                      ${Number(product.price).toLocaleString('es-AR', { minimumFractionDigits: 2 })}
                    </p>
                    <span className={`text-[10px] font-black uppercase tracking-widest px-2 py-1 rounded-md ${product.stock > 0 ? 'text-emerald-500 bg-emerald-50' : 'text-rose-500 bg-rose-50'}`}>
                      {product.stock > 0 ? `Stock: ${product.stock}` : 'Agotado'}
                    </span>
                  </div>
                </div>

                <div className="space-y-8 flex-1">
                  {product.description && (
                    <div>
                      <h4 className="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] mb-3">Descripción</h4>
                      <p className="text-gray-600 leading-relaxed font-medium">
                        {product.description}
                      </p>
                    </div>
                  )}

                  {ingredients.length > 0 && (
                    <div>
                      <h4 className="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] mb-4">Ingredientes</h4>
                      <div className="flex flex-wrap gap-2">
                        {ingredients.map((ing) => (
                          <span key={ing.id} className="px-4 py-1.5 bg-gray-100/50 border border-gray-100 text-gray-600 rounded-xl text-sm font-semibold">
                            {ing.nombre}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {allergens.length > 0 && (
                    <div className="p-4 bg-rose-50/50 border border-rose-100 rounded-[1.5rem]">
                      <h4 className="text-[10px] font-black text-rose-500 uppercase tracking-[0.2em] mb-3 flex items-center gap-2">
                        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" /></svg>
                        Alérgenos
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        {allergens.map((a) => (
                          <span key={a.id} className="px-3 py-1 bg-white text-rose-600 rounded-lg text-xs font-bold border border-rose-100 shadow-sm">
                            {a.nombre}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                <div className="flex gap-4 pt-12 mt-auto">
                  <button
                    onClick={handleAddToCart}
                    disabled={product.stock === 0}
                    className="flex-[2] btn-premium py-4"
                  >
                    {product.stock === 0 ? 'Sin stock' : 'Agregar al carrito'}
                  </button>
                  <Link
                    to={`/producto/${product.id}`}
                    onClick={onClose}
                    className="flex-1 flex items-center justify-center bg-white border-2 border-gray-100 text-gray-900 font-bold rounded-[1.5rem] hover:bg-gray-50 transition-all active:scale-95 text-sm"
                  >
                    Detalles
                  </Link>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
};
