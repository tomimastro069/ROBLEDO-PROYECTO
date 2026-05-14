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
    `flex items-center gap-3 px-6 py-4 transition-all text-xs font-bold uppercase tracking-widest ${
      isActive
        ? 'bg-[#d32f2f] text-white'
        : 'text-gray-500 hover:bg-gray-50 hover:text-[#d32f2f]'
    }`;

  return (
    <div className="min-h-screen bg-gray-50 flex font-sans">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r-2 border-gray-100 flex flex-col fixed inset-y-0 z-10">
        <div className="p-8 border-b-2 border-gray-100">
          <div className="text-xl font-black text-[#d32f2f] tracking-tighter uppercase mb-1">
            PANEL <span className="font-light text-gray-400">CONTROL</span>
          </div>
          <p className="text-[10px] text-[#d32f2f] font-black uppercase tracking-[0.2em]">{role.replace('_', ' ')}</p>
        </div>

        <nav className="flex-1 py-6 space-y-1 overflow-y-auto">
          {role === 'admin' && (
            <NavLink to="/admin/usuarios" className={navLinkClass}>
              USUARIOS
            </NavLink>
          )}
          {(role === 'admin' || role === 'gestor_pedidos') && (
            <NavLink to="/admin/pedidos" className={navLinkClass}>
              PEDIDOS
            </NavLink>
          )}
          {(role === 'admin' || role === 'gestor_stock') && (
            <>
              <NavLink to="/admin/categorias" className={navLinkClass}>
                CATEGORÍAS
              </NavLink>
              <NavLink to="/admin/ingredientes" className={navLinkClass}>
                INGREDIENTES
              </NavLink>
              <NavLink to="/admin/productos" className={navLinkClass}>
                PRODUCTOS
              </NavLink>
            </>
          )}
        </nav>

        <div className="p-6 border-t-2 border-gray-100 space-y-2">
          <button
            onClick={() => navigate('/')}
            className="flex items-center justify-center w-full py-3 text-[10px] font-bold uppercase tracking-widest text-gray-400 hover:text-gray-900 transition-colors"
          >
            [ VOLVER A TIENDA ]
          </button>
          <button
            onClick={handleLogout}
            className="flex items-center justify-center w-full py-3 bg-gray-100 text-gray-600 hover:bg-red-600 hover:text-white text-[10px] font-bold uppercase tracking-widest transition-all"
          >
            CERRAR SESIÓN
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
