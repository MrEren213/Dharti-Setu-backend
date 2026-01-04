"""
DhartiSetu Configuration
FREE-TIER + LAZY LOADING SAFE
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # --------------------------------------------------
    # App
    # --------------------------------------------------
    APP_NAME: str = "DhartiSetu"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # --------------------------------------------------
    # API
    # --------------------------------------------------
    API_PREFIX: str = "/api/v1"
    ALLOWED_ORIGINS: List[str] = ["*"]

    # --------------------------------------------------
    # Image Upload
    # --------------------------------------------------
    MAX_IMAGE_SIZE: int = 10 * 1024 * 1024
    ALLOWED_IMAGE_TYPES: List[str] = [
        "image/jpeg",
        "image/png",
        "image/jpg"
    ]

    # --------------------------------------------------
    # HuggingFace Model Paths (RELATIVE TO REPO)
    # --------------------------------------------------
    MODEL_PATHS = {
        "aqi": {
            "model": "aqi/aqi_xgb.pkl",
            "encoder": "aqi/city_encoder.pkl"
        },
        "co2": {
            "model": "co2/co2_model.pkl",
            "scaler": "co2/co2_scaler.pkl"
        },
        "crop": {
            "model": "crop/crop_xgboost.pkl",
            "scaler": "crop/crop_scaler.pkl",
            "encoder": "crop/crop_label_encoder.pkl"
        },
        "flood": {
            "model": "flood/flood_rf.pkl"
        },
        "ndvi": {
            "model": "ndvi/ndvi_rf.pkl"
        },
        "plant_disease": {
            "model": "plant_disease/pytorch_model.bin"
        },
        "price": {
            "model": "price/crop_price_xgb.pkl",
            "encoders": "price/price_encoders.pkl"
        },
        "profit": {
            "model": "profit/crop_profit_model.pkl",
            "encoders": "profit/profit_encoders.pkl"
        },
        "rainfall": {
            "model": "rainfall/rainfall_rf.pkl",
            "encoder": "rainfall/subdivision_encoder.pkl"
        },
        "soil_cnn": {
            "model": "soil_cnn/soil_type_model.h5"
        },
        "soil_health": {
            "model": "soil_health/soil_health_xgb.pkl"
        },
        "storm": {
            "model": "storm/storm_rf.pkl"
        },
        "water": {
            "model": "water/water_rf.pkl"
        },
        "yield": {
            "model": "yield/yield_xgb.pkl"
        }
    }


# ✅ SINGLE SETTINGS INSTANCE
settings = Settings()
