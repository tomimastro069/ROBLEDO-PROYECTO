import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { direccionesApi, type Address, type AddressPayload } from '@/shared/api/direccionesApi';

const emptyForm: AddressPayload = { street: '', numero: '', piso: '', city: '', state: '', zip_code: '' };

export const DireccionesPage = () => {
  const qc = useQueryClient();
  const [showForm, setShowForm] = useState(false);
  const [editId, setEditId] = useState<number | null>(null);
  const [form, setForm] = useState<AddressPayload>(emptyForm);

  const { data: addresses, isLoading } = useQuery({ queryKey: ['direcciones'], queryFn: direccionesApi.list });

  const invalidate = () => qc.invalidateQueries({ queryKey: ['direcciones'] });

  const createMutation = useMutation({ mutationFn: direccionesApi.create, onSuccess: () => { invalidate(); setShowForm(false); setForm(emptyForm); } });
  const updateMutation = useMutation({ mutationFn: ({ id, payload }: { id: number; payload: Partial<AddressPayload> }) => direccionesApi.update(id, payload), onSuccess: () => { invalidate(); setEditId(null); setForm(emptyForm); } });
  const deleteMutation = useMutation({ mutationFn: direccionesApi.remove, onSuccess: invalidate });
  const defaultMutation = useMutation({ mutationFn: direccionesApi.setDefault, onSuccess: invalidate });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (editId !== null) updateMutation.mutate({ id: editId, payload: form });
    else createMutation.mutate(form);
  };

  const startEdit = (addr: Address) => {
    setEditId(addr.id);
    setForm({ street: addr.street, numero: addr.numero ?? '', piso: addr.piso ?? '', city: addr.city, state: addr.state, zip_code: addr.zip_code });
    setShowForm(true);
  };

  if (isLoading) return <div className="p-8 text-gray-500">Cargando...</div>;

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Mis Direcciones</h1>
        <button onClick={() => { setShowForm(true); setEditId(null); setForm(emptyForm); }}
          className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition">
          + Nueva dirección
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="bg-white border border-gray-200 rounded-xl p-5 mb-6 space-y-3">
          <h2 className="font-semibold text-gray-700">{editId ? 'Editar dirección' : 'Nueva dirección'}</h2>
          {(['street', 'numero', 'piso', 'city', 'state', 'zip_code'] as (keyof AddressPayload)[]).map((field) => (
            <div key={field}>
              <label className="block text-sm text-gray-600 mb-1 capitalize">{field.replace('_', ' ')}</label>
              <input
                value={form[field] ?? ''}
                onChange={(e) => setForm(f => ({ ...f, [field]: e.target.value }))}
                required={['street', 'city', 'state', 'zip_code'].includes(field)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400"
              />
            </div>
          ))}
          <div className="flex gap-2 pt-2">
            <button type="submit" className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-lg text-sm transition">
              {editId ? 'Guardar cambios' : 'Crear'}
            </button>
            <button type="button" onClick={() => { setShowForm(false); setEditId(null); }}
              className="border border-gray-300 px-4 py-2 rounded-lg text-sm hover:bg-gray-50 transition">
              Cancelar
            </button>
          </div>
        </form>
      )}

      {addresses?.length === 0 && <p className="text-gray-500">No tenés direcciones guardadas.</p>}

      <div className="space-y-3">
        {addresses?.map((addr) => (
          <div key={addr.id} className={`bg-white border rounded-xl p-4 ${addr.is_default ? 'border-orange-400' : 'border-gray-200'}`}>
            <div className="flex justify-between items-start">
              <div>
                {addr.is_default && <span className="text-xs bg-orange-100 text-orange-600 px-2 py-0.5 rounded-full font-medium mb-1 inline-block">Predeterminada</span>}
                <p className="font-medium text-gray-800">{addr.street} {addr.numero} {addr.piso && `- ${addr.piso}`}</p>
                <p className="text-sm text-gray-500">{addr.city}, {addr.state} ({addr.zip_code})</p>
              </div>
              <div className="flex gap-2 ml-4">
                {!addr.is_default && (
                  <button onClick={() => defaultMutation.mutate(addr.id)}
                    className="text-xs text-orange-500 hover:underline">
                    Predeterminar
                  </button>
                )}
                <button onClick={() => startEdit(addr)} className="text-xs text-blue-500 hover:underline">Editar</button>
                <button onClick={() => deleteMutation.mutate(addr.id)} className="text-xs text-red-500 hover:underline">Eliminar</button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
