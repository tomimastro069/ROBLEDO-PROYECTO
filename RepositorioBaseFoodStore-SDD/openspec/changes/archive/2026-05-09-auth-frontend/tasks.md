# Tasks: auth-frontend

## Implementation Checklist

- [x] Crear `src/features/auth/api/authApi.ts` con tipos y llamadas a `/auth/login`, `/auth/register`, `/auth/refresh`, `/auth/me`
- [x] Crear `src/features/auth/hooks/useLogin.ts` con useMutation + encadenamiento a `/auth/me`
- [x] Crear `src/features/auth/hooks/useRegister.ts` con useMutation
- [x] Actualizar `src/entities/auth/model/authStore.ts` — agregar `refreshToken`, remover `localStorage.setItem` manual
- [x] Actualizar `src/pages/login/ui/LoginPage.tsx` — conectar con `useLogin`, mostrar error y estado loading, usar `<Navigate>` declarativo

## Out of Scope

- [ ] RegisterPage (nuevo change)
- [ ] Refresh automático de tokens (nuevo change)
- [ ] Interceptor de retry en 401 con refresh (nuevo change)
