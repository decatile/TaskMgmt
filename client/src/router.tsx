import { createBrowserRouter, Outlet } from 'react-router-dom';
import Auth from './pages/Auth/Auth';
import Register from './pages/Register/Register';
import Profile from './pages/Profile/Profile';
import PublicRoute from './pages/PublicRoute/PublicRoute';
import PrivateRoute from './pages/PrivateRoute/PrivateRoute';

const Layout = () => {
  return (
    <>
      <header>header</header>
      <main>
        <Outlet />
      </main>
    </>
  );
};

export const router = createBrowserRouter([
  {
    path: '/',
    children: [
      {
        path: '/',
        element: <h1>hello world</h1>,
      },

      //Public Routes - сюда нельзя попасть если пользователь авторизован
      {
        element: <PublicRoute />,
        children: [
          {
            path: '/login',
            element: <Auth />,
          },
          {
            path: '/register',
            element: <Register />,
          },
        ],
      },

      //Private Routes - сюда нельзя попасть если пользователь не авторизован
      {
        element: <PrivateRoute />,
        children: [
          {
            path: '/profile',
            element: <Profile />,
          },
        ],
      },

      //Other Routes - все публичные пути
      //на которые можно попасть вне зависимости от того авторизован пользователь или нет
      {
        path: '/test',
        element: <h1>Test Text</h1>,
      },
      {
        path: '*',
        element: <h1>404 Page Not Found</h1>,
      },
    ],
  },
]);
