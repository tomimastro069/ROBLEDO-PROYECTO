import { useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { pagosApi } from '@/shared/api/pagosApi';

export const PagoExitoPage = () => {
  const [params] = useSearchParams();
  const orderId = params.get('external_reference');
  const [verifying, setVerifying] = useState(true);

  useEffect(() => {
    if (orderId) {
      pagosApi.verificar(Number(orderId))
        .finally(() => setVerifying(false));
    } else {
      setVerifying(false);
    }
  }, [orderId]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 font-sans">
      <div className="bg-white p-10 max-w-md text-center shadow-sm border border-gray-100">
        <div className="text-6xl mb-6">✅</div>
        <h1 className="text-3xl font-black text-[#1a1a1a] tracking-tighter uppercase mb-4">
          ¡PAGO <span className="text-[#d32f2f]">RECIBIDO</span>!
        </h1>
        
        {verifying ? (
          <p className="text-gray-400 text-xs font-bold uppercase tracking-[0.2em] animate-pulse">
            Confirmando transacción...
          </p>
        ) : (
          <>
            <p className="text-gray-500 text-sm font-medium leading-relaxed mb-8 uppercase tracking-wide">
              Tu pedido ha sido procesado correctamente y ya está en marcha.
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
              [ Historial de pedidos ]
            </Link>
          </>
        )}
      </div>
    </div>
  );
};
