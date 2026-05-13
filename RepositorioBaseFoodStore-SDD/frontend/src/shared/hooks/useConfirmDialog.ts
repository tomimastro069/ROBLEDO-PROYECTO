import { useState, useCallback } from 'react';

export function useConfirmDialog<Entity>() {
  const [isOpen, setIsOpen] = useState(false);
  const [item, setItem] = useState<Entity | null>(null);

  const open = useCallback((entityItem: Entity) => {
    setItem(entityItem);
    setIsOpen(true);
  }, []);

  const close = useCallback(() => {
    setIsOpen(false);
    setTimeout(() => setItem(null), 200);
  }, []);

  return { isOpen, item, open, close };
}
