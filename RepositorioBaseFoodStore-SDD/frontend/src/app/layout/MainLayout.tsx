import { useState } from 'react';
import { Outlet, Link, NavLink, useNavigate } from 'react-router-dom';
import { useAuthStore } from '@/entities/auth/model/authStore';
import { CartButton } from '@/widgets/cart/ui/CartButton';
import CartDrawer from '@/widgets/cart/ui/CartDrawer';

export const MainLayout = () => {
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { isAuthenticated, user, clearAuth } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => { clearAuth(); navigate('/login'); };

  const role = user?.role ?? '';
  const isCliente = !role || role === 'cliente';
  const isGestorPedidos = role === 'gestor_pedidos' || role === 'admin';
  const isGestorStock = role === 'gestor_stock' || role === 'admin';
  const isAuth = isAuthenticated;

  const navLinkClass = ({ isActive }: { isActive: boolean }) =>
    `text-sm font-medium transition-colors ${isActive ? 'text-orange-500' : 'text-gray-600 hover:text-orange-500'}`;

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-40 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <Link to="/" className="text-xl font-bold text-orange-500 shrink-0">
              🍔 FoodStore
            </Link>

            {/* Desktop nav */}
            <nav className="hidden md:flex items-center gap-6">
              <NavLink to="/catalogo" className={navLinkClass}>Catálogo</NavLink>
              {isAuth && (isCliente || role === 'admin') && (
                <>
                  <NavLink to="/pedidos" className={navLinkClass}>Mis pedidos</NavLink>
                  <NavLink to="/direcciones" className={navLinkClass}>Direcciones</NavLink>
                </>
              )}
              {isAuth && isGestorPedidos && (
                <NavLink to="/gestor-pedidos" className={navLinkClass}>Panel pedidos</NavLink>
              )}
              {isAuth && isGestorStock && (
                <NavLink to="/catalogo" className={navLinkClass}>Gestión catálogo</NavLink>
              )}
            </nav>

            {/* Desktop actions */}
            <div className="hidden md:flex items-center gap-3">
              {isAuth ? (
                <>
                  <CartButton onClick={() => setIsCartOpen(true)} />
                  <NavLink to="/perfil" className={navLinkClass}>
                    {user?.name ?? user?.email ?? 'Mi perfil'}
                  </NavLink>
                  <button onClick={handleLogout}
                    className="text-sm text-gray-400 hover:text-red-500 transition">
                    Salir
                  </button>
                </>
              ) : (
                <>
                  <Link to="/login" className="text-sm text-gray-600 hover:text-orange-500 transition font-medium">
                    Ingresar
                  </Link>
                  <Link to="/register"
                    className="bg-orange-500 hover:bg-orange-600 text-white text-sm px-4 py-2 rounded-lg font-medium transition">
                    Registrarse
                  </Link>
                </>
              )}
            </div>

            {/* Mobile: cart + hamburger */}
            <div className="flex md:hidden items-center gap-2">
              {isAuth && <CartButton onClick={() => setIsCartOpen(true)} />}
              <button
                onClick={() => setMobileMenuOpen(o => !o)}
                className="p-2 rounded-lg text-gray-600 hover:bg-gray-100 transition"
                aria-label="Menú"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  {mobileMenuOpen
                    ? <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    : <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />}
                </svg>
              </button>
            </div>
          </div>
        </div>

        {/* Mobile menu */}
        {mobileMenuOpen && (
          <div className="md:hidden border-t border-gray-100 bg-white px-4 py-3 space-y-2">
            <NavLink to="/catalogo" className={navLinkClass} onClick={() => setMobileMenuOpen(false)}>Catálogo</NavLink>
            {isAuth && (isCliente || role === 'admin') && (
              <>
                <NavLink to="/pedidos" className={({ isActive }) => `block py-1 ${navLinkClass({ isActive })}`} onClick={() => setMobileMenuOpen(false)}>Mis pedidos</NavLink>
                <NavLink to="/direcciones" className={({ isActive }) => `block py-1 ${navLinkClass({ isActive })}`} onClick={() => setMobileMenuOpen(false)}>Direcciones</NavLink>
              </>
            )}
            {isAuth && isGestorPedidos && (
              <NavLink to="/gestor-pedidos" className={({ isActive }) => `block py-1 ${navLinkClass({ isActive })}`} onClick={() => setMobileMenuOpen(false)}>Panel pedidos</NavLink>
            )}
            {isAuth && (
              <NavLink to="/perfil" className={({ isActive }) => `block py-1 ${navLinkClass({ isActive })}`} onClick={() => setMobileMenuOpen(false)}>Mi perfil</NavLink>
            )}
            {isAuth ? (
              <button onClick={handleLogout} className="block w-full text-left text-sm text-red-500 py-1">Cerrar sesión</button>
            ) : (
              <div className="flex gap-3 pt-1">
                <Link to="/login" className="text-sm text-gray-600 font-medium" onClick={() => setMobileMenuOpen(false)}>Ingresar</Link>
                <Link to="/register" className="text-sm text-orange-500 font-medium" onClick={() => setMobileMenuOpen(false)}>Registrarse</Link>
              </div>
            )}
          </div>
        )}
      </header>

      <main className="flex-1">
        <Outlet />
      </main>

      <footer className="bg-white border-t border-gray-200 py-4 text-center text-xs text-gray-400 mt-auto">
        © 2026 FoodStore
      </footer>

      <CartDrawer open={isCartOpen} onClose={() => setIsCartOpen(false)} />
    </div>
  );
};
