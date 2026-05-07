## 1. Base Configuration

- [x] 1.1 Verify SQLModel and Alembic installation in the backend environment.
- [x] 1.2 Create `Base` SQLModel class and common database connection utilities if they don't exist.

## 2. Models Implementation (Auth & Users)

- [x] 2.1 Create `Role` model (id, name, description).
- [x] 2.2 Create `User` model (id, email, hashed_password, role_id) with foreign key to Role.

## 3. Models Implementation (Catalog)

- [x] 3.1 Create `Category` model with self-referential `parent_id`.
- [x] 3.2 Create `Product` model with basic fields (name, description, price, stock, category_id).
- [x] 3.3 Create `ProductIngredient` and `ProductAllergen` tables and establish relationships with Product.

## 4. Models Implementation (Orders & Payments)

- [x] 4.1 Create `Order` model with an Enum for FSM status (PENDING, PAID, PREPARING, SHIPPED, DELIVERED).
- [x] 4.2 Create `OrderItem` association model linking `Order` and `Product` (includes quantity and historical price).
- [x] 4.3 Create `Payment` and `Address` models linked to `User` and `Order`.

## 5. Database Migrations

- [x] 5.1 Initialize or update Alembic configuration to load all new models into `target_metadata`.
- [x] 5.2 Generate the initial Alembic migration script for all domain models.
- [x] 5.3 Apply the migration to the PostgreSQL database and verify the schema.
