"""Integration tests for ProductsService."""

import pytest
from decimal import Decimal
from fastapi import HTTPException

from app.core.models import Product, ProductIngredient, ProductAllergen
from products.service import ProductsService


class TestProductsCRUD:
    """Test CRUD operations on products."""
    
    def test_create_product(self, service: ProductsService, test_category):
        """Test creating a new product."""
        product = service.create(
            name="New Product",
            description="A new product",
            price=Decimal("19.99"),
            stock=50,
            category_id=test_category.id
        )
        
        assert product.id is not None
        assert product.name == "New Product"
        assert product.price == Decimal("19.99")
        assert product.stock == 50
        assert product.category_id == test_category.id
    
    def test_create_product_invalid_category(self, service: ProductsService):
        """Test creating a product with non-existent category raises error."""
        with pytest.raises(HTTPException) as exc_info:
            service.create(
                name="Invalid Product",
                description="Should fail",
                price=Decimal("10.00"),
                stock=0,
                category_id=999
            )
        
        assert exc_info.value.status_code == 404
        assert "not found" in exc_info.value.detail
    
    def test_get_product_by_id(self, service: ProductsService, test_product):
        """Test retrieving a product by ID."""
        product = service.get_by_id(test_product.id)
        
        assert product.id == test_product.id
        assert product.name == test_product.name
        assert product.price == Decimal("9.99")
    
    def test_get_product_not_found(self, service: ProductsService):
        """Test retrieving non-existent product raises error."""
        with pytest.raises(HTTPException) as exc_info:
            service.get_by_id(999)
        
        assert exc_info.value.status_code == 404
    
    def test_update_product(self, service: ProductsService, test_product):
        """Test updating a product."""
        updated = service.update(
            test_product.id,
            name="Updated Product",
            price=Decimal("15.99")
        )
        
        assert updated.name == "Updated Product"
        assert updated.price == Decimal("15.99")
    
    def test_get_all_products_with_pagination(self, service: ProductsService, test_product):
        """Test retrieving all products with pagination."""
        # Create another product
        service.create(
            name="Product 2",
            description="Second product",
            price=Decimal("20.00"),
            stock=30,
            category_id=None
        )
        
        products, total = service.get_all(limit=1, offset=0)
        
        assert len(products) == 1
        assert total == 2  # We have 2 products total


class TestProductIngredients:
    """Test ingredient management."""
    
    def test_add_ingredient(self, service: ProductsService, test_product):
        """Test adding an ingredient to a product."""
        ingredient = service.add_ingredient(test_product.id, "Flour")
        
        assert ingredient.id is not None
        assert ingredient.product_id == test_product.id
        assert ingredient.name == "Flour"
    
    def test_add_duplicate_ingredient_raises_error(self, service: ProductsService, test_product):
        """Test adding duplicate ingredient raises error."""
        service.add_ingredient(test_product.id, "Sugar")
        
        with pytest.raises(HTTPException) as exc_info:
            service.add_ingredient(test_product.id, "Sugar")
        
        assert exc_info.value.status_code == 400
    
    def test_get_ingredients(self, service: ProductsService, test_product):
        """Test retrieving ingredients for a product."""
        service.add_ingredient(test_product.id, "Eggs")
        service.add_ingredient(test_product.id, "Milk")
        
        ingredients = service.get_ingredients(test_product.id)
        
        assert len(ingredients) == 2
        assert any(i.name == "Eggs" for i in ingredients)
        assert any(i.name == "Milk" for i in ingredients)
    
    def test_remove_ingredient(self, service: ProductsService, test_product):
        """Test removing an ingredient from a product."""
        ingredient = service.add_ingredient(test_product.id, "Butter")
        
        service.remove_ingredient(test_product.id, ingredient.id)
        
        ingredients = service.get_ingredients(test_product.id)
        assert len(ingredients) == 0


