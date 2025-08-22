#!/usr/bin/env python3
"""
Debug script to test chat functionality
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Load environment variables
load_dotenv()

from app.services.embeddings import search_similar_chunks
from app.services.ai_chat import generate_ai_response
from app.core.config import settings

async def test_chat_functionality():
    """Test the chat functionality step by step"""
    
    print("=== Chat Functionality Debug Test ===\n")
    
    # Test 1: Check environment variables
    print("1. Checking environment variables...")
    print(f"   HUGGINGFACE_API_KEY: {'✓ Set' if settings.HUGGINGFACE_API_KEY else '✗ Missing'}")
    print(f"   HUGGINGFACE_CHAT_MODEL: {settings.HUGGINGFACE_CHAT_MODEL}")
    print(f"   HUGGINGFACE_EMBEDDING_MODEL: {settings.HUGGINGFACE_EMBEDDING_MODEL}")
    print(f"   QDRANT_URL: {'✓ Set' if settings.QDRANT_URL else '✗ Missing'}")
    print(f"   QDRANT_API_KEY: {'✓ Set' if settings.QDRANT_API_KEY else '✗ Missing'}")
    
    # Test 2: Test AI response generation
    print("\n2. Testing AI response generation...")
    try:
        test_message = "What are the operating hours?"
        test_context = "Our store is open Monday to Friday from 9 AM to 6 PM, and Saturday from 10 AM to 4 PM."
        
        response = await generate_ai_response(test_message, test_context)
        print(f"   ✓ AI Response: {response}")
    except Exception as e:
        print(f"   ✗ AI Response Error: {e}")
    
    # Test 3: Test embeddings search (if we have a website_id)
    print("\n3. Testing embeddings search...")
    try:
        # You'll need to replace this with an actual website_id from your database
        website_id = input("Enter a website_id to test embeddings search (or press Enter to skip): ").strip()
        
        if website_id:
            results = await search_similar_chunks(website_id, "operating hours", top_k=3)
            print(f"   ✓ Found {len(results)} similar chunks")
            for i, result in enumerate(results):
                print(f"      {i+1}. Score: {result['score']:.3f}, URL: {result['url']}")
                print(f"         Content: {result['content'][:100]}...")
        else:
            print("   ⚠ Skipped embeddings search test")
    except Exception as e:
        print(f"   ✗ Embeddings Search Error: {e}")
    
    print("\n=== Debug Test Complete ===")

if __name__ == "__main__":
    asyncio.run(test_chat_functionality()) 