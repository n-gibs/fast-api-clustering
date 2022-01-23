

from fastapi import APIRouter

from src.app.api.routes import heartbeat, prediction, cluster, customer

api_router = APIRouter()
api_router.include_router(heartbeat.router, tags=["health"], prefix="/health")
api_router.include_router(prediction.router, tags=[
                          "prediction"], prefix="/model")
api_router.include_router(cluster.router, tags=[
                          "cluster"], prefix="/model")
api_router.include_router(customer.router, tags=[
                          "customer"], prefix="/customer")
