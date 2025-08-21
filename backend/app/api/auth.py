from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer
from app.core.database import get_supabase, get_supabase_admin
from app.core.auth import verify_password, get_password_hash, create_access_token, get_current_active_user
from app.models.user import UserCreate, User, UserLogin, Token, UserUpdate
from datetime import datetime
import uuid
import logging

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()
security = HTTPBearer()

@router.post("/register", response_model=Token)
async def register(user_data: UserCreate):
    """
    Register a new user with proper password hashing and database storage.
    
    Args:
        user_data: UserCreate model containing email, password, and full_name
        
    Returns:
        Token: JWT token and user information
        
    Raises:
        HTTPException: 400 if email already exists, 500 for server errors
    """
    logger.info(f"Registration attempt for email: {user_data.email}")
    
    try:
        # Get Supabase client
        supabase = await get_supabase()
        
        # Check if user already exists
        logger.info(f"Checking if user exists: {user_data.email}")
        existing_user = supabase.table("users").select("id").eq("email", user_data.email).execute()
        
        if existing_user.data:
            logger.warning(f"Registration failed - email already exists: {user_data.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash the password using bcrypt
        logger.info(f"Hashing password for: {user_data.email}")
        password_hash = get_password_hash(user_data.password)
        
        # Create user profile in database with hashed password
        user_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        user_profile = {
            "id": user_id,
            "email": user_data.email.lower().strip(),
            "password_hash": password_hash,  # Save the hashed password
            "full_name": user_data.full_name.strip() if user_data.full_name else None,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
            "is_active": True
        }
        
        logger.info(f"Creating user profile in database: {user_data.email}")
        profile_response = supabase.table("users").insert(user_profile).execute()
        
        if not profile_response.data:
            logger.error(f"Failed to create user profile in database: {user_data.email}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user profile"
            )
        
        # Create access token
        logger.info(f"Creating access token for: {user_data.email}")
        access_token = create_access_token(data={"sub": user_data.email})
        
        # Prepare user data for response (exclude password_hash)
        user_response_data = {
            "id": user_id,
            "email": user_data.email.lower().strip(),
            "full_name": user_data.full_name.strip() if user_data.full_name else None,
            "created_at": now,
            "updated_at": now,
            "is_active": True
        }
        
        # Log successful registration
        logger.info(f"User registered successfully: {user_data.email}")
        
        return Token(
            access_token=access_token,
            user=User(**user_response_data)
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as they already have proper status codes
        raise
    except Exception as e:
        # Log the full error for debugging
        logger.error(f"Registration failed for {user_data.email}: {str(e)}", exc_info=True)
        
        # Return a generic error message to the client
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed. Please try again later."
        )

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    """
    Login user and return access token.
    
    Args:
        user_credentials: UserLogin model containing email and password
        
    Returns:
        Token: JWT token and user information
        
    Raises:
        HTTPException: 401 for invalid credentials, 500 for server errors
    """
    logger.info(f"Login attempt for email: {user_credentials.email}")
    
    try:
        # Get Supabase client
        supabase = await get_supabase()
        
        # Get user from database
        logger.info(f"Fetching user profile: {user_credentials.email}")
        user_response = supabase.table("users").select("*").eq("email", user_credentials.email.lower().strip()).single().execute()
        
        if not user_response.data:
            logger.warning(f"Login failed - user not found: {user_credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        user_data = user_response.data
        
        # Check if user is active
        if not user_data.get("is_active", True):
            logger.warning(f"Login attempt for inactive user: {user_credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is deactivated"
            )
        
        # Verify password
        logger.info(f"Verifying password for: {user_credentials.email}")
        if not verify_password(user_credentials.password, user_data.get("password_hash", "")):
            logger.warning(f"Login failed - invalid password for: {user_credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Create access token
        logger.info(f"Creating access token for: {user_credentials.email}")
        access_token = create_access_token(data={"sub": user_credentials.email})
        
        # Log successful login
        logger.info(f"User logged in successfully: {user_credentials.email}")
        
        return Token(
            access_token=access_token,
            user=User(**user_data)
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as they already have proper status codes
        raise
    except Exception as e:
        # Log the full error for debugging
        logger.error(f"Login failed for {user_credentials.email}: {str(e)}", exc_info=True)
        
        # Return a generic error message to the client
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed. Please try again later."
        )

@router.get("/me", response_model=User)
async def get_current_user_profile(current_user: User = Depends(get_current_active_user)):
    """Get current user profile"""
    return current_user

@router.put("/me", response_model=User)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update current user profile"""
    supabase = await get_supabase()
    
    try:
        update_data = user_update.dict(exclude_unset=True)
        if not update_data:
            return current_user
        
        update_data["updated_at"] = datetime.utcnow().isoformat()
        
        # Update user profile
        response = supabase.table("users").update(update_data).eq("id", current_user.id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        updated_user = response.data[0]
        return User(**updated_user)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Update failed: {str(e)}"
        )

@router.post("/logout")
async def logout():
    """Logout user (client should discard token)"""
    return {"message": "Successfully logged out"}

@router.post("/refresh")
async def refresh_token(current_user: User = Depends(get_current_active_user)):
    """Refresh access token"""
    access_token = create_access_token(data={"sub": current_user.email})
    return {"access_token": access_token, "token_type": "bearer"} 