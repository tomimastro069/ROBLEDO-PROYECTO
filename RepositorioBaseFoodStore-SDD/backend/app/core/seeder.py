import os
from sqlmodel import Session, select
from app.core.database import engine
from app.core.models import Role, User, Category, Product, Ingrediente, Address, Payment
from orders.models import Order, OrderItem, OrderStatus, FormaPago
from auth.utils import pwd_context
from decimal import Decimal

from auth.roles import Role as RoleEnum

ROLES = [
    {"name": RoleEnum.ADMIN.value, "description": "Administrador del sistema"},
    {"name": RoleEnum.CLIENTE.value, "description": "Cliente final"},
    {"name": RoleEnum.GESTOR_STOCK.value, "description": "Encargado de inventario"},
    {"name": RoleEnum.GESTOR_PEDIDOS.value, "description": "Encargado de preparar pedidos"},
    {"name": RoleEnum.SISTEMA.value, "description": "Usuario del sistema para tareas automatizadas"}
]

CATEGORIES = [
    {"name": "Pizzas", "description": "Pizzas artesanales"},
    {"name": "Hamburguesas", "description": "Burgers premium"},
    {"name": "Bebidas", "description": "Gaseosas y jugos"}
]

INGREDIENTES = [
    {"nombre": "Mussarela", "es_alergeno": True},
    {"nombre": "Tomate", "es_alergeno": False},
    {"nombre": "Huevo", "es_alergeno": True},
    {"nombre": "Panceta", "es_alergeno": False},
    {"nombre": "Cheddar", "es_alergeno": True}
]

ADMIN_EMAIL = os.getenv("DEFAULT_ADMIN_EMAIL", "admin@foodstore.local")
ADMIN_PASSWORD = "admin123"

def seed_roles(session: Session):
    for role_data in ROLES:
        # Buscar por nombre (case-insensitive si es posible, o simplemente buscar ambos)
        statement = select(Role).where(Role.name.ilike(role_data["name"]))
        existing_role = session.exec(statement).first()
        
        if existing_role:
            if existing_role.name != role_data["name"]:
                print(f"Normalizing role name: {existing_role.name} -> {role_data['name']}")
                existing_role.name = role_data["name"]
                session.add(existing_role)
        else:
            print(f"Creating role: {role_data['name']}")
            role = Role(**role_data)
            session.add(role)
    session.commit()

def seed_categories(session: Session):
    for cat_data in CATEGORIES:
        statement = select(Category).where(Category.name == cat_data["name"])
        if not session.exec(statement).first():
            print(f"Creating category: {cat_data['name']}")
            session.add(Category(**cat_data))
    session.commit()

def seed_ingredients(session: Session):
    for ing_data in INGREDIENTES:
        statement = select(Ingrediente).where(Ingrediente.nombre == ing_data["nombre"])
        if not session.exec(statement).first():
            print(f"Creating ingredient: {ing_data['nombre']}")
            session.add(Ingrediente(**ing_data))
    session.commit()

def seed_formas_pago(session: Session):
    formas = ["MERCADOPAGO", "EFECTIVO", "TRANSFERENCIA"]
    for codigo in formas:
        statement = select(FormaPago).where(FormaPago.codigo == codigo)
        if not session.exec(statement).first():
            print(f"Creating forma de pago: {codigo}")
            session.add(FormaPago(codigo=codigo, habilitado=True))
    session.commit()

def seed_products(session: Session):
    pizza_cat = session.exec(select(Category).where(Category.name == "Pizzas")).first()
    burger_cat = session.exec(select(Category).where(Category.name == "Hamburguesas")).first()
    bebida_cat = session.exec(select(Category).where(Category.name == "Bebidas")).first()

    products = [
        # Pizzas
        {"name": "Pizza Margarita", "description": "Tomate, mozzarella y albahaca", "price": Decimal("1200.00"), "stock": 50, "category_id": pizza_cat.id if pizza_cat else None},
        {"name": "Pizza Especial", "description": "Jamón, morrón y olivas", "price": Decimal("1500.00"), "stock": 40, "category_id": pizza_cat.id if pizza_cat else None},
        {"name": "Pizza Fugazzetta", "description": "Mucha cebolla y queso", "price": Decimal("1400.00"), "stock": 35, "category_id": pizza_cat.id if pizza_cat else None},
        
        # Burgers
        {"name": "Burger Doble Cheddar", "description": "Doble carne, doble queso", "price": Decimal("1500.00"), "stock": 30, "category_id": burger_cat.id if burger_cat else None},
        {"name": "Burger BBQ Bacon", "description": "Panceta crocante y salsa BBQ", "price": Decimal("1700.00"), "stock": 25, "category_id": burger_cat.id if burger_cat else None},
        {"name": "Burger Veggie", "description": "Medallón de lentejas y palta", "price": Decimal("1300.00"), "stock": 20, "category_id": burger_cat.id if burger_cat else None},
        
        # Bebidas
        {"name": "Coca-Cola 500ml", "description": "Bien fría", "price": Decimal("500.00"), "stock": 100, "category_id": bebida_cat.id if bebida_cat else None},
        {"name": "Cerveza IPA 473ml", "description": "Artesanal local", "price": Decimal("900.00"), "stock": 60, "category_id": bebida_cat.id if bebida_cat else None},
        {"name": "Agua Mineral 500ml", "description": "Sin gas", "price": Decimal("400.00"), "stock": 150, "category_id": bebida_cat.id if bebida_cat else None}
    ]

    for prod_data in products:
        statement = select(Product).where(Product.name == prod_data["name"])
        if not session.exec(statement).first():
            print(f"Creating product: {prod_data['name']}")
            session.add(Product(**prod_data))
    session.commit()

def seed_users_and_orders(session: Session):
    # Admin
    admin_role = session.exec(select(Role).where(Role.name == RoleEnum.ADMIN.value)).first()
    if not session.exec(select(User).where(User.email == ADMIN_EMAIL)).first():
        print(f"Creating admin: {ADMIN_EMAIL}")
        hashed_pw = pwd_context.hash(ADMIN_PASSWORD)
        session.add(User(email=ADMIN_EMAIL, hashed_password=hashed_pw, role_id=admin_role.id, is_active=True))

    # Cliente de prueba
    cliente_role = session.exec(select(Role).where(Role.name == RoleEnum.CLIENTE.value)).first()
    cliente_email = "cliente@test.com"
    cliente = session.exec(select(User).where(User.email == cliente_email)).first()
    if not cliente:
        print(f"Creating test client: {cliente_email}")
        hashed_pw = pwd_context.hash("cliente123")
        cliente = User(email=cliente_email, hashed_password=hashed_pw, role_id=cliente_role.id, is_active=True, name="Juan Perez")
        session.add(cliente)
        session.commit()
        session.refresh(cliente)

    # Dirección para el cliente
    if not session.exec(select(Address).where(Address.user_id == cliente.id)).first():
        print(f"Creating address for {cliente_email}")
        address = Address(
            street="Av. Siempre Viva", numero="742", city="Springfield", 
            state="ST", zip_code="1234", is_default=True, user_id=cliente.id
        )
        session.add(address)
        session.commit()
        session.refresh(address)

        # Crear una orden de prueba
        prod = session.exec(select(Product)).first()
        if prod:
            print(f"Creating test order for {cliente_email}")
            order = Order(
                user_id=cliente.id,
                status=OrderStatus.ENTREGADO,
                total=prod.price,
                direccion_calle=address.street,
                direccion_numero=address.numero,
                direccion_ciudad=address.city
            )
            session.add(order)
            session.commit()
            session.refresh(order)
            
            item = OrderItem(order_id=order.id, product_id=prod.id, quantity=1, price_snapshot=prod.price)
            session.add(item)
            session.commit()

def seed_product_ingredients(session: Session):
    pizza_margarita = session.exec(select(Product).where(Product.name == "Pizza Margarita")).first()
    tomate = session.exec(select(Ingrediente).where(Ingrediente.nombre == "Tomate")).first()
    mussarela = session.exec(select(Ingrediente).where(Ingrediente.nombre == "Mussarela")).first()

    from app.core.models import ProductIngrediente
    if pizza_margarita and tomate and mussarela:
        links = [
            {"product_id": pizza_margarita.id, "ingrediente_id": tomate.id},
            {"product_id": pizza_margarita.id, "ingrediente_id": mussarela.id}
        ]
        for link_data in links:
            statement = select(ProductIngrediente).where(
                ProductIngrediente.product_id == link_data["product_id"],
                ProductIngrediente.ingrediente_id == link_data["ingrediente_id"]
            )
            if not session.exec(statement).first():
                session.add(ProductIngrediente(**link_data))
    session.commit()

def run_seed():
    print("\n--- Starting Enhanced Database Seeder ---")
    with Session(engine) as session:
        seed_roles(session)
        seed_categories(session)
        seed_ingredients(session)
        seed_formas_pago(session)
        seed_products(session)
        seed_product_ingredients(session) # Nueva llamada
        seed_users_and_orders(session)
    print("--- Seeding completed successfully ---\n")

if __name__ == "__main__":
    run_seed()
