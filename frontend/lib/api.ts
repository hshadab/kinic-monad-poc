import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface ChatRequest {
  message: string;
  top_k?: number;
}

export interface ChatResponse {
  response: string;
  memories_used: Array<{
    text: string;
    score: number;
    tag: string;
  }>;
  num_memories: number;
  monad_tx: string;
}

export interface InsertRequest {
  content: string;
  user_tags?: string;
}

export interface InsertResponse {
  kinic_result: any;
  monad_tx: string;
  metadata: {
    title: string;
    summary: string;
    tags: string;
    content_hash: string;
  };
}

export interface SearchRequest {
  query: string;
  top_k?: number;
}

export interface SearchResponse {
  results: Array<{
    score: number;
    text: string;
    tag?: string;
  }>;
  monad_tx: string;
  num_results: number;
}

export interface StatsResponse {
  total_memories_on_chain: number;
  agent_memories: number;
  contract_address: string;
  agent_address: string;
}

// API Methods
export const chatAPI = {
  send: async (request: ChatRequest): Promise<ChatResponse> => {
    const { data } = await api.post('/chat', request);
    return data;
  },
};

export const memoryAPI = {
  insert: async (request: InsertRequest): Promise<InsertResponse> => {
    const { data } = await api.post('/insert', request);
    return data;
  },

  // Convenience method with simpler signature
  insertMemory: async (content: string, tags?: string): Promise<InsertResponse> => {
    const { data } = await api.post('/insert', { content, user_tags: tags });
    return data;
  },

  search: async (request: SearchRequest): Promise<SearchResponse> => {
    const { data} = await api.post('/search', request);
    return data;
  },

  // Convenience method with simpler signature
  searchMemories: async (query: string, top_k: number = 5) => {
    const { data } = await api.post('/search', { query, top_k });
    return data.results || [];
  },

  getStats: async (): Promise<StatsResponse> => {
    const { data } = await api.get('/stats');
    return data;
  },
};

export const healthAPI = {
  check: async () => {
    const { data } = await api.get('/health');
    return data;
  },
};

export default api;
