import { makeAutoObservable } from 'mobx';
import * as AuthService from '../services/AuthService';

class AuthStore {
  user: any = null;
  status: 'idle' | 'loading' | 'succeeded' | 'failed' = 'idle';
  error: string | null = null;

  constructor() {
    makeAutoObservable(this);
  }

  async register(loginName: string, password: string) {
    this.status = 'loading';
    this.error = null;

    try {
      const response = await AuthService.register(loginName, password);
      this.user = response.data;
      this.status = 'succeeded';
    } catch (err: any) {
      this.status = 'failed';
      this.error = err.message;
    }
  }

  async login(loginName: string, password: string) {
    this.status = 'loading';
    this.error = null;

    try {
      const response = await AuthService.login(loginName, password);
      this.user = response.data;
      this.status = 'succeeded';
    } catch (err: any) {
      this.status = 'failed';
      this.error = err.message;
    }
  }

  async logout() {
    this.user = null;
  }
}

const authStore = new AuthStore();
export default authStore;
