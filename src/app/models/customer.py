from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    gender = Column(String)
    age = Column(Integer)
    annual_income = Column(String)
    spend_score = Column(String)


    class Config:
            orm_mode = True
