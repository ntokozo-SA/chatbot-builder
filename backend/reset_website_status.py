import asyncio
from app.core.database import get_supabase
from app.models.website import WebsiteStatus

async def reset_website_status():
    supabase = await get_supabase()
    
    # Get the specific website that failed
    website_id = 'db32e4bb-4e43-4a35-af5c-444eeb1c6ee4'
    
    # Reset the specific website to pending status
    result = supabase.table('websites').update({
        'status': WebsiteStatus.PENDING.value,
        'pages_scraped': 0,
        'total_chunks': 0,
        'error_message': None,
        'updated_at': '2025-08-22T15:53:53.307645+00:00'
    }).eq('id', website_id).execute()
    
    print("Website status reset successfully")
    print("Result:", result.data)

if __name__ == "__main__":
    asyncio.run(reset_website_status()) 