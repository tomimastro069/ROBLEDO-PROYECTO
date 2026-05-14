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
            {/* Logo */}
            <Link to="/" className="text-xl font-bold text-[#d32f2f] tracking-tighter uppercase flex items-center gap-2">
              <span className="border-2 border-[#d32f2f] px-1">FOOD</span> 
              <span className="font-light">STORE</span>
            </Link>

            {/* Desktop nav */}
            <nav className="hidden md:flex items-center gap-8">
              <NavLink to="/catalogo" className={({ isActive }) => 
                `text-xs font-bold uppercase tracking-widest transition-colors ${isActive ? 'text-[#d32f2f]' : 'text-gray-500 hover:text-[#d32f2f]'}`
              }>Catálogo</NavLink>
              {isAuth && (isCliente || role === 'admin') && (
                <>
                  <NavLink to="/pedidos" className={({ isActive }) => 
                    `text-xs font-bold uppercase tracking-widest transition-colors ${isActive ? 'text-[#d32f2f]' : 'text-gray-500 hover:text-[#d32f2f]'}`
                  }>Pedidos</NavLink>
                </>
              )}
              {isAuth && isGestorPedidos && (
                <NavLink to="/admin/pedidos" className={({ isActive }) => 
                  `text-xs font-bold uppercase tracking-widest transition-colors ${isActive ? 'text-[#d32f2f]' : 'text-gray-500 hover:text-[#d32f2f]'}`
                }>Gestión</NavLink>
              )}
              {isAuth && isGestorStock && (
                <NavLink to="/admin" className={({ isActive }) => 
                  `text-xs font-bold uppercase tracking-widest transition-colors ${isActive ? 'text-[#d32f2f]' : 'text-gray-500 hover:text-[#d32f2f]'}`
                }>Admin</NavLink>
              )}
            </nav>

            {/* Desktop actions */}
            <div className="hidden md:flex items-center gap-5">
              {isAuth ? (
                <>
                  <CartButton onClick={() => setIsCartOpen(true)} />
                  <NavLink to="/perfil" className="text-xs font-bold uppercase tracking-widest text-gray-500 hover:text-[#d32f2f]">
                    {user?.name ?? 'Perfil'}
                  </NavLink>
                  <button onClick={handleLogout}
                    className="text-[10px] font-bold uppercase tracking-widest text-gray-400 hover:text-red-600 transition">
                    [ Salir ]
                  </button>
                </>
              ) : (
                <>
                  <Link to="/login" className="text-xs font-bold uppercase tracking-widest text-gray-500 hover:text-[#d32f2f] transition">
                    Ingresar
                  </Link>
                  <Link to="/register"
                    className="bg-[#d32f2f] hover:bg-[#b71c1c] text-white text-xs px-5 py-2 font-bold uppercase tracking-widest transition">
                    Unirse
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
              <NavLink to="/admin/pedidos" className={({ isActive }) => `block py-1 ${navLinkClass({ isActive })}`} onClick={() => setMobileMenuOpen(false)}>Panel pedidos</NavLink>
            )}
            {isAuth && isGestorStock && (
              <NavLink to="/admin" className={({ isActive }) => `block py-1 ${navLinkClass({ isActive })}`} onClick={() => setMobileMenuOpen(false)}>Dashboard</NavLink>
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
