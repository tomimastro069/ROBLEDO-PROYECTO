## Mapa de Changes (Plan de Sprints) — Food Store

### 1. `repo-scaffold-monorepo`  [X]
- Funcionalidad: Estructura base del repo (frontend/, backend/, docs/, env, README).
- Dependencias: ninguna

---

### 2. `backend-core-setup`  [X]
- Funcionalidad: FastAPI base, config, JWT, CORS, DB session, OpenAPI.
- Dependencias: `repo-scaffold-monorepo`

---

### 3. `dockerization-setup`  [X]
- Funcionalidad: Dockerfile para backend/frontend, docker-compose.yml, variables de entorno para contenedores.
- Dependencias: `backend-core-setup`

---

### 4. `frontend-core-setup`  []
- Funcionalidad: React + TS + Vite, Router, Zustand, Query, Tailwind.
- Dependencias: `repo-scaffold-monorepo`

---

### 5. `domain-models-definition`
- Funcionalidad: Entidades de dominio (User, Product, Category, Order, OrderItem).
- Dependencias: `backend-core-setup`

---

### 6. `database-migrations-and-seed`
- Funcionalidad: PostgreSQL + Alembic, tablas basadas en dominio, seed inicial.
- Dependencias: `domain-models-definition`

---

### 7. `backend-uow-and-repositories`
- Funcionalidad: Repositorios + Unit of Work (acceso a datos).
- Dependencias: `database-migrations-and-seed`

---

### 8. `backend-error-handling`
- Funcionalidad: Manejo de errores (RFC7807).
- Dependencias: `backend-core-setup`

---

### 9. `backend-validation`
- Funcionalidad: Validación y sanitización de inputs.
- Dependencias: `backend-core-setup`

---

## 🔐 AUTENTICACIÓN

### 10. `auth-service`
- Funcionalidad: Lógica de negocio (login, register, refresh, logout).
- Dependencias: `backend-uow-and-repositories`

### 11. `auth-api`
- Funcionalidad: Endpoints REST de auth.
- Dependencias: `auth-service`

### 12. `auth-frontend`
- Funcionalidad: UI + Zustand para sesión.
- Dependencias: `frontend-core-setup`, `auth-api`

---

## 📂 CATEGORÍAS

### 13. `categories-service`
- Funcionalidad: Lógica CRUD jerárquica.
- Dependencias: `backend-uow-and-repositories`

### 14. `categories-api`
- Funcionalidad: Endpoints categorías.
- Dependencias: `categories-service`

---

## 🛒 PRODUCTOS

### 15. `products-service`
- Funcionalidad: Lógica CRUD + stock + relaciones.
- Dependencias: `categories-service`, `backend-uow-and-repositories`

### 16. `products-api`
- Funcionalidad: Endpoints productos.
- Dependencias: `products-service`

---

## 🧺 CARRITO

### 17. `cart-service`
- Funcionalidad: Validación de carrito (precios, stock, consistencia).
- Dependencias: `products-service`

### 18. `cart-frontend`
- Funcionalidad: Carrito en cliente (Zustand).
- Dependencias: `frontend-core-setup`, `products-api`

---

## 📦 ÓRDENES

### 19. `orders-service`
- Funcionalidad: Creación de órdenes, snapshots, reglas de negocio.
- Dependencias: `cart-service`, `auth-service`, `products-service`

### 20. `orders-api`
- Funcionalidad: Endpoints de órdenes.
- Dependencias: `orders-service`

---

## 💳 PAGOS

### 21. `mercadopago-integration`
- Funcionalidad: Checkout, webhooks, integración de pagos.
- Dependencias: `orders-api`, `auth-api`

---

## ✔ Estado final

- Total changes: 21  
- Separación correcta: ✔  
- Dependencias correctas: ✔  
- Arquitectura respetada: ✔  