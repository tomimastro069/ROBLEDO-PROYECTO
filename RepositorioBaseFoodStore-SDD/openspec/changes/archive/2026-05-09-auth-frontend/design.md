# Design: auth-frontend

## Technical Approach

Implementar la capa `features/auth` siguiendo FSD. La feature expone únicamente los hooks (`useLogin`, `useRegister`) y el API layer (`authApi`). Las páginas y el store son capas superiores/inferiores — no se cruzan entre sí.

## Architecture Decisions

### Decision: features/auth como feature slice

**Choice**: `features/auth/api/` + `features/auth/hooks/`
**Alternatives considered**: Hooks directamente en `pages/login`
**Rationale**: FSD prohíbe que `pages` tenga lógica de negocio. La feature encapsula el "cómo" de auth; la página solo maneja el "qué mostrar".

### Decision: Encadenar login → me() en useLogin

**Choice**: Tras el login, llamar `/auth/me` para hidratar el store con los datos del usuario
**Alternatives considered**: Decodificar el JWT en el cliente
**Rationale**: El backend es la fuente de verdad. Decodificar JWTs en el cliente es frágil ante cambios de payload. El endpoint `/me` ya existe y es seguro.

### Decision: No auto-refresh en este change

**Choice**: El refresh automático de tokens queda fuera de scope
**Rationale**: El interceptor de Axios ya limpia el store en 401. El refresh automático requiere lógica de retry y se implementará en un change dedicado.

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `src/features/auth/api/authApi.ts` | Create | Contrato tipado con el backend |
| `src/features/auth/hooks/useLogin.ts` | Create | Mutation login + hidratación del store |
| `src/features/auth/hooks/useRegister.ts` | Create | Mutation register |
| `src/entities/auth/model/authStore.ts` | Modify | Agrega `refreshToken`, limpia `localStorage` manual |
| `src/pages/login/ui/LoginPage.tsx` | Modify | Conecta con `useLogin`, muestra error y loading |

## Interfaces / Contracts

```typescript
// features/auth/api/authApi.ts
interface LoginPayload { email: string; password: string; }
interface TokenResponse { access_token: string; refresh_token: string; token_type: 'bearer'; }

// features/auth/hooks/useLogin.ts — returns useMutation result
// features/auth/hooks/useRegister.ts — returns useMutation result

// entities/auth/model/authStore.ts
interface AuthState {
  user: User | null;
  token: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  setAuth: (user: User, token: string, refreshToken: string) => void;
  clearAuth: () => void;
}
```
