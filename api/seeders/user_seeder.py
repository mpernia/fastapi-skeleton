from sqlalchemy.orm import Session
from api.models.user import User
from api.middlewares.authenticate import AuthHandler

auth_handler = AuthHandler()

def seed_admin_user(db: Session):
    # Check if admin user already exists
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        # Create admin user
        admin_user = User(
            username="admin",
            hashed_password=auth_handler.get_password_hash("admin"),
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print("Admin user created successfully!")
    else:
        print("Admin user already exists!")
