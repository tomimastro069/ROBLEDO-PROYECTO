import { create } from 'zustand';

interface Toast {
  id: string;
  message: string;
  type: 'success' | 'error' | 'info' | 'warning';
}

interface UIState {
  isLoading: boolean;
  isModalOpen: boolean;
  toasts: Toast[];
  setLoading: (loading: boolean) => void;
  toggleModal: (open?: boolean) => void;
  addToast: (message: string, type: Toast['type']) => void;
  removeToast: (id: string) => void;
}

export const useUIStore = create<UIState>((set) => ({
  isLoading: false,
  isModalOpen: false,
  toasts: [],
  setLoading: (loading) => set({ isLoading: loading }),
  toggleModal: (open) =>
    set((state) => ({ isModalOpen: open !== undefined ? open : !state.isModalOpen })),
  addToast: (message, type) =>
    set((state) => ({
      toasts: [...state.toasts, { id: Math.random().toString(36).substring(2, 9), message, type }],
    })),
  removeToast: (id) =>
    set((state) => ({
      toasts: state.toasts.filter((t) => t.id !== id),
    })),
}));
