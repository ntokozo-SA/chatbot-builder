from fastapi import APIRouter, HTTPException, status, Depends, Request
from typing import List, Optional
from app.core.database import get_supabase
from app.core.auth import get_current_active_user
from app.models.user import User
from app.models.chat import ChatRequest, ChatResponse, Conversation, ChatMessage, MessageRole
from app.services.embeddings import search_similar_chunks
from app.services.ai_chat import generate_ai_response
from datetime import datetime
import uuid
import httpx
import json

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat(
    chat_request: ChatRequest,
    request: Request,
    current_user: Optional[User] = Depends(get_current_active_user)
):
    """Handle chat messages and generate AI responses"""
    supabase = await get_supabase()
    
    try:
        # Get client IP and user agent
        client_ip = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        
        # Get or create conversation
        conversation_id = chat_request.conversation_id
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
            
            # Create new conversation
            conversation_data = {
                "id": conversation_id,
                "website_id": chat_request.website_id,
                "user_agent": user_agent,
                "ip_address": client_ip,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "message_count": 0
            }
            
            supabase.table("conversations").insert(conversation_data).execute()
        
        # Verify website exists and is completed
        website_response = supabase.table("websites").select("status").eq("id", chat_request.website_id).single().execute()
        if not website_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Website not found"
            )
        
        if website_response.data["status"] != "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Website is not ready for chat. Please wait for processing to complete."
            )
        
        # Search for relevant content
        similar_chunks = await search_similar_chunks(
            chat_request.website_id, 
            chat_request.message, 
            top_k=3
        )
        
        # Generate AI response
        context = "\n\n".join([chunk['content'] for chunk in similar_chunks])
        ai_response = await generate_ai_response(chat_request.message, context)
        
        # Store user message
        user_message_data = {
            "id": str(uuid.uuid4()),
            "conversation_id": conversation_id,
            "role": MessageRole.USER.value,
            "content": chat_request.message,
            "timestamp": datetime.utcnow().isoformat()
        }
        supabase.table("messages").insert(user_message_data).execute()
        
        # Store AI response
        ai_message_data = {
            "id": str(uuid.uuid4()),
            "conversation_id": conversation_id,
            "role": MessageRole.ASSISTANT.value,
            "content": ai_response,
            "timestamp": datetime.utcnow().isoformat()
        }
        supabase.table("messages").insert(ai_message_data).execute()
        
        # Update conversation
        supabase.table("conversations").update({
            "updated_at": datetime.utcnow().isoformat(),
            "message_count": supabase.table("messages").select("id", count="exact").eq("conversation_id", conversation_id).execute().count
        }).eq("id", conversation_id).execute()
        
        # Prepare sources
        sources = []
        for chunk in similar_chunks:
            if chunk['url'] not in sources:
                sources.append(chunk['url'])
        
        return ChatResponse(
            message=ai_response,
            conversation_id=conversation_id,
            sources=sources[:3],  # Limit to 3 sources
            confidence=similar_chunks[0]['score'] if similar_chunks else 0.0
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat failed: {str(e)}"
        )

@router.get("/conversations/{website_id}", response_model=List[Conversation])
async def get_conversations(
    website_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get conversations for a specific website"""
    supabase = await get_supabase()
    
    try:
        # Verify website belongs to user
        website_response = supabase.table("websites").select("id").eq("id", website_id).eq("user_id", current_user.id).execute()
        if not website_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Website not found"
            )
        
        # Get conversations
        response = supabase.table("conversations").select("*").eq("website_id", website_id).order("updated_at", desc=True).execute()
        
        conversations = []
        for conv_data in response.data:
            conversations.append(Conversation(**conv_data))
        
        return conversations
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch conversations: {str(e)}"
        )

@router.get("/conversations/{conversation_id}/messages", response_model=List[ChatMessage])
async def get_conversation_messages(
    conversation_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get messages for a specific conversation"""
    supabase = await get_supabase()
    
    try:
        # Verify conversation belongs to user's website
        conv_response = supabase.table("conversations").select("website_id").eq("id", conversation_id).single().execute()
        if not conv_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        website_response = supabase.table("websites").select("id").eq("id", conv_response.data["website_id"]).eq("user_id", current_user.id).execute()
        if not website_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        # Get messages
        response = supabase.table("messages").select("*").eq("conversation_id", conversation_id).order("timestamp", asc=True).execute()
        
        messages = []
        for msg_data in response.data:
            messages.append(ChatMessage(**msg_data))
        
        return messages
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch messages: {str(e)}"
        )

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a conversation"""
    supabase = await get_supabase()
    
    try:
        # Verify conversation belongs to user's website
        conv_response = supabase.table("conversations").select("website_id").eq("id", conversation_id).single().execute()
        if not conv_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        website_response = supabase.table("websites").select("id").eq("id", conv_response.data["website_id"]).eq("user_id", current_user.id).execute()
        if not website_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        # Delete messages first
        supabase.table("messages").delete().eq("conversation_id", conversation_id).execute()
        
        # Delete conversation
        supabase.table("conversations").delete().eq("id", conversation_id).execute()
        
        return {"message": "Conversation deleted successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete conversation: {str(e)}"
        ) 