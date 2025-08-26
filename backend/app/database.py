import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker


user = os.environ["PGUSER"]
password = os.environ["PGPASS"]

url = URL.create("postgresql", username=user, password=password, host="localhost", database="Dummy")
engine = create_engine(url)

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()