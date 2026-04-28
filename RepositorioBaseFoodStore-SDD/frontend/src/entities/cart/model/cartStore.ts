import { create } from 'zustand';

interface CartItem {
  id: number;
  name: string;
  price: number;
  quantity: number;
  imageUrl?: string;
}

interface CartState {
  items: CartItem[];
  total: number;
  addItem: (item: CartItem) => void;
  removeItem: (itemId: number) => void;
  updateQuantity: (itemId: number, quantity: number) => void;
  clearCart: () => void;
}

export const useCartStore = create<CartState>((set) => ({
  items: [],
  total: 0,
  addItem: (item) =>
    set((state) => {
      const existingItem = state.items.find((i) => i.id === item.id);
      let newItems;
      if (existingItem) {
        newItems = state.items.map((i) =>
          i.id === item.id ? { ...i, quantity: i.quantity + item.quantity } : i
        );
      } else {
        newItems = [...state.items, item];
      }
      return {
        items: newItems,
        total: newItems.reduce((acc, i) => acc + i.price * i.quantity, 0),
      };
    }),
  removeItem: (itemId) =>
    set((state) => {
      const newItems = state.items.filter((i) => i.id !== itemId);
      return {
        items: newItems,
        total: newItems.reduce((acc, i) => acc + i.price * i.quantity, 0),
      };
    }),
  updateQuantity: (itemId, quantity) =>
    set((state) => {
      const newItems = state.items.map((i) =>
        i.id === itemId ? { ...i, quantity } : i
      );
      return {
        items: newItems,
        total: newItems.reduce((acc, i) => acc + i.price * i.quantity, 0),
      };
    }),
  clearCart: () => set({ items: [], total: 0 }),
}));
