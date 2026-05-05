import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { App } from '../App';

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
  },
]);

export const AppRouter = () => {
  return <RouterProvider router={router} />;
};
