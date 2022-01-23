from pydantic import BaseModel


class CustomerResult(BaseModel):
    customers: list