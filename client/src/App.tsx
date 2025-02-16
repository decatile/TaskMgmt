import { RouterProvider } from 'react-router-dom';
import './App.css';
import { router } from './router';
import { observer } from 'mobx-react';
import { MantineProvider } from '@mantine/core';
import '@mantine/core/styles.css';

const App = observer(() => {
  // if (authStore.status === 'loading') return <div>Загрузка...</div>;

  return (
    <MantineProvider>
      <RouterProvider router={router} />
    </MantineProvider>
  );
});

export default App;
