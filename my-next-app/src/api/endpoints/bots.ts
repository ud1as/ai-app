import { apiClient } from '../client';

export interface Bot {
  id: string;
  name: string;
  description: string;
  type?: 'Чат-Бот' | 'АГЕНТ' | 'РАБОЧИЙ ПРОЦЕСС';
}

export interface BotCreateRequest {
  name: string;
  description: string;
}

export interface BotConfigureRequest {
  prompt_template: string;
  dataset_id: string;
}

export interface ChatRequest {
  query: string;
  conversation_id: string;
  dataset_id?: string;
}

export interface ChatResponse {
  answer: string;
  relevant_context: string;
}

export interface MessageResponse {
  message: string;
}

export const botApi = {
  getAll: () => 
    apiClient.get<Bot[]>('/api/bots'),

  getById: (id: string) => 
    apiClient.get<Bot>(`/api/bots/${id}`),

  create: (data: BotCreateRequest) => 
    apiClient.post<MessageResponse>('/api/bots', data),

  configure: (id: string, data: BotConfigureRequest) =>
    apiClient.post<MessageResponse>(`/api/bots/${id}/configure`, data),

  chat: (id: string, data: ChatRequest) =>
    apiClient.post<ChatResponse>(`/api/bots/${id}/chat`, data),
};