import { useState } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { useAuthStore } from '@/entities/auth/model/authStore';
import { useRegister } from '@/features/auth/hooks/useRegister';

export const RegisterPage = () => {
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { isAuthenticated } = useAuthStore();
  const { mutate: register, isPending, error } = useRegister();

  if (isAuthenticated) return <Navigate to="/" replace />;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    register({ name, email, password, phone: phone || undefined });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#fafafa] relative overflow-hidden px-4 py-12">
      {/* Decorative blobs */}
      <div className="absolute -top-24 -right-24 w-96 h-96 bg-orange-100 rounded-full blur-3xl opacity-50" />
      <div className="absolute -bottom-24 -left-24 w-96 h-96 bg-rose-100 rounded-full blur-3xl opacity-50" />
      
      <div className="w-full max-w-md relative">
        <div className="glass-card rounded-[2.5rem] p-8 sm:p-12 border-white/60 shadow-2xl">
          <div className="mb-10 text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 premium-gradient rounded-2xl shadow-lg shadow-orange-200 mb-6 transform rotate-6">
              <span className="text-3xl text-white font-bold">FS</span>
            </div>
            <h1 className="text-3xl font-bold text-gray-900 tracking-tight mb-2">Crear Cuenta</h1>
            <p className="text-gray-500 font-medium">Unite a la comunidad FoodStore</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div className="grid grid-cols-1 gap-5">
              <div className="space-y-2">
                <label className="block text-sm font-semibold text-gray-700 ml-1">Nombre</label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Tu nombre completo"
                  required
                  className="input-premium"
                />
              </div>
              <div className="space-y-2">
                <label className="block text-sm font-semibold text-gray-700 ml-1">Email</label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="hola@ejemplo.com"
                  required
                  className="input-premium"
                />
              </div>
              <div className="space-y-2">
                <label className="block text-sm font-semibold text-gray-700 ml-1">Teléfono (Opcional)</label>
                <input
                  type="tel"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  placeholder="Ej: 11 1234 5678"
                  className="input-premium"
                />
              </div>
              <div className="space-y-2">
                <label className="block text-sm font-semibold text-gray-700 ml-1">Contraseña</label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Mínimo 8 caracteres"
                  required
                  minLength={8}
                  className="input-premium"
                />
              </div>
            </div>

            {error && (
              <div className="bg-rose-50 border border-rose-100 rounded-2xl px-4 py-3 animate-in fade-in slide-in-from-top-2 duration-300">
                <p className="text-sm text-rose-600 font-medium text-center">
                  {(error as { response?: { data?: { detail?: string } } })?.response?.data?.detail ?? 'Error al registrarse'}
                </p>
              </div>
            )}

            <button
              type="submit"
              disabled={isPending}
              className="btn-premium w-full text-base tracking-wide mt-4"
            >
              {isPending ? (
                <span className="flex items-center justify-center gap-2">
                  <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Creando cuenta...
                </span>
              ) : 'Registrarse'}
            </button>
          </form>

          <div className="mt-10 text-center">
            <p className="text-gray-500 text-sm font-medium">
              ¿Ya tenés cuenta?{' '}
              <Link to="/login" className="text-orange-600 hover:text-orange-700 font-bold transition-colors">
                Iniciá sesión
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
