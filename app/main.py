from contextlib import asynccontextmanager
from sqlalchemy import text
from app.db.database import engine, Base
from app.models.task import Task
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Check database connection
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    #Create database tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    yield

    # Close database connection
    engine.dispose()



app = FastAPI(
    title = "TaskFlow API",
    description = "A multi-user project management REST API",
    version = "1.0.0",
    lifespan=lifespan
)

@app.get("/")
def root():
    return{
        "message": "Welcome to TaskFlow API",
        "status": "running",
    }

@app.get("/health")
def health_check():
    return{
        "status": "healthy",
    }