import api from './api';

export const ENDPOINTS = {
  REGISTER: '/auth/register',
  LOGIN: '/auth/login',
  REFRESH_TOKEN: '/auth/refresh/roll',
  LOGOUT: '/auth/refresh/logout',
};

export const register = (email: string, username: string, password: string) => {
  return api.post(ENDPOINTS.REGISTER, { email, username, password });
};

export const login = (email: string, password: string) => {
  return api.post(ENDPOINTS.LOGIN, { email, password });
};

export const refreshToken = () => {
  return api.post(ENDPOINTS.REFRESH_TOKEN, null, {
    withCredentials: true,
  });
};

export const logout = () => {
  return api.post(ENDPOINTS.LOGOUT);
};
