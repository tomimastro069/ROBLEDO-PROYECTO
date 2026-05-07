## 1. Scaffolding y configuración base

- [x] 1.1 Bootstrap con Vite + React + TypeScript strict
- [x] 1.2 Configurar aliases de paths en `vite.config.ts` (FSD layers)
- [x] 1.3 Configurar `tsconfig.json` con paths estrictos
- [x] 1.4 Configurar Tailwind CSS + PostCSS

## 2. Arquitectura FSD — Estructura de capas

- [x] 2.1 Crear capa `app/` (providers, router)
- [x] 2.2 Crear capa `pages/` con páginas base (Home, Login, NotFound)
- [x] 2.3 Crear capa `widgets/` (placeholder inicial)
- [x] 2.4 Crear capa `features/` (placeholder inicial)
- [x] 2.5 Crear capa `entities/` (auth, cart, payment)
- [x] 2.6 Crear capa `shared/` (api, model, ui)

## 3. State Management

- [x] 3.1 Configurar TanStack Query (`QueryClientProvider` en `app/providers.tsx`)
- [x] 3.2 Agregar `ReactQueryDevtools` al provider
- [x] 3.3 Implementar `authStore` con Zustand
- [x] 3.4 Implementar `cartStore` con Zustand
- [x] 3.5 Implementar `paymentStore` con Zustand
- [x] 3.6 Implementar `uiStore` con Zustand

## 4. HTTP Client

- [x] 4.1 Crear instancia de Axios en `shared/api/axios.ts`
- [x] 4.2 Interceptor de request: inyección de JWT desde `authStore`
- [x] 4.3 Interceptor de response: manejo de 401 y limpieza de auth

## 5. Routing y Guards

- [x] 5.1 Configurar React Router con `createBrowserRouter`
- [x] 5.2 Implementar `ProtectedRoute` HOC con RBAC por rol
- [x] 5.3 Definir rutas base: `/`, `/login`, `/unauthorized`

## 6. App Shell

- [x] 6.1 Conectar `Providers` + `AppRouter` en `App.tsx`
- [x] 6.2 Verificar `main.tsx` monta correctamente con `Providers`
- [x] 6.3 Confirmar que el dev server levanta sin errores (`npm run dev`)
