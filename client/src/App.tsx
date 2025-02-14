import { RouterProvider } from 'react-router-dom';
import './App.css';
import { router } from './router';
import { observer } from 'mobx-react';

const App = observer(() => {
  // if (authStore.status === 'loading') return <div>Загрузка...</div>;

  return <RouterProvider router={router} />;
});

export default App;
