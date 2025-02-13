import { makeAutoObservable } from 'mobx';
import * as AuthService from '../services/AuthService';

class AuthStore {
  accessToken: string | null = '';
  status: 'idle' | 'loading' | 'success' | 'failed' = 'idle';
  error: string | null = null;

  constructor() {
    makeAutoObservable(this);
    // this.refreshToken();
  }

  async register(email: string, username: string, password: string) {
    this.setLoading()

    try {
      const response = await AuthService.register(email, username, password);
      this.setToken(response.data.access_token)
    } catch (err: any) {
      this.setError(err.message)
    }
  }

  async login(email: string, password: string) {
    this.status = 'loading';
    this.error = null;

    try {
      const response = await AuthService.login(email, password);
      this.setToken(response.data.access_token)
    } catch (err: any) {
      this.setError(err.message)
    }
  }

  async refreshToken() {
    this.status = 'loading';
    this.error = null;
    try {
      const response = await AuthService.refreshToken();
      this.setToken(response.data.access_token)
    } catch (err: any) {
      this.setError(err.message)
    }
  }

  async logout() {
    this.setToken(null)
  }

  private setLoading() {
    this.status = 'loading'
    this.error = null
  }

  private setToken(token: string | null) {
    this.accessToken = token
    this.status = 'success'
  }

  private setError(error: string) {
    this.error = error
    this.status = 'failed'
  }
}

const authStore = new AuthStore();
export default authStore;
