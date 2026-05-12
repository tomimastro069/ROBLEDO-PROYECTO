import axiosInstance from './axios';

export interface Category {
  id: number;
  name: string;
  description: string | null;
  parent_id: number | null;
}

export const categoriesApi = {
  list: async () => {
    const { data } = await axiosInstance.get<Category[]>('/categories');
    return data;
  },

  getById: async (id: number) => {
    const { data } = await axiosInstance.get<Category>(`/categories/${id}`);
    return data;
  },

  create: async (payload: { name: string; description?: string; parent_id?: number }) => {
    const { data } = await axiosInstance.post<Category>('/categories', payload);
    return data;
  },

  update: async (id: number, payload: { name?: string; description?: string; parent_id?: number }) => {
    const { data } = await axiosInstance.put<Category>(`/categories/${id}`, payload);
    return data;
  },

  remove: async (id: number) => {
    await axiosInstance.delete(`/categories/${id}`);
  },
};
