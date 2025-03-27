from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from api.config.settings import get_settings

settings = get_settings()

DATABASE_URL = str(settings.DATABASE_URL)
REDIS_URL = str(settings.REDIS_URL) if settings.REDIS_URL else None

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
