"""
Stream-View Backend API

FastAPI application for analyzing HLS and DASH stream manifests.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.analyze import router as analyze_router

app = FastAPI(
    title="Stream-View API",
    description="API for analyzing HLS and DASH stream manifests",
    version="0.1.0",
)

# Configure CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(analyze_router)


@app.get("/api/health")
async def health_check():
    """
    Health check endpoint for monitoring service availability.

    Returns:
        dict: Status information
    """
    return {
        "status": "healthy",
        "service": "stream-view-api",
        "version": "0.1.0"
    }


@app.get("/")
async def root():
    """
    Root endpoint with API information.

    Returns:
        dict: Welcome message and documentation link
    """
    return {
        "message": "Stream-View API",
        "docs": "/docs",
        "health": "/api/health"
    }
