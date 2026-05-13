import { createBrowserRouter, RouterProvider, Navigate } from 'react-router-dom';

import { MainLayout } from './layout/MainLayout';
import { ProtectedRoute } from '@/shared/ui/ProtectedRoute';

import { HomePage } from '@pages/home/ui/HomePage';
import { LoginPage } from '@pages/login/ui/LoginPage';
import { RegisterPage } from '@pages/register/ui/RegisterPage';
import { NotFoundPage } from '@pages/not-found/ui/NotFoundPage';
import { UnauthorizedPage } from '@pages/unauthorized/ui/UnauthorizedPage';

import { CatalogPage } from '@pages/catalog/ui/CatalogPage';
import { ProductDetailPage } from '@pages/product-detail/ui/ProductDetailPage';

import { DireccionesPage } from '@pages/direcciones/ui/DireccionesPage';
import { CheckoutPage } from '@pages/checkout/ui/CheckoutPage';

import { OrdersPage } from '@pages/orders/ui/OrdersPage';
import { OrderDetailPage } from '@pages/orders/ui/OrderDetailPage';

import { PagoExitoPage } from '@pages/pago/ui/PagoExitoPage';
import { PagoErrorPage } from '@pages/pago/ui/PagoErrorPage';
import { PagoPendientePage } from '@pages/pago/ui/PagoPendientePage';

import { PerfilPage } from '@pages/perfil/ui/PerfilPage';
import { GestorPedidosPage } from '@pages/gestor-pedidos/ui/GestorPedidosPage';
import { AdminLayout } from './layout/AdminLayout';
import { CategoriesAdminPage } from '@/pages/admin/categories/ui/CategoriesAdminPage';

const CLIENTE = ['cliente'];
const GESTOR_PEDIDOS = ['gestor_pedidos', 'admin'];
const AUTHENTICATED = ['cliente', 'admin', 'gestor_stock', 'gestor_pedidos'];

const router = createBrowserRouter([
  {
    path: '/',
    element: <MainLayout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'login', element: <LoginPage /> },
      { path: 'register', element: <RegisterPage /> },
      { path: 'unauthorized', element: <UnauthorizedPage /> },
      { path: '*', element: <NotFoundPage /> },

      // Catálogo — público
      { path: 'catalogo', element: <CatalogPage /> },
      { path: 'producto/:id', element: <ProductDetailPage /> },

      // Retorno de pago — público (MercadoPago redirige aquí)
      { path: 'pago/exito', element: <PagoExitoPage /> },
      { path: 'pago/error', element: <PagoErrorPage /> },
      { path: 'pago/pendiente', element: <PagoPendientePage /> },

      // Rutas de cliente autenticado
      {
        path: 'direcciones',
        element: <ProtectedRoute allowedRoles={AUTHENTICATED}><DireccionesPage /></ProtectedRoute>,
      },
      {
        path: 'checkout',
        element: <ProtectedRoute allowedRoles={CLIENTE}><CheckoutPage /></ProtectedRoute>,
      },
      {
        path: 'pedidos',
        element: <ProtectedRoute allowedRoles={CLIENTE}><OrdersPage /></ProtectedRoute>,
      },
      {
        path: 'pedidos/:id',
        element: <ProtectedRoute allowedRoles={AUTHENTICATED}><OrderDetailPage /></ProtectedRoute>,
      },
      {
        path: 'perfil',
        element: <ProtectedRoute allowedRoles={AUTHENTICATED}><PerfilPage /></ProtectedRoute>,
      },

      // Gestor de pedidos (público) - deprecated, movido a /admin
      {
        path: 'gestor-pedidos',
        element: <ProtectedRoute allowedRoles={GESTOR_PEDIDOS}><Navigate to="/admin/pedidos" replace /></ProtectedRoute>,
      },
    ],
  },
  {
    path: '/admin',
    element: <ProtectedRoute allowedRoles={['admin', 'gestor_pedidos', 'gestor_stock']}><AdminLayout /></ProtectedRoute>,
    children: [
      { index: true, element: <Navigate to="categorias" replace /> },
      { path: 'categorias', element: <CategoriesAdminPage /> },
      { path: 'pedidos', element: <GestorPedidosPage /> },
      { path: 'ingredientes', element: <div className="p-8"><h1>En construcción</h1></div> },
      { path: 'productos', element: <div className="p-8"><h1>En construcción</h1></div> },
    ],
  },
]);

export const AppRouter = () => <RouterProvider router={router} />;
