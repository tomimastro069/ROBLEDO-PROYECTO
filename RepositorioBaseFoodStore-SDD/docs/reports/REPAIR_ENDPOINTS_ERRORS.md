# Reporte Técnico de Estabilización — FoodStore Backend
**Fecha**: 12 de Mayo de 2026
**Responsable**: Antigravity (AI Architect)

## 1. Resumen Ejecutivo
Durante la sesión de desarrollo, se identificaron y resolvieron múltiples bloqueadores técnicos que afectaban la integridad del sistema de autenticación, la gestión de inventario y el flujo de pedidos. Se logró estabilizar el backend mediante la implementación del patrón **Unit of Work** y la normalización de esquemas.

---

## 2. Errores Críticos Encontrados y Soluciones

### ❌ E01: Conflicto de Versiones en Bcrypt/Passlib
- **Problema**: El servidor crasheaba al intentar hashear passwords debido a que `bcrypt` 4.x cambió su API interna y `passlib` no lo soportaba.
- **Error**: `AttributeError: module 'bcrypt' has no attribute '__about__'`
- **Solución**: Se fijó la versión de `bcrypt==3.2.0` en el `requirements.txt`.

### ❌ E02: Fallo de Validación JWT (Claves Inconsistentes)
- **Problema**: Los tokens generados eran rechazados con error 401 porque el servicio de login usaba una clave secreta distinta a la del middleware de autenticación.
- **Error**: `401 Unauthorized - No autenticado o token inválido.`
- **Solución**: Se centralizó la configuración en un objeto `settings` único para todo el sistema.

### ❌ E03: Discrepancia de Case-Sensitivity en Roles
- **Problema**: El seeder creaba roles como `"Admin"`, pero el código esperaba `"admin"`. Al intentar validar el rol del token, el Enum de Python fallaba.
- **Solución**: Se normalizaron todos los roles a minúsculas en el Enum, en el Seeder y se aplicó un parche de normalización en la base de datos existente.

### ❌ E04: Método Faltante en Repositorio de Ingredientes
- **Problema**: El servicio de productos intentaba filtrar ingredientes usando un método no implementado en la capa de persistencia.
- **Error**: `AttributeError: 'IngredienteRepository' object has no attribute 'get_por_producto'`
- **Solución**: Se implementó `get_por_producto` en `IngredienteRepository` realizando el `join` con la tabla intermedia `ProductIngrediente`.

### ❌ E05: Desincronización Modelo/Esquema en Órdenes
- **Problema**: La API fallaba con error 500 al listar órdenes porque el modelo de base de datos usaba el campo `price`, mientras que el esquema de respuesta exigía `price_snapshot`.
- **Error**: `fastapi.exceptions.ResponseValidationError: Field required: 'price_snapshot'`
- **Solución**: Se renombró el campo en el modelo `OrderItem` para que coincida con el concepto de "snapshot" histórico de precios.

### ❌ E06: Error de Conexión en Inicialización (Docker)
- **Problema**: Al borrar volúmenes, el backend intentaba conectarse antes de que Postgres terminara su proceso de arranque inicial.
- **Error**: `psycopg2.OperationalError: connection to server at "db" failed: Connection refused`
- **Solución**: Se agregó un bucle de reintento con `time.sleep` en el método `init_db()` para esperar a la base de datos de forma resiliente.

---

## 3. Mejoras de Arquitectura Implementadas
1. **Unificación de Ingredientes/Alérgenos**: Se eliminaron los endpoints redundantes en `/products` para centralizar todo en `/ingredientes`, usando un flag `es_alergeno` para mayor simplicidad.
2. **Patrón Unit of Work (UoW)**: Se refactorizó `OrderService` para usar `AppUnitOfWork`, permitiendo que la creación de pedidos sea atómica (descuenta stock, valida dirección y calcula precios en una sola transacción).
3. **Seeder Enriquecido**: El sistema ahora inicia con una base de datos completa con usuarios, direcciones, categorías, productos con ingredientes vinculados y órdenes de prueba.

---
**Estado Final**: El sistema se encuentra 100% operacional y verificado mediante tests integrales.
