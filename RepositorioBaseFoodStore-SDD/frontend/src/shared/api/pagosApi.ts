import axiosInstance from './axios';

export interface PagoCreatePayload {
  pedido_id: number;
  forma_pago_codigo?: string;
}

export interface PagoResponse {
  pedido_id: number;
  preference_id: string | null;
  init_point: string | null;
  status: string;
}

export const pagosApi = {
  crear: async (payload: PagoCreatePayload): Promise<PagoResponse> => {
    const { data } = await axiosInstance.post('/pagos/crear', payload);
    return data;
  },
  consultar: async (pedido_id: number): Promise<PagoResponse> => {
    const { data } = await axiosInstance.get(`/pagos/pedido/${pedido_id}`);
    return data;
  },
};

