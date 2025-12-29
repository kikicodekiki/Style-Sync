import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear token and redirect to login
      localStorage.removeItem('token');
      localStorage.removeItem('userId');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth APIs
export const authAPI = {
  login: async (username, password) => {
    const response = await api.post('/api/login', { username, password });
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('userId', response.data.userId || response.data.user_id);
    }
    return response.data;
  },
  
  signup: async (username, password) => {
    const response = await api.post('/api/signup', { username, password });
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('userId', response.data.userId || response.data.user_id);
    }
    return response.data;
  },
};

// Wardrobe APIs
export const wardrobeAPI = {
  getWardrobe: async (userId) => {
    const response = await api.get(`/api/users/${userId}/wardrobe`);
    return response.data;
  },
  
  addItem: async (userId, formData) => {
    const response = await api.post(`/api/users/${userId}/wardrobe`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
  
  deleteItem: async (userId, itemId) => {
    const response = await api.delete(`/api/users/${userId}/wardrobe/${itemId}`);
    return response.data;
  },
};

// Weather API
export const weatherAPI = {
  getWeather: async () => {
    const response = await api.get('/api/weather');
    return response.data;
  },
};

// Outfit Generation API
export const outfitAPI = {
  generateOutfit: async (userId, occasion, weatherData) => {
    const response = await api.post(`/api/users/${userId}/outfit/generate`, {
      occasion,
      weather: weatherData,
    });
    return response.data;
  },
  
  getSavedOutfits: async (userId) => {
    const response = await api.get(`/api/users/${userId}/outfits/saved`);
    return response.data;
  },
  
  saveOutfit: async (userId, outfitId) => {
    const response = await api.post(`/api/users/${userId}/outfits/saved`, {
      outfit_id: outfitId,
    });
    return response.data;
  },
};

// Feedback API
export const feedbackAPI = {
  submitFeedback: async (userId, outfitId, feedback) => {
    const response = await api.post(`/api/users/${userId}/feedback`, {
      outfit_id: outfitId,
      feedback, // 'liked' or 'disliked'
    });
    return response.data;
  },
};

export default api;
