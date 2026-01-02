from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import stock, portfolio, health, search
from app.utils.logger import setup_logger, get_logger

# Setup logger
setup_logger()
logger = get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    logger.info("="*60)
    logger.info("AI Stock Risk Analysis Platform Starting...")
    logger.info("="*60)
    
    yield
    
    # Shutdown
    logger.info("AI Stock Risk Analysis Platform Shutting Down...")

# Create FastAPI app with lifespan
app = FastAPI(
    title="AI Stock & Portfolio Risk Analysis Platform",
    version="1.0.0",
    description="Deterministic risk analysis with AI-powered explanations",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(search.router, prefix="/api", tags=["search"])
app.include_router(stock.router, prefix="/api", tags=["stock"])
app.include_router(portfolio.router, prefix="/api", tags=["portfolio"])

@app.get("/")
async def root():
    """Root endpoint"""
    logger.info("Root endpoint accessed")
    return {
        "message": "AI Stock Risk Analysis Platform API",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs"
    }
