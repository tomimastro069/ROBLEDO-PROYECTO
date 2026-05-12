"""
Integration Tests for Categories API

Este archivo contiene tests de integración para validar que los endpoints
de categorías funcionan correctamente, respetando RBAC y reglas de negocio.

Para ejecutar:
  pytest backend/tests/api/test_categories_integration.py -v

Nota: Requiere que las dependencias estén instaladas (pytest, fastapi, sqlmodel, etc.)
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool

# Imports del proyecto
from main import app
from app.core.uow.unit_of_work import AppUnitOfWork, get_uow
from auth.schemas import TokenData
from auth.roles import Role
from auth.dependencies import get_current_user
from app.core.models import Category


# ============================================================================
# Fixtures: Database & Client Setup
# ============================================================================

@pytest.fixture(name="session")
def session_fixture():
    """Crea una sesión de BD en memoria para testing."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Crea un TestClient con la BD de testing."""
    
    def get_session_override():
        return session

    app.dependency_overrides[Session] = get_session_override
    
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="admin_token")
def admin_token_fixture():
    """Crea un TokenData simulado para usuario Admin."""
    return TokenData(sub="1", role=Role.ADMIN, email="admin@test.com")


@pytest.fixture(name="client_token")
def client_token_fixture():
    """Crea un TokenData simulado para usuario Client."""
    return TokenData(sub="2", role=Role.CLIENTE, email="client@test.com")


@pytest.fixture(name="stock_manager_token")
def stock_manager_token_fixture():
    """Crea un TokenData simulado para usuario Stock Manager."""
    return TokenData(sub="3", role=Role.GESTOR_STOCK, email="stock@test.com")


# ============================================================================
# Tests: GET Endpoints (Public)
# ============================================================================

