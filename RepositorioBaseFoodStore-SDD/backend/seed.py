from sqlmodel import SQLModel, Session, create_engine
from models import User

# Define the database URL or file path (update if needed)
DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL)

# Seed data for the 'User' table
seed_users = [
    User(name="Alice", email="alice@example.com"),
    User(name="Bob", email="bob@example.com"),
    User(name="Charlie", email="charlie@example.com")
]

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def load_seed_data():
    with Session(engine) as session:
        # Avoid duplicating seed data
        existing_users = session.query(User).count()
        if existing_users == 0:
            session.add_all(seed_users)
            session.commit()

if __name__ == "__main__":
    create_db_and_tables()
    load_seed_data()
    print("Database initialized and seed data populated.")