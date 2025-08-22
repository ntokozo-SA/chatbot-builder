import asyncio
import httpx
import json
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8000"
WEBSITE_ID = "db32e4bb-4e43-4a35-af5c-444eeb1c6ee4"  # Your Go Glass website ID

# Test questions for the Go Glass website
TEST_QUESTIONS = [
    "What services does Go Glass offer?",
    "Do they install aluminium windows?",
    "What types of doors do they sell?",
    "Do they offer frameless glass balustrades?",
    "What is their contact information?",
    "Do they provide free quotes?",
    "What areas do they serve?",
    "What are their business hours?"
]

async def test_chatbot():
    """Test the chatbot with various questions"""
    print("🤖 Testing Chatbot for Go Glass Website")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        for i, question in enumerate(TEST_QUESTIONS, 1):
            print(f"\n📝 Test {i}: {question}")
            print("-" * 40)
            
            try:
                # Send chat request
                response = await client.post(
                    f"{BACKEND_URL}/api/chat/test",
                    json={
                        "message": question,
                        "website_id": WEBSITE_ID,
                        "conversation_id": None
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Response: {data['message']}")
                    print(f"🔗 Sources: {data.get('sources', [])}")
                    print(f"🎯 Confidence: {data.get('confidence', 'N/A')}")
                else:
                    print(f"❌ Error {response.status_code}: {response.text}")
                    
            except Exception as e:
                print(f"❌ Exception: {e}")
            
            # Small delay between requests
            await asyncio.sleep(1)

async def test_embedding_search():
    """Test the embedding search functionality"""
    print("\n🔍 Testing Embedding Search")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        test_query = "aluminium windows"
        
        try:
            response = await client.get(
                f"{BACKEND_URL}/api/embeddings/search/{WEBSITE_ID}",
                params={"query": test_query, "top_k": 3},
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Search Results for '{test_query}':")
                for i, result in enumerate(data['results'], 1):
                    print(f"  {i}. Score: {result['score']:.3f}")
                    print(f"     Content: {result['content'][:100]}...")
                    print(f"     URL: {result['url']}")
                    print()
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")

async def test_website_status():
    """Check the current website status"""
    print("\n📊 Website Status Check")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BACKEND_URL}/api/websites/{WEBSITE_ID}",
                timeout=10.0
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Website: {data.get('name', 'Unknown')}")
                print(f"   URL: {data.get('url')}")
                print(f"   Status: {data.get('status')}")
                print(f"   Pages Scraped: {data.get('pages_scraped', 0)}")
                print(f"   Total Chunks: {data.get('total_chunks', 0)}")
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")

async def main():
    """Run all tests"""
    print("🧪 Starting Chatbot Tests...")
    print(f"🌐 Backend URL: {BACKEND_URL}")
    print(f"🏢 Website ID: {WEBSITE_ID}")
    
    # Check if backend is running
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BACKEND_URL}/docs", timeout=5.0)
            if response.status_code == 200:
                print("✅ Backend is running!")
            else:
                print("⚠️  Backend might not be running properly")
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("💡 Make sure to start the backend with: python -m uvicorn app.main:app --reload")
        return
    
    # Run tests
    await test_website_status()
    await test_embedding_search()
    await test_chatbot()
    
    print("\n🎉 Testing completed!")

if __name__ == "__main__":
    asyncio.run(main()) 