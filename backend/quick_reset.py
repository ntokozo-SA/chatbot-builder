import asyncio
from app.core.database import get_supabase
from app.models.website import WebsiteStatus

async def reset_website():
    supabase = await get_supabase()
    result = supabase.table('websites').update({
        "status": WebsiteStatus.PENDING.value,
        "pages_scraped": 0,
        "total_chunks": 0,
        "error_message": None
    }).eq("id", "0739d78d-537e-4052-9826-8c96127a57b8").execute()
    print("Website reset to pending status")

asyncio.run(reset_website()) 