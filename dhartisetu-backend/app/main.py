import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.loader import model_loader
from app.config import settings

# Routers
from app.routers import (
    aqi, co2, crop, flood, ndvi, plant_disease,
    price, profit, rainfall, soil, soil_health,
    storm, water, yield_pred, location
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dhartisetu")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting DhartiSetu on Hugging Face...")
    model_loader.load_all_models()
    logger.info("✅ Models loaded")
    yield
    logger.info("🛑 Shutting down")

app = FastAPI(
    title="DhartiSetu API",
    version="1.0.0",
    lifespan=lifespan
)

# 🔓 IMPORTANT: allow all origins (HF + Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API = "/api/v1"

app.include_router(aqi.router, prefix=f"{API}/aqi")
app.include_router(co2.router, prefix=f"{API}/co2")
app.include_router(crop.router, prefix=f"{API}/crop")
app.include_router(flood.router, prefix=f"{API}/flood")
app.include_router(ndvi.router, prefix=f"{API}/ndvi")
app.include_router(plant_disease.router, prefix=f"{API}/plant-disease")
app.include_router(price.router, prefix=f"{API}/price")
app.include_router(profit.router, prefix=f"{API}/profit")
app.include_router(rainfall.router, prefix=f"{API}/rainfall")
app.include_router(soil.router, prefix=f"{API}/soil")
app.include_router(soil_health.router, prefix=f"{API}/soil-health")
app.include_router(storm.router, prefix=f"{API}/storm")
app.include_router(water.router, prefix=f"{API}/water")
app.include_router(yield_pred.router, prefix=f"{API}/yield")
app.include_router(location.router, prefix=f"{API}/location")

@app.get("/")
def root():
    return {"status": "DhartiSetu backend running"}

# ⚠️ HF ENTRYPOINT
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 7860))
    )
