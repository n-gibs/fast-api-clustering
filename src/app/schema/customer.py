from pydantic import BaseModel

class Customer(BaseModel):
    id: int
    gender: str
    age: int
    annual_income: int
    spend_score: int

    class Config:
        orm_mode = True