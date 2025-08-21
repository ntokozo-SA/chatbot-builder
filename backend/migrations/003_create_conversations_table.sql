-- Migration: 003_create_conversations_table.sql
-- Description: Create the conversations and messages tables for storing chat history
-- Date: 2024-01-01

-- Create conversations table
CREATE TABLE IF NOT EXISTS public.conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    website_id UUID NOT NULL REFERENCES public.websites(id) ON DELETE CASCADE,
    user_session_id TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create messages table
CREATE TABLE IF NOT EXISTS public.messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES public.conversations(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_conversations_website_id ON public.conversations(website_id);
CREATE INDEX IF NOT EXISTS idx_conversations_session_id ON public.conversations(user_session_id);
CREATE INDEX IF NOT EXISTS idx_conversations_created_at ON public.conversations(created_at);

CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON public.messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_role ON public.messages(role);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON public.messages(created_at);

-- Create trigger to automatically update updated_at on row updates
CREATE TRIGGER update_conversations_updated_at 
    BEFORE UPDATE ON public.conversations 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Add comments for documentation
COMMENT ON TABLE public.conversations IS 'Chat conversations for each website';
COMMENT ON COLUMN public.conversations.id IS 'Unique identifier for the conversation';
COMMENT ON COLUMN public.conversations.website_id IS 'Foreign key to the website this conversation belongs to';
COMMENT ON COLUMN public.conversations.user_session_id IS 'Session identifier for the user';
COMMENT ON COLUMN public.conversations.created_at IS 'Timestamp when the conversation was created';
COMMENT ON COLUMN public.conversations.updated_at IS 'Timestamp when the conversation was last updated';

COMMENT ON TABLE public.messages IS 'Individual messages within conversations';
COMMENT ON COLUMN public.messages.id IS 'Unique identifier for the message';
COMMENT ON COLUMN public.messages.conversation_id IS 'Foreign key to the conversation this message belongs to';
COMMENT ON COLUMN public.messages.role IS 'Role of the message sender (user or assistant)';
COMMENT ON COLUMN public.messages.content IS 'Content of the message';
COMMENT ON COLUMN public.messages.created_at IS 'Timestamp when the message was created';

-- Refresh PostgREST schema cache
NOTIFY pgrst, 'reload schema'; 