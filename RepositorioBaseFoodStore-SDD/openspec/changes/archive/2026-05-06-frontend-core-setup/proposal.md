# Proposal: frontend-core-setup

## Intent
Establecer la infraestructura core del frontend utilizando un stack moderno y escalable, siguiendo la arquitectura Feature-Sliced Design (FSD).

## Scope
- **Scaffolding**: Configuración de Vite con React y TypeScript en modo estricto.
- **Routing**: Implementación de React Router DOM para la navegación SPA.
- **State Management**: 
  - Zustand para estado global del cliente (Auth, UI, Carrito).
  - TanStack Query para el manejo de estado del servidor y caché.
- **Styling**: Configuración de Tailwind CSS con un sistema de diseño base.
- **HTTP Client**: Configuración de Axios con interceptores para manejo de JWT.
- **Architecture**: Creación de las capas FSD (`app`, `pages`, `widgets`, `features`, `entities`, `shared`).

## Capabilities
### New Capabilities
- `frontend-infrastructure`: Provee el esqueleto base y las herramientas core para el desarrollo del frontend.

## Technical Approach
Se utilizará FSD para organizar el código por capas de responsabilidad. `TanStack Query` se configurará globalmente en el layer `app` mediante un `QueryClientProvider`. Los stores de `Zustand` se ubicarán en los layers correspondientes (ej. `authStore` en `entities/auth`).

## Risks
- Curva de aprendizaje de FSD si el equipo no está familiarizado.
- Complejidad inicial en la configuración de interceptores de Axios para refresh tokens.

## Rollback Plan
- Eliminar la carpeta `frontend/src` y revertir el `package.json` a su estado inicial.
