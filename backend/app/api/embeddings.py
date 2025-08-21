from fastapi import APIRouter, HTTPException, status, Depends
from app.core.database import get_supabase
from app.core.auth import get_current_active_user
from app.models.user import User
from app.services.embeddings import search_similar_chunks
from typing import List, Dict, Any

router = APIRouter()

@router.get("/search/{website_id}")
async def search_embeddings(
    website_id: str,
    query: str,
    top_k: int = 5,
    current_user: User = Depends(get_current_active_user)
):
    """Search embeddings for a specific website"""
    supabase = await get_supabase()
    
    try:
        # Verify website belongs to user
        website_response = supabase.table("websites").select("id, status").eq("id", website_id).eq("user_id", current_user.id).single().execute()
        if not website_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Website not found"
            )
        
        if website_response.data["status"] != "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Website is not ready for search. Please wait for processing to complete."
            )
        
        # Search for similar chunks
        results = await search_similar_chunks(website_id, query, top_k)
        
        return {
            "query": query,
            "website_id": website_id,
            "results": results,
            "total_results": len(results)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )

@router.get("/stats/{website_id}")
async def get_embedding_stats(
    website_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get embedding statistics for a website"""
    supabase = await get_supabase()
    
    try:
        # Verify website belongs to user
        website_response = supabase.table("websites").select("*").eq("id", website_id).eq("user_id", current_user.id).single().execute()
        if not website_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Website not found"
            )
        
        website = website_response.data
        
        # Get conversation stats
        conversations_response = supabase.table("conversations").select("id", count="exact").eq("website_id", website_id).execute()
        total_conversations = conversations_response.count or 0
        
        # Get message stats
        messages_response = supabase.table("messages").select("id", count="exact").eq("conversation_id", conversations_response.data).execute()
        total_messages = messages_response.count or 0
        
        return {
            "website_id": website_id,
            "website_name": website.get("name", "Unknown"),
            "website_url": website.get("url", ""),
            "status": website.get("status", "unknown"),
            "pages_scraped": website.get("pages_scraped", 0),
            "total_chunks": website.get("total_chunks", 0),
            "total_conversations": total_conversations,
            "total_messages": total_messages,
            "last_scraped_at": website.get("last_scraped_at"),
            "created_at": website.get("created_at")
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get stats: {str(e)}"
        )

@router.post("/test/{website_id}")
async def test_embeddings(
    website_id: str,
    test_queries: List[str],
    current_user: User = Depends(get_current_active_user)
):
    """Test embeddings with multiple queries"""
    supabase = await get_supabase()
    
    try:
        # Verify website belongs to user
        website_response = supabase.table("websites").select("id, status").eq("id", website_id).eq("user_id", current_user.id).single().execute()
        if not website_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Website not found"
            )
        
        if website_response.data["status"] != "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Website is not ready for testing. Please wait for processing to complete."
            )
        
        # Test each query
        test_results = []
        for query in test_queries[:10]:  # Limit to 10 queries
            try:
                results = await search_similar_chunks(website_id, query, top_k=3)
                test_results.append({
                    "query": query,
                    "results": results,
                    "success": True
                })
            except Exception as e:
                test_results.append({
                    "query": query,
                    "error": str(e),
                    "success": False
                })
        
        return {
            "website_id": website_id,
            "test_results": test_results,
            "total_queries": len(test_queries),
            "successful_queries": len([r for r in test_results if r["success"]])
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Test failed: {str(e)}"
        ) 