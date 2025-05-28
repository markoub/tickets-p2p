import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from models import Base, User
from auth import get_password_hash, verify_password, create_access_token, verify_token
import tempfile
import os

# Create a temporary database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def setup_database():
    """Create tables before each test and drop them after"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)

@pytest.fixture
def test_user_data():
    """Sample user data for testing"""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }

class TestAuthUtilities:
    """Test authentication utility functions"""
    
    def test_password_hashing(self):
        """Test password hashing and verification"""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert verify_password(password, hashed) is True
        assert verify_password("wrongpassword", hashed) is False
    
    def test_token_creation_and_verification(self):
        """Test JWT token creation and verification"""
        user_data = {"sub": "1", "user_id": 1}
        token = create_access_token(data=user_data)
        
        assert token is not None
        assert isinstance(token, str)
        
        # Verify token
        payload = verify_token(token)
        assert payload["sub"] == "1"
        assert payload["user_id"] == 1

class TestUserRegistration:
    """Test user registration endpoint"""
    
    def test_register_user_success(self, client, setup_database, test_user_data):
        """Test successful user registration"""
        response = client.post("/api/auth/register", json=test_user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert "user" in data
        assert "token" in data
        assert data["user"]["username"] == test_user_data["username"]
        assert data["user"]["email"] == test_user_data["email"]
        assert data["token"]["access_token"] is not None
        assert "password" not in data  # Password should not be returned
    
    def test_register_user_duplicate_username(self, client, setup_database, test_user_data):
        """Test registration with duplicate username"""
        # Register first user
        client.post("/api/auth/register", json=test_user_data)
        
        # Try to register with same username
        duplicate_data = test_user_data.copy()
        duplicate_data["email"] = "different@example.com"
        response = client.post("/api/auth/register", json=duplicate_data)
        
        assert response.status_code == 400
        assert "username already taken" in response.json()["detail"].lower()
    
    def test_register_user_duplicate_email(self, client, setup_database, test_user_data):
        """Test registration with duplicate email"""
        # Register first user
        client.post("/api/auth/register", json=test_user_data)
        
        # Try to register with same email
        duplicate_data = test_user_data.copy()
        duplicate_data["username"] = "differentuser"
        response = client.post("/api/auth/register", json=duplicate_data)
        
        assert response.status_code == 400
        assert "email already registered" in response.json()["detail"].lower()
    
    def test_register_user_invalid_data(self, client, setup_database):
        """Test registration with invalid data"""
        invalid_data = {
            "username": "",  # Empty username
            "email": "invalid-email",  # Invalid email format
            "password": "123"  # Too short password
        }
        
        response = client.post("/api/auth/register", json=invalid_data)
        assert response.status_code == 422  # Validation error

class TestUserLogin:
    """Test user login endpoint"""
    
    def test_login_success(self, client, setup_database, test_user_data):
        """Test successful user login"""
        # Register user first
        client.post("/api/auth/register", json=test_user_data)
        
        # Login with correct credentials (using email)
        login_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
        response = client.post("/api/auth/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "user" in data
        assert "token" in data
        assert data["user"]["username"] == test_user_data["username"]
        assert data["user"]["email"] == test_user_data["email"]
        assert data["token"]["access_token"] is not None
    
    def test_login_wrong_password(self, client, setup_database, test_user_data):
        """Test login with wrong password"""
        # Register user first
        client.post("/api/auth/register", json=test_user_data)
        
        # Login with wrong password
        login_data = {
            "email": test_user_data["email"],
            "password": "wrongpassword"
        }
        response = client.post("/api/auth/login", json=login_data)
        
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()
    
    def test_login_nonexistent_user(self, client, setup_database):
        """Test login with non-existent user"""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "password123"
        }
        response = client.post("/api/auth/login", json=login_data)
        
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()

class TestProtectedEndpoints:
    """Test protected endpoints and authentication middleware"""
    
    def test_get_current_user_success(self, client, setup_database, test_user_data):
        """Test getting current user with valid token"""
        # Register and get token
        register_response = client.post("/api/auth/register", json=test_user_data)
        token = register_response.json()["token"]["access_token"]
        
        # Access protected endpoint
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/auth/me", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == test_user_data["username"]
        assert data["email"] == test_user_data["email"]
        assert "created_at" in data
    
    def test_get_current_user_no_token(self, client, setup_database):
        """Test accessing protected endpoint without token"""
        response = client.get("/api/auth/me")
        
        assert response.status_code == 403  # FastAPI returns 403 for missing auth
        assert "not authenticated" in response.json()["detail"].lower()
    
    def test_get_current_user_invalid_token(self, client, setup_database):
        """Test accessing protected endpoint with invalid token"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/auth/me", headers=headers)
        
        assert response.status_code == 401
        assert "could not validate credentials" in response.json()["detail"].lower()
    
    def test_logout_success(self, client, setup_database, test_user_data):
        """Test successful logout"""
        # Register and get token
        register_response = client.post("/api/auth/register", json=test_user_data)
        token = register_response.json()["token"]["access_token"]
        
        # Logout
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post("/api/auth/logout", headers=headers)
        
        assert response.status_code == 200
        assert "logged out" in response.json()["message"].lower()
    
    def test_logout_no_token(self, client, setup_database):
        """Test logout without token"""
        response = client.post("/api/auth/logout")
        
        assert response.status_code == 403  # FastAPI returns 403 for missing auth
        assert "not authenticated" in response.json()["detail"].lower()

class TestInputValidation:
    """Test input validation and error handling"""
    
    def test_register_missing_fields(self, client, setup_database):
        """Test registration with missing required fields"""
        incomplete_data = {"username": "testuser"}
        response = client.post("/api/auth/register", json=incomplete_data)
        
        assert response.status_code == 422
    
    def test_register_invalid_email_format(self, client, setup_database):
        """Test registration with invalid email format"""
        invalid_data = {
            "username": "testuser",
            "email": "not-an-email",
            "password": "password123"
        }
        response = client.post("/api/auth/register", json=invalid_data)
        
        assert response.status_code == 422
    
    def test_register_short_password(self, client, setup_database):
        """Test registration with too short password"""
        invalid_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "123"
        }
        response = client.post("/api/auth/register", json=invalid_data)
        
        assert response.status_code == 422

# Cleanup after tests
def teardown_module():
    """Clean up test database"""
    if os.path.exists("test.db"):
        os.remove("test.db") 