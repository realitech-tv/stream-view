import axios from 'axios';
import type { AnalyzeRequest, AnalyzeResponse, ErrorResponse } from '../types/api';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 seconds for analysis
  headers: {
    'Content-Type': 'application/json',
  },
});

export const analyzeStream = async (url: string): Promise<AnalyzeResponse> => {
  try {
    const request: AnalyzeRequest = { url };
    const response = await apiClient.post<AnalyzeResponse>('/api/analyze', request);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      const errorData = error.response.data as ErrorResponse;
      throw new Error(errorData.detail || 'Failed to analyze stream');
    }
    throw new Error('Network error: Could not connect to the server');
  }
};

export const checkHealth = async (): Promise<boolean> => {
  try {
    const response = await apiClient.get('/api/health');
    return response.status === 200;
  } catch {
    return false;
  }
};
