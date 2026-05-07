import os
from sqlmodel import Session, select
from app.core.database import engine
from app.core.models import Role, User
from app.core.auth import pwd_context

ROLES = [
    {"name": "Admin", "description": "Administrador del sistema"},
    {"name": "Cliente", "description": "Cliente final"},
    {"name": "Gestor Stock", "description": "Encargado de inventario"},
    {"name": "Gestor Pedidos", "description": "Encargado de preparar pedidos"},
    {"name": "Sistema", "description": "Usuario del sistema para tareas automatizadas"}
]

ADMIN_EMAIL = os.getenv("DEFAULT_ADMIN_EMAIL", "admin@foodstore.local")
ADMIN_PASSWORD = os.getenv("DEFAULT_ADMIN_PASSWORD", "admin123")

def seed_roles(session: Session):
    for role_data in ROLES:
        statement = select(Role).where(Role.name == role_data["name"])
        existing_role = session.exec(statement).first()
        if not existing_role:
            print(f"Creating role: {role_data['name']}")
            new_role = Role(**role_data)
            session.add(new_role)
        else:
            print(f"Role already exists: {role_data['name']}")
    session.commit()

def seed_admin_user(session: Session):
    statement = select(User).where(User.email == ADMIN_EMAIL)
    existing_user = session.exec(statement).first()
    
    if not existing_user:
        print(f"Creating default admin user: {ADMIN_EMAIL}")
        # Get admin role
        role_stmt = select(Role).where(Role.name == "Admin")
        admin_role = session.exec(role_stmt).first()
        
        if admin_role:
            hashed_pw = pwd_context.hash(ADMIN_PASSWORD)
            new_admin = User(
                email=ADMIN_EMAIL,
                hashed_password=hashed_pw,
                role_id=admin_role.id
            )
            session.add(new_admin)
            session.commit()
        else:
            print("Error: Admin role not found. Run seed_roles first.")
    else:
        print(f"Default admin user already exists: {ADMIN_EMAIL}")

def run_seed():
    print("Starting database seeder...")
    with Session(engine) as session:
        seed_roles(session)
        seed_admin_user(session)
    print("Seeding completed successfully.")

if __name__ == "__main__":
    run_seed()
