from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import os
import logging
from dotenv import load_dotenv

from app.api import auth, websites, chat, embeddings
from app.core.config import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AI Chatbot Builder API",
    description="A portfolio-ready AI chatbot builder that allows businesses to create custom chatbots for their websites",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event to validate configuration
@app.on_event("startup")
async def startup_event():
    """Validate configuration on startup"""
    logger.info("Starting AI Chatbot Builder API...")
    
    # Check for placeholder values
    placeholder_checks = [
        ("SUPABASE_URL", settings.SUPABASE_URL, "your-project-id"),
        ("SUPABASE_ANON_KEY", settings.SUPABASE_ANON_KEY, "your-anon-key"),
        ("SUPABASE_SERVICE_ROLE_KEY", settings.SUPABASE_SERVICE_ROLE_KEY, "your-service-role-key"),
        ("SECRET_KEY", settings.SECRET_KEY, "your-secret-key"),
    ]
    
    for name, value, placeholder in placeholder_checks:
        if placeholder in str(value):
            logger.warning(f"⚠️  {name} contains placeholder value: {value}")
            logger.warning("   This will cause authentication and database operations to fail!")
    
    logger.info("Configuration validation completed")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(websites.router, prefix="/api/websites", tags=["Websites"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(embeddings.router, prefix="/api/embeddings", tags=["Embeddings"])

@app.get("/")
async def root():
    return {
        "message": "AI Chatbot Builder API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors"""
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": exc.errors(),
            "message": "Invalid request data"
        }
    )

@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    """Handle Pydantic model validation errors"""
    logger.error(f"Pydantic validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": exc.errors(),
            "message": "Invalid data format"
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "message": str(exc)}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 