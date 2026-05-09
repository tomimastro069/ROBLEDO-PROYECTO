# Proposal: auth-frontend

## Problem Statement

El frontend tiene la estructura base de auth (store, ProtectedRoute, LoginPage) pero sin conexión real al backend. `LoginPage` tiene un `console.log` como placeholder y `authStore` no persiste el `refresh_token`.

## Proposed Solution

Implementar la capa de features de autenticación en FSD:
- `features/auth/api/authApi.ts` — contrato tipado con los endpoints del backend
- `features/auth/hooks/useLogin.ts` — mutation con TanStack Query
- `features/auth/hooks/useRegister.ts` — mutation con TanStack Query
- Actualizar `authStore` para incluir `refreshToken`
- Conectar `LoginPage` con los hooks reales

## Scope

- **In**: API layer, hooks de login/register, actualización del store, LoginPage funcional
- **Out**: RegisterPage (no está en scope de este change), refresh automático de tokens (futuro)

## Dependencies

- `frontend-core-setup` [X] — Zustand, TanStack Query, Axios, FSD structure
- `auth-api` [X] — Contratos HTTP definidos y archivados
