import { Link } from 'react-router-dom';
import { useAuthStore } from '@/entities/auth/model/authStore';

export const HomePage = () => {
  const { isAuthenticated } = useAuthStore();

  return (
    <div className="max-w-4xl mx-auto px-4 py-20 text-center">
      <h1 className="text-4xl font-bold text-gray-800 mb-4">Bienvenido a <span className="text-orange-500">FoodStore</span></h1>
      <p className="text-lg text-gray-500 mb-10">Los mejores productos de comida, directo a tu puerta.</p>
      <div className="flex justify-center gap-4 flex-wrap">
        <Link to="/catalogo" className="bg-orange-500 hover:bg-orange-600 text-white font-semibold px-8 py-3 rounded-xl transition text-lg">
          Ver catálogo
        </Link>
        {!isAuthenticated && (
          <Link to="/register" className="border border-orange-500 text-orange-500 hover:bg-orange-50 font-semibold px-8 py-3 rounded-xl transition text-lg">
            Crear cuenta
          </Link>
        )}
      </div>
    </div>
  );
};
