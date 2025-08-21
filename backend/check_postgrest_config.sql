-- PostgREST Configuration Check
-- Run this to diagnose PostgREST schema cache issues

-- 1. Check if PostgREST is listening for notifications
SELECT 
    pid,
    application_name,
    state,
    query_start,
    query
FROM pg_stat_activity 
WHERE application_name LIKE '%postgrest%' 
OR query LIKE '%pgrst%';

-- 2. Check current PostgREST configuration
SELECT 
    name,
    setting,
    context
FROM pg_settings 
WHERE name LIKE '%search_path%' 
OR name LIKE '%schema%';

-- 3. Check if tables are visible to PostgREST
SELECT 
    schemaname,
    tablename,
    tableowner,
    hasindexes,
    hasrules,
    hastriggers
FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename IN ('users', 'websites')
ORDER BY tablename;

-- 4. Check table permissions
SELECT 
    grantee,
    table_name,
    privilege_type,
    is_grantable
FROM information_schema.table_privileges 
WHERE table_schema = 'public' 
AND table_name IN ('users', 'websites')
ORDER BY table_name, grantee, privilege_type;

-- 5. Check if the schema is in search path
SHOW search_path;

-- 6. Check if tables have the correct structure
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

-- 7. Test direct table access
SELECT COUNT(*) as websites_count FROM public.websites;
SELECT COUNT(*) as users_count FROM public.users;

-- 8. Check for any schema cache issues
-- This will show if there are any pending notifications
SELECT 
    pid,
    notification,
    payload
FROM pg_notification_queue; 