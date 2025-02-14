import { Navigate, RouterProvider } from 'react-router-dom';
import './App.css';
import { router } from './router';
import { useEffect } from 'react';
import authStore from './stores/authStore';
import { observer } from 'mobx-react';

const App = observer(() => {
  // if (authStore.status === 'loading') return <div>Загрузка...</div>;

  return <RouterProvider router={router} />;
});

export default App;
