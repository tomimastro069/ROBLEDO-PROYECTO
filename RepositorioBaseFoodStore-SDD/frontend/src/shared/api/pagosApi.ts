import api from './axios';

export interface PagoCreatePayload {
  pedido_id: number;
}

export interface PagoResponse {
  pedido_id: number;
  preference_id: string | null;
  init_point: string | null;
  status: string;
}

export const pagosApi = {
  crear: async (payload: PagoCreatePayload): Promise<PagoResponse> => {
    const { data } = await api.post('/pagos/crear', payload);
    return data;
  },
  consultar: async (pedido_id: number): Promise<PagoResponse> => {
    const { data } = await api.get(`/pagos/pedido/${pedido_id}`);
    return data;
  },
};
