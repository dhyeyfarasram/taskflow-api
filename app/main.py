from fastapi import FastAPI

app = FastAPI(
    title = "TaskFlow API",
    description = "A multi-user project management REST API",
    version = "1.0.0",
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