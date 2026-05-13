import { Outlet, NavLink, Navigate, useNavigate } from 'react-router-dom';
import { useAuthStore } from '@/entities/auth/model/authStore';

export const AdminLayout = () => {
  const { isAuthenticated, user, clearAuth } = useAuthStore();
  const navigate = useNavigate();

  const role = user?.role ?? '';
  const isAdmin = role === 'admin' || role === 'gestor_pedidos' || role === 'gestor_stock';

  if (!isAuthenticated || !isAdmin) {
    return <Navigate to="/login" replace />;
  }

  const handleLogout = () => {
    clearAuth();
    navigate('/login');
  };

  const navLinkClass = ({ isActive }: { isActive: boolean }) =>
    `flex items-center gap-3 px-4 py-3 rounded-xl transition-all font-medium ${
      isActive
        ? 'bg-orange-500 text-white shadow-md shadow-orange-200'
        : 'text-gray-600 hover:bg-orange-50 hover:text-orange-600'
    }`;

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-gray-200 flex flex-col fixed inset-y-0 z-10 shadow-sm">
        <div className="p-6 border-b border-gray-100">
          <h1 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
            <span className="text-orange-500">⚙️</span> Panel
          </h1>
          <p className="text-xs text-gray-400 mt-1 uppercase tracking-wider font-semibold">{role.replace('_', ' ')}</p>
        </div>

        <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
          {(role === 'admin' || role === 'gestor_pedidos') && (
            <NavLink to="/admin/pedidos" className={navLinkClass}>
              <span>📦</span> Pedidos
            </NavLink>
          )}
          {(role === 'admin' || role === 'gestor_stock') && (
            <>
              <NavLink to="/admin/categorias" className={navLinkClass}>
                <span>🗂️</span> Categorías
              </NavLink>
              <NavLink to="/admin/ingredientes" className={navLinkClass}>
                <span>🥬</span> Ingredientes
              </NavLink>
              <NavLink to="/admin/productos" className={navLinkClass}>
                <span>🍔</span> Productos
              </NavLink>
            </>
          )}
        </nav>

        <div className="p-4 border-t border-gray-100">
          <button
            onClick={() => navigate('/')}
            className="flex items-center gap-3 px-4 py-3 w-full rounded-xl text-gray-600 hover:bg-gray-100 transition-all font-medium mb-2"
          >
            <span>🏠</span> Volver a la Tienda
          </button>
          <button
            onClick={handleLogout}
            className="flex items-center gap-3 px-4 py-3 w-full rounded-xl text-red-500 hover:bg-red-50 transition-all font-medium"
          >
            <span>🚪</span> Salir
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 ml-64 min-h-screen">
        <Outlet />
      </main>
    </div>
  );
};
