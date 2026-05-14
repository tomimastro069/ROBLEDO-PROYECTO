import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useQuery, useMutation } from "@tanstack/react-query";
import { direccionesApi } from "@/shared/api/direccionesApi";
import { ordersApi } from "@/shared/api/ordersApi";
import { pagosApi } from "@/shared/api/pagosApi";
import { useCartStore } from "@/entities/cart/model/cartStore";
import { initMercadoPago, Wallet } from "@mercadopago/sdk-react";

// Initialize MercadoPago with a placeholder or env variable
initMercadoPago(import.meta.env.VITE_MP_PUBLIC_KEY || "TEST-public-key");

export const CheckoutPage = () => {
  const navigate = useNavigate();
  const { items, total, clearCart } = useCartStore();
  const [selectedAddressId, setSelectedAddressId] = useState<number | null>(
    null,
  );
  const [error, setError] = useState<string | null>(null);
  const [preferenceId, setPreferenceId] = useState<string | null>(null);
  const [createdOrder, setCreatedOrder] = useState<any | null>(null);
  const [formaPago, setFormaPago] = useState<string>("MERCADOPAGO");
  const [orderSnapshot, setOrderSnapshot] = useState<{
    items: any[];
    total: number;
  } | null>(null);

  const { data: addresses, isLoading: loadingAddr } = useQuery({
    queryKey: ["direcciones"],
    queryFn: direccionesApi.list,
  });

  const createOrder = useMutation({
    mutationFn: ordersApi.create,
    onSuccess: async (order) => {
      setCreatedOrder(order);
      try {
        const pago = await pagosApi.crear({
          pedido_id: order.id,
          forma_pago_codigo: formaPago,
        });
        if (pago.preference_id) {
          setPreferenceId(pago.preference_id);
        }
        clearCart(); // Clear cart as order is already created
      } catch (err) {
        console.error(err);
        setError("Error al iniciar el pago con MercadoPago.");
      }
    },
    onError: () =>
      setError("Error al crear el pedido. Verificá el stock disponible."),
  });

  if (createdOrder && formaPago !== "MERCADOPAGO") {
    return (
      <div className="max-w-xl mx-auto px-4 py-20 text-center">
        <div className="bg-white border-2 border-[#d32f2f] p-10 space-y-6">
          <div className="w-16 h-16 border-4 border-[#d32f2f] text-[#d32f2f] rounded-full flex items-center justify-center mx-auto text-2xl font-black">
            OK
          </div>
          <h2 className="text-3xl font-black text-gray-900 uppercase tracking-tighter">
            Pedido Confirmado
          </h2>
          <p className="text-gray-500 font-medium uppercase tracking-widest text-xs">
            Orden <span className="text-[#d32f2f]">#{createdOrder.id}</span> registrada para pago vía {formaPago}.
          </p>
          <button
            onClick={() => navigate(`/pedidos/${createdOrder.id}`)}
            className="w-full bg-[#d32f2f] hover:bg-[#b71c1c] text-white font-bold py-4 uppercase tracking-widest text-xs transition"
          >
            Ver Detalle de Orden
          </button>
        </div>
      </div>
    );
  }

  if (items.length === 0 && !preferenceId && !createdOrder) {
    return (
      <div className="max-w-xl mx-auto px-4 py-20 text-center border-2 border-dashed border-gray-100 mt-10">
        <p className="text-sm font-bold text-gray-400 uppercase tracking-widest">El carrito está vacío.</p>
        <button
          onClick={() => navigate("/catalogo")}
          className="mt-4 text-[#d32f2f] font-bold uppercase tracking-widest text-xs hover:underline"
        >
          Ir al catálogo
        </button>
      </div>
    );
  }

  const selected = addresses?.find((a) => a.id === selectedAddressId);

  const handleConfirm = () => {
    if (!selected) {
      setError("SELECCIONÁ UNA DIRECCIÓN DE ENTREGA.");
      return;
    }
    setError(null);
    setOrderSnapshot({ items: [...items], total });

    createOrder.mutate({
      items: items.map((i) => ({
        product_id: i.id,
        quantity: i.quantity,
      })),
      shipping_address_id: selected.id,
    });
  };

  const displayItems = orderSnapshot ? orderSnapshot.items : items;
  const displayTotal = orderSnapshot ? orderSnapshot.total : total;

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 className="text-4xl font-black text-[#1a1a1a] mb-12 uppercase tracking-tighter border-b-4 border-[#d32f2f] inline-block">
        Finalizar Compra
      </h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
        {/* Columna izquierda — Forma de pago + Dirección o MP Wallet */}
        <div className="space-y-10">
          {!preferenceId && !createdOrder && (
            <div className="bg-white border-t-4 border-[#d32f2f] p-8 shadow-sm">
              <h2 className="font-bold text-[#1a1a1a] uppercase tracking-widest text-sm mb-6">
                1. Método de Pago
              </h2>
              <div className="grid grid-cols-1 gap-3">
                {[
                  { code: "MERCADOPAGO", label: "MERCADO PAGO" },
                  { code: "EFECTIVO", label: "EFECTIVO EN LOCAL" },
                  { code: "TRANSFERENCIA", label: "TRANSFERENCIA BANCARIA" },
                ].map((fp) => (
                  <label
                    key={fp.code}
                    className={`flex items-center justify-between border-2 px-6 py-4 cursor-pointer transition ${formaPago === fp.code ? "border-[#d32f2f] bg-gray-50 text-[#d32f2f] font-black" : "border-gray-100 text-gray-500 hover:border-gray-200"}`}
                  >
                    <input
                      type="radio"
                      name="formaPago"
                      checked={formaPago === fp.code}
                      onChange={() => setFormaPago(fp.code)}
                      className="sr-only"
                    />
                    <span className="text-xs uppercase tracking-[0.2em]">{fp.label}</span>
                    {formaPago === fp.code && <span className="text-xs font-black">●</span>}
                  </label>
                ))}
              </div>
            </div>
          )}

          {preferenceId ? (
            <div className="bg-white border-t-4 border-[#d32f2f] p-8 shadow-sm">
              <h2 className="font-bold text-[#1a1a1a] uppercase tracking-widest text-sm mb-6">
                2. Completar Pago
              </h2>
              <p className="text-xs font-medium text-gray-400 uppercase tracking-widest leading-loose mb-6">
                ESTÁS A UN PASO. POR FAVOR, COMPLETÁ LA TRANSACCIÓN PARA PROCESAR TU ORDEN.
              </p>
              <Wallet initialization={{ preferenceId }} />
              {createdOrder && (
                <button
                  onClick={() => navigate(`/pedidos/${createdOrder.id}`)}
                  className="mt-6 w-full border-2 border-gray-100 text-gray-400 hover:text-[#d32f2f] hover:border-[#d32f2f] font-bold py-3 uppercase tracking-widest text-[10px] transition"
                >
                  Ver Pedido #{createdOrder.id}
                </button>
              )}
            </div>
          ) : (
            <div className="bg-white border-t-4 border-[#d32f2f] p-8 shadow-sm">
              <h2 className="font-bold text-[#1a1a1a] uppercase tracking-widest text-sm mb-6">
                2. Dirección de Envío
              </h2>
              {loadingAddr ? (
                <p className="text-xs font-bold text-gray-300 animate-pulse">CARGANDO...</p>
              ) : addresses?.length === 0 ? (
                <p className="text-xs font-bold text-gray-400 uppercase tracking-widest">
                  No hay direcciones registradas.{" "}
                  <button
                    onClick={() => navigate("/direcciones")}
                    className="text-[#d32f2f] underline"
                  >
                    AGREGAR
                  </button>
                </p>
              ) : (
                <div className="space-y-4">
                  {addresses?.map((addr) => (
                    <label
                      key={addr.id}
                      className={`flex items-start gap-4 border-2 p-6 cursor-pointer transition ${selectedAddressId === addr.id ? "border-[#d32f2f] bg-gray-50" : "border-gray-100 hover:border-gray-200"}`}
                    >
                      <input
                        type="radio"
                        name="address"
                        checked={selectedAddressId === addr.id}
                        onChange={() => setSelectedAddressId(addr.id)}
                        className="mt-1 accent-[#d32f2f]"
                      />
                      <div className="flex-1">
                        <p className="text-sm font-black text-gray-900 uppercase tracking-tight">
                          {addr.street} {addr.numero}
                        </p>
                        <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mt-1">
                          {addr.city}, {addr.state} — {addr.zip_code}
                        </p>
                      </div>
                    </label>
                  ))}
                  <button
                    onClick={() => navigate("/direcciones")}
                    className="text-[10px] font-bold text-[#d32f2f] uppercase tracking-[0.2em] mt-2 hover:underline"
                  >
                    + NUEVA DIRECCIÓN
                  </button>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Columna derecha — Resumen + confirmar */}
        <div className="space-y-8">
          <div className="bg-gray-900 p-8 text-white">
            <h2 className="font-bold uppercase tracking-[0.3em] text-[10px] mb-8 text-gray-400 border-b border-gray-800 pb-4">
              Resumen de Orden
            </h2>
            <ul className="divide-y divide-gray-800">
              {displayItems.map((item) => (
                <li
                  key={item.id}
                  className="py-4 flex justify-between items-start"
                >
                  <div className="max-w-[70%]">
                    <p className="text-xs font-black uppercase tracking-tight">
                      {item.name}
                    </p>
                    <p className="text-[10px] font-bold text-gray-500 uppercase tracking-widest mt-1">
                      {item.quantity} UNIT. × ${Number(item.price).toFixed(2)}
                    </p>
                  </div>
                  <span className="text-xs font-black">
                    ${(Number(item.price) * item.quantity).toFixed(2)}
                  </span>
                </li>
              ))}
            </ul>
            <div className="pt-8 mt-8 border-t border-gray-800 flex justify-between items-end">
              <span className="text-[10px] font-bold uppercase tracking-[0.3em] text-gray-400">Total Final</span>
              <span className="text-3xl font-black text-[#d32f2f]">
                ${Number(displayTotal).toFixed(2)}
              </span>
            </div>
          </div>

          {error && (
            <div className="bg-red-50 border-l-4 border-red-500 px-6 py-4">
              <p className="text-[10px] font-bold text-red-600 uppercase tracking-widest">{error}</p>
            </div>
          )}

          {!preferenceId && (
            <div className="space-y-4">
              <button
                onClick={handleConfirm}
                disabled={createOrder.isPending}
                className="w-full bg-[#d32f2f] hover:bg-[#b71c1c] text-white font-black py-6 uppercase tracking-[0.2em] text-xs transition disabled:opacity-50"
              >
                {createOrder.isPending
                  ? "PROCESANDO..."
                  : "CONFIRMAR Y PAGAR"}
              </button>

              <button
                onClick={() => navigate(-1)}
                className="w-full text-gray-400 hover:text-gray-900 text-[10px] font-bold uppercase tracking-widest transition"
              >
                [ VOLVER AL CARRITO ]
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

