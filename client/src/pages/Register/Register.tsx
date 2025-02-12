import { observer } from 'mobx-react';
import { useState } from 'react';
import authStore from '../../stores/authStore';

const Register = observer(() => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await authStore.register(email, username, password);
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="">Username</label>
          <input
            type="text"
            value={username}
            onChange={e => setUsername(e.target.value)}
            placeholder="Username"
          />
        </div>
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
          {authStore.status === 'loading' ? 'Loading...' : 'Register'}
        </button>
        {authStore.status === 'failed' && <p>Error: {authStore.error}</p>}
      </form>
    </div>
  );
});

export default Register;
