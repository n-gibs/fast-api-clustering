from fastapi import APIRouter, Depends
from starlette.requests import Request

from src.app.core import security
from src.app.models.cluster_payload import CustomerSegmentationPayload
from src.app.models.cluster_prediction import CustomerSegmentationResult
from src.app.services.cluster_model import CustomerSegmentationModel

router = APIRouter()


@router.post("/cluster", response_model=CustomerSegmentationResult, name="cluster")
def post_predict(
    request: Request,
    authenticated: bool = Depends(security.validate_request),
    block_data: CustomerSegmentationPayload = None
) -> CustomerSegmentationResult:

    model: CustomerSegmentationPayload = request.app.state.model
    prediction: CustomerSegmentationResult = model.predict(block_data)

    return prediction
