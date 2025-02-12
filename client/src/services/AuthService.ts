import api from './api';

export const ENDPOINTS = {
  REGISTER: '/auth/register',
  LOGIN: '/auth/login',
  LOGOUT: '/auth/logout',
};

export const register = (email: string, username: string, password: string) => {
  return api.post(ENDPOINTS.REGISTER, { email, username, password });
};

export const login = (email: string, password: string) => {
  return api.post(ENDPOINTS.LOGIN, { email, password });
};

export const logout = () => {
  return api.post(ENDPOINTS.LOGOUT);
};
