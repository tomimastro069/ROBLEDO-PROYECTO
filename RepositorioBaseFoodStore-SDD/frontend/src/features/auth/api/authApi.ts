import axiosInstance from '@/shared/api/axios';

// --- Types ---

export interface LoginPayload {
  email: string;
  password: string;
}

export interface RegisterPayload {
  email: string;
  password: string;
  name?: string;
  phone?: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: 'bearer';
}

export interface MeResponse {
  id: string;
  email: string;
  role: string;
  name?: string;
}

// --- API calls ---

export const authApi = {
  login: async (payload: LoginPayload): Promise<TokenResponse> => {
    // El backend usa OAuth2PasswordRequestForm, que requiere Form Data y el campo 'username'
    const formData = new URLSearchParams();
    formData.append('username', payload.email);
    formData.append('password', payload.password);

    const { data } = await axiosInstance.post<TokenResponse>('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return data;
  },

  register: async (payload: RegisterPayload): Promise<{ id: string; email: string }> => {
    const { data } = await axiosInstance.post('/auth/register', payload);
    return data;
  },

  refresh: async (refreshToken: string): Promise<TokenResponse> => {
    const { data } = await axiosInstance.post<TokenResponse>('/auth/refresh', {
      refresh_token: refreshToken,
    });
    return data;
  },

  me: async (): Promise<MeResponse> => {
    const { data } = await axiosInstance.get<MeResponse>('/auth/me');
    return data;
  },
};
