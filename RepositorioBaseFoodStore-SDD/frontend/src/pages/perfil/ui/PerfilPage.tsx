import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { perfilApi } from '@/shared/api/perfilApi';
import { direccionesApi, type Address, type AddressPayload } from '@/shared/api/direccionesApi';
import { PageContainer } from '@/shared/ui/PageContainer';

const emptyAddress: AddressPayload = { street: '', numero: '', piso: '', city: '', state: '', zip_code: '' };

export const PerfilPage = () => {
  const qc = useQueryClient();
  const { data: perfil, isLoading: profileLoading } = useQuery({ queryKey: ['perfil'], queryFn: perfilApi.get });
  const { data: addresses, isLoading: addrLoading } = useQuery({ queryKey: ['direcciones'], queryFn: direccionesApi.list });

  // Profile data state
  const [editMode, setEditMode] = useState(false);
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');

  // Password state
  const [changingPwd, setChangingPwd] = useState(false);
  const [pwdActual, setPwdActual] = useState('');
  const [pwdNueva, setPwdNueva] = useState('');
  const [pwdMsg, setPwdMsg] = useState<{ ok: boolean; msg: string } | null>(null);

  // Address form state
  const [showAddrForm, setShowAddrForm] = useState(false);
  const [editAddrId, setEditAddrId] = useState<number | null>(null);
  const [addrForm, setAddrForm] = useState<AddressPayload>(emptyAddress);

  const invalidate = () => qc.invalidateQueries({ queryKey: ['perfil', 'direcciones'] });

  const updateMutation = useMutation({
    mutationFn: perfilApi.update,
    onSuccess: () => { invalidate(); setEditMode(false); },
  });

  const pwdMutation = useMutation({
    mutationFn: perfilApi.changePassword,
    onSuccess: () => { setPwdMsg({ ok: true, msg: 'Contraseña actualizada.' }); setPwdActual(''); setPwdNueva(''); setChangingPwd(false); },
    onError: () => setPwdMsg({ ok: false, msg: 'Contraseña actual incorrecta.' }),
  });

  const addrMutation = useMutation({
    mutationFn: (payload: AddressPayload) => editAddrId !== null ? direccionesApi.update(editAddrId, payload) : direccionesApi.create(payload),
    onSuccess: () => { invalidate(); setShowAddrForm(false); setEditAddrId(null); setAddrForm(emptyAddress); }
  });

  const deleteAddrMutation = useMutation({ mutationFn: direccionesApi.remove, onSuccess: invalidate });
  const defaultAddrMutation = useMutation({ mutationFn: direccionesApi.setDefault, onSuccess: invalidate });

  const startEdit = () => {
    setName(perfil?.name ?? '');
    setPhone(perfil?.phone ?? '');
    setEditMode(true);
  };

  const startEditAddr = (addr: Address) => {
    setEditAddrId(addr.id);
    setAddrForm({ street: addr.street, numero: addr.numero ?? '', piso: addr.piso ?? '', city: addr.city, state: addr.state, zip_code: addr.zip_code });
    setShowAddrForm(true);
  };

  if (profileLoading || addrLoading) return <div className="p-8 text-center text-gray-400 animate-pulse">Cargando...</div>;

  return (
    <PageContainer title="Mi Cuenta" description="Gestioná tus datos, direcciones y seguridad.">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Lado izquierdo: Datos Personales */}
        <div className="lg:col-span-1 space-y-6">
          <div className="glass-card rounded-[2rem] p-8 border-white/60">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold text-gray-900">Datos Personales</h2>
              {!editMode && (
                <button onClick={startEdit} className="text-orange-600 hover:text-orange-700 font-bold text-sm">Editar</button>
              )}
            </div>

            {!editMode ? (
              <div className="space-y-6">
                <div>
                  <label className="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1">Email</label>
                  <p className="text-gray-900 font-medium">{perfil?.email}</p>
                </div>
                <div>
                  <label className="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1">Nombre Completo</label>
                  <p className="text-gray-900 font-medium">{perfil?.name || '—'}</p>
                </div>
                <div>
                  <label className="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1">Teléfono</label>
                  <p className="text-gray-900 font-medium">{perfil?.phone || '—'}</p>
                </div>
              </div>
            ) : (
              <form onSubmit={(e) => { e.preventDefault(); updateMutation.mutate({ name, phone }); }} className="space-y-4">
                <div>
                  <label className="block text-xs font-bold text-gray-500 mb-1.5 ml-1">Nombre</label>
                  <input value={name} onChange={(e) => setName(e.target.value)} className="input-premium py-2 px-3" />
                </div>
                <div>
                  <label className="block text-xs font-bold text-gray-500 mb-1.5 ml-1">Teléfono</label>
                  <input value={phone} onChange={(e) => setPhone(e.target.value)} className="input-premium py-2 px-3" />
                </div>
                <div className="flex gap-3 pt-2">
                  <button type="submit" className="flex-1 btn-premium py-2 text-sm">Guardar</button>
                  <button type="button" onClick={() => setEditMode(false)} className="flex-1 bg-gray-100 text-gray-600 font-bold py-2 rounded-xl text-sm">Cancelar</button>
                </div>
              </form>
            )}
          </div>

          {/* Seguridad */}
          <div className="glass-card rounded-[2rem] p-8 border-white/60">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Seguridad</h2>
            {!changingPwd ? (
              <button onClick={() => { setChangingPwd(true); setPwdMsg(null); }} className="text-orange-600 hover:text-orange-700 font-bold text-sm flex items-center gap-2">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
                Cambiar contraseña
              </button>
            ) : (
              <form onSubmit={(e) => { e.preventDefault(); pwdMutation.mutate({ password_actual: pwdActual, password_nueva: pwdNueva }); }} className="space-y-4">
                <div>
                  <label className="block text-xs font-bold text-gray-500 mb-1.5 ml-1">Contraseña Actual</label>
                  <input type="password" value={pwdActual} onChange={(e) => setPwdActual(e.target.value)} required className="input-premium py-2 px-3" />
                </div>
                <div>
                  <label className="block text-xs font-bold text-gray-500 mb-1.5 ml-1">Nueva Contraseña</label>
                  <input type="password" value={pwdNueva} onChange={(e) => setPwdNueva(e.target.value)} required minLength={8} className="input-premium py-2 px-3" />
                </div>
                {pwdMsg && <p className={`text-xs font-bold ${pwdMsg.ok ? 'text-green-600' : 'text-rose-500'}`}>{pwdMsg.msg}</p>}
                <div className="flex gap-3 pt-2">
                  <button type="submit" className="flex-1 btn-premium py-2 text-sm">Actualizar</button>
                  <button type="button" onClick={() => setChangingPwd(false)} className="flex-1 bg-gray-100 text-gray-600 font-bold py-2 rounded-xl text-sm">Cancelar</button>
                </div>
              </form>
            )}
          </div>
        </div>

        {/* Lado derecho: Direcciones */}
        <div className="lg:col-span-2">
          <div className="glass-card rounded-[2rem] p-8 border-white/60 min-h-full">
            <div className="flex justify-between items-center mb-8">
              <h2 className="text-2xl font-bold text-gray-900">Mis Direcciones</h2>
              {!showAddrForm && (
                <button 
                  onClick={() => { setShowAddrForm(true); setEditAddrId(null); setAddrForm(emptyAddress); }}
                  className="btn-premium py-2 px-6 text-sm"
                >
                  + Nueva Dirección
                </button>
              )}
            </div>

            {showAddrForm && (
              <form onSubmit={(e) => { e.preventDefault(); addrMutation.mutate(addrForm); }} className="bg-orange-50/50 border border-orange-100 rounded-3xl p-6 mb-8 animate-in fade-in slide-in-from-top-4 duration-300">
                <h3 className="font-bold text-gray-900 mb-4">{editAddrId ? 'Editar Dirección' : 'Nueva Dirección'}</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="md:col-span-2">
                    <label className="block text-xs font-bold text-gray-500 mb-1.5 ml-1">Calle</label>
                    <input required value={addrForm.street} onChange={e => setAddrForm(f => ({ ...f, street: e.target.value }))} className="input-premium py-2 px-3" />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-gray-500 mb-1.5 ml-1">Número</label>
                    <input required value={addrForm.numero} onChange={e => setAddrForm(f => ({ ...f, numero: e.target.value }))} className="input-premium py-2 px-3" />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-gray-500 mb-1.5 ml-1">Piso/Depto</label>
                    <input value={addrForm.piso} onChange={e => setAddrForm(f => ({ ...f, piso: e.target.value }))} className="input-premium py-2 px-3" />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-gray-500 mb-1.5 ml-1">Localidad</label>
                    <input required value={addrForm.city} onChange={e => setAddrForm(f => ({ ...f, city: e.target.value }))} className="input-premium py-2 px-3" />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-gray-500 mb-1.5 ml-1">Provincia</label>
                    <input required value={addrForm.state} onChange={e => setAddrForm(f => ({ ...f, state: e.target.value }))} className="input-premium py-2 px-3" />
                  </div>
                </div>
                <div className="flex gap-3 mt-6">
                  <button type="submit" className="btn-premium py-2 px-8 text-sm">Guardar Dirección</button>
                  <button type="button" onClick={() => setShowAddrForm(false)} className="bg-white text-gray-600 font-bold py-2 px-6 rounded-xl text-sm border border-gray-200">Cancelar</button>
                </div>
              </form>
            )}

            {addresses?.length === 0 && !showAddrForm ? (
              <div className="text-center py-12 bg-gray-50/50 rounded-3xl border-2 border-dashed border-gray-200">
                <p className="text-gray-400 font-bold uppercase tracking-widest text-xs">No tenés direcciones guardadas</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {addresses?.map((addr) => (
                  <div key={addr.id} className={`group relative bg-white border-2 rounded-3xl p-6 transition-all duration-300 ${addr.is_default ? 'border-orange-500 shadow-lg shadow-orange-100' : 'border-gray-100 hover:border-orange-200'}`}>
                    {addr.is_default && (
                      <span className="absolute top-4 right-4 bg-orange-500 text-white text-[10px] font-black uppercase px-2 py-1 rounded-lg">Predeterminada</span>
                    )}
                    <div className="mb-4">
                      <p className="text-xl font-bold text-gray-900 mb-1">{addr.street} {addr.numero}</p>
                      {addr.piso && <p className="text-sm font-medium text-gray-500 mb-1">Piso {addr.piso}</p>}
                      <p className="text-sm font-medium text-gray-400">{addr.city}, {addr.state}</p>
                    </div>
                    <div className="flex items-center gap-4 pt-4 border-t border-gray-50">
                      {!addr.is_default && (
                        <button onClick={() => defaultAddrMutation.mutate(addr.id)} className="text-xs font-bold text-orange-600 hover:underline">Principal</button>
                      )}
                      <button onClick={() => startEditAddr(addr)} className="text-xs font-bold text-gray-400 hover:text-gray-600">Editar</button>
                      <button onClick={() => deleteAddrMutation.mutate(addr.id)} className="text-xs font-bold text-rose-400 hover:text-rose-600 ml-auto">Eliminar</button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

      </div>
    </PageContainer>
  );
};
