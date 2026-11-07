from contextlib import asynccontextmanager
from sqlalchemy import text
from app.db.database import engine, Base
from app.models.task import Task
from fastapi import FastAPI
from app.routers.task import router as task_router
from app.routers.auth import router as auth_router
from app.models.user import User


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

app.include_router(auth_router)
app.include_router(task_router)