import { makeAutoObservable } from 'mobx';
import * as AuthService from '../services/AuthService';

class AuthStore {
  status: 'idle' | 'loading' | 'success' | 'failed' = 'idle';
  error: string | null = null;

  constructor() {
    makeAutoObservable(this);
    // this.refreshToken();
  }

  async register(email: string, username: string, password: string) {
    this.setLoading();

    try {
      const response = await AuthService.register(email, username, password);
      this.setToken(response.data.access_token);
    } catch (err: unknown) {
      if (err instanceof Error) {
        this.setError(err.message);
      }
    }
  }

  async login(email: string, password: string) {
    this.setLoading();

    try {
      const response = await AuthService.login(email, password);
      this.setToken(response.data.access_token);
    } catch (err: unknown) {
      if (err instanceof Error) {
        console.log('Login error:', err);

        this.setError(err.message);
      }
    }
  }

  async refreshToken() {
    this.setLoading();

    try {
      const response = await AuthService.refreshToken();
      this.setToken(response.data.access_token);
      console.log('New access token:', localStorage.getItem('token'));
    } catch (err: unknown) {
      if (err instanceof Error) {
        this.setError(err.message);
      }
    }
  }

  async logout() {
    this.setToken(null);
    await AuthService.logout();
  }

  getToken() {
    return localStorage.getItem('token');
  }

  private setLoading() {
    this.error = null;
    this.status = 'loading';
  }

  private setToken(token: string | null) {
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
    }

    this.status = 'success';
  }

  private setError(error: string) {
    this.error = error;
    this.status = 'failed';
  }
}

const authStore = new AuthStore();
export default authStore;
