-- SQL script to add user authentication to the educhat_db database
-- Run this script on your existing educhat_db database

USE educhat_db;

-- Create the users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(4) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_username (username)
);
select * from chat_sessions;

ALTER TABLE chat_sessions ADD COLUMN user_id VARCHAR(4) AFTER id;
ALTER TABLE chat_sessions ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE;
CREATE INDEX idx_session_user_id ON chat_sessions(user_id);

-- Note: If you have existing chat_sessions without a user_id, you'll need to:
-- 1. Create a default user first
-- 2. Update existing sessions with that user's ID
-- This is a manual migration that depends on your setup.

-- If all your chat_sessions are obsolete and you want to start fresh:
-- DELETE FROM chat_messages;
-- DELETE FROM chat_sessions;

-- Then uncomment the ALTER TABLE commands above to add the user_id column
