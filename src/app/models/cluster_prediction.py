from pydantic import BaseModel


class CustomerSegmentationResult(BaseModel):
    clusters: dict