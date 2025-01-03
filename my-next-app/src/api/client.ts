import { getToken, removeToken } from './endpoints/auth';
import Router from 'next/router';

export const API_BASE_URL = 'http://localhost:8000';

export class APIError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'APIError';
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    if (response.status === 401) {
      removeToken();
      await Router.push('/login');
      throw new APIError(response.status, 'Session expired. Please login again.');
    }
    const error = await response.json().catch(() => ({ message: 'An error occurred' }));
    throw new APIError(response.status, error.message);
  }
  return response.json();
}

export const apiClient = {
  async get<T>(endpoint: string): Promise<T> {
    const token = getToken();
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      credentials: 'include',
      headers: {
        Authorization: token ? `Bearer ${token}` : '',
      },
    });
    return handleResponse<T>(response);
  },

  async post<T>(endpoint: string, data?: unknown): Promise<T> {
    const token = getToken();
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        Authorization: token ? `Bearer ${token}` : '',
      },
      body: data ? JSON.stringify(data) : undefined,
    });
    return handleResponse<T>(response);
  },

  async postForm<T>(endpoint: string, formData: FormData): Promise<T> {
    const token = getToken();
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        Authorization: token ? `Bearer ${token}` : '',
      },
      body: formData,
    });
    return handleResponse<T>(response);
  },

  async put<T>(endpoint: string, data: unknown): Promise<T> {
    const token = getToken();
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'PUT',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        Authorization: token ? `Bearer ${token}` : '',
      },
      body: JSON.stringify(data),
    });
    return handleResponse<T>(response);
  },

  async delete<T>(endpoint: string): Promise<T> {
    const token = getToken();
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'DELETE',
      credentials: 'include',
      headers: {
        Authorization: token ? `Bearer ${token}` : '',
      },
    });
    return handleResponse<T>(response);
  },
};