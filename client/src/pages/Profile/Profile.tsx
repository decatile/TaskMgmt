import React, { useEffect, useState } from 'react';
import { getCurrentUser } from '../../services/UserService';
import authStore from '../../stores/authStore';

const Profile = () => {
  const [user, setUser] = useState({} as any);
  useEffect(() => {
    const getUser = async () => {
      console.log('token', authStore.accessToken);

      const response = await getCurrentUser();
      console.log('profile', response.data);
      setUser({ ...response.data });
    };
    getUser();
  }, []);
  return (
    <>
      <div>email: {user.email}</div>
      <div>username: {user.username}</div>
      <div>date: {user.registered_at}</div>
    </>
  );
};

export default Profile;
