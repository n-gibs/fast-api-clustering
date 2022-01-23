from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

import sqlalchemy
from src.app.db import db, metadata, sqlalchemy

customers = sqlalchemy.Table(
    "customers",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("gender", sqlalchemy.String),
    sqlalchemy.Column("age", sqlalchemy.Integer),
    sqlalchemy.Column("annual_income", sqlalchemy.Integer),
    sqlalchemy.Column("spend_score", sqlalchemy.Integer),
)


class Customer:
    @classmethod
    async def get(cls, id):
        query = customers.select().where(customers.c.id == id)
        customer = await db.fetch_one(query)
        return customer

    @classmethod
    async def get_all(cls):
        query = customers.select().limit(5)
        all_customers = await db.fetch_all(query)
        for cust in all_customers:
            print(type(cust))
            for item in cust:
                print(item)

        return all_customers

    @classmethod
    async def create(cls, **customer):
        query = customers.insert().values(**customer)
        customer_id = await db.execute(query)
        return customer_id
