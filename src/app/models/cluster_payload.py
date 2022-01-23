from pydantic import BaseModel

class CustomerSegmentationPayload(BaseModel):
    table_name: str
