import { observer } from 'mobx-react';
import React, { useState } from 'react';
import authStore from '../../stores/authStore';
import { useNavigate } from 'react-router-dom';

const Auth = observer(() => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await authStore.login(email, password);
    navigate('/profile');
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="">Email</label>
          <input
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            placeholder="Email"
          />
        </div>
        <div>
          <label htmlFor="">Password</label>
          <input
            type="text"
            value={password}
            onChange={e => setPassword(e.target.value)}
            placeholder="Password"
          />
        </div>
        <button type="submit" disabled={authStore.status === 'loading'}>
          {authStore.status === 'loading' ? 'Loading...' : 'Login'}
        </button>
        {authStore.status === 'failed' && <p>Error: {authStore.error}</p>}
      </form>
    </div>
  );
});

export default Auth;
