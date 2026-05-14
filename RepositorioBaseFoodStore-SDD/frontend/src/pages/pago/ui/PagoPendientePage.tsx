import { Link, useSearchParams } from 'react-router-dom';

export const PagoPendientePage = () => {
  const [params] = useSearchParams();
  const orderId = params.get('external_reference');
  const formaPago = params.get('forma_pago');

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 font-sans">
      <div className="bg-white p-10 max-w-md text-center shadow-sm border border-gray-100">
        <div className="text-6xl mb-6">⏳</div>
        <h1 className="text-3xl font-black text-[#1a1a1a] tracking-tighter uppercase mb-4">
          PEDIDO <span className="text-yellow-600">RECIBIDO</span>
        </h1>
        
        <p className="text-gray-500 text-sm font-medium leading-relaxed mb-8 uppercase tracking-wide">
          {formaPago === 'EFECTIVO' 
            ? "Tu pedido ya está en preparación. Podrás abonarlo en efectivo al momento de la entrega o retiro."
            : "Estamos esperando la confirmación de tu pago. El pedido comenzará a prepararse apenas se acredite."}
        </p>

        {orderId && (
          <Link 
            to={`/pedidos/${orderId}`} 
            className="block w-full bg-[#d32f2f] hover:bg-[#b71c1c] text-white py-4 font-bold uppercase tracking-widest text-xs transition-all mb-4"
          >
            Ver pedido #{orderId}
          </Link>
        )}
        <Link 
          to="/pedidos" 
          className="text-[10px] font-bold text-gray-400 hover:text-[#d32f2f] uppercase tracking-widest transition-colors"
        >
          [ Mis pedidos ]
        </Link>
      </div>
    </div>
  );
};
