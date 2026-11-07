from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import settings

#creating database engine
engine = create_engine(
        settings.DATABASE_URL, 
        echo=True
    )

#creating a session factory
SessionLocal = sessionmaker(
        bind=engine,
        autocommit=False, 
        autoflush=False, 
    )

#creating a base class for declarative models
class Base(DeclarativeBase):
    pass

#dependency function to get a database session
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
