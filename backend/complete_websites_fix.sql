-- Complete Fix for Websites Table and PostgREST Schema Cache
-- Run this in your Supabase SQL Editor

-- Step 1: Enable required extensions
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Step 2: Drop the existing table if it exists (to fix constraints)
DROP TABLE IF EXISTS public.websites CASCADE;

-- Step 3: Create the websites table with proper constraints
CREATE TABLE public.websites (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    url TEXT NOT NULL,
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Step 4: Add additional columns that your application expects
ALTER TABLE public.websites 
ADD COLUMN name TEXT,
ADD COLUMN description TEXT,
ADD COLUMN status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'scraping', 'processing', 'completed', 'failed')),
ADD COLUMN pages_scraped INTEGER DEFAULT 0,
ADD COLUMN total_chunks INTEGER DEFAULT 0,
ADD COLUMN total_conversations INTEGER DEFAULT 0,
ADD COLUMN total_messages INTEGER DEFAULT 0,
ADD COLUMN error_message TEXT,
ADD COLUMN last_scraped_at TIMESTAMPTZ,
ADD COLUMN updated_at TIMESTAMPTZ DEFAULT NOW();

-- Step 5: Create indexes for better performance
CREATE INDEX idx_websites_user_id ON public.websites(user_id);
CREATE INDEX idx_websites_status ON public.websites(status);
CREATE INDEX idx_websites_created_at ON public.websites(created_at);
CREATE INDEX idx_websites_url ON public.websites(url);

-- Step 6: Create unique constraint to prevent duplicate websites per user
CREATE UNIQUE INDEX idx_websites_user_url ON public.websites(user_id, url);

-- Step 7: Create function to automatically update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Step 8: Create trigger to automatically update updated_at on row updates
CREATE TRIGGER update_websites_updated_at 
    BEFORE UPDATE ON public.websites 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Step 9: Grant necessary permissions for PostgREST
-- This is CRITICAL for fixing the PGRST205 error
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON public.websites TO anon, authenticated;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated;

-- Step 10: Refresh PostgREST schema cache
-- This is the key step to fix the PGRST205 error
NOTIFY pgrst, 'reload schema';

-- Step 11: Verify the table was created correctly
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_schema = 'public' 
AND table_name = 'websites'
ORDER BY ordinal_position;

-- Step 12: Test that the table is accessible
SELECT 'websites table row count:' as info, COUNT(*) as count FROM public.websites; 