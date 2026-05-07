import { Link } from 'react-router-dom';

export const UnauthorizedPage = () => {
  return (
    <div>
      <h1>403 — Sin autorización</h1>
      <p>No tenés permisos para acceder a esta sección.</p>
      <Link to="/">Volver al inicio</Link>
    </div>
  );
};
