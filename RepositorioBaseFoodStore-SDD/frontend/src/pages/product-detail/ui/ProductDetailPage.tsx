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

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-white">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-red-100 border-t-red-600 rounded-full animate-spin" />
          <p className="text-xs font-bold uppercase tracking-widest text-gray-400">Cargando delicias...</p>
        </div>
      </div>
    );
  }

  if (isError || !product) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-white p-8">
        <div className="text-center">
           <h1 className="text-6xl mb-4">😕</h1>
           <p className="text-xl font-bold text-gray-900 mb-6">Producto no encontrado</p>
           <button onClick={() => navigate('/catalogo')} className="btn-premium">Volver al catálogo</button>
        </div>
      </div>
    );
  }

  const ingredientesList = product.ingredientes ?? [];
  const allergens = ingredientesList.filter(i => i.es_alergeno);
  const ingredients = ingredientesList.filter(i => !i.es_alergeno);

  return (
    <div className="min-h-screen bg-gray-50/50">
      {/* Hero Header */}
      <div className="bg-gradient-to-br from-red-50 via-white to-red-100 border-b border-red-100 relative overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-full opacity-10 pointer-events-none">
           <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[60%] bg-red-400 rounded-full blur-[120px]" />
           <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[60%] bg-orange-200 rounded-full blur-[120px]" />
        </div>
        
        <div className="max-w-7xl mx-auto px-4 pt-8 pb-16 relative z-10">
          <button 
            onClick={() => navigate(-1)} 
            className="group flex items-center gap-2 text-[10px] font-black uppercase tracking-[0.3em] text-gray-400 hover:text-red-600 transition-colors mb-12"
          >
            <svg className="w-4 h-4 transform group-hover:-translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M15 19l-7-7 7-7" /></svg>
            Volver
          </button>

          <div className="flex flex-col md:flex-row items-center gap-12 md:gap-24">
            <div className="flex-1 flex justify-center">
              <div className="relative group">
                <div className="absolute inset-0 bg-red-600/10 blur-[80px] rounded-full transform group-hover:scale-125 transition-transform duration-700" />
                <span className="text-[12rem] relative z-10 drop-shadow-[0_25px_25px_rgba(0,0,0,0.15)] transform group-hover:rotate-6 transition-transform duration-500">
                  {product.category_id === 1 ? '🍔' : product.category_id === 2 ? '🍕' : '🍽️'}
                </span>
              </div>
            </div>

            <div className="flex-1 text-center md:text-left">
              <span className="inline-block text-[10px] font-black uppercase tracking-[0.4em] text-red-600 mb-6 bg-red-50 px-4 py-2 rounded-full">
                Sabor Premium
              </span>
              <h1 className="text-6xl md:text-7xl font-bold text-gray-900 tracking-tighter leading-[0.9] mb-6">
                {product.name}
              </h1>
              <div className="flex flex-col md:flex-row items-center md:items-baseline gap-4 md:gap-8">
                <p className="text-5xl font-black text-[#d32f2f]">
                  ${Number(product.price).toLocaleString('es-AR', { minimumFractionDigits: 2 })}
                </p>
                <span className={`text-[10px] font-black uppercase tracking-widest px-4 py-2 rounded-xl border ${product.stock > 0 ? 'text-emerald-600 bg-emerald-50 border-emerald-100' : 'text-red-600 bg-red-50 border-red-100'}`}>
                  {product.stock > 0 ? `Stock Disponible: ${product.stock}` : 'Sin Stock'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Content Section */}
      <div className="max-w-7xl mx-auto px-4 -mt-12 pb-24 relative z-20">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Info */}
          <div className="lg:col-span-2 space-y-8">
            <div className="glass-card p-10 rounded-[2.5rem]">
               <h3 className="text-xs font-black uppercase tracking-[0.3em] text-gray-400 mb-6">Sobre este producto</h3>
               <p className="text-xl text-gray-600 leading-relaxed font-medium">
                 {product.description || 'Una deliciosa opción preparada con los mejores ingredientes seleccionados para brindarte una experiencia única en cada bocado.'}
               </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {/* Ingredientes */}
              <div className="glass-card p-10 rounded-[2.5rem]">
                <h3 className="text-xs font-black uppercase tracking-[0.3em] text-gray-400 mb-8 flex items-center gap-2">
                  <svg className="w-4 h-4 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                  Ingredientes
                </h3>
                {ingredients.length > 0 ? (
                  <div className="flex flex-wrap gap-3">
                    {ingredients.map((ing) => (
                      <span key={ing.id} className="px-5 py-2 bg-white border border-gray-100 shadow-sm rounded-xl text-sm font-bold text-gray-700">
                        {ing.nombre}
                      </span>
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-gray-400 italic">No se especificaron ingredientes.</p>
                )}
              </div>

              {/* Alérgenos */}
              <div className={`p-10 rounded-[2.5rem] border ${allergens.length > 0 ? 'bg-red-50 border-red-100' : 'glass-card'}`}>
                <h3 className="text-xs font-black uppercase tracking-[0.3em] text-red-600 mb-8 flex items-center gap-2">
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" /></svg>
                  Alérgenos
                </h3>
                {allergens.length > 0 ? (
                  <div className="flex flex-wrap gap-3">
                    {allergens.map((a) => (
                      <span key={a.id} className="px-5 py-2 bg-white text-red-600 rounded-xl text-sm font-black shadow-sm border border-red-100">
                        {a.nombre}
                      </span>
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-gray-400 italic">Producto libre de alérgenos comunes.</p>
                )}
              </div>
            </div>
          </div>

          {/* Action Sidebar */}
          <div className="lg:col-span-1">
            <div className="glass-card p-8 rounded-[2.5rem] sticky top-24 border-red-100/50">
               <div className="mb-8">
                  <h4 className="text-[10px] font-black uppercase tracking-[0.3em] text-gray-400 mb-2 text-center">Resumen de orden</h4>
                  <div className="flex justify-between items-center py-4 border-b border-gray-100">
                    <span className="font-bold text-gray-900">{product.name}</span>
                    <span className="font-black text-red-600">${Number(product.price).toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between items-center py-4 border-b border-gray-100 text-sm">
                    <span className="text-gray-500 font-medium">Envío</span>
                    <span className="text-emerald-500 font-bold">¡Bonificado!</span>
                  </div>
               </div>

               <button
                 onClick={() => addItem({ id: product.id, name: product.name, price: Number(product.price), quantity: 1 })}
                 disabled={product.stock === 0}
                 className="w-full btn-premium py-5 text-lg"
               >
                 {product.stock === 0 ? 'Sin stock' : 'Agregar al carrito'}
               </button>

               <p className="mt-6 text-[10px] text-gray-400 text-center font-medium leading-relaxed">
                 * El tiempo de entrega estimado es de 30 a 45 minutos dependiendo de tu ubicación.
               </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
