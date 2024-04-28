// axios.js
import axios from 'axios';
import store from './store';
import authService from '../utils/authService';

axios.interceptors.request.use(
  (config) => {
    const token = store.state.token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error),
);

axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response.status === 401) {
      await authService.refreshToken();
      return axios(error.config);
    }
    return Promise.reject(error);
  },
);

export default axios;