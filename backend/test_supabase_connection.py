#!/usr/bin/env python3
"""
Test Supabase Connection and Websites Table Access
"""

import os
import asyncio
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

async def test_supabase_connection():
    """Test Supabase connection and table access"""
    
    print("🔍 Testing Supabase Connection...")
    print("=" * 50)
    
    # Get environment variables
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    print(f"Supabase URL: {supabase_url}")
    print(f"Supabase Key: {supabase_key[:20]}..." if supabase_key else "Not set")
    
    if not supabase_url or not supabase_key:
        print("❌ Missing Supabase credentials")
        return False
    
    try:
        # Create Supabase client
        supabase: Client = create_client(supabase_url, supabase_key)
        print("✅ Supabase client created successfully")
        
        # Test connection by checking if we can query the users table
        print("\n🔍 Testing users table access...")
        users_response = supabase.table("users").select("id").limit(1).execute()
        print(f"✅ Users table accessible: {len(users_response.data)} rows found")
        
        # Test websites table access
        print("\n🔍 Testing websites table access...")
        try:
            websites_response = supabase.table("websites").select("id").limit(1).execute()
            print(f"✅ Websites table accessible: {len(websites_response.data)} rows found")
            
            # Show table structure
            print("\n📋 Websites table structure:")
            if websites_response.data:
                for key in websites_response.data[0].keys():
                    print(f"  - {key}")
            else:
                print("  - Table is empty")
                
        except Exception as e:
            print(f"❌ Websites table error: {str(e)}")
            
            # Try to get more details about the error
            if "PGRST205" in str(e):
                print("\n🔧 This is a PostgREST schema cache issue!")
                print("Solutions:")
                print("1. Restart PostgREST in Supabase Dashboard")
                print("2. Run: NOTIFY pgrst, 'reload schema'; in SQL Editor")
                print("3. Wait 30-60 seconds after restart")
            
            return False
        
        # Test inserting a dummy record
        print("\n🔍 Testing website creation...")
        try:
            # Get a user ID first
            users = supabase.table("users").select("id").limit(1).execute()
            if users.data:
                user_id = users.data[0]['id']
                
                # Try to insert a test website
                test_website = {
                    "url": "https://test.example.com",
                    "user_id": user_id,
                    "name": "Test Website"
                }
                
                insert_response = supabase.table("websites").insert(test_website).execute()
                print(f"✅ Website creation successful: {insert_response.data[0]['id']}")
                
                # Clean up - delete the test record
                supabase.table("websites").delete().eq("url", "https://test.example.com").execute()
                print("✅ Test record cleaned up")
                
            else:
                print("⚠️  No users found - cannot test website creation")
                
        except Exception as e:
            print(f"❌ Website creation failed: {str(e)}")
            return False
        
        print("\n🎉 All tests passed! Your Supabase connection is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Supabase connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(test_supabase_connection()) 