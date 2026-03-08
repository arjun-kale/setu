import { create } from "zustand";

interface AuthState {
  userId: string | null;
  email: string | null;
  token: string | null;
  isAuthenticated: boolean;
  setAuth: (userId: string, email: string, token: string) => void;
  clearAuth: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  userId: null,
  email: null,
  token: null,
  isAuthenticated: false,
  setAuth: (userId, email, token) =>
    set({ userId, email, token, isAuthenticated: true }),
  clearAuth: () =>
    set({ userId: null, email: null, token: null, isAuthenticated: false }),
}));
