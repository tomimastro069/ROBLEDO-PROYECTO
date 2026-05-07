# Design: frontend-core-setup

## Technical Approach

Utilizar Feature-Sliced Design (FSD) como arquitectura de capas, con Vite como bundler, React 18 + TypeScript strict como base, y una separación clara entre estado del servidor (TanStack Query) y estado del cliente (Zustand).

## Architecture Decisions

### Decision: Feature-Sliced Design

**Choice**: FSD con 6 capas: `app`, `pages`, `widgets`, `features`, `entities`, `shared`
**Alternatives considered**: Arquitectura por tipo (components/hooks/services), modular flat
**Rationale**: FSD escala mejor en e-commerce con múltiples dominios (auth, productos, carrito, pedidos). Importaciones unidireccionales evitan dependencias circulares.

### Decision: TanStack Query + Zustand (sin Redux)

**Choice**: TanStack Query para server state, Zustand para client state
**Alternatives considered**: Redux Toolkit, Context API, Jotai
**Rationale**: TanStack Query elimina el boilerplate de loading/error/cache para requests. Zustand es minimalista y evita el over-engineering de Redux para un estado de cliente relativamente simple.

### Decision: Axios con interceptores (no fetch nativo)

**Choice**: Axios con instancia singleton en `shared/api`
**Alternatives considered**: fetch nativo, ky, wretch
**Rationale**: Interceptores de Axios simplifican la inyección del JWT en request y el manejo de 401 en response sin duplicar código.

## Data Flow

```
[Componente] → useQuery/useMutation → [TanStack Query]
                                            │
                                     axiosInstance (shared/api)
                                            │
                                     [FastAPI Backend]

[Componente] → useAuthStore() → [Zustand Store] ← interceptor de Axios
```

## File Changes

| Archivo | Acción | Descripción |
|---------|--------|-------------|
| `src/app/providers.tsx` | Existente | QueryClientProvider + ReactQueryDevtools |
| `src/app/router.tsx` | Completar | Rutas base con ProtectedRoute |
| `src/entities/auth/model/authStore.ts` | Existente | Store de auth con Zustand |
| `src/entities/cart/model/cartStore.ts` | Existente | Store del carrito |
| `src/entities/payment/model/paymentStore.ts` | Existente | Store de pagos |
| `src/shared/model/uiStore.ts` | Existente | Store de UI global |
| `src/shared/api/axios.ts` | Existente | Axios + interceptores JWT |
| `src/shared/ui/ProtectedRoute.tsx` | Existente | HOC con RBAC por rol |
| `src/pages/` | Crear | Directorio con páginas base (Home, Login) |
| `src/widgets/` | Crear | Directorio para componentes compostos |
| `src/App.tsx` | Modificar | Conectar Providers + AppRouter |
| `src/main.tsx` | Verificar | Entry point con Providers wrapping |

## Interfaces / Contracts

```typescript
// entities/auth/model/authStore.ts
interface AuthState {
  token: string | null;
  user: { id: string; role: string } | null;
  isAuthenticated: boolean;
  clearAuth: () => void;
}

// shared/ui/ProtectedRoute.tsx
interface ProtectedRouteProps {
  children: ReactNode;
  allowedRoles?: string[];
}
```

## Testing Strategy

| Layer | Qué testear | Approach |
|-------|-------------|----------|
| Unit | Stores de Zustand | Vitest — mutaciones de estado directas |
| Unit | ProtectedRoute | Vitest + React Testing Library |
| Integration | Interceptores Axios | Mock de servidor con msw (futuro) |
| E2E | Flujo de auth completo | Playwright (futuro) |

## Migration / Rollout

No migration requerida. Cambio es puramente de frontend. Se puede desplegar de forma independiente al backend.

## Open Questions

- [ ] ¿Recharts va en `shared/ui` o en un widget específico de admin?
- [ ] ¿El `AppRouter` debe manejar rutas de admin desde el inicio o se agrega al implementar el módulo admin?
