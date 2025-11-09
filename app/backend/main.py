"""
FastAPI main application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from api import optimization, export

# Create FastAPI app
app = FastAPI(
    title="KLM Cargo Optimization API",
    description="API for cargo loading optimization and visualization",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(optimization.router, prefix="/api/v1/optimization", tags=["Optimization"])
app.include_router(export.router, prefix="/api/v1/export", tags=["Export"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "KLM Cargo Optimization API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=settings.DEBUG)

