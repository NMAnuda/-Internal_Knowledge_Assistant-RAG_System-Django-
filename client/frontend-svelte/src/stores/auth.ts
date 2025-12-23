import { writable } from 'svelte/store';
import { goto } from '$app/navigation';  // SvelteKit routing


interface User {
  id: number;
  username: string;
  role: string;
}

const { subscribe, set, update } = writable<{ user: User | null; token: string | null }>({ user: null, token: null });

export const auth = {
  subscribe,
  login: async (username: string, password: string) => {
    try {
      const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/accounts/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      const data = await res.json();
      if (res.ok) {
        localStorage.setItem('token', data.access);
        localStorage.setItem('user', JSON.stringify(data.user));
        set({ user: data.user as User, token: data.access });
        goto('/chat');
      } else throw new Error(data.message || 'Login failed');
    } catch (error) {
      console.error(error);
    }
  },
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    set({ user: null, token: null });
    goto('/login');
  },
  init: () => {
    const token = localStorage.getItem('token');
    const userStr = localStorage.getItem('user');
    if (token && userStr) {
      set({ user: JSON.parse(userStr) as User, token });  
    }
  }
};

// Init on load
auth.init();