class TestProductAllergens:
    """Test allergen management."""
    
    def test_add_allergen(self, service: ProductsService, test_product):
        """Test adding an allergen to a product."""
        allergen = service.add_allergen(test_product.id, "peanuts")
        
        assert allergen.id is not None
        assert allergen.product_id == test_product.id
        assert allergen.name == "peanuts"
    
    def test_add_duplicate_allergen_raises_error(self, service: ProductsService, test_product):
        """Test adding duplicate allergen raises error."""
        service.add_allergen(test_product.id, "gluten")
        
        with pytest.raises(HTTPException) as exc_info:
            service.add_allergen(test_product.id, "gluten")
        
        assert exc_info.value.status_code == 400
    
    def test_get_allergens(self, service: ProductsService, test_product):
        """Test retrieving allergens for a product."""
        service.add_allergen(test_product.id, "dairy")
        service.add_allergen(test_product.id, "shellfish")
        
        allergens = service.get_allergens(test_product.id)
        
        assert len(allergens) == 2
        assert any(a.name == "dairy" for a in allergens)
        assert any(a.name == "shellfish" for a in allergens)
    
    def test_remove_allergen(self, service: ProductsService, test_product):
        """Test removing an allergen from a product."""
        allergen = service.add_allergen(test_product.id, "tree nuts")
        
        service.remove_allergen(test_product.id, allergen.id)
        
        allergens = service.get_allergens(test_product.id)
        assert len(allergens) == 0


class TestStockManagement:
    """Test stock validation and updates."""
    
    def test_validate_stock_available(self, service: ProductsService, test_product):
        """Test checking stock availability."""
        # Test with sufficient stock
        assert service.validate_stock_available(test_product.id, 50) is True
        
        # Test with insufficient stock
        assert service.validate_stock_available(test_product.id, 150) is False
    
    def test_validate_stock_product_not_found(self, service: ProductsService):
        """Test validating stock for non-existent product returns False."""
        assert service.validate_stock_available(999, 10) is False
    
    def test_decrease_stock(self, service: ProductsService, test_product):
        """Test decreasing stock."""
        initial_stock = test_product.stock
        
        updated = service.decrease_stock(test_product.id, 30)
        
        assert updated.stock == initial_stock - 30
    
    def test_decrease_stock_insufficient_raises_error(self, service: ProductsService, test_product):
        """Test decreasing stock with insufficient quantity raises error."""
        with pytest.raises(HTTPException) as exc_info:
            service.decrease_stock(test_product.id, 200)
        
        assert exc_info.value.status_code == 400
        assert "Insufficient stock" in exc_info.value.detail
    
    def test_increase_stock(self, service: ProductsService, test_product):
        """Test increasing stock."""
        initial_stock = test_product.stock
        
        updated = service.increase_stock(test_product.id, 20)
        
        assert updated.stock == initial_stock + 20
    
    def test_stock_precision_with_decimal(self, service: ProductsService, test_product):
        """Test that prices maintain Decimal precision through operations."""
        product = service.get_by_id(test_product.id)
        
        # Verify price is Decimal, not float
        assert isinstance(product.price, Decimal)
        assert product.price == Decimal("9.99")


class TestProductQueries:
    """Test specialized product queries."""
    
    def test_get_products_by_category(self, service: ProductsService, test_category):
        """Test retrieving products by category."""
        service.create("Product A", "Desc A", Decimal("10.00"), 10, test_category.id)
        service.create("Product B", "Desc B", Decimal("20.00"), 20, test_category.id)
        
        products, total = service.get_by_category(test_category.id)
        
        assert len(products) == 2
        assert total == 2
    
    def test_search_by_name(self, service: ProductsService):
        """Test searching products by name."""
        service.create("Chocolate Cake", "A cake", Decimal("15.00"), 5, None)
        service.create("Chocolate Mousse", "A mousse", Decimal("8.00"), 10, None)
        service.create("Vanilla Cake", "A cake", Decimal("12.00"), 8, None)
        
        results, total = service.search_by_name("Chocolate")
        
        assert len(results) == 2
        assert total == 2
        assert all("Chocolate" in p.name for p in results)
    
    def test_search_by_name_case_insensitive(self, service: ProductsService):
        """Test search is case-insensitive."""
        service.create("Premium Coffee", "Coffee", Decimal("5.00"), 20, None)
        
        results, total = service.search_by_name("coffee")
        
        assert len(results) == 1
        assert results[0].name == "Premium Coffee"
