from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

#creating database engine
engine = create_engine(
        settings.DATABASE_URL, 
        echo=True
    )

#creating a session factory
SessionLocal = sessionmaker(
        autocommit=False, 
        autoflush=False, 
        bind=engine
    )

#creating a base class for declarative models
class Base(declarative_base()):
    pass

#dependency function to get a database session
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
