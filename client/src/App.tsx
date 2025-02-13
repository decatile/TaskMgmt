import { RouterProvider } from 'react-router-dom';
import './App.css';
import { router } from './router';
import { useEffect } from 'react';
import authStore from './stores/authStore';

function App() {
  // useEffect(() => {
  //   authStore.refreshToken();
  // }, []);
  return (
    <>
      <RouterProvider router={router} />
    </>
  );
}

export default App;
