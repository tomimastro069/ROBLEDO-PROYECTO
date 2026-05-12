import axiosInstance from './axios';

export interface Perfil {
  id: number;
  email: string;
  name: string | null;
  phone: string | null;
  is_active: boolean;
}

export const perfilApi = {
  get: async () => {
    const { data } = await axiosInstance.get<Perfil>('/perfil');
    return data;
  },

  update: async (payload: { name?: string; phone?: string }) => {
    const { data } = await axiosInstance.put<Perfil>('/perfil', payload);
    return data;
  },

  changePassword: async (payload: { password_actual: string; password_nueva: string }) => {
    await axiosInstance.put('/perfil/password', payload);
  },
};
