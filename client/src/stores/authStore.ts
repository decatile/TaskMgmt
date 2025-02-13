import { makeAutoObservable } from 'mobx';
import * as AuthService from '../services/AuthService';

class AuthStore {
  accessToken: string | null = '';
  status: 'idle' | 'loading' | 'success' | 'failed' = 'idle';
  error: string | null = null;

  constructor() {
    makeAutoObservable(this);
    this.refreshToken();
  }

  async register(email: string, username: string, password: string) {
    this.status = 'loading';
    this.error = null;

    try {
      const response = await AuthService.register(email, username, password);
      console.log('res', response);
      this.accessToken = response.data.access_token;
      this.status = 'success';
    } catch (err: any) {
      this.status = 'failed';
      this.error = err.message;
    }
  }

  async login(email: string, password: string) {
    this.status = 'loading';
    this.error = null;

    try {
      const response = await AuthService.login(email, password);
      this.accessToken = response.data.access_token;
      this.status = 'success';
    } catch (err: any) {
      this.status = 'failed';
      this.error = err.message;
    }
  }

  async refreshToken() {
    this.status = 'loading';
    this.error = null;
    try {
      const response = await AuthService.refreshToken();
      this.accessToken = response.data.access_token;
      this.status = 'success';
    } catch (err: any) {
      this.status = 'failed';
      this.error = err.message;
    }
  }

  async logout() {
    this.accessToken = null;
  }
}

const authStore = new AuthStore();
export default authStore;
