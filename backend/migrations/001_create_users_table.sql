-- Migration: 001_create_users_table.sql
-- Description: Create the users table for authentication and user management
-- Date: 2024-01-01

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create users table
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

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON public.users(email);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON public.users(created_at);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON public.users(is_active);

-- Create a function to automatically update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at on row updates
CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON public.users 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Add comments for documentation
COMMENT ON TABLE public.users IS 'User accounts for the AI Chatbot Builder application';
COMMENT ON COLUMN public.users.id IS 'Unique identifier for the user';
COMMENT ON COLUMN public.users.email IS 'User email address (unique)';
COMMENT ON COLUMN public.users.password_hash IS 'Hashed password for authentication';
COMMENT ON COLUMN public.users.full_name IS 'User full name';
COMMENT ON COLUMN public.users.website_url IS 'User website URL for chatbot integration';
COMMENT ON COLUMN public.users.company_name IS 'User company name';
COMMENT ON COLUMN public.users.is_active IS 'Whether the user account is active';
COMMENT ON COLUMN public.users.created_at IS 'Timestamp when the user was created';
COMMENT ON COLUMN public.users.updated_at IS 'Timestamp when the user was last updated';

-- Grant necessary permissions (adjust as needed for your setup)
-- GRANT SELECT, INSERT, UPDATE, DELETE ON public.users TO your_app_role;
-- GRANT USAGE ON SEQUENCE public.users_id_seq TO your_app_role;

-- Refresh PostgREST schema cache
NOTIFY pgrst, 'reload schema'; 