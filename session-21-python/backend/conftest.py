import os
import pytest
from fastapi.testclient import TestClient

# Ensure test DB is used
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from app.main import app
from app.db import Base, engine

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test.db"):
        try:
            os.remove("./test.db")
        except OSError:
            pass

@pytest.fixture
def client():
    return TestClient(app)
