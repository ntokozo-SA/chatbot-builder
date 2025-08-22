from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional
from datetime import datetime
import re

class UserBase(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    full_name: Optional[str] = Field(None, max_length=100, description="User's full name")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=128, description="User's password")
    full_name: str = Field(..., min_length=2, max_length=100, description="User's full name")
    
    @validator('password')
    def validate_password(cls, v):
        """Validate password strength"""
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        if len(v) > 128:
            raise ValueError('Password must be less than 128 characters')
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('Password must contain at least one letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v
    
    @validator('full_name')
    def validate_full_name(cls, v):
        """Validate full name"""
        if not v or not v.strip():
            raise ValueError('Full name is required')
        if len(v.strip()) < 2:
            raise ValueError('Full name must be at least 2 characters long')
        if len(v.strip()) > 100:
            raise ValueError('Full name must be less than 100 characters')
        return v.strip()
    
    @validator('email')
    def validate_email(cls, v):
        """Normalize email to lowercase"""
        return v.lower().strip() if v else v

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, description="User's email address")
    full_name: Optional[str] = Field(None, min_length=2, max_length=100, description="User's full name")
    website_url: Optional[str] = Field(None, max_length=500, description="User's website URL")
    company_name: Optional[str] = Field(None, max_length=200, description="User's company name")
    
    @validator('full_name')
    def validate_full_name(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError('Full name cannot be empty')
            if len(v.strip()) < 2:
                raise ValueError('Full name must be at least 2 characters long')
            if len(v.strip()) > 100:
                raise ValueError('Full name must be less than 100 characters')
            return v.strip()
        return v
    
    @validator('website_url')
    def validate_website_url(cls, v):
        if v is not None:
            if not v.startswith(('http://', 'https://')):
                raise ValueError('Website URL must start with http:// or https://')
            if len(v) > 500:
                raise ValueError('Website URL must be less than 500 characters')
        return v

class UserInDB(UserBase):
    id: str = Field(..., description="Unique user identifier")
    created_at: datetime = Field(..., description="User creation timestamp")
    updated_at: datetime = Field(..., description="User last update timestamp")
    website_url: Optional[str] = Field(None, max_length=500, description="User's website URL")
    company_name: Optional[str] = Field(None, max_length=200, description="User's company name")
    is_active: bool = Field(True, description="Whether the user account is active")

class User(UserInDB):
    pass

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")
    
    @validator('email')
    def validate_email(cls, v):
        """Normalize email to lowercase"""
        return v.lower().strip() if v else v
    
    @validator('password')
    def validate_password(cls, v):
        """Validate password is not empty"""
        if not v or len(v.strip()) == 0:
            raise ValueError('Password is required')
        return v

class Token(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type")
    user: User = Field(..., description="User information")

class TokenData(BaseModel):
    email: Optional[str] = Field(None, description="User email from token") 