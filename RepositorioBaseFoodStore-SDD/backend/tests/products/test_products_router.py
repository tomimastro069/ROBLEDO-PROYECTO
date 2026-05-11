"""
Integration tests for Products API router — TDD (red phase first).

Covers all scenarios from openspec/changes/products-api/specs/product-api/spec.md
"""

import pytest
from decimal import Decimal
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool

from main import app
from app.core.uow.unit_of_work import AppUnitOfWork, get_uow
from app.core.models import Category, Product, ProductIngredient, ProductAllergen
from auth.dependencies import get_current_user
from auth.schemas import TokenData
from auth.roles import Role


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture(name="engine")
def engine_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture(name="session")
def session_fixture(engine):
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(engine):
    def get_uow_override():
        return AppUnitOfWork(engine=engine)

    app.dependency_overrides[get_uow] = get_uow_override
    client = TestClient(app, raise_server_exceptions=True)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="admin_token")
def admin_token_fixture():
    return TokenData(sub="1", role=Role.ADMIN, email="admin@test.com")


@pytest.fixture(name="gestor_stock_token")
def gestor_stock_token_fixture():
    return TokenData(sub="2", role=Role.GESTOR_STOCK, email="stock@test.com")


@pytest.fixture(name="cliente_token")
def cliente_token_fixture():
    return TokenData(sub="3", role=Role.CLIENTE, email="cliente@test.com")


@pytest.fixture(name="gestor_pedidos_token")
def gestor_pedidos_token_fixture():
    return TokenData(sub="4", role=Role.GESTOR_PEDIDOS, email="pedidos@test.com")


@pytest.fixture(name="test_category")
def test_category_fixture(session: Session):
    category = Category(name="Verduras", description="Productos frescos")
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@pytest.fixture(name="test_product")
def test_product_fixture(session: Session, test_category: Category):
    product = Product(
        name="Tomate",
        description="Tomate fresco",
        price=Decimal("2.50"),
        stock=50,
        category_id=test_category.id,
    )
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


@pytest.fixture(name="deleted_product")
def deleted_product_fixture(session: Session, test_category: Category):
    from datetime import datetime
    product = Product(
        name="Producto eliminado",
        description="Soft deleted",
        price=Decimal("1.00"),
        stock=0,
        category_id=test_category.id,
        deleted_at=datetime.now(),
    )
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


# ============================================================================
# Tests: GET /products (listado paginado)
# ============================================================================

