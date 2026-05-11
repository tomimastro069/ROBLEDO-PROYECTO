"""Fixtures for product service tests."""

import pytest
from decimal import Decimal
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool

from app.core.models import Category, Product, ProductIngredient, ProductAllergen
from app.core.uow.unit_of_work import AppUnitOfWork
from products.service import ProductsService


@pytest.fixture(name="session")
def session_fixture():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="uow_mock")
def uow_mock_fixture(session: Session):
    """Create a mocked AppUnitOfWork with test session."""
    uow = AppUnitOfWork(engine=session.get_bind())
    # Override the session to use our test session
    uow.session = session
    return uow


@pytest.fixture(name="service")
def service_fixture(session: Session):
    """Create a ProductsService instance with test UnitOfWork."""
    class TestAppUnitOfWork(AppUnitOfWork):
        def __enter__(self):
            # Return self with the test session already set
            self.users = None  # Not needed for product tests
            self.roles = None
            self.categories = None
            from app.core.repositories.products_repository import ProductsRepository
            from app.core.repositories.product_ingredient_repository import ProductIngredientRepository
            from app.core.repositories.product_allergen_repository import ProductAllergenRepository
            
            self.products = ProductsRepository(session)
            self.product_ingredients = ProductIngredientRepository(session)
            self.product_allergens = ProductAllergenRepository(session)
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            # Don't close the test session
            if exc_type is None:
                session.commit()
            else:
                session.rollback()
            return False
    
    uow = TestAppUnitOfWork()
    return ProductsService(uow)


@pytest.fixture(name="test_category")
def test_category_fixture(session: Session):
    """Create a test category."""
    category = Category(name="Test Category", description="A test category")
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@pytest.fixture(name="test_product")
def test_product_fixture(session: Session, test_category):
    """Create a test product."""
    product = Product(
        name="Test Product",
        description="A test product",
        price=Decimal("9.99"),
        stock=100,
        category_id=test_category.id
    )
    session.add(product)
    session.commit()
    session.refresh(product)
    return product
