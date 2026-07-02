from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv('../.env')

engine = create_engine(
    os.getenv('DATABASE_URL'),
    pool_pre_ping=True,
    pool_recycle=300
)

def get_connection():
    return engine.connect()