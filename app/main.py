"""Rural AI Assistant Backend — FastAPI application entrypoint."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.config import get_settings
from app.routes import api_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Startup and shutdown lifecycle (DB pools, clients, etc.)."""
    # Startup: init DB connections, DynamoDB client, S3, etc.
    yield
    # Shutdown: close connections
    pass


app = FastAPI(
    title=settings.app_name,
    description="Backend for Rural AI Assistant — schemes, eligibility, voice, WhatsApp.",
    version=__version__,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API router (health at /health, future APIs under prefix)
app.include_router(api_router)


@app.get("/")
def root() -> dict[str, str]:
    """Root redirect/info."""
    return {
        "service": settings.app_name,
        "version": __version__,
        "docs": "/docs",
        "health": "/health",
    }
