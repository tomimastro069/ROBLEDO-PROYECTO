import { useMutation } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { authApi, LoginPayload } from '../api/authApi';
import { useAuthStore } from '@/entities/auth/model/authStore';

export const useLogin = () => {
  const navigate = useNavigate();
  const { setAuth } = useAuthStore();

  return useMutation({
    mutationFn: (payload: LoginPayload) => authApi.login(payload),
    onSuccess: async (tokenData) => {
      // Guardamos el refresh_token en el store
      setAuth(
        { id: '', email: '', role: '' }, // placeholder, se sobreescribe con /me
        tokenData.access_token,
        tokenData.refresh_token,
      );

      // Obtenemos el perfil del usuario y actualizamos el store
      const me = await authApi.me();
      setAuth(me, tokenData.access_token, tokenData.refresh_token);

      navigate('/');
    },
  });
};
