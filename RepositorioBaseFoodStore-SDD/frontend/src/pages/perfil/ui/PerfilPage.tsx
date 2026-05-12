import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { perfilApi } from '@/shared/api/perfilApi';

export const PerfilPage = () => {
  const qc = useQueryClient();
  const { data: perfil, isLoading } = useQuery({ queryKey: ['perfil'], queryFn: perfilApi.get });

  const [editMode, setEditMode] = useState(false);
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');

  const [changingPwd, setChangingPwd] = useState(false);
  const [pwdActual, setPwdActual] = useState('');
  const [pwdNueva, setPwdNueva] = useState('');
  const [pwdMsg, setPwdMsg] = useState<{ ok: boolean; msg: string } | null>(null);

  const updateMutation = useMutation({
    mutationFn: perfilApi.update,
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['perfil'] }); setEditMode(false); },
  });

  const pwdMutation = useMutation({
    mutationFn: perfilApi.changePassword,
    onSuccess: () => { setPwdMsg({ ok: true, msg: 'Contraseña actualizada.' }); setPwdActual(''); setPwdNueva(''); setChangingPwd(false); },
    onError: () => setPwdMsg({ ok: false, msg: 'Contraseña actual incorrecta.' }),
  });

  const startEdit = () => {
    setName(perfil?.name ?? '');
    setPhone(perfil?.phone ?? '');
    setEditMode(true);
  };

  if (isLoading) return <div className="p-8 text-gray-500">Cargando...</div>;

  return (
    <div className="max-w-xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Mi Perfil</h1>

      <div className="bg-white border border-gray-200 rounded-xl p-6 mb-5">
        {!editMode ? (
          <>
            <div className="space-y-3">
              <div><span className="text-xs text-gray-400 uppercase">Email</span><p className="text-gray-800 font-medium">{perfil?.email}</p></div>
              <div><span className="text-xs text-gray-400 uppercase">Nombre</span><p className="text-gray-800">{perfil?.name ?? '—'}</p></div>
              <div><span className="text-xs text-gray-400 uppercase">Teléfono</span><p className="text-gray-800">{perfil?.phone ?? '—'}</p></div>
            </div>
            <button onClick={startEdit} className="mt-5 bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition">
              Editar datos
            </button>
          </>
        ) : (
          <form onSubmit={(e) => { e.preventDefault(); updateMutation.mutate({ name, phone }); }} className="space-y-3">
            <div>
              <label className="block text-sm text-gray-600 mb-1">Nombre</label>
              <input value={name} onChange={(e) => setName(e.target.value)} className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-orange-400 focus:outline-none" />
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">Teléfono</label>
              <input value={phone} onChange={(e) => setPhone(e.target.value)} className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-orange-400 focus:outline-none" />
            </div>
            <div className="flex gap-2 pt-1">
              <button type="submit" className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-lg text-sm transition">Guardar</button>
              <button type="button" onClick={() => setEditMode(false)} className="border border-gray-300 px-4 py-2 rounded-lg text-sm hover:bg-gray-50 transition">Cancelar</button>
            </div>
          </form>
        )}
      </div>

      {/* Cambio de contraseña */}
      <div className="bg-white border border-gray-200 rounded-xl p-6">
        <h2 className="font-semibold text-gray-700 mb-3">Cambiar contraseña</h2>
        {!changingPwd ? (
          <button onClick={() => { setChangingPwd(true); setPwdMsg(null); }}
            className="text-sm text-orange-500 hover:underline">
            Cambiar contraseña
          </button>
        ) : (
          <form onSubmit={(e) => { e.preventDefault(); pwdMutation.mutate({ password_actual: pwdActual, password_nueva: pwdNueva }); }} className="space-y-3">
            <div>
              <label className="block text-sm text-gray-600 mb-1">Contraseña actual</label>
              <input type="password" value={pwdActual} onChange={(e) => setPwdActual(e.target.value)} required className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-orange-400 focus:outline-none" />
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">Nueva contraseña</label>
              <input type="password" value={pwdNueva} onChange={(e) => setPwdNueva(e.target.value)} required minLength={8} className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-orange-400 focus:outline-none" />
            </div>
            {pwdMsg && <p className={`text-sm ${pwdMsg.ok ? 'text-green-600' : 'text-red-500'}`}>{pwdMsg.msg}</p>}
            <div className="flex gap-2 pt-1">
              <button type="submit" className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-lg text-sm transition">Actualizar</button>
              <button type="button" onClick={() => setChangingPwd(false)} className="border border-gray-300 px-4 py-2 rounded-lg text-sm hover:bg-gray-50 transition">Cancelar</button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};
