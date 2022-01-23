from fastapi import APIRouter
from typing import List

from src.app.models.customer_async import Customer as ModelCustomer
from src.app.schema.customer import Customer as SchemaCustomer
from src.app.models.customer_payload import CustomerResult
from src.app.db import db

router = APIRouter()

@router.post("/")
async def create_user(
    customer: SchemaCustomer):
    customer_id = await ModelCustomer.create(**customer.dict())
    return {"customer_id": customer_id}

@router.get("/{id}", response_model=SchemaCustomer)
async def get_customer(id: int):
    customer = await ModelCustomer.get(id)
    return SchemaCustomer(**customer).dict()

@router.get("/", response_model=List[SchemaCustomer])
async def get_all_customers():
    customer = await ModelCustomer.get_all()
    return customer

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)