from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from typing import List
from app.core.database import get_supabase
from app.core.auth import get_current_active_user
from app.models.user import User
from app.models.website import Website, WebsiteCreate, WebsiteUpdate, WebsiteStatus
from app.services.scraper import scrape_website
from app.services.embeddings import process_website_embeddings
from datetime import datetime
import uuid

router = APIRouter()

@router.post("/", response_model=Website)
async def create_website(
    website_data: WebsiteCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new website for the current user"""
    supabase = await get_supabase()
    
    try:
        # Check if user already has this website
        existing_website = supabase.table("websites").select("id").eq("user_id", current_user.id).eq("url", str(website_data.url)).execute()
        if existing_website.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Website already exists for this user"
            )
        
        # Create website record
        website_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        website_record = {
            "id": website_id,
            "user_id": current_user.id,
            "url": str(website_data.url),
            "name": website_data.name or f"Website {len(existing_website.data) + 1}",
            "description": website_data.description,
            "status": WebsiteStatus.PENDING.value,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat()
        }
        
        response = supabase.table("websites").insert(website_record).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create website"
            )
        
        return Website(**response.data[0])
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create website: {str(e)}"
        )

@router.get("/", response_model=List[Website])
async def get_user_websites(current_user: User = Depends(get_current_active_user)):
    """Get all websites for the current user"""
    supabase = await get_supabase()
    
    try:
        response = supabase.table("websites").select("*").eq("user_id", current_user.id).order("created_at", desc=True).execute()
        return [Website(**website) for website in response.data]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch websites: {str(e)}"
        )

@router.get("/{website_id}", response_model=Website)
async def get_website(
    website_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific website by ID"""
    supabase = await get_supabase()
    
    try:
        response = supabase.table("websites").select("*").eq("id", website_id).eq("user_id", current_user.id).single().execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Website not found"
            )
        
        return Website(**response.data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch website: {str(e)}"
        )

@router.put("/{website_id}", response_model=Website)
async def update_website(
    website_id: str,
    website_update: WebsiteUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update a website"""
    supabase = await get_supabase()
    
    try:
        # Check if website exists and belongs to user
        existing_website = supabase.table("websites").select("id").eq("id", website_id).eq("user_id", current_user.id).execute()
        if not existing_website.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Website not found"
            )
        
        update_data = website_update.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No update data provided"
            )
        
        update_data["updated_at"] = datetime.utcnow().isoformat()
        
        response = supabase.table("websites").update(update_data).eq("id", website_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update website"
            )
        
        return Website(**response.data[0])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update website: {str(e)}"
        )

@router.delete("/{website_id}")
async def delete_website(
    website_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a website"""
    supabase = await get_supabase()
    
    try:
        # Check if website exists and belongs to user
        existing_website = supabase.table("websites").select("id").eq("id", website_id).eq("user_id", current_user.id).execute()
        if not existing_website.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Website not found"
            )
        
        # Delete website
        supabase.table("websites").delete().eq("id", website_id).execute()
        
        return {"message": "Website deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete website: {str(e)}"
        )

@router.post("/{website_id}/scrape")
async def start_website_scraping(
    website_id: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user)
):
    """Start scraping a website"""
    supabase = await get_supabase()
    
    try:
        # Check if website exists and belongs to user
        website_response = supabase.table("websites").select("*").eq("id", website_id).eq("user_id", current_user.id).single().execute()
        if not website_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Website not found"
            )
        
        website = Website(**website_response.data)
        
        # Update status to scraping
        supabase.table("websites").update({
            "status": WebsiteStatus.SCRAPING.value,
            "updated_at": datetime.utcnow().isoformat()
        }).eq("id", website_id).execute()
        
        # Start background scraping task
        background_tasks.add_task(scrape_and_process_website, website_id, website.url)
        
        return {"message": "Website scraping started", "website_id": website_id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start scraping: {str(e)}"
        )

async def scrape_and_process_website(website_id: str, website_url: str):
    """Background task to scrape and process website"""
    supabase = await get_supabase()
    
    try:
        # Scrape website
        scraped_content = await scrape_website(website_url)
        
        # Update status to processing
        supabase.table("websites").update({
            "status": WebsiteStatus.PROCESSING.value,
            "pages_scraped": len(scraped_content),
            "updated_at": datetime.utcnow().isoformat()
        }).eq("id", website_id).execute()
        
        # Process embeddings
        total_chunks = await process_website_embeddings(website_id, scraped_content)
        
        # Update status to completed
        supabase.table("websites").update({
            "status": WebsiteStatus.COMPLETED.value,
            "total_chunks": total_chunks,
            "last_scraped_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }).eq("id", website_id).execute()
        
    except Exception as e:
        # Update status to failed
        supabase.table("websites").update({
            "status": WebsiteStatus.FAILED.value,
            "error_message": str(e),
            "updated_at": datetime.utcnow().isoformat()
        }).eq("id", website_id).execute() 