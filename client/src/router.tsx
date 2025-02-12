import { createBrowserRouter } from 'react-router-dom';
import Auth from './pages/Auth/Auth';
import Register from './pages/Register/Register';

export const router = createBrowserRouter([
  {
    path: '/',
    children: [
      {
        path: '/',
        element: <h1>hello world</h1>,
      },
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
]);
