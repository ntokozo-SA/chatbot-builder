from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime
from enum import Enum

class WebsiteStatus(str, Enum):
    PENDING = "pending"
    SCRAPING = "scraping"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class WebsiteBase(BaseModel):
    url: HttpUrl
    name: Optional[str] = None
    description: Optional[str] = None

class WebsiteCreate(WebsiteBase):
    user_id: str

class WebsiteUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[WebsiteStatus] = None

class WebsiteInDB(WebsiteBase):
    id: str
    user_id: str
    status: WebsiteStatus = WebsiteStatus.PENDING
    pages_scraped: int = 0
    total_chunks: int = 0
    created_at: datetime
    updated_at: datetime
    last_scraped_at: Optional[datetime] = None
    error_message: Optional[str] = None

class Website(WebsiteInDB):
    pass

class WebsiteWithStats(Website):
    total_conversations: int = 0
    total_messages: int = 0 