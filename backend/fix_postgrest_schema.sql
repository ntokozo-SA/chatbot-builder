-- Fix PostgREST Schema Cache Issue
-- This script creates the missing tables and configures PostgREST properly

-- Step 1: Enable UUID extension (required for gen_random_uuid())
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Step 2: Create users table if it doesn't exist
CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT,
    website_url TEXT,
    company_name TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Step 3: Create websites table with the exact structure you specified
CREATE TABLE IF NOT EXISTS public.websites (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    url TEXT NOT NULL,
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Step 4: Add additional columns that your application expects
ALTER TABLE public.websites 
ADD COLUMN IF NOT EXISTS name TEXT,
ADD COLUMN IF NOT EXISTS description TEXT,
ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'scraping', 'processing', 'completed', 'failed')),
ADD COLUMN IF NOT EXISTS pages_scraped INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS total_chunks INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS total_conversations INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS total_messages INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS error_message TEXT,
ADD COLUMN IF NOT EXISTS last_scraped_at TIMESTAMP WITH TIME ZONE,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();

-- Step 5: Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON public.users(email);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON public.users(created_at);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON public.users(is_active);

CREATE INDEX IF NOT EXISTS idx_websites_user_id ON public.websites(user_id);
CREATE INDEX IF NOT EXISTS idx_websites_status ON public.websites(status);
CREATE INDEX IF NOT EXISTS idx_websites_created_at ON public.websites(created_at);
CREATE INDEX IF NOT EXISTS idx_websites_url ON public.websites(url);

-- Step 6: Create unique constraint to prevent duplicate websites per user
CREATE UNIQUE INDEX IF NOT EXISTS idx_websites_user_url ON public.websites(user_id, url);

-- Step 7: Create function to automatically update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Step 8: Create triggers to automatically update updated_at on row updates
CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON public.users 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_websites_updated_at 
    BEFORE UPDATE ON public.websites 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Step 9: Grant necessary permissions for PostgREST
-- Note: Adjust these permissions based on your Supabase setup
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON public.users TO anon, authenticated;
GRANT ALL ON public.websites TO anon, authenticated;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated;

-- Step 10: Refresh PostgREST schema cache
-- This is the key step to fix the PGRST205 error
NOTIFY pgrst, 'reload schema';

-- Step 11: Verify the tables were created correctly
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_schema = 'public' 
AND table_name IN ('users', 'websites')
ORDER BY table_name, ordinal_position;

-- Step 12: Test that the tables are accessible
SELECT 'users table row count:' as info, COUNT(*) as count FROM public.users
UNION ALL
SELECT 'websites table row count:' as info, COUNT(*) as count FROM public.websites; 