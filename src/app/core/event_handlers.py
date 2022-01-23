from typing import Callable

from fastapi import FastAPI
from loguru import logger

from src.app.config import DEFAULT_MODEL_PATH, CLUSTER_MODEL_PATH
from src.app.services.models import HousePriceModel
from src.app.services.cluster_model import CustomerSegmentationModel
from src.app.db import db

def _startup_model(app: FastAPI) -> None:
    cluster_model_path = CLUSTER_MODEL_PATH
    cluster_model_instance = CustomerSegmentationModel(cluster_model_path)
    # model_path = DEFAULT_MODEL_PATH
    # model_instance = HousePriceModel(model_path)
    app.state.model = cluster_model_instance


def _shutdown_model(app: FastAPI) -> None:
    app.state.model = None


def start_app_handler(app: FastAPI) -> Callable:
    async def startup() -> None:
        logger.info("Running app start handler.")
        await db.connect()
        _startup_model(app)
    return startup


def stop_app_handler(app: FastAPI) -> Callable:
    async def shutdown() -> None:
        logger.info("Running app shutdown handler.")
        await db.disconnect()
        _shutdown_model(app)
    return shutdown
