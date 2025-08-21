#!/usr/bin/env python3
"""
Test script to verify the registration endpoint works correctly
"""

import asyncio
import sys
import json
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent / "app"))

async def test_registration():
    """Test the registration endpoint"""
    
    print("🧪 Testing Registration Endpoint...")
    print("=" * 50)
    
    try:
        # Import the necessary modules
        from app.api.auth import register
        from app.models.user import UserCreate
        from app.core.database import get_supabase
        
        # Test data
        test_user = UserCreate(
            email="test@example.com",
            password="password123",
            full_name="Test User"
        )
        
        print(f"📝 Testing registration for: {test_user.email}")
        
        # Test the registration function
        result = await register(test_user)
        
        print("✅ Registration successful!")
        print(f"   User ID: {result.user.id}")
        print(f"   Email: {result.user.email}")
        print(f"   Full Name: {result.user.full_name}")
        print(f"   Token: {result.access_token[:20]}...")
        
        # Verify the user was saved in the database
        print("\n🔍 Verifying user in database...")
        supabase = await get_supabase()
        db_user = supabase.table("users").select("*").eq("email", test_user.email).single().execute()
        
        if db_user.data:
            print("✅ User found in database!")
            print(f"   Has password_hash: {'password_hash' in db_user.data}")
            print(f"   Is active: {db_user.data.get('is_active', False)}")
        else:
            print("❌ User not found in database!")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Registration test failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_registration())
    sys.exit(0 if success else 1) 