import axios from 'axios';
import { useAuthStore } from '@/entities/auth/model/authStore';

const axiosInstance = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar el token desde el store de Zustand
axiosInstance.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor para manejar 401 y errores globales
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Si recibimos un 401, limpiamos el estado de auth
      useAuthStore.getState().clearAuth();
      // Opcionalmente redirigir a login
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;
