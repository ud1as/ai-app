import { apiClient } from '../client';
import Router from 'next/router';

export interface UserRegisterRequest {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
}

export interface UserResponse {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
}

export interface UserLoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface MessageResponse {
  message: string;
}

export const TOKEN_STORAGE_KEY = 'access_token';

export const saveToken = (token: string): void => {
  try {
    if (typeof window !== 'undefined') {
      localStorage.setItem(TOKEN_STORAGE_KEY, token);
    }
  } catch (err) {
    console.error('Failed to save token:', err);
  }
};

export const getToken = (): string | null => {
  try {
    if (typeof window !== 'undefined') {
      return localStorage.getItem(TOKEN_STORAGE_KEY);
    }
    return null;
  } catch (err) {
    console.error('Failed to get token:', err);
    return null;
  }
};

export const removeToken = (): void => {
  try {
    if (typeof window !== 'undefined') {
      localStorage.removeItem(TOKEN_STORAGE_KEY);
    }
  } catch (err) {
    console.error('Failed to remove token:', err);
  }
};

export const authApi = {
  register: async (data: UserRegisterRequest): Promise<UserResponse> => {
    try {
      const response = await apiClient.post<UserResponse>('/api/auth/register', data);
      return response;
    } catch (err) {
      throw err;
    }
  },

  login: async (data: UserLoginRequest): Promise<LoginResponse> => {
    try {
      const response = await apiClient.post<LoginResponse>('/api/auth/login', data);
      saveToken(response.access_token);
      await Router.push('/studio');
      return response;
    } catch (err) {
      throw err;
    }
  },

  logout: async (): Promise<void> => {
    try {
      removeToken();
      await Router.push('/login');
    } catch (err) {
      console.error('Logout error:', err);
    }
  },

  getCurrentUser: async (): Promise<UserResponse> => {
    try {
      return await apiClient.get<UserResponse>('/api/auth/me');
    } catch (err) {
      throw err;
    }
  }
};