class TestListProducts:

    def test_list_products_empty(self, client: TestClient):
        response = client.get("/products")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert data["items"] == []
        assert data["total"] == 0

    def test_list_products_returns_products(self, client: TestClient, test_product: Product):
        response = client.get("/products")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert len(data["items"]) == 1
        assert data["items"][0]["name"] == "Tomate"

    def test_list_products_pagination(self, client: TestClient, session: Session, test_category: Category):
        for i in range(5):
            session.add(Product(name=f"Producto {i}", price=Decimal("1.00"), stock=10, category_id=test_category.id))
        session.commit()

        response = client.get("/products?skip=2&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 5

    def test_list_products_filter_by_category(self, client: TestClient, test_product: Product, test_category: Category, session: Session):
        other_cat = Category(name="Carnes")
        session.add(other_cat)
        session.commit()
        session.refresh(other_cat)
        session.add(Product(name="Pollo", price=Decimal("5.00"), stock=10, category_id=other_cat.id))
        session.commit()

        response = client.get(f"/products?category_id={test_category.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["name"] == "Tomate"

    def test_list_products_search_by_name(self, client: TestClient, test_product: Product):
        response = client.get("/products?search=tomate")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["name"] == "Tomate"

    def test_list_products_empty_category(self, client: TestClient):
        response = client.get("/products?category_id=999")
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0

    def test_list_excludes_soft_deleted(self, client: TestClient, test_product: Product, deleted_product: Product):
        response = client.get("/products")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["name"] == "Tomate"


# ============================================================================
# Tests: GET /products/{id}
# ============================================================================

class TestGetProductById:

    def test_get_product_found(self, client: TestClient, test_product: Product):
        response = client.get(f"/products/{test_product.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_product.id
        assert data["name"] == "Tomate"
        assert "ingredients" in data
        assert "allergens" in data

    def test_get_product_not_found(self, client: TestClient):
        response = client.get("/products/9999")
        assert response.status_code == 404

    def test_get_soft_deleted_product_returns_404(self, client: TestClient, deleted_product: Product):
        response = client.get(f"/products/{deleted_product.id}")
        assert response.status_code == 404


# ============================================================================
# Tests: POST /products (crear producto)
# ============================================================================

class TestCreateProduct:

    def test_create_product_as_admin(self, client: TestClient, admin_token: TokenData, test_category: Category):
        app.dependency_overrides[get_current_user] = lambda: admin_token
        payload = {
            "name": "Lechuga",
            "description": "Lechuga fresca",
            "price": "1.50",
            "stock": 100,
            "category_id": test_category.id,
        }
        response = client.post("/products", json=payload)
        app.dependency_overrides.pop(get_current_user, None)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Lechuga"
        assert "id" in data

    def test_create_product_as_gestor_stock(self, client: TestClient, gestor_stock_token: TokenData, test_category: Category):
        app.dependency_overrides[get_current_user] = lambda: gestor_stock_token
        payload = {"name": "Zanahoria", "price": "0.80", "stock": 200, "category_id": test_category.id}
        response = client.post("/products", json=payload)
        app.dependency_overrides.pop(get_current_user, None)
        assert response.status_code == 201

    def test_create_product_no_auth(self, client: TestClient, test_category: Category):
        payload = {"name": "Berenjena", "price": "2.00", "stock": 30, "category_id": test_category.id}
        response = client.post("/products", json=payload)
        assert response.status_code == 401

    def test_create_product_as_cliente_forbidden(self, client: TestClient, cliente_token: TokenData, test_category: Category):
        app.dependency_overrides[get_current_user] = lambda: cliente_token
        payload = {"name": "Berenjena", "price": "2.00", "stock": 30, "category_id": test_category.id}
        response = client.post("/products", json=payload)
        app.dependency_overrides.pop(get_current_user, None)
        assert response.status_code == 403

    def test_create_product_invalid_payload(self, client: TestClient, admin_token: TokenData):
        app.dependency_overrides[get_current_user] = lambda: admin_token
        payload = {"name": "X", "price": -5, "stock": 10}
        response = client.post("/products", json=payload)
        app.dependency_overrides.pop(get_current_user, None)
        assert response.status_code == 422


# ============================================================================
# Tests: PUT /products/{id} (actualizar producto)
# ============================================================================

class TestUpdateProduct:

    def test_update_product_as_gestor_stock(self, client: TestClient, gestor_stock_token: TokenData, test_product: Product):
        app.dependency_overrides[get_current_user] = lambda: gestor_stock_token
        payload = {"price": "3.99"}
        response = client.put(f"/products/{test_product.id}", json=payload)
        app.dependency_overrides.pop(get_current_user, None)
        assert response.status_code == 200
        assert Decimal(response.json()["price"]) == Decimal("3.99")

    def test_update_product_not_found(self, client: TestClient, admin_token: TokenData):
        app.dependency_overrides[get_current_user] = lambda: admin_token
        response = client.put("/products/9999", json={"name": "X"})
        app.dependency_overrides.pop(get_current_user, None)
        assert response.status_code == 404

    def test_update_product_as_cliente_forbidden(self, client: TestClient, cliente_token: TokenData, test_product: Product):
        app.dependency_overrides[get_current_user] = lambda: cliente_token
        response = client.put(f"/products/{test_product.id}", json={"name": "X"})
        app.dependency_overrides.pop(get_current_user, None)
        assert response.status_code == 403


# ============================================================================
# Tests: DELETE /products/{id} (soft-delete)
# ============================================================================

class TestDeleteProduct:

    def test_delete_product_as_admin(self, client: TestClient, admin_token: TokenData, test_product: Product, session: Session):
        app.dependency_overrides[get_current_user] = lambda: admin_token
        response = client.delete(f"/products/{test_product.id}")
        app.dependency_overrides.pop(get_current_user, None)
        assert response.status_code == 204

        # Verificar soft-delete en DB
        session.expire_all()
        from sqlmodel import select
        stmt = select(Product).where(Product.id == test_product.id)
        product_in_db = session.exec(stmt).first()
        assert product_in_db is not None
        assert product_in_db.deleted_at is not None

    def test_delete_product_not_found(self, client: TestClient, admin_token: TokenData):
        app.dependency_overrides[get_current_user] = lambda: admin_token
        response = client.delete("/products/9999")
        app.dependency_overrides.pop(get_current_user, None)
        assert response.status_code == 404

    def test_delete_product_as_gestor_pedidos_forbidden(self, client: TestClient, gestor_pedidos_token: TokenData, test_product: Product):
        app.dependency_overrides[get_current_user] = lambda: gestor_pedidos_token
        response = client.delete(f"/products/{test_product.id}")
        app.dependency_overrides.pop(get_current_user, None)
        assert response.status_code == 403


# ============================================================================
# Tests: /products/{id}/ingredients
# ============================================================================

class TestProductIngredients:

    def test_list_ingredients_public(self, client: TestClient, test_product: Product, session: Session):
        session.add(ProductIngredient(product_id=test_product.id, name="Agua"))
        session.commit()
        response = client.get(f"/products/{test_product.id}/ingredients")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Agua"

    def test_add_ingredient_as_admin(self, client: TestClient, admin_token: TokenData, test_product: Product):
        app.dependency_overrides[get_current_user] = lambda: admin_token
        response = client.post(f"/products/{test_product.id}/ingredients", json={"name": "Sal"})
        app.dependency_overrides.pop(get_current_user, None)
        assert response.status_code == 201
        assert response.json()["name"] == "Sal"

    def test_delete_ingredient_as_gestor_stock(self, client: TestClient, gestor_stock_token: TokenData, test_product: Product, session: Session):
        ing = ProductIngredient(product_id=test_product.id, name="Azucar")
        session.add(ing)
        session.commit()
        session.refresh(ing)

        app.dependency_overrides[get_current_user] = lambda: gestor_stock_token
        response = client.delete(f"/products/{test_product.id}/ingredients/{ing.id}")
        app.dependency_overrides.pop(get_current_user, None)
        assert response.status_code == 204

    def test_add_ingredient_product_not_found(self, client: TestClient, admin_token: TokenData):
        app.dependency_overrides[get_current_user] = lambda: admin_token
        response = client.post("/products/9999/ingredients", json={"name": "Sal"})
        app.dependency_overrides.pop(get_current_user, None)
        assert response.status_code == 404


# ============================================================================
# Tests: /products/{id}/allergens
# ============================================================================

class TestProductAllergens:

    def test_list_allergens_public(self, client: TestClient, test_product: Product, session: Session):
        session.add(ProductAllergen(product_id=test_product.id, name="Gluten"))
        session.commit()
        response = client.get(f"/products/{test_product.id}/allergens")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Gluten"

    def test_add_allergen_as_admin(self, client: TestClient, admin_token: TokenData, test_product: Product):
        app.dependency_overrides[get_current_user] = lambda: admin_token
        response = client.post(f"/products/{test_product.id}/allergens", json={"name": "Lactosa"})
        app.dependency_overrides.pop(get_current_user, None)
        assert response.status_code == 201
        assert response.json()["name"] == "Lactosa"

    def test_delete_allergen_as_gestor_stock(self, client: TestClient, gestor_stock_token: TokenData, test_product: Product, session: Session):
        alg = ProductAllergen(product_id=test_product.id, name="Maní")
        session.add(alg)
        session.commit()
        session.refresh(alg)

        app.dependency_overrides[get_current_user] = lambda: gestor_stock_token
        response = client.delete(f"/products/{test_product.id}/allergens/{alg.id}")
        app.dependency_overrides.pop(get_current_user, None)
        assert response.status_code == 204
