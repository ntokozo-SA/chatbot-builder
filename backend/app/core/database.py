from supabase import create_client, Client
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Initialize Supabase client
supabase: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_ANON_KEY
)

# Service role client for admin operations
supabase_admin: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_SERVICE_ROLE_KEY
)

async def get_supabase() -> Client:
    """Get Supabase client instance"""
    return supabase

async def get_supabase_admin() -> Client:
    """Get Supabase admin client instance for privileged operations"""
    return supabase_admin

async def test_connection():
    """Test database connection"""
    try:
        # Try to fetch a single row from a test table or use a simple query
        result = supabase.table("users").select("id").limit(1).execute()
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False 