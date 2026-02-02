import pytest
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.model.model import Base

DATABASE = 'sqlite:///:memory:'

@pytest.fixture
def session():
    engine = create_engine(DATABASE)
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    yield session

    session.close()