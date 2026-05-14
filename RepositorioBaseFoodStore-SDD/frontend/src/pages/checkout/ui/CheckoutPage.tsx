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
        <div className="bg-green-50 border border-green-200 rounded-2xl p-8 space-y-6">
          <div className="w-16 h-16 bg-green-500 text-white rounded-full flex items-center justify-center mx-auto text-2xl font-bold">
            ✓
          </div>
          <h2 className="text-2xl font-bold text-gray-800">
            ¡Pedido registrado con éxito!
          </h2>
          <p className="text-gray-600">
            Tu pedido <span className="font-semibold">#{createdOrder.id}</span>{" "}
            ha sido creado para pagar mediante{" "}
            <span className="font-bold">{formaPago}</span>.
          </p>
          <button
            onClick={() => navigate(`/pedidos/${createdOrder.id}`)}
            className="w-full bg-orange-500 hover:bg-orange-600 text-white font-bold py-4 rounded-xl text-lg transition shadow-md"
          >
            Ir al detalle del pedido
          </button>
        </div>
      </div>
    );
  }

  if (items.length === 0 && !preferenceId && !createdOrder) {
    return (
      <div className="max-w-xl mx-auto px-4 py-20 text-center">
        <p className="text-xl text-gray-400">Tu carrito está vacío.</p>
        <button
          onClick={() => navigate("/catalogo")}
          className="mt-4 text-orange-500 hover:underline"
        >
          Ir al catálogo
        </button>
      </div>
    );
  }

  const selected = addresses?.find((a) => a.id === selectedAddressId);

  const handleConfirm = () => {
    if (!selected) {
      setError("Seleccioná una dirección de entrega.");
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
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-2xl sm:text-3xl font-bold text-gray-800 mb-8">
        Confirmar pedido
      </h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Columna izquierda — Forma de pago + Dirección o MP Wallet */}
        <div className="space-y-6">
          {!preferenceId && !createdOrder && (
            <div className="bg-white border border-gray-200 rounded-xl p-6">
              <h2 className="font-semibold text-gray-800 text-lg mb-4">
                Forma de pago
              </h2>
              <div className="grid grid-cols-3 gap-3">
                {[
                  { code: "MERCADOPAGO", label: "💳 MP" },
                  { code: "EFECTIVO", label: "💵 Efectivo" },
                  { code: "TRANSFERENCIA", label: "🏦 Transf." },
                ].map((fp) => (
                  <label
                    key={fp.code}
                    className={`flex flex-col items-center justify-center border rounded-xl p-3 cursor-pointer text-center transition ${formaPago === fp.code ? "border-orange-500 bg-orange-50 text-orange-600 font-semibold" : "border-gray-200 text-gray-600 hover:border-gray-300"}`}
                  >
                    <input
                      type="radio"
                      name="formaPago"
                      checked={formaPago === fp.code}
                      onChange={() => setFormaPago(fp.code)}
                      className="sr-only"
                    />
                    <span className="text-sm">{fp.label}</span>
                  </label>
                ))}
              </div>
            </div>
          )}

          {preferenceId ? (
            <div className="bg-white border border-gray-200 rounded-xl p-6">
              <h2 className="font-semibold text-gray-800 text-lg mb-4">
                Realizar Pago Seguro
              </h2>
              <p className="text-sm text-gray-500 mb-4">
                Estás a un paso de confirmar tu pedido. Por favor, completá el
                pago de forma segura a través de MercadoPago.
              </p>
              <Wallet initialization={{ preferenceId }} />
              {createdOrder && (
                <button
                  onClick={() => navigate(`/pedidos/${createdOrder.id}`)}
                  className="mt-4 w-full bg-orange-100 hover:bg-orange-200 text-orange-700 font-semibold py-3 rounded-xl text-sm transition"
                >
                  Simular Pago / Ir al Pedido #{createdOrder.id}
                </button>
              )}
            </div>
          ) : (
            <div className="bg-white border border-gray-200 rounded-xl p-6">
              <h2 className="font-semibold text-gray-800 text-lg mb-4">
                Dirección de entrega
              </h2>
              {loadingAddr ? (
                <p className="text-sm text-gray-400">Cargando...</p>
              ) : addresses?.length === 0 ? (
                <p className="text-sm text-gray-500">
                  No tenés direcciones.{" "}
                  <button
                    onClick={() => navigate("/direcciones")}
                    className="text-orange-500 hover:underline"
                  >
                    Agregar una
                  </button>
                </p>
              ) : (
                <div className="space-y-3">
                  {addresses?.map((addr) => (
                    <label
                      key={addr.id}
                      className={`flex items-start gap-3 border rounded-xl p-4 cursor-pointer transition ${selectedAddressId === addr.id ? "border-orange-400 bg-orange-50" : "border-gray-200 hover:border-gray-300"}`}
                    >
                      <input
                        type="radio"
                        name="address"
                        checked={selectedAddressId === addr.id}
                        onChange={() => setSelectedAddressId(addr.id)}
                        className="mt-0.5 accent-orange-500"
                      />
                      <div className="flex-1">
                        <p className="text-sm font-medium text-gray-800">
                          {addr.street} {addr.numero}
                          {addr.piso ? `, piso ${addr.piso}` : ""}
                        </p>
                        <p className="text-xs text-gray-500 mt-0.5">
                          {addr.city}, {addr.state} — {addr.zip_code}
                        </p>
                        {addr.is_default && (
                          <span className="text-xs text-orange-500 font-medium mt-1 inline-block">
                            ★ Predeterminada
                          </span>
                        )}
                      </div>
                    </label>
                  ))}
                  <button
                    onClick={() => navigate("/direcciones")}
                    className="text-sm text-orange-500 hover:underline mt-1"
                  >
                    + Agregar nueva dirección
                  </button>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Columna derecha — Resumen + confirmar */}
        <div className="space-y-6">
          <div className="bg-white border border-gray-200 rounded-xl p-6">
            <h2 className="font-semibold text-gray-800 text-lg mb-4">
              Resumen del pedido
            </h2>
            <ul className="divide-y divide-gray-100">
              {displayItems.map((item) => (
                <li
                  key={item.id}
                  className="py-3 flex justify-between items-center"
                >
                  <div>
                    <p className="text-sm font-medium text-gray-800">
                      {item.name}
                    </p>
                    <p className="text-xs text-gray-400">
                      x{item.quantity} · ${Number(item.price).toFixed(2)} c/u
                    </p>
                  </div>
                  <span className="text-sm font-semibold text-gray-700">
                    ${(Number(item.price) * item.quantity).toFixed(2)}
                  </span>
                </li>
              ))}
            </ul>
            <div className="border-t border-gray-200 pt-4 mt-4 flex justify-between">
              <span className="font-bold text-gray-800">Total</span>
              <span className="font-bold text-xl text-orange-500">
                ${Number(displayTotal).toFixed(2)}
              </span>
            </div>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-xl px-4 py-3">
              <p className="text-sm text-red-600">{error}</p>
            </div>
          )}

          {!preferenceId && (
            <>
              <button
                onClick={handleConfirm}
                disabled={createOrder.isPending}
                className="w-full bg-orange-500 hover:bg-orange-600 text-white font-bold py-4 rounded-xl text-lg transition disabled:opacity-50 shadow-sm"
              >
                {createOrder.isPending
                  ? "Preparando pago..."
                  : "Proceder al pago"}
              </button>

              <button
                onClick={() => navigate(-1)}
                className="w-full text-gray-400 hover:text-gray-600 text-sm transition"
              >
                ← Volver al carrito
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

