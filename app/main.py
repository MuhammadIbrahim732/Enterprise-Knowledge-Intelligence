from fastapi import FastAPI

from pathlib import Path
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.schemas.api_schemas import HealthResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.chat_routes import router as chat_router
from app.api.routes.document_routes import router as document_router


app = FastAPI(
    title=settings.APP_NAME,
    description="Enterprise Knowledge Intelligence System powered by RAG and Gemini.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():

    return {
        "message": "Welcome to Enterprise Knowledge Intelligence API",
        "status": "running"
    }


@app.get("/health", response_model=HealthResponse)
def health_check():

    return HealthResponse(
        status="healthy",
        application=settings.APP_NAME
    )

app.include_router(document_router)
app.include_router(chat_router)


FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

app.mount(
    "/",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="frontend"
)