from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# User schemas
class UserBase(BaseModel):
    """Base user schema with common fields"""
    username: str = Field(..., min_length=3, max_length=50, description="Username must be 3-50 characters")
    email: EmailStr = Field(..., description="Valid email address")

class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=6, max_length=100, description="Password must be at least 6 characters")

class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., description="Password")

class UserResponse(UserBase):
    """Schema for user response (without password)"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Authentication schemas
class Token(BaseModel):
    """Schema for authentication token"""
    access_token: str
    token_type: str = "bearer"

class UserWithToken(BaseModel):
    """Schema for user response with authentication token"""
    user: UserResponse
    token: Token

class TokenData(BaseModel):
    """Schema for token payload data"""
    username: Optional[str] = None
    user_id: Optional[int] = None

# Response schemas
class MessageResponse(BaseModel):
    """Schema for simple message responses"""
    message: str

class ErrorResponse(BaseModel):
    """Schema for error responses"""
    detail: str 