class TestGetEndpoints:
    """Tests para endpoints GET (públicos, sin autenticación)."""

    def test_list_categories_empty(self, client: TestClient):
        """GET /categories cuando no hay categorías debe retornar lista vacía."""
        response = client.get("/api/v1/categories")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_categories_with_data(self, client: TestClient, session: Session):
        """GET /categories debe retornar todas las categorías."""
        # Agregar categorías a la BD
        cat1 = Category(name="Produce", description="Fresh vegetables")
        cat2 = Category(name="Dairy", description="Milk and cheese")
        session.add(cat1)
        session.add(cat2)
        session.commit()

        response = client.get("/api/v1/categories")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "Produce"
        assert data[1]["name"] == "Dairy"

    def test_get_category_by_id_success(self, client: TestClient, session: Session):
        """GET /categories/{id} debe retornar la categoría correcta."""
        cat = Category(name="Produce", description="Fresh vegetables")
        session.add(cat)
        session.commit()
        session.refresh(cat)

        response = client.get(f"/api/v1/categories/{cat.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Produce"
        assert data["description"] == "Fresh vegetables"
        assert data["id"] == cat.id

    def test_get_category_by_id_not_found(self, client: TestClient):
        """GET /categories/{id} debe retornar 404 si la categoría no existe."""
        response = client.get("/api/v1/categories/999")
        assert response.status_code == 404
        assert "no encontrada" in response.json()["detail"].lower()

    def test_get_category_with_hierarchy(self, client: TestClient, session: Session):
        """GET /categories/{id} debe incluir subcategorías (hierarchy)."""
        parent = Category(name="Produce", description="Parent category")
        session.add(parent)
        session.commit()
        session.refresh(parent)

        child = Category(name="Vegetables", description="Child category", parent_id=parent.id)
        session.add(child)
        session.commit()
        session.refresh(child)

        response = client.get(f"/api/v1/categories/{parent.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Produce"
        # La respuesta debe incluir subcategorías
        assert "subcategories" in data


# ============================================================================
# Tests: POST Endpoint (Create - Admin only)
# ============================================================================

class TestPostEndpoint:
    """Tests para endpoint POST (crear categoría)."""

    def test_create_category_as_admin_success(self, client: TestClient, admin_token: TokenData):
        """POST /categories como Admin debe crear la categoría."""
        # Override dependency para simular usuario autenticado
        def get_current_user_override():
            return admin_token
        app.dependency_overrides[get_current_user] = get_current_user_override

        payload = {
            "name": "Produce",
            "description": "Fresh vegetables and fruits",
            "parent_id": None
        }
        response = client.post("/api/v1/categories", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Produce"
        assert data["description"] == "Fresh vegetables and fruits"
        assert "id" in data

        app.dependency_overrides.clear()

    def test_create_category_as_client_forbidden(self, client: TestClient, client_token: TokenData):
        """POST /categories como Cliente debe retornar 403 Forbidden."""
        def get_current_user_override():
            return client_token
        app.dependency_overrides[get_current_user] = get_current_user_override

        payload = {
            "name": "Produce",
            "description": "Fresh vegetables",
            "parent_id": None
        }
        response = client.post("/api/v1/categories", json=payload)
        assert response.status_code == 403
        assert "denegado" in response.json()["detail"].lower()

        app.dependency_overrides.clear()

    def test_create_category_missing_name(self, client: TestClient, admin_token: TokenData):
        """POST /categories sin nombre debe retornar 422 Unprocessable Entity."""
        def get_current_user_override():
            return admin_token
        app.dependency_overrides[get_current_user] = get_current_user_override

        payload = {
            "description": "Fresh vegetables",
            "parent_id": None
        }
        response = client.post("/api/v1/categories", json=payload)
        assert response.status_code == 422  # Validation error

        app.dependency_overrides.clear()

    def test_create_category_with_invalid_parent_id(self, client: TestClient, admin_token: TokenData):
        """POST /categories con parent_id inválido debe retornar 404."""
        def get_current_user_override():
            return admin_token
        app.dependency_overrides[get_current_user] = get_current_user_override

        payload = {
            "name": "Subcategory",
            "description": "A subcategory",
            "parent_id": 999  # No existe
        }
        response = client.post("/api/v1/categories", json=payload)
        assert response.status_code == 404

        app.dependency_overrides.clear()


# ============================================================================
# Tests: PUT Endpoint (Update - Admin or Stock Manager)
# ============================================================================

class TestPutEndpoint:
    """Tests para endpoint PUT (actualizar categoría)."""

    def test_update_category_as_admin_success(self, client: TestClient, session: Session, admin_token: TokenData):
        """PUT /categories/{id} como Admin debe actualizar la categoría."""
        cat = Category(name="Produce", description="Original description")
        session.add(cat)
        session.commit()
        session.refresh(cat)

        def get_current_user_override():
            return admin_token
        app.dependency_overrides[get_current_user] = get_current_user_override

        payload = {
            "name": "Produce Updated",
            "description": "Updated description"
        }
        response = client.put(f"/api/v1/categories/{cat.id}", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Produce Updated"
        assert data["description"] == "Updated description"

        app.dependency_overrides.clear()

    def test_update_category_as_stock_manager_success(self, client: TestClient, session: Session, stock_manager_token: TokenData):
        """PUT /categories/{id} como Stock Manager debe actualizar la categoría."""
        cat = Category(name="Produce", description="Original")
        session.add(cat)
        session.commit()
        session.refresh(cat)

        def get_current_user_override():
            return stock_manager_token
        app.dependency_overrides[get_current_user] = get_current_user_override

        payload = {"name": "Produce Updated"}
        response = client.put(f"/api/v1/categories/{cat.id}", json=payload)
        assert response.status_code == 200

        app.dependency_overrides.clear()

    def test_update_category_as_client_forbidden(self, client: TestClient, session: Session, client_token: TokenData):
        """PUT /categories/{id} como Cliente debe retornar 403."""
        cat = Category(name="Produce")
        session.add(cat)
        session.commit()
        session.refresh(cat)

        def get_current_user_override():
            return client_token
        app.dependency_overrides[get_current_user] = get_current_user_override

        payload = {"name": "Updated"}
        response = client.put(f"/api/v1/categories/{cat.id}", json=payload)
        assert response.status_code == 403

        app.dependency_overrides.clear()

    def test_update_category_not_found(self, client: TestClient, admin_token: TokenData):
        """PUT /categories/999 debe retornar 404."""
        def get_current_user_override():
            return admin_token
        app.dependency_overrides[get_current_user] = get_current_user_override

        payload = {"name": "Updated"}
        response = client.put("/api/v1/categories/999", json=payload)
        assert response.status_code == 404

        app.dependency_overrides.clear()


# ============================================================================
# Tests: DELETE Endpoint (Admin only)
# ============================================================================

class TestDeleteEndpoint:
    """Tests para endpoint DELETE (eliminar categoría)."""

    def test_delete_category_as_admin_success(self, client: TestClient, session: Session, admin_token: TokenData):
        """DELETE /categories/{id} como Admin debe eliminar la categoría."""
        cat = Category(name="Produce")
        session.add(cat)
        session.commit()
        session.refresh(cat)

        def get_current_user_override():
            return admin_token
        app.dependency_overrides[get_current_user] = get_current_user_override

        response = client.delete(f"/api/v1/categories/{cat.id}")
        assert response.status_code == 204
        assert response.content == b""  # No Content

        app.dependency_overrides.clear()

    def test_delete_category_as_stock_manager_forbidden(self, client: TestClient, session: Session, stock_manager_token: TokenData):
        """DELETE /categories/{id} como Stock Manager debe retornar 403."""
        cat = Category(name="Produce")
        session.add(cat)
        session.commit()
        session.refresh(cat)

        def get_current_user_override():
            return stock_manager_token
        app.dependency_overrides[get_current_user] = get_current_user_override

        response = client.delete(f"/api/v1/categories/{cat.id}")
        assert response.status_code == 403

        app.dependency_overrides.clear()

    def test_delete_category_not_found(self, client: TestClient, admin_token: TokenData):
        """DELETE /categories/999 debe retornar 404."""
        def get_current_user_override():
            return admin_token
        app.dependency_overrides[get_current_user] = get_current_user_override

        response = client.delete("/api/v1/categories/999")
        assert response.status_code == 404

        app.dependency_overrides.clear()


# ============================================================================
# Tests: Business Rules Validation
# ============================================================================

class TestBusinessRules:
    """Tests para validar reglas de negocio."""

    def test_cannot_create_duplicate_name(self, client: TestClient, session: Session, admin_token: TokenData):
        """No se puede crear dos categorías con el mismo nombre."""
        # Crear primera categoría
        cat = Category(name="Produce")
        session.add(cat)
        session.commit()

        # Intentar crear segunda con mismo nombre
        def get_current_user_override():
            return admin_token
        app.dependency_overrides[get_current_user] = get_current_user_override

        payload = {"name": "Produce", "description": "Duplicate"}
        response = client.post("/api/v1/categories", json=payload)
        assert response.status_code == 400
        assert "ya existe" in response.json()["detail"].lower()

        app.dependency_overrides.clear()

    def test_cannot_update_self_as_parent(self, client: TestClient, session: Session, admin_token: TokenData):
        """Una categoría no puede ser su propio padre."""
        cat = Category(name="Produce")
        session.add(cat)
        session.commit()
        session.refresh(cat)

        def get_current_user_override():
            return admin_token
        app.dependency_overrides[get_current_user] = get_current_user_override

        payload = {"parent_id": cat.id}  # Self-reference
        response = client.put(f"/api/v1/categories/{cat.id}", json=payload)
        assert response.status_code == 400
        assert "propio padre" in response.json()["detail"].lower()

        app.dependency_overrides.clear()

    def test_cannot_delete_category_with_children(self, client: TestClient, session: Session, admin_token: TokenData):
        """No se puede eliminar una categoría que tiene subcategorías."""
        parent = Category(name="Produce")
        session.add(parent)
        session.commit()
        session.refresh(parent)

        child = Category(name="Vegetables", parent_id=parent.id)
        session.add(child)
        session.commit()

        def get_current_user_override():
            return admin_token
        app.dependency_overrides[get_current_user] = get_current_user_override

        response = client.delete(f"/api/v1/categories/{parent.id}")
        assert response.status_code == 409  # Conflict
        assert "subcategorías" in response.json()["detail"].lower()

        app.dependency_overrides.clear()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
