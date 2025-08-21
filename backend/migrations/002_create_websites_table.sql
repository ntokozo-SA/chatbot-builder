-- Migration: 002_create_websites_table.sql
-- Description: Create the websites table for storing user websites and their status
-- Date: 2024-01-01

-- Create websites table
CREATE TABLE IF NOT EXISTS public.websites (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    name TEXT,
    description TEXT,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'scraping', 'processing', 'completed', 'failed')),
    pages_scraped INTEGER DEFAULT 0,
    total_chunks INTEGER DEFAULT 0,
    total_conversations INTEGER DEFAULT 0,
    total_messages INTEGER DEFAULT 0,
    error_message TEXT,
    last_scraped_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_websites_user_id ON public.websites(user_id);
CREATE INDEX IF NOT EXISTS idx_websites_status ON public.websites(status);
CREATE INDEX IF NOT EXISTS idx_websites_created_at ON public.websites(created_at);
CREATE INDEX IF NOT EXISTS idx_websites_url ON public.websites(url);

-- Create unique constraint to prevent duplicate websites per user
CREATE UNIQUE INDEX IF NOT EXISTS idx_websites_user_url ON public.websites(user_id, url);

-- Create trigger to automatically update updated_at on row updates
CREATE TRIGGER update_websites_updated_at 
    BEFORE UPDATE ON public.websites 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Add comments for documentation
COMMENT ON TABLE public.websites IS 'Websites added by users for chatbot creation';
COMMENT ON COLUMN public.websites.id IS 'Unique identifier for the website';
COMMENT ON COLUMN public.websites.user_id IS 'Foreign key to the user who owns this website';
COMMENT ON COLUMN public.websites.url IS 'The website URL';
COMMENT ON COLUMN public.websites.name IS 'User-defined name for the website';
COMMENT ON COLUMN public.websites.description IS 'User-defined description for the website';
COMMENT ON COLUMN public.websites.status IS 'Current processing status of the website';
COMMENT ON COLUMN public.websites.pages_scraped IS 'Number of pages successfully scraped';
COMMENT ON COLUMN public.websites.total_chunks IS 'Total number of content chunks created';
COMMENT ON COLUMN public.websites.total_conversations IS 'Total number of conversations with this chatbot';
COMMENT ON COLUMN public.websites.total_messages IS 'Total number of messages in conversations';
COMMENT ON COLUMN public.websites.error_message IS 'Error message if processing failed';
COMMENT ON COLUMN public.websites.last_scraped_at IS 'Timestamp of last scraping attempt';
COMMENT ON COLUMN public.websites.created_at IS 'Timestamp when the website was added';
COMMENT ON COLUMN public.websites.updated_at IS 'Timestamp when the website was last updated';

-- Refresh PostgREST schema cache
NOTIFY pgrst, 'reload schema'; 