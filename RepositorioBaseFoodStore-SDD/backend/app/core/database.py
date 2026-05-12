import time
from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.exc import OperationalError
from app.core.config import settings

engine = create_engine(settings.DB_URL, echo=True)

def init_db():
    """
    Inicializa la base de datos creando todas las tablas.
    Incluye un mecanismo de reintento para esperar a que el contenedor de DB esté listo.
    """
    max_retries = 10
    retry_interval = 3
    
    for i in range(max_retries):
        try:
            # Importamos modelos aquí para asegurar que estén registrados en SQLModel.metadata
            from app.core.models import Role, User, Category, Product, Ingrediente, Address, Payment
            from orders.models import Order, OrderItem
            
            SQLModel.metadata.create_all(engine)
            print("✅ Database tables created successfully.")
            return
        except OperationalError as e:
            if i < max_retries - 1:
                print(f"⚠️ Database not ready yet (retry {i+1}/{max_retries}). Waiting {retry_interval}s...")
                time.sleep(retry_interval)
            else:
                print("❌ Could not connect to database after several retries.")
                raise e

def get_session():
    with Session(engine) as session:
        yield session
