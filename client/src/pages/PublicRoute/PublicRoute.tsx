import { observer } from 'mobx-react';
import React, { useEffect } from 'react';
import authStore from '../../stores/authStore';
import { Navigate, Outlet } from 'react-router-dom';

const PublicRoute = observer(() => {
  console.log('PublicRoute: accessToken =', authStore.getToken());

  if (authStore.getToken()) {
    return <Navigate to="/profile" replace />;
  }

  return <Outlet />;
});

export default PublicRoute;
