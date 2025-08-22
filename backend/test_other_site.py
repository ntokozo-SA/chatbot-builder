import asyncio
import logging
from app.services.scraper import scrape_website

logging.basicConfig(level=logging.INFO)

async def test_other_sites():
    """Test scraping with different websites"""
    
    # Test websites that are known to work well with static scraping
    test_sites = [
        "https://example.com",
        "https://httpbin.org/html",
        "https://quotes.toscrape.com",
        "https://books.toscrape.com"
    ]
    
    for url in test_sites:
        print(f"\n🔍 Testing: {url}")
        print("-" * 50)
        
        try:
            result = await scrape_website(url)
            print(f"✅ Success! Found {len(result)} pages")
            
            if result:
                print(f"   Sample page: {result[0]['url']}")
                print(f"   Content length: {len(result[0]['content'])} characters")
                print(f"   Content preview: {result[0]['content'][:100]}...")
            else:
                print("   ⚠️  No pages found")
                
        except Exception as e:
            print(f"❌ Failed: {e}")
        
        print("-" * 30)

if __name__ == "__main__":
    asyncio.run(test_other_sites()) 