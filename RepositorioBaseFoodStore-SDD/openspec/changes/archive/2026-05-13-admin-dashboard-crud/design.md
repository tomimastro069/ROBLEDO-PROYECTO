# Design — admin-dashboard-crud

## Architecture

### Routing
- Nueva rama `/admin` con `AdminLayout` (sidebar fijo, área de contenido a la derecha)
- `ProtectedRoute` wrapping `AdminLayout` con roles `['admin', 'gestor_pedidos', 'gestor_stock']`
- Rutas hijas: `categorias`, `ingredientes`, `productos`, `pedidos`

### Layout (AdminLayout)
- Sidebar fijo de 256px con `NavLink` por sección
- Links dinámicos por rol: pedidos (admin/gestor_pedidos), catálogo (admin/gestor_stock)
- Volver a tienda + Cerrar sesión en footer del sidebar

### Shared Foundation (src/shared/)
```
hooks/
  useFormModal.ts       — estado de modal + form data + selectedItem
  useConfirmDialog.ts   — estado de dialog de confirmación de borrado
  usePagination.ts      — paginación local de arrays
  useActionState.ts     — polyfill React 18 para useActionState de React 19
types/
  form.ts               — FormState<T>
utils/
  logger.ts             — handleError, logWarning
  helpContent.tsx       — registro centralizado de textos de ayuda
ui/
  HelpButton.tsx        — botón de ayuda con modal
  PageContainer.tsx     — wrapper de página con title, description, helpContent, actions
```

### CRUD Pages Pattern
Cada página sigue el mismo patrón:
1. `useQuery` para listar datos
2. `useFormModal` + `useConfirmDialog` para estado de UI
3. `useMutation` (create, update, delete) con `invalidateQueries` on success
4. Tabla con esqueleto de carga
5. Modal con `HelpButton` como primer elemento
6. Dialog de confirmación de borrado

### Auth Changes
- `useLogin.ts`: redirige a `/admin` si el rol es `admin`, `gestor_pedidos` o `gestor_stock`
- `RegisterPage.tsx`: agrega campo `phone` opcional
- `auth/schemas.py` (backend): `UserCreate` incluye `phone`
- `auth/service.py` (backend): persiste `phone` al crear usuario

## Files Created/Modified

| Archivo | Acción |
|---|---|
| `src/app/layout/AdminLayout.tsx` | Nuevo |
| `src/shared/hooks/useFormModal.ts` | Nuevo |
| `src/shared/hooks/useConfirmDialog.ts` | Nuevo |
| `src/shared/hooks/usePagination.ts` | Nuevo |
| `src/shared/hooks/useActionState.ts` | Nuevo |
| `src/shared/types/form.ts` | Nuevo |
| `src/shared/utils/logger.ts` | Nuevo |
| `src/shared/utils/helpContent.tsx` | Nuevo |
| `src/shared/ui/HelpButton.tsx` | Nuevo |
| `src/shared/ui/PageContainer.tsx` | Nuevo |
| `src/shared/api/ingredientesApi.ts` | Nuevo |
| `src/pages/admin/categories/ui/CategoriesAdminPage.tsx` | Nuevo |
| `src/pages/admin/ingredientes/ui/IngredientesAdminPage.tsx` | Nuevo |
| `src/pages/admin/products/ui/ProductsAdminPage.tsx` | Nuevo |
| `src/app/router.tsx` | Modificado — rama /admin |
| `src/features/auth/hooks/useLogin.ts` | Modificado — redirect por rol |
| `src/pages/register/ui/RegisterPage.tsx` | Modificado — campo phone |
| `src/features/auth/api/authApi.ts` | Modificado — phone en RegisterPayload |
| `backend/auth/schemas.py` | Modificado — phone en UserCreate |
| `backend/auth/service.py` | Modificado — phone al crear usuario |
