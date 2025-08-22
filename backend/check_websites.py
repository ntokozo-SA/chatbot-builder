import asyncio
from app.core.database import get_supabase

async def check_websites():
    supabase = await get_supabase()
    result = supabase.table('websites').select('*').execute()
    print('Websites:', result.data)
    
    if result.data:
        for website in result.data:
            print(f"Website: {website.get('name', 'Untitled')}")
            print(f"URL: {website.get('url')}")
            print(f"Status: {website.get('status')}")
            print(f"Pages scraped: {website.get('pages_scraped', 0)}")
            print(f"Total chunks: {website.get('total_chunks', 0)}")
            print(f"Error: {website.get('error_message', 'None')}")
            print("-" * 50)
    else:
        print("No websites found in database")

if __name__ == "__main__":
    asyncio.run(check_websites()) 