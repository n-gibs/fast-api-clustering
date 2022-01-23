from fastapi import APIRouter, Depends
from starlette.requests import Request

from src.app.core import security
from src.app.models.payload import HousePredictionPayload
from src.app.models.prediction import HousePredictionResult
from src.app.services.models import HousePriceModel

router = APIRouter()


@router.post("/predict", response_model=HousePredictionResult, name="predict")
def post_predict(
    request: Request,
    authenticated: bool = Depends(security.validate_request),
    block_data: HousePredictionPayload = None
) -> HousePredictionResult:

    model: HousePriceModel = request.app.state.model
    prediction: HousePredictionResult = model.predict(block_data)

    return prediction
