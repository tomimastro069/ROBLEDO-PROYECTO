import { useMutation } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { authApi, RegisterPayload } from '../api/authApi';

export const useRegister = () => {
  const navigate = useNavigate();

  return useMutation({
    mutationFn: (payload: RegisterPayload) => authApi.register(payload),
    onSuccess: () => {
      // Tras registrarse, redirigimos al login para que el usuario inicie sesión
      navigate('/login');
    },
  });
};
