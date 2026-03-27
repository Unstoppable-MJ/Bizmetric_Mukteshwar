import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8004/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 5000, // 5s timeout
});

// Request Throttling (3-second debounce to be snappier for retries)
let lastRequestTime = 0;
const THROTTLE_MS = 3000;

api.interceptors.request.use((config) => {
  const now = Date.now();
  if (now - lastRequestTime < THROTTLE_MS) {
    const remaining = Math.ceil((THROTTLE_MS - (now - lastRequestTime)) / 1000);
    return Promise.reject({
      message: `Safety Pulse: Please wait ${remaining}s.`,
      isThrottled: true,
      remaining
    });
  }
  lastRequestTime = now;
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const { response } = error;

    if (response) {
      if (response.status === 429) {
        error.isRateLimit = true;
        error.message = "API Quota Limit Reached (429).";
      } else if (response.status >= 500) {
        error.isServerError = true;
        error.message = `Server Disturbance (${response.status}).`;
      }
    } else if (error.code === 'ECONNABORTED') {
      error.message = "Connection Timeout: Server not responding.";
    }

    return Promise.reject(error);
  }
);

export const getTrainStatus = async (trainNo) => {
  const response = await api.get(`/train/${trainNo}/`);
  return response.data;
};

export const getTrainPrediction = async (trainNo, model) => {
  const response = await api.get(`/predict/${trainNo}/`, {
    params: { model }
  });
  return response.data;
};

export default api;
