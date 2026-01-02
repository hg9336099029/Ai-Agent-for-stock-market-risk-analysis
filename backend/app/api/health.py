"""
Health check API endpoint
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    """System health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Stock Risk Analysis Platform",
        "version": "1.0.0"
    }
