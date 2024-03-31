from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, drop_database, database_exists
import pytest
from main import app
from routers import get_db, create_user, get_user, update_user, delete_user
from models import Base
from schemas import UserCreate, UserUpdate

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

#SQLAlchemy engine and session for testing
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def setup_module(module):
    if not database_exists(SQLALCHEMY_DATABASE_URL):
        create_database(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(bind=engine)

@pytest.fixture
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

client = TestClient(app)

user_id = None

def test_create_user():
    global user_id
    user_data = {"name": "Test User", "email": "test@example.com", "password": "password"}
    response = client.post("/api/create/", json=user_data)    
    assert response.status_code == 200  
    assert response.json()["name"] == "Test User"
    assert response.json()["email"] == "test@example.com"
    user_id = response.json()["id"]

def test_get_user():
    global user_id
    response = client.get(f"/api/user/{user_id}")
    assert response.status_code == 200

def test_update_user():
    global user_id
    updated_user_data = {"name": "Updated"}
    response = client.put(f"/api/update/{user_id}", json=updated_user_data)
    assert response.status_code == 200

def test_delete_user():
    global user_id
    response = client.delete(f"/api/delete/{user_id}")
    assert response.status_code == 200
