import httpx
import json
import logging
from app.core.config import settings
from app.services.simple_chat import generate_simple_response

logger = logging.getLogger(__name__)

async def generate_ai_response(user_message: str, context: str) -> str:
    """Generate AI response using simple chatbot (HuggingFace fallback disabled due to API issues)"""
    try:
        # Use simple chatbot as primary method since HuggingFace API is not working
        logger.info("Using simple chatbot for response generation")
        return generate_simple_response(user_message, context)
            
    except Exception as e:
        logger.error(f"Error generating AI response: {e}")
        return _generate_fallback_response(user_message, context)

def _clean_response(generated_text: str, prompt: str) -> str:
    """Clean up the generated response"""
    # Remove the prompt from the beginning if it's there
    if prompt in generated_text:
        response = generated_text.replace(prompt, "").strip()
    else:
        response = generated_text.strip()
    
    # Remove any remaining prompt artifacts
    response = response.replace("Answer:", "").strip()
    
    # Clean up extra whitespace
    response = " ".join(response.split())
    
    # Ensure the response ends with proper punctuation
    if response and not response[-1] in ['.', '!', '?']:
        response += '.'
    
    return response

def _generate_fallback_response(user_message: str, context: str) -> str:
    """Generate a fallback response when AI model is not available"""
    user_message_lower = user_message.lower()
    
    # Simple keyword-based responses
    if any(word in user_message_lower for word in ['hour', 'time', 'open', 'close', 'schedule']):
        if 'hour' in context.lower() or 'time' in context.lower() or 'open' in context.lower():
            return "Based on the available information, I can see some details about operating hours in the content. However, for the most accurate and up-to-date information, I recommend checking the website directly or contacting the business."
        else:
            return "I don't see specific operating hours information in the available content. Please check the website directly or contact the business for current hours."
    
    elif any(word in user_message_lower for word in ['price', 'cost', 'fee', 'charge', 'rate']):
        if any(word in context.lower() for word in ['price', 'cost', '$', '€', '£']):
            return "I can see some pricing information in the content, but for the most current and accurate pricing, please check the website directly or contact the business."
        else:
            return "I don't see specific pricing information in the available content. Please check the website directly or contact the business for current pricing."
    
    elif any(word in user_message_lower for word in ['contact', 'phone', 'email', 'address', 'location']):
        if any(word in context.lower() for word in ['contact', 'phone', 'email', '@', 'address']):
            return "I can see some contact information in the content. For the most up-to-date contact details, please check the website directly."
        else:
            return "I don't see specific contact information in the available content. Please check the website directly for contact details."
    
    elif any(word in user_message_lower for word in ['service', 'product', 'offer', 'provide']):
        if context.strip():
            return f"Based on the available content, I can see information about their services and offerings. Here's what I found: {context[:200]}..."
        else:
            return "I don't have enough information about their services in the available content. Please check the website directly for detailed information about their offerings."
    
    else:
        if context.strip():
            return f"I found some relevant information in the content: {context[:300]}... For more detailed information, please check the website directly."
        else:
            return "I don't have enough information to answer your question. Please check the website directly or contact the business for more details."

async def generate_simple_response_async(user_message: str) -> str:
    """Generate a simple response when no context is available (async version)"""
    try:
        prompt = f"User: {user_message}\nAssistant:"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://api-inference.huggingface.co/models/{settings.HUGGINGFACE_CHAT_MODEL}",
                headers={
                    "Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "inputs": prompt,
                    "parameters": {
                        "max_length": 200,
                        "temperature": 0.7,
                        "do_sample": True
                    }
                },
                timeout=30.0
            )
            
            if response.status_code != 200:
                return "I'm here to help! Please ask me a question about the website content."
            
            result = response.json()
            
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get('generated_text', '')
            elif isinstance(result, dict):
                generated_text = result.get('generated_text', '')
            else:
                generated_text = str(result)
            
            response_text = _clean_response(generated_text, prompt)
            
            if not response_text:
                return "I'm here to help! Please ask me a question about the website content."
            
            return response_text
            
    except Exception as e:
        logger.error(f"Error generating simple response: {e}")
        return "I'm here to help! Please ask me a question about the website content." 