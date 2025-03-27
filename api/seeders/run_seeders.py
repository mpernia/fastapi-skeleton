from api.config.database import SessionLocal
from api.seeders.user_seeder import seed_admin_user

def run_seeders():
    db = SessionLocal()
    try:
        print("Running seeders...")
        seed_admin_user(db)
        print("Seeders completed!")
    finally:
        db.close()

if __name__ == "__main__":
    run_seeders()
