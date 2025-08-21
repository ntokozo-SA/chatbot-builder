from pydantic_settings import BaseSettings
from pydantic import validator, root_validator
from typing import List, Union
import os
import json
import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # Supabase Configuration
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str
    
    # HuggingFace Configuration
    HUGGINGFACE_API_KEY: str
    HUGGINGFACE_EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    HUGGINGFACE_CHAT_MODEL: str = "google/flan-t5-base"
    
    # Qdrant Configuration
    QDRANT_URL: str
    QDRANT_API_KEY: str
    
    # Application Configuration
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:4173"
    ]
    
    # Scraping Configuration
    MAX_PAGES_TO_SCRAPE: int = 50
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    
    @validator('ALLOWED_ORIGINS', pre=True)
    def parse_allowed_origins(cls, v):
        """
        Parse ALLOWED_ORIGINS from various formats:
        - JSON list: ["http://localhost:3000", "http://127.0.0.1:3000"]
        - Comma-separated string: "http://localhost:3000,http://127.0.0.1:3000"
        - Single string: "http://localhost:3000"
        """
        if isinstance(v, list):
            # Already a list, validate each item
            return [str(origin).strip() for origin in v if origin and str(origin).strip()]
        
        if isinstance(v, str):
            v = v.strip()
            if not v:
                return []
            
            # Try to parse as JSON first
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return [str(origin).strip() for origin in parsed if origin and str(origin).strip()]
                elif isinstance(parsed, str):
                    # JSON string, treat as single origin
                    return [parsed.strip()] if parsed.strip() else []
                else:
                    raise ValueError(f"Invalid JSON format for ALLOWED_ORIGINS: {v}")
            except json.JSONDecodeError:
                # Not JSON, treat as comma-separated string
                origins = [origin.strip() for origin in v.split(',') if origin.strip()]
                return origins
        
        # Fallback to default
        logger.warning(f"Invalid ALLOWED_ORIGINS format: {v}. Using default origins.")
        return [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://localhost:4173"
        ]
    
    @validator('ALLOWED_ORIGINS')
    def validate_allowed_origins(cls, v):
        """Validate that all origins are valid URLs"""
        if not v:
            logger.warning("ALLOWED_ORIGINS is empty. CORS may not work properly.")
            return v
        
        valid_origins = []
        for origin in v:
            origin = origin.strip()
            if not origin:
                continue
            
            # Basic URL validation
            if origin.startswith(('http://', 'https://')):
                valid_origins.append(origin)
            else:
                logger.warning(f"Invalid origin format (must start with http:// or https://): {origin}")
        
        if not valid_origins:
            logger.warning("No valid origins found in ALLOWED_ORIGINS. Using default origins.")
            return [
                "http://localhost:3000",
                "http://localhost:5173",
                "http://localhost:4173"
            ]
        
        logger.info(f"Configured CORS origins: {valid_origins}")
        return valid_origins
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings() 