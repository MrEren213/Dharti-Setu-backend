"""
DhartiSetu - Main FastAPI Application
LAZY LOADING ENABLED (FREE TIER SAFE)
"""

import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.models.loader import model_loader

# Routers
from app.routers import (
    aqi, co2, crop, flood, ndvi, plant_disease,
    price, profit, rainfall, soil, soil_health,
    storm, water, yield_pred, location
)

# --------------------------------------------------
# Logging
# --------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger("dhartisetu")

# --------------------------------------------------
# Utilities
# --------------------------------------------------
def get_memory_usage():
    try:
        import psutil
        process = psutil.Process(os.getpid())
        return f"{process.memory_info().rss / 1024 / 1024:.1f} MB"
    except Exception:
        return "N/A"

# --------------------------------------------------
# Lifespan (NO MODEL LOADING HERE)
# --------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 DhartiSetu API starting (LAZY MODELS ENABLED)")
    logger.info(f"📊 Memory usage (startup): {get_memory_usage()}")
    yield
    logger.info("🛑 DhartiSetu API shutting down")

# --------------------------------------------------
# FastAPI App
# --------------------------------------------------
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-Powered Agricultural Intelligence Platform",
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# --------------------------------------------------
# CORS
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Routers
# --------------------------------------------------
API = settings.API_PREFIX

app.include_router(aqi.router, prefix=f"{API}/aqi", tags=["AQI"])
app.include_router(co2.router, prefix=f"{API}/co2", tags=["CO2"])
app.include_router(crop.router, prefix=f"{API}/crop", tags=["Crop"])
app.include_router(flood.router, prefix=f"{API}/flood", tags=["Flood"])
app.include_router(ndvi.router, prefix=f"{API}/ndvi", tags=["NDVI"])
app.include_router(plant_disease.router, prefix=f"{API}/plant-disease", tags=["Plant Disease"])
app.include_router(price.router, prefix=f"{API}/price", tags=["Price"])
app.include_router(profit.router, prefix=f"{API}/profit", tags=["Profit"])
app.include_router(rainfall.router, prefix=f"{API}/rainfall", tags=["Rainfall"])
app.include_router(soil.router, prefix=f"{API}/soil", tags=["Soil"])
app.include_router(soil_health.router, prefix=f"{API}/soil-health", tags=["Soil Health"])
app.include_router(storm.router, prefix=f"{API}/storm", tags=["Storm"])
app.include_router(water.router, prefix=f"{API}/water", tags=["Water"])
app.include_router(yield_pred.router, prefix=f"{API}/yield", tags=["Yield"])
app.include_router(location.router, prefix=f"{API}/location", tags=["Location"])

# --------------------------------------------------
# Root & Health
# --------------------------------------------------
@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "memory": get_memory_usage()
    }

# --------------------------------------------------
# OPTIONAL WARMUP (CALL BEFORE DEMO)
# --------------------------------------------------
@app.get("/warmup/{model_name}")
def warmup(model_name: str):
    model_loader.get_model(model_name)
    return {"status": f"{model_name} warmed"}

# --------------------------------------------------
# Global Exception Handler
# --------------------------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("🔥 Unhandled exception", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "error": str(exc) if settings.DEBUG else "Something went wrong"
        }
    )

# --------------------------------------------------
# Local Dev Run ONLY
# --------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
