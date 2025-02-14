import { observer } from 'mobx-react';
import authStore from '../../stores/authStore';
import { Navigate, Outlet } from 'react-router-dom';

const PrivateRoute = observer(() => {
  if (!authStore.getToken()) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
});

export default PrivateRoute;
