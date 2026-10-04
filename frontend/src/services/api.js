import axios from 'axios';

const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const searchCorpus = async (params) => {
  const response = await api.post('/search', {
    query: params.query,
    mode: params.mode || 'AND',
    ranking: params.ranking || 'tfidf',
    language: params.language || 'all',
    limit: params.limit || 10,
    page: params.page || 1,
    use_naive: params.use_naive || false,
  });
  return response.data;
};

export const getIndexStats = async () => {
  const response = await api.get('/stats');
  return response.data;
};

export const runBenchmark = async (params) => {
  const response = await api.post('/benchmark', {
    query: params.query || 'కంప్యూటర్',
    sample_sizes: params.sample_sizes || [500, 1000, 2500, 5000],
    runs_per_size: params.runs_per_size || 3,
  });
  return response.data;
};

export const getIndexStatus = async () => {
  const response = await api.get('/index/status');
  return response.data;
};

export const triggerRebuildIndex = async () => {
  const response = await api.post('/index/build');
  return response.data;
};

export default api;
