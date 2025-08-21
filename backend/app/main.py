from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

from app.api import auth, websites, chat, embeddings
from app.core.config import settings

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

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "message": str(exc)}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 