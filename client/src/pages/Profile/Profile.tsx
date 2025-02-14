import { useEffect, useState } from 'react';
import { getCurrentUser } from '../../services/UserService';
import authStore from '../../stores/authStore';
import { useNavigate } from 'react-router-dom';

const Profile = () => {
  const [user, setUser] = useState({} as any);
  const navigate = useNavigate();
  useEffect(() => {
    const getUser = async () => {
      console.log('token', authStore.getToken());

      const response = await getCurrentUser();
      console.log('profile', response.data);
      setUser({ ...response.data });
    };
    getUser();
  }, []);

  const handleLogout = async () => {
    await authStore.logout();
    navigate('/login');
  };

  return (
    <>
      <div>email: {user.email}</div>
      <div>username: {user.username}</div>
      <div>date: {user.registered_at}</div>
      <button onClick={handleLogout}>Exit</button>
    </>
  );
};

export default Profile;
