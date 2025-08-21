import httpx
import json
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

async def generate_ai_response(user_message: str, context: str) -> str:
    """Generate AI response using HuggingFace model"""
    try:
        # Prepare the prompt with context
        prompt = f"""Based on the following context, answer the user's question. If the context doesn't contain enough information to answer the question, say so politely.

Context:
{context}

User Question: {user_message}

Answer:"""

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
                        "max_length": 500,
                        "temperature": 0.7,
                        "do_sample": True,
                        "top_p": 0.9
                    }
                },
                timeout=30.0
            )
            
            if response.status_code != 200:
                logger.error(f"HuggingFace API error: {response.status_code} - {response.text}")
                return "I apologize, but I'm having trouble generating a response right now. Please try again later."
            
            result = response.json()
            
            # Extract the generated text
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get('generated_text', '')
            elif isinstance(result, dict):
                generated_text = result.get('generated_text', '')
            else:
                generated_text = str(result)
            
            # Clean up the response
            response_text = _clean_response(generated_text, prompt)
            
            if not response_text or len(response_text.strip()) < 10:
                return "I apologize, but I couldn't generate a meaningful response. Please try rephrasing your question."
            
            return response_text
            
    except Exception as e:
        logger.error(f"Error generating AI response: {e}")
        return "I apologize, but I'm experiencing technical difficulties. Please try again later."

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

async def generate_simple_response(user_message: str) -> str:
    """Generate a simple response when no context is available"""
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