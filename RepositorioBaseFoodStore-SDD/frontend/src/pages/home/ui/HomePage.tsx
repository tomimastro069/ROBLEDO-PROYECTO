import { Link } from 'react-router-dom';
import { useAuthStore } from '@/entities/auth/model/authStore';

export const HomePage = () => {
  const { isAuthenticated } = useAuthStore();

  return (
    <div className="relative min-h-[90vh] flex flex-col justify-center items-center bg-white overflow-hidden">
      {/* Background Decorative Element */}
      <div className="absolute top-0 left-0 w-full h-full opacity-[0.03] pointer-events-none select-none flex flex-wrap gap-10 p-10">
        {Array.from({ length: 20 }).map((_, i) => (
          <span key={i} className="text-9xl font-black tracking-tighter uppercase">FOODSTORE</span>
        ))}
      </div>

      <div className="relative z-10 max-w-5xl mx-auto px-4 text-center">
        <h2 className="text-[10px] font-black uppercase tracking-[0.5em] text-gray-400 mb-6">Est. 2026 — Delivery de Alta Calidad</h2>
        <h1 className="text-6xl md:text-8xl font-bold text-[#1a1a1a] tracking-tighter mb-8 leading-[0.9]">
          SABOR REAL.<br />
          <span className="text-[#d32f2f]">COCINA PURA.</span>
        </h1>

        <p className="max-w-xl mx-auto text-sm md:text-base text-gray-500 font-medium leading-relaxed mb-12 uppercase tracking-wide">
          Seleccionamos los mejores ingredientes para llevar la experiencia del restaurante directamente a tu mesa. Sin vueltas, sin artificios.
        </p>

        <div className="flex flex-col sm:flex-row justify-center gap-6 items-center">
          <Link to="/catalogo" className="w-full sm:w-auto bg-[#d32f2f] hover:bg-[#b71c1c] text-white font-bold px-12 py-4 transition-all uppercase tracking-widest text-xs border-2 border-[#d32f2f]">
            Explorar Menú
          </Link>
          {!isAuthenticated && (
            <Link to="/register" className="w-full sm:w-auto border-2 border-gray-900 text-gray-900 hover:bg-gray-900 hover:text-white font-bold px-12 py-4 transition-all uppercase tracking-widest text-xs">
              Crear Cuenta
            </Link>
          )}
        </div>
      </div>

      {/* Side Label */}
      <div className="absolute right-8 bottom-20 hidden lg:block origin-bottom-right rotate-90">
        <span className="text-[10px] font-bold tracking-[0.8em] text-gray-300 uppercase whitespace-nowrap">
          CALIDAD CERTIFICADA / 100% ARTESANAL
        </span>
      </div>
    </div>
  );
};
