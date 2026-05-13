import React from 'react';

export const helpContent = {
  categories: (
    <div className="space-y-3">
      <p>Administra <strong>categorías</strong> del sistema.</p>
      <ul className="list-disc pl-5 space-y-2">
        <li><strong>Crear:</strong> Añade nuevas categorías para agrupar productos.</li>
        <li><strong>Editar:</strong> Modifica nombres o estado de las categorías.</li>
        <li><strong>Eliminar:</strong> Borra categorías que ya no se utilicen.</li>
      </ul>
    </div>
  ),
  products: (
    <div className="space-y-3">
      <p>Administra <strong>productos</strong> del sistema.</p>
      <ul className="list-disc pl-5 space-y-2">
        <li><strong>Crear:</strong> Añade productos con precio y stock.</li>
        <li><strong>Editar:</strong> Modifica detalles del producto.</li>
        <li><strong>Eliminar:</strong> Borra productos inactivos.</li>
      </ul>
    </div>
  ),
  ingredients: (
    <div className="space-y-3">
      <p>Administra <strong>ingredientes</strong> del sistema.</p>
      <ul className="list-disc pl-5 space-y-2">
        <li><strong>Crear:</strong> Añade ingredientes base.</li>
        <li><strong>Editar:</strong> Modifica detalles o si es alérgeno.</li>
        <li><strong>Eliminar:</strong> Borra ingredientes.</li>
      </ul>
    </div>
  )
};
