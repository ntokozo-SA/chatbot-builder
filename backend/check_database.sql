-- Database Diagnostic Script for PostgREST Schema Cache Issue
-- Run this in your Supabase SQL Editor to check the current state

-- 1. Check if the websites table exists in public schema
SELECT 
    table_schema,
    table_name,
    table_type
FROM information_schema.tables 
WHERE table_name = 'websites'
ORDER BY table_schema, table_name;

-- 2. Check all tables in public schema
SELECT 
    table_name,
    table_type
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;

-- 3. Check if users table exists (required for foreign key)
SELECT 
    table_schema,
    table_name,
    table_type
FROM information_schema.tables 
WHERE table_name = 'users'
ORDER BY table_schema, table_name;

-- 4. Check PostgREST configuration
SELECT 
    schemaname,
    tablename,
    tableowner
FROM pg_tables 
WHERE tablename IN ('users', 'websites')
ORDER BY schemaname, tablename;

-- 5. Check if UUID extension is enabled
SELECT 
    extname,
    extversion
FROM pg_extension 
WHERE extname = 'uuid-ossp';

-- 6. Check current search path
SHOW search_path; 