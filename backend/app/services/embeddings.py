import asyncio
import httpx
import json
from typing import List, Dict, Any
import logging
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import numpy as np
from app.core.config import settings
import re

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        self.qdrant_client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY
        )
        self.embedding_model = settings.HUGGINGFACE_EMBEDDING_MODEL
        self.chunk_size = settings.CHUNK_SIZE
        self.chunk_overlap = settings.CHUNK_OVERLAP

    async def process_website_embeddings(self, website_id: str, pages: List[Dict[str, str]]) -> int:
        """Process website content and store embeddings in Qdrant"""
        try:
            # Create collection for this website if it doesn't exist
            collection_name = f"website_{website_id}"
            await self._create_collection_if_not_exists(collection_name)
            
            # Clear existing data for this website
            await self._clear_collection(collection_name)
            
            total_chunks = 0
            
            for page in pages:
                # Chunk the content
                chunks = self._chunk_text(page['content'])
                
                # Generate embeddings for chunks
                embeddings = await self._generate_embeddings([chunk['text'] for chunk in chunks])
                
                # Store in Qdrant
                points = []
                for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                    point = PointStruct(
                        id=f"{website_id}_{page['url']}_{i}",
                        vector=embedding.tolist(),
                        payload={
                            'website_id': website_id,
                            'url': page['url'],
                            'title': page['title'],
                            'content': chunk['text'],
                            'chunk_index': i,
                            'total_chunks': len(chunks)
                        }
                    )
                    points.append(point)
                
                # Insert points in batches
                if points:
                    self.qdrant_client.upsert(
                        collection_name=collection_name,
                        points=points
                    )
                    total_chunks += len(points)
            
            logger.info(f"Processed {total_chunks} chunks for website {website_id}")
            return total_chunks
            
        except Exception as e:
            logger.error(f"Error processing embeddings for website {website_id}: {e}")
            raise

    def _chunk_text(self, text: str) -> List[Dict[str, Any]]:
        """Split text into overlapping chunks"""
        chunks = []
        
        # Clean text
        text = re.sub(r'\s+', ' ', text).strip()
        
        if len(text) <= self.chunk_size:
            chunks.append({
                'text': text,
                'start': 0,
                'end': len(text)
            })
            return chunks
        
        # Split into overlapping chunks
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            
            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence endings
                sentence_endings = ['.', '!', '?', '\n']
                for ending in sentence_endings:
                    last_ending = text.rfind(ending, start, end)
                    if last_ending > start + self.chunk_size * 0.7:  # Only break if we're at least 70% through
                        end = last_ending + 1
                        break
            
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append({
                    'text': chunk_text,
                    'start': start,
                    'end': end
                })
            
            # Move start position with overlap
            start = end - self.chunk_overlap
            if start >= len(text):
                break
        
        return chunks

    async def _generate_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        """Generate embeddings using HuggingFace API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"https://api-inference.huggingface.co/models/{self.embedding_model}",
                    headers={
                        "Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={"inputs": texts},
                    timeout=30.0
                )
                
                if response.status_code != 200:
                    raise Exception(f"HuggingFace API error: {response.status_code} - {response.text}")
                
                embeddings = response.json()
                
                # Convert to numpy arrays
                if isinstance(embeddings, list):
                    return [np.array(emb) for emb in embeddings]
                else:
                    # Single embedding returned
                    return [np.array(embeddings)]
                    
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise

    async def _create_collection_if_not_exists(self, collection_name: str):
        """Create Qdrant collection if it doesn't exist"""
        try:
            collections = self.qdrant_client.get_collections()
            collection_names = [col.name for col in collections.collections]
            
            if collection_name not in collection_names:
                self.qdrant_client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(
                        size=384,  # Size for all-MiniLM-L6-v2
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Created collection: {collection_name}")
        except Exception as e:
            logger.error(f"Error creating collection {collection_name}: {e}")
            raise

    async def _clear_collection(self, collection_name: str):
        """Clear all points from a collection"""
        try:
            self.qdrant_client.delete(
                collection_name=collection_name,
                points_selector={"all": True}
            )
            logger.info(f"Cleared collection: {collection_name}")
        except Exception as e:
            logger.error(f"Error clearing collection {collection_name}: {e}")
            raise

    async def search_similar_chunks(self, website_id: str, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar chunks in a website's collection"""
        try:
            collection_name = f"website_{website_id}"
            
            # Generate embedding for query
            query_embeddings = await self._generate_embeddings([query])
            query_vector = query_embeddings[0].tolist()
            
            # Search in Qdrant
            search_results = self.qdrant_client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=top_k,
                with_payload=True
            )
            
            # Format results
            results = []
            for result in search_results:
                results.append({
                    'content': result.payload['content'],
                    'url': result.payload['url'],
                    'title': result.payload['title'],
                    'score': result.score
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching chunks for website {website_id}: {e}")
            raise

# Global embedding service instance
embedding_service = EmbeddingService()

async def process_website_embeddings(website_id: str, pages: List[Dict[str, str]]) -> int:
    """Main function to process website embeddings"""
    return await embedding_service.process_website_embeddings(website_id, pages)

async def search_similar_chunks(website_id: str, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Main function to search for similar chunks"""
    return await embedding_service.search_similar_chunks(website_id, query, top_k) 