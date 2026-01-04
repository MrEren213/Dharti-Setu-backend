# app/models/loader.py

import joblib
import logging
from typing import Dict, Any, Optional

import tensorflow as tf
from huggingface_hub import hf_hub_download

from app.config import settings

logger = logging.getLogger(__name__)

HF_REPO_ID = "crimson1232/dhartisetu-ml-models"
HF_CACHE_DIR = "hf_models"


class ModelLoader:
    """
    Lazy-loading ML model loader.
    Models load ONLY when requested.
    """

    _instance = None
    _models: Dict[str, Dict[str, Any]] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # -----------------------------
    # INTERNAL LOADERS
    # -----------------------------
    def _load_pickle(self, hf_path: str):
        logger.info(f"⬇️ Downloading pickle model: {hf_path}")
        path = hf_hub_download(
            repo_id=HF_REPO_ID,
            filename=hf_path,
            cache_dir=HF_CACHE_DIR
        )
        return joblib.load(path)

    def _load_keras(self, hf_path: str):
        logger.info(f"⬇️ Downloading keras model: {hf_path}")
        path = hf_hub_download(
            repo_id=HF_REPO_ID,
            filename=hf_path,
            cache_dir=HF_CACHE_DIR
        )
        return tf.keras.models.load_model(path, compile=False)

    # -----------------------------
    # LAZY LOAD SINGLE MODEL
    # -----------------------------
    def get_model(self, model_name: str, component: str = "model") -> Optional[Any]:
        if model_name not in self._models:
            self._models[model_name] = {}

            paths = settings.MODEL_PATHS.get(model_name, {})
            for comp, hf_path in paths.items():
                try:
                    if hf_path.endswith(".pkl"):
                        self._models[model_name][comp] = self._load_pickle(hf_path)

                    elif hf_path.endswith((".h5", ".keras")):
                        self._models[model_name][comp] = self._load_keras(hf_path)

                except Exception as e:
                    logger.error(
                        f"❌ Failed loading {model_name}/{comp}: {e}",
                        exc_info=True
                    )

        return self._models.get(model_name, {}).get(component)

    # -----------------------------
    # GET ALL COMPONENTS
    # -----------------------------
    def get_all(self, model_name: str) -> Optional[Dict[str, Any]]:
        # Force lazy load
        self.get_model(model_name)
        return self._models.get(model_name)


# ✅ SINGLETON
model_loader = ModelLoader()
