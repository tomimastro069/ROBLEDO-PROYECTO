# Proposal — admin-dashboard-crud

## Intent

Construir un panel de administración dedicado (`/admin`) con sidebar propio, separado del catálogo público de clientes. El panel expone las páginas de gestión CRUD de Categorías, Ingredientes y Productos, más el panel de Pedidos ya existente, todo bajo un layout exclusivo protegido por rol.

## Scope

### In scope
- `AdminLayout` con sidebar de navegación lateral (rutas `/admin/*`)
- Hooks reutilizables base: `useFormModal`, `useConfirmDialog`, `usePagination`
- Tipos compartidos: `FormState<T>`
- Utilidades: `logger.ts`, `helpContent.tsx`
- Componentes UI compartidos: `HelpButton`, `PageContainer`
- Página CRUD Categorías (`/admin/categorias`)
- Página CRUD Ingredientes (`/admin/ingredientes`)
- Página CRUD Productos (`/admin/productos`) con paginación y relación a categoría
- Redirección post-login al `/admin` para roles `admin`, `gestor_stock`, `gestor_pedidos`
- Campo `phone` en registro de usuario (backend schema + frontend form)

### Out of scope
- Métricas/gráficos (us-007-admin)
- Gestión de usuarios desde el panel admin
- Upload de imágenes de productos

## Approach

Skill `dashboard-crud-page` como contrato de diseño. Todos los CRUDs usan el hook trio `useFormModal + useConfirmDialog + usePagination`, TanStack Query para cache/mutaciones, y el mismo patrón de modal + tabla + confirm dialog. No se usó `useActionState` real (React 18 en el proyecto) sino un polyfill propio.

## Dependencies

- `us-001-auth` — requiere sesión y roles resueltos
- `us-002-categorias`, `us-003-productos` — los endpoints CRUD del backend deben estar operativos (confirmado ✅)
