import { create } from 'zustand';

interface PaymentState {
  preferenceId: string | null;
  paymentStatus: 'pending' | 'success' | 'failure' | 'rejected' | null;
  setPreference: (id: string) => void;
  setStatus: (status: 'pending' | 'success' | 'failure' | 'rejected' | null) => void;
  reset: () => void;
}

export const usePaymentStore = create<PaymentState>((set) => ({
  preferenceId: null,
  paymentStatus: null,
  setPreference: (id) => set({ preferenceId: id }),
  setStatus: (status) => set({ paymentStatus: status }),
  reset: () => set({ preferenceId: null, paymentStatus: null }),
}));
