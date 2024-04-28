// authService.js
import axios from 'axios';

import { URL_DATOS } from './constantes';

const authService = {
  login: async (EMAIL, CONTRASENIA) => {
    const response = await axios.post(`${URL_DATOS}api/login`, { EMAIL, CONTRASENIA });
    const { token, refreshToken } = response.data;
    localStorage.setItem('token', token);
    localStorage.setItem('refreshToken', refreshToken);
    return token;
  },
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
  },
  refreshToken: async () => {
    const refreshToken = localStorage.getItem('refreshToken');
    const response = await axios.post(`${BASE_URL}/refreshToken`, { refreshToken });
    const { token } = response.data;
    localStorage.setItem('token', token);
    return token;
  },
};

export default authService;