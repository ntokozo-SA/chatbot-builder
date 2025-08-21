# Database Migrations

This directory contains SQL migration files for setting up and maintaining the database schema.

## Migration Files

- `001_create_users_table.sql` - Creates the initial users table for authentication

## Running Migrations

### Option 1: Using psql directly

```bash
# Connect to your PostgreSQL database
psql -h your_host -U your_username -d your_database

# Run the migration
\i migrations/001_create_users_table.sql
```

### Option 2: Using a migration tool

If you're using a migration tool like Flyway, Liquibase, or Alembic, you can import these SQL files.

### Option 3: Using Supabase CLI

```bash
# If using Supabase
supabase db reset
# or
supabase migration up
```

## Schema Verification

After running migrations, you can verify the schema:

```sql
-- Check if the table exists
\d public.users

-- Check table structure
SELECT column_name, data_type, is_nullable, column_default 
FROM information_schema.columns 
WHERE table_schema = 'public' AND table_name = 'users';

-- Check indexes
SELECT indexname, indexdef 
FROM pg_indexes 
WHERE tablename = 'users';
```

## PostgREST Schema Cache

After running migrations, refresh the PostgREST schema cache:

```sql
NOTIFY pgrst, 'reload schema';
```

This ensures that PostgREST (if you're using it) picks up the new schema changes immediately.

## Rollback

To rollback the users table creation:

```sql
-- Drop the table (WARNING: This will delete all data)
DROP TABLE IF EXISTS public.users CASCADE;

-- Drop the function
DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;

-- Refresh PostgREST schema cache
NOTIFY pgrst, 'reload schema';
```

## Notes

- The migration uses `IF NOT EXISTS` to prevent errors if run multiple times
- UUID extension is enabled for the `gen_random_uuid()` function
- Automatic timestamp updates are handled by triggers
- Indexes are created for better query performance
- Comments are added for documentation purposes 