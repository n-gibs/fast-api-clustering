import os
from databases import Database
from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

db = Database(os.environ["DATABASE_URI"])
engine = sqlalchemy.create_engine(
    os.environ["DATABASE_URI"]
)

metadata = sqlalchemy.MetaData()

Session = sessionmaker(bind=engine)
