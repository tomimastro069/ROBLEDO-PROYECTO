import { useState } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuthStore } from '@/entities/auth/model/authStore';
import { useLogin } from '@/features/auth/hooks/useLogin';

export const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { isAuthenticated } = useAuthStore();
  const { mutate: login, isPending, error } = useLogin();

  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    login({ email, password });
  };

  return (
    <div>
      <h1>Iniciar sesión</h1>
      <form onSubmit={handleSubmit}>
        <input
          id="login-email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
        />
        <input
          id="login-password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Contraseña"
          required
        />
        {error && (
          <p role="alert">
            {(error as { response?: { data?: { detail?: string } } })?.response?.data?.detail ??
              'Credenciales inválidas'}
          </p>
        )}
        <button id="login-submit" type="submit" disabled={isPending}>
          {isPending ? 'Ingresando...' : 'Ingresar'}
        </button>
      </form>
    </div>
  );
};
