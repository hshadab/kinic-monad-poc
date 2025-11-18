import axios from 'axios';

// No baseURL needed - API is served from same domain
// Use relative URLs: /insert, /search, /chat, etc.
const api = axios.create({
  headers: {
    'Content-Type': 'application/json',
  },
});

console.log('API client configured (using same-origin relative URLs)');

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
    try {
      const { data } = await api.post('/insert', request);
      return data;
    } catch (error: any) {
      console.error('Insert API error:', error);
      console.error('Error response:', error.response?.data);
      console.error('Error status:', error.response?.status);
      throw new Error(error.response?.data?.detail || error.message || 'Insert failed');
    }
  },

  // Convenience method with simpler signature
  insertMemory: async (content: string, tags?: string): Promise<InsertResponse> => {
    try {
      const { data } = await api.post('/insert', { content, user_tags: tags });
      return data;
    } catch (error: any) {
      console.error('InsertMemory API error:', error);
      console.error('Error response:', error.response?.data);
      console.error('Error status:', error.response?.status);
      throw new Error(error.response?.data?.detail || error.message || 'Failed to insert memory');
    }
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

// Monad Blockchain Metadata Search
export interface MonadMemory {
  id: number;
  user: string;
  opType: number;  // 0=INSERT, 1=SEARCH
  title: string;
  summary: string;
  tags: string;
  contentHash: string;
  timestamp: number;
}

export interface MonadSearchRequest {
  tags?: string;
  title?: string;
  summary?: string;
  op_type?: number;
  limit?: number;
}

export interface MonadSearchResponse {
  results: MonadMemory[];
  num_results: number;
  source: string;
}

export interface MonadStatsResponse {
  synced: boolean;
  last_sync: string | null;
  total_memories: number;
  insert_operations: number;
  search_operations: number;
  unique_tags: number;
  unique_users: number;
  most_active_user: string | null;
}

export interface TrendingTag {
  tag: string;
  count: number;
}

export const monadAPI = {
  // Search Monad metadata
  search: async (request: MonadSearchRequest): Promise<MonadSearchResponse> => {
    const { data } = await api.post('/monad/search', request);
    return data;
  },

  // Get cache statistics
  getStats: async (): Promise<MonadStatsResponse> => {
    const { data } = await api.get('/monad/stats');
    return data;
  },

  // Get trending tags
  getTrending: async (limit: number = 10): Promise<TrendingTag[]> => {
    const { data } = await api.get(`/monad/trending?limit=${limit}`);
    return data;
  },

  // Refresh cache from blockchain
  refresh: async () => {
    const { data } = await api.post('/monad/refresh');
    return data;
  },

  // Convenience: Search by tags
  searchByTags: async (tags: string, limit: number = 20): Promise<MonadMemory[]> => {
    const response = await monadAPI.search({ tags, limit });
    return response.results;
  },

  // Convenience: Get recent memories
  getRecent: async (limit: number = 20): Promise<MonadMemory[]> => {
    const response = await monadAPI.search({ limit });
    return response.results;
  },
};

export default api;
