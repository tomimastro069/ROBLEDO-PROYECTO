import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { HomePage } from '@pages/home/ui/HomePage';
import { LoginPage } from '@pages/login/ui/LoginPage';
import { NotFoundPage } from '@pages/not-found/ui/NotFoundPage';
import { UnauthorizedPage } from '@pages/unauthorized/ui/UnauthorizedPage';

import { MainLayout } from './layout/MainLayout';

const router = createBrowserRouter([
  {
    path: '/',
    element: <MainLayout />,
    children: [
      {
        index: true,
        element: <HomePage />,
      },
      {
        path: 'login',
        element: <LoginPage />,
      },
      {
        path: 'unauthorized',
        element: <UnauthorizedPage />,
      },
      {
        path: '*',
        element: <NotFoundPage />,
      },
    ],
  },
]);

export const AppRouter = () => {
  return <RouterProvider router={router} />;
};
