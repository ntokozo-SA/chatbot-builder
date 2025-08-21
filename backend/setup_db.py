#!/usr/bin/env python3
"""
Database Setup Script for AI Chatbot Builder
This script helps set up the required database tables in Supabase.
"""

import os
import sys
from pathlib import Path

def read_sql_file(file_path):
    """Read SQL file content"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: SQL file not found: {file_path}")
        return None

def setup_database():
    """Set up the database tables"""
    print("🚀 Setting up AI Chatbot Builder Database...")
    print("=" * 50)
    
    # Read the setup SQL file
    sql_file = Path(__file__).parent / "setup_database.sql"
    sql_content = read_sql_file(sql_file)
    
    if not sql_content:
        print("❌ Failed to read SQL setup file")
        return False
    
    print("📋 SQL Setup Script:")
    print("-" * 30)
    print(sql_content)
    print("-" * 30)
    
    print("\n📝 Instructions to run this setup:")
    print("1. Go to your Supabase dashboard")
    print("2. Navigate to SQL Editor")
    print("3. Copy and paste the SQL content above")
    print("4. Click 'Run' to execute the script")
    print("\nAlternatively, you can run the individual migration files:")
    print("- backend/migrations/001_create_users_table.sql")
    print("- backend/migrations/002_create_websites_table.sql") 
    print("- backend/migrations/003_create_conversations_table.sql")
    
    print("\n✅ After running the SQL script, your database will have:")
    print("   - users table (for authentication)")
    print("   - websites table (for storing user websites)")
    print("   - conversations table (for chat history)")
    print("   - messages table (for individual messages)")
    
    return True

def check_environment():
    """Check if environment variables are set"""
    print("\n🔍 Checking environment setup...")
    
    required_vars = [
        'SUPABASE_URL',
        'SUPABASE_ANON_KEY', 
        'SUPABASE_SERVICE_ROLE_KEY',
        'SECRET_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n📝 Please set these in your .env file")
        return False
    else:
        print("✅ All required environment variables are set")
        return True

if __name__ == "__main__":
    print("AI Chatbot Builder - Database Setup")
    print("=" * 40)
    
    # Check environment
    env_ok = check_environment()
    
    # Setup database
    setup_ok = setup_database()
    
    if setup_ok and env_ok:
        print("\n🎉 Setup instructions completed!")
        print("Next steps:")
        print("1. Run the SQL script in your Supabase dashboard")
        print("2. Start your backend: python -m uvicorn app.main:app --reload")
        print("3. Start your frontend: npm run dev")
    else:
        print("\n⚠️  Please fix the issues above before proceeding")
        sys.exit(1) 