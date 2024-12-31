import { apiClient } from '../client';

// Data Models
export interface FileChunk {
  content: string;
  chunk_index: number;
  chunk_total: number;
}

export interface FilePreviewResponse {
  chunks: FileChunk[];
  total_chunks: number;
}

export interface FileProcessResponse {
  success: boolean;
  dataset_id?: string;
  error?: string;
}

export interface FileProcessRequest {
  tenant_id: string;
}

export interface Dataset {
  id: string;
  tenant_id: string;
  created_by?: string;
  name?: string;
}

export interface DatasetRequest {
  name: string;
  created_by?: string;
}

export interface MessageResponse {
  message: string;
}

// Constants
export const DEFAULT_TENANT_ID = '00000000-0000-0000-0000-000000000001';

// Validation utilities
export const validateFile = (file: File) => {
  const MAX_SIZE = 10 * 1024 * 1024; // 10MB
  const ALLOWED_TYPES = [
    'text/plain',
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
  ];

  if (!file) {
    throw new Error('No file selected');
  }

  if (file.size > MAX_SIZE) {
    throw new Error('File size exceeds 10MB limit');
  }

  if (!ALLOWED_TYPES.includes(file.type)) {
    throw new Error('Unsupported file type');
  }
};

export const knowledgeApi = {
  // Datasets
  getDatasets: () => 
    apiClient.get<Dataset[]>('/api/knowledge/datasets'),

  getDataset: (id: string) => 
    apiClient.get<Dataset>(`/api/knowledge/datasets/${id}`),

  createDataset: (data: DatasetRequest) =>
    apiClient.post<Dataset>('/api/knowledge/datasets', data),

  deleteDataset: (id: string) => 
    apiClient.delete<MessageResponse>(`/api/knowledge/datasets/${id}`),

  // File Operations
  previewFile: async (file: File) => {
    validateFile(file);
    const formData = new FormData();
    formData.append('file', file);
    return apiClient.postForm<FilePreviewResponse>('/api/knowledge/preview', formData);
  },

  processFile: async (file: File, tenant_id: string = DEFAULT_TENANT_ID) => {
    validateFile(file);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('tenant_id', tenant_id);
    return apiClient.postForm<FileProcessResponse>('/api/knowledge/process', formData);
  }
};