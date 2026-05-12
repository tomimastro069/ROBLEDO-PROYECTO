import axiosInstance from './axios';

export interface Address {
  id: number;
  street: string;
  numero: string | null;
  piso: string | null;
  city: string;
  state: string;
  zip_code: string;
  is_default: boolean;
}

export interface AddressPayload {
  street: string;
  numero?: string;
  piso?: string;
  city: string;
  state: string;
  zip_code: string;
}

export const direccionesApi = {
  list: async () => {
    const { data } = await axiosInstance.get<Address[]>('/direcciones');
    return data;
  },

  create: async (payload: AddressPayload) => {
    const { data } = await axiosInstance.post<Address>('/direcciones', payload);
    return data;
  },

  update: async (id: number, payload: Partial<AddressPayload>) => {
    const { data } = await axiosInstance.put<Address>(`/direcciones/${id}`, payload);
    return data;
  },

  remove: async (id: number) => {
    await axiosInstance.delete(`/direcciones/${id}`);
  },

  setDefault: async (id: number) => {
    const { data } = await axiosInstance.patch<Address>(`/direcciones/${id}/predeterminada`);
    return data;
  },
};
