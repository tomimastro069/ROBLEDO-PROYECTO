import axiosInstance from './axios';

export type OrderStatus = 'PENDIENTE' | 'CONFIRMADO' | 'EN_PREPARACION' | 'EN_CAMINO' | 'ENTREGADO' | 'CANCELADO';

export interface OrderItem {
  product_id: number;
  quantity: number;
  price: number;
  exclusions?: number[];
}

export interface Order {
  id: number;
  user_id: number;
  status: OrderStatus;
  total: number;
  direccion_calle: string;
  direccion_numero: string;
  direccion_ciudad: string;
  created_at: string;
  updated_at: string;
  items: OrderItem[];
}

export interface CreateOrderPayload {
  items: { product_id: number; quantity: number; price: number; exclusions?: number[] }[];
  direccion_calle: string;
  direccion_numero: string;
  direccion_ciudad: string;
}

export const ordersApi = {
  list: async (params?: { skip?: number; limit?: number }) => {
    const { data } = await axiosInstance.get<Order[]>('/orders/', { params });
    return data;
  },

  getById: async (id: number) => {
    const { data } = await axiosInstance.get<Order>(`/orders/${id}`);
    return data;
  },

  create: async (payload: CreateOrderPayload) => {
    const { data } = await axiosInstance.post<Order>('/orders/', payload);
    return data;
  },

  cancel: async (id: number, reason?: string) => {
    const { data } = await axiosInstance.patch<Order>(`/orders/${id}/cancel`, { reason });
    return data;
  },

  listAll: async (params?: { skip?: number; limit?: number }) => {
    const { data } = await axiosInstance.get<Order[]>('/orders/admin/orders', { params });
    return data;
  },

  updateStatus: async (id: number, new_status: OrderStatus, reason?: string) => {
    const { data } = await axiosInstance.patch<Order>(`/orders/admin/orders/${id}/status`, {
      new_status,
      reason,
    });
    return data;
  },
};
