import api from './api';
const USER_ENDPOINTS = {
  GET_CURRENT_USER: 'profile/me',
};

export const getCurrentUser = () => {
  return api.post(USER_ENDPOINTS.GET_CURRENT_USER);
};
