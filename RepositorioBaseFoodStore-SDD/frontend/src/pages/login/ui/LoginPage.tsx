import { useState } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { useAuthStore } from '@/entities/auth/model/authStore';
import { useLogin } from '@/features/auth/hooks/useLogin';

export const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { isAuthenticated } = useAuthStore();
  const { mutate: login, isPending, error } = useLogin();

  if (isAuthenticated) return <Navigate to="/" replace />;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    login({ email, password });
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center bg-gray-50 px-4">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-2xl shadow-md p-8 sm:p-10">
          <h1 className="text-2xl font-bold text-gray-800 mb-2 text-center">Iniciar sesión</h1>
          <p className="text-sm text-gray-400 text-center mb-8">Ingresá con tu cuenta de FoodStore</p>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="tu@email.com"
                required
                className="w-full border border-gray-300 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent transition"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">Contraseña</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                className="w-full border border-gray-300 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent transition"
              />
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 rounded-xl px-4 py-3">
                <p className="text-sm text-red-600">
                  {(error as { response?: { data?: { detail?: string } } })?.response?.data?.detail ?? 'Credenciales inválidas'}
                </p>
              </div>
            )}

            <button
              type="submit"
              disabled={isPending}
              className="w-full bg-orange-500 hover:bg-orange-600 text-white font-semibold py-2.5 rounded-xl transition disabled:opacity-50 text-sm"
            >
              {isPending ? 'Ingresando...' : 'Ingresar'}
            </button>
          </form>

          <p className="text-center text-sm text-gray-500 mt-6">
            ¿No tenés cuenta?{' '}
            <Link to="/register" className="text-orange-500 hover:underline font-medium">
              Registrarse
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};
