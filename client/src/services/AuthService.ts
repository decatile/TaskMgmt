import api from './api';

export const ENDPOINTS = {
  REGISTER: '/auth/register',
  LOGIN: '/auth/login',
  LOGOUT: '/auth/logout',
};

export const register = (login: string, password: string) => {
  return api.post(ENDPOINTS.REGISTER, { login, password });
};

export const login = (login: string, password: string) => {
  return api.post(ENDPOINTS.LOGIN, { login, password });
};

export const logout = () => {
  return api.post(ENDPOINTS.LOGOUT);
};
