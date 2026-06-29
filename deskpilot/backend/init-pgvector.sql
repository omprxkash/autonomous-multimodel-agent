-- Enable pgvector extension before table creation.
-- This script is mounted into the Postgres container as an init file.
CREATE EXTENSION IF NOT EXISTS vector;

-- Verify installation
SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';
