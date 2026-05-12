import { Link, useSearchParams } from 'react-router-dom';

export const PagoErrorPage = () => {
  const [params] = useSearchParams();
  const orderId = params.get('external_reference');

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white rounded-xl shadow-md p-10 max-w-md text-center">
        <div className="text-6xl mb-4">❌</div>
        <h1 className="text-2xl font-bold text-red-500 mb-2">Pago rechazado</h1>
        <p className="text-gray-600 mb-6">No se pudo procesar el pago. Podés intentarlo de nuevo.</p>
        {orderId && (
          <Link to={`/pedidos/${orderId}`} className="block mb-3 bg-orange-500 hover:bg-orange-600 text-white px-6 py-2 rounded-lg font-medium transition">
            Reintentar pago
          </Link>
        )}
        <Link to="/pedidos" className="text-sm text-gray-500 hover:underline">Ver mis pedidos</Link>
      </div>
    </div>
  );
};
