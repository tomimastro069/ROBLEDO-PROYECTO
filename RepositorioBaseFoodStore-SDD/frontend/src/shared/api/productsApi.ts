import axiosInstance from './axios';

export interface Product {
  id: number;
  name: string;
  description: string | null;
  price: number;
  stock: number;
  category_id: number | null;
  ingredient_ids?: number[];
}

export interface Ingrediente {
  id: number;
  nombre: string;
  es_alergeno: boolean;
}

export interface ProductDetail extends Product {
  ingredientes: Ingrediente[];
}

export interface PaginatedProducts {
  items: Product[];
  total: number;
  limit: number;
  offset: number;
}

export const productsApi = {
  list: async (params?: { skip?: number; limit?: number; category_id?: number; search?: string }) => {
    const { data } = await axiosInstance.get<PaginatedProducts>('/products', { params });
    return data;
  },

  getById: async (id: number) => {
    const { data } = await axiosInstance.get<ProductDetail>(`/products/${id}`);
    return data;
  },

  create: async (payload: Omit<Product, 'id'>) => {
    const { data } = await axiosInstance.post<Product>('/products', payload);
    return data;
  },

  update: async (id: number, payload: Partial<Omit<Product, 'id'>>) => {
    const { data } = await axiosInstance.put<Product>(`/products/${id}`, payload);
    return data;
  },

  remove: async (id: number) => {
    await axiosInstance.delete(`/products/${id}`);
  },
};
