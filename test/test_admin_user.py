import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import the app directly in the test file
from main import app
from database import Base, get_db
from models.admin import Admin
from utils import get_password_hash

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_db():
    # Drop all tables to ensure a clean state
    Base.metadata.drop_all(bind=engine)

    # Create the tables in the test database
    Base.metadata.create_all(bind=engine)

    # Create the admin user
    db = TestingSessionLocal()
    admin = Admin(
        name="Administrator",
        email="admin@example.com",
        hashed_password=get_password_hash("securepassword"),
        role="admin",
        is_active=True,
    )
    db.add(admin)
    db.commit()
    db.close()

    yield

    # Drop all tables after the tests
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def admin_token(setup_db):
    response = client.post(
        "/admin/login",
        data={"username": "admin@example.com", "password": "securepassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    return response.json()["token_de_acceso"]

def test_create_admin(admin_token):
    user_data = {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "password": "password123",
        "is_active": True,
        "role": "admin",
    }

    headers = {
        "Authorization": f"Bearer {admin_token}",
    }

    response = client.post("/admin/register", json=user_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "johndoe@example.com"

def test_read_admins(admin_token):
    headers = {
        "Authorization": f"Bearer {admin_token}",
    }

    response = client.get("/admin/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_admin(admin_token):
    headers = {
        "Authorization": f"Bearer {admin_token}",
    }

    # Use a unique email for the update
    user_update_data = {
        "name": "John Smith",
        "email": "johnsmith@example.com",
        "password": "password123",
        "is_active": True,
        "role": "admin",
    }

    # Assuming admin with ID 1 exists
    response = client.put("/admin/1", json=user_update_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "John Smith"

def test_delete_admin(admin_token):
    headers = {
        "Authorization": f"Bearer {admin_token}",
    }

    # Create the admin
    response = client.post(
        "/admin/register",
        json={
            "name": "John Doe",
            "email": "johndoe2@example.com",
            "password": "password123",
            "is_active": True,
            "role": "admin",
        },
        headers=headers,
    )
    assert response.status_code == 200

    # Get the admin ID
    admin_id = response.json()["id"]

    # Delete the admin
    response = client.delete(f"/admin/{admin_id}", headers=headers)
    assert response.status_code == 204
    assert response.content == b""  # Check if the response is empty