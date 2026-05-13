import { useState, useCallback } from 'react';

export function useFormModal<FormData, Entity>(initialData: FormData) {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedItem, setSelectedItem] = useState<Entity | null>(null);
  const [formData, setFormData] = useState<FormData>(initialData);

  const openCreate = useCallback((initialOverride?: Partial<FormData>) => {
    setSelectedItem(null);
    setFormData(prev => ({ ...initialData, ...initialOverride }));
    setIsOpen(true);
  }, [initialData]);

  const openEdit = useCallback((item: Entity, dataToEdit: FormData) => {
    setSelectedItem(item);
    setFormData(dataToEdit);
    setIsOpen(true);
  }, []);

  const close = useCallback(() => {
    setIsOpen(false);
    // Agregamos un pequeño delay para que la animación de cierre termine antes de resetear datos
    setTimeout(() => {
      setSelectedItem(null);
      setFormData(initialData);
    }, 200);
  }, [initialData]);

  return { isOpen, selectedItem, formData, setFormData, openCreate, openEdit, close };
}
