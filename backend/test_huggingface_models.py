#!/usr/bin/env python3
"""
Test different HuggingFace models to find working ones
"""

import asyncio
import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')

# Test models - these are commonly available and free
TEST_MODELS = [
    "microsoft/DialoGPT-small",
    "microsoft/DialoGPT-medium", 
    "microsoft/DialoGPT-large",
    "gpt2",
    "distilgpt2",
    "google/flan-t5-small",
    "google/flan-t5-base",
    "google/flan-t5-large",
    "facebook/opt-125m",
    "facebook/opt-350m",
    "EleutherAI/gpt-neo-125M",
    "EleutherAI/gpt-neo-1.3B"
]

async def test_model(model_name: str) -> bool:
    """Test if a model is accessible"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://api-inference.huggingface.co/models/{model_name}",
                headers={
                    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "inputs": "Hello, how are you?",
                    "parameters": {
                        "max_length": 50,
                        "temperature": 0.7
                    }
                },
                timeout=10.0
            )
            
            if response.status_code == 200:
                print(f"✓ {model_name} - Working")
                return True
            else:
                print(f"✗ {model_name} - Error {response.status_code}")
                return False
                
    except Exception as e:
        print(f"✗ {model_name} - Exception: {str(e)[:50]}...")
        return False

async def test_embedding_models():
    """Test embedding models"""
    embedding_models = [
        "sentence-transformers/paraphrase-MiniLM-L3-v2",
        "sentence-transformers/paraphrase-MiniLM-L6-v2", 
        "sentence-transformers/all-MiniLM-L6-v2",
        "sentence-transformers/all-mpnet-base-v2"
    ]
    
    print("\n=== Testing Embedding Models ===")
    for model in embedding_models:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model}",
                    headers={
                        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "inputs": "This is a test sentence."
                    },
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    print(f"✓ {model} - Working")
                else:
                    print(f"✗ {model} - Error {response.status_code}")
                    
        except Exception as e:
            print(f"✗ {model} - Exception: {str(e)[:50]}...")

async def main():
    print("=== Testing HuggingFace Models ===")
    print(f"API Key: {'✓ Set' if HUGGINGFACE_API_KEY else '✗ Missing'}")
    
    working_models = []
    
    for model in TEST_MODELS:
        if await test_model(model):
            working_models.append(model)
    
    print(f"\n=== Results ===")
    print(f"Working models: {len(working_models)}/{len(TEST_MODELS)}")
    if working_models:
        print("Recommended models:")
        for model in working_models[:3]:  # Show first 3
            print(f"  - {model}")
    
    await test_embedding_models()

if __name__ == "__main__":
    asyncio.run(main()) 