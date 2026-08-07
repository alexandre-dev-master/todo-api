"""
Application entry point.

Creates the FastAPI application, configures middleware,
initializes the database, and registers API routes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routes import auth_routes, task_routes


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Notes API",
    description="REST API for task management with JWT authentication.",
    version="1.0.0",
    swagger_ui_parameters={
        "persistAuthorization": True,
    },
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_routes.router)
app.include_router(task_routes.router)


@app.get("/")
def health_check():
    """Returns the current API status."""

    return {
        "status": "online",
        "version": "1.0.0",
        "message": "Notes API is running.",
    }