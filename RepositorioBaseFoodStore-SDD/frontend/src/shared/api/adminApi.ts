import axiosInstance from './axios';

export interface AdminUser {
  id: number;
  email: string;
  name: string | null;
  phone: string | null;
  is_active: boolean;
  role_id: number | null;
}

export interface Role {
  id: number;
  name: string;
  description: string | null;
}

export interface MetricasResumen {
  total_usuarios: number;
  total_categorias: number;
  total_productos: number;
}

export const adminApi = {
  listUsers: async (params?: { skip?: number; limit?: number }) => {
    const { data } = await axiosInstance.get<AdminUser[]>('/admin/usuarios', { params });
    return data;
  },

  updateUser: async (id: number, payload: { name?: string; role_id?: number; is_active?: boolean }) => {
    const { data } = await axiosInstance.put<AdminUser>(`/admin/usuarios/${id}`, payload);
    return data;
  },

  createUser: async (payload: any) => {
    const { data } = await axiosInstance.post<AdminUser>('/admin/usuarios', payload);
    return data;
  },

  listRoles: async () => {
    const { data } = await axiosInstance.get<Role[]>('/admin/roles');
    return data;
  },

  toggleUserActive: async (id: number, is_active: boolean) => {
    const { data } = await axiosInstance.patch<AdminUser>(`/admin/usuarios/${id}/estado`, null, {
      params: { is_active },
    });
    return data;
  },

  getMetricasResumen: async () => {
    const { data } = await axiosInstance.get<MetricasResumen>('/admin/metricas/resumen');
    return data;
  },
};
