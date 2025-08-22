import asyncio
from app.services.scraper import scrape_website
from app.services.embeddings import EmbeddingService
from app.core.database import get_supabase
from app.models.website import WebsiteStatus
from datetime import datetime

async def test_scraping():
    website_id = 'db32e4bb-4e43-4a35-af5c-444eeb1c6ee4'
    website_url = 'https://www.goglass.co.za/'
    
    supabase = await get_supabase()
    
    try:
        print("Starting website scraping...")
        
        # Update status to scraping
        supabase.table("websites").update({
            "status": WebsiteStatus.SCRAPING.value,
            "updated_at": datetime.utcnow().isoformat()
        }).eq("id", website_id).execute()
        
        # Scrape website
        print("Scraping website content...")
        scraped_content = await scrape_website(website_url)
        print(f"Scraped {len(scraped_content)} pages")
        
        # Update status to processing
        supabase.table("websites").update({
            "status": WebsiteStatus.PROCESSING.value,
            "pages_scraped": len(scraped_content),
            "updated_at": datetime.utcnow().isoformat()
        }).eq("id", website_id).execute()
        
        # Process embeddings
        print("Processing embeddings...")
        embedding_service = EmbeddingService()
        total_chunks = await embedding_service.process_website_embeddings(website_id, scraped_content)
        print(f"Processed {total_chunks} chunks")
        
        # Update status to completed
        supabase.table("websites").update({
            "status": WebsiteStatus.COMPLETED.value,
            "total_chunks": total_chunks,
            "last_scraped_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }).eq("id", website_id).execute()
        
        print("Website processing completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        # Update status to failed
        supabase.table("websites").update({
            "status": WebsiteStatus.FAILED.value,
            "error_message": str(e),
            "updated_at": datetime.utcnow().isoformat()
        }).eq("id", website_id).execute()

if __name__ == "__main__":
    asyncio.run(test_scraping()) 