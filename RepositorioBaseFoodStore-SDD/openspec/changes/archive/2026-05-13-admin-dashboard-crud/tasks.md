# Tasks — admin-dashboard-crud

## Status: COMPLETED ✅

### Foundation
- [x] 1. Crear `AdminLayout` con sidebar por rol
- [x] 2. Crear `useFormModal<F, E>` hook
- [x] 3. Crear `useConfirmDialog<E>` hook
- [x] 4. Crear `usePagination` hook
- [x] 5. Crear `FormState<T>` type
- [x] 6. Crear `logger.ts` (handleError, logWarning)
- [x] 7. Crear `helpContent.tsx` (categorias, productos, ingredientes)
- [x] 8. Crear `HelpButton` componente
- [x] 9. Crear `PageContainer` componente

### API Clients
- [x] 10. Crear `ingredientesApi.ts`

### CRUD Pages
- [x] 11. Crear `CategoriesAdminPage` (list + create + edit + delete)
- [x] 12. Crear `IngredientesAdminPage` (list + create + edit + delete, badge alérgeno)
- [x] 13. Crear `ProductsAdminPage` (list + create + edit + delete, precio/stock/categoría)

### Routing
- [x] 14. Agregar rama `/admin` en router con `AdminLayout` + rutas hijas
- [x] 15. Redirects en `useLogin.ts` para roles admin/gestor

### Auth
- [x] 16. Agregar campo `phone` a `UserCreate` (backend)
- [x] 17. Persistir `phone` en `auth/service.py`
- [x] 18. Agregar campo `phone` a `RegisterPayload` (frontend)
- [x] 19. Agregar input de teléfono en `RegisterPage`
