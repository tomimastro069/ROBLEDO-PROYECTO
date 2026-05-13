import axiosInstance from './axios';

export interface Ingrediente {
  id: number;
  nombre: string;
  es_alergeno: boolean;
}

export const ingredientesApi = {
  list: async () => {
    const { data } = await axiosInstance.get<Ingrediente[]>('/ingredientes');
    return data;
  },

  getById: async (id: number) => {
    const { data } = await axiosInstance.get<Ingrediente>(`/ingredientes/${id}`);
    return data;
  },

  create: async (payload: { nombre: string; es_alergeno: boolean }) => {
    const { data } = await axiosInstance.post<Ingrediente>('/ingredientes', payload);
    return data;
  },

  update: async (id: number, payload: { nombre?: string; es_alergeno?: boolean }) => {
    const { data } = await axiosInstance.put<Ingrediente>(`/ingredientes/${id}`, payload);
    return data;
  },

  remove: async (id: number) => {
    await axiosInstance.delete(`/ingredientes/${id}`);
  },
};
