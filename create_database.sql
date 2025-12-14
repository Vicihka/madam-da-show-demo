-- SQL script to create PostgreSQL database for MADAM DA
-- Run this with: psql -U postgres -f create_database.sql

-- Create database (if not exists)
SELECT 'CREATE DATABASE madamda_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'madamda_db')\gexec

-- Connect to the new database
\c madamda_db

-- Grant privileges (if needed)
-- GRANT ALL PRIVILEGES ON DATABASE madamda_db TO postgres;

-- Display success message
SELECT 'Database madamda_db created successfully!' AS message;

