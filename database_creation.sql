-- Create the database
CREATE DATABASE IF NOT EXISTS educhat_db;
USE educhat_db;

-- Create the table
CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    class INT NOT NULL,
    book VARCHAR(255) NOT NULL,
    filepath VARCHAR(255) NOT NULL
);

-- Insert sample records pointing to the 'books/' folder
INSERT INTO books (class, book, filepath) VALUES
(1, 'biology-1', 'books/biology-1.pdf'),
(1, 'physics-1', 'books/physics-1.pdf'),
(2, 'bengaly-1', 'books/bengaly-1.pdf');

-- Table to store individual chat sessions
CREATE TABLE chat_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    class_level INT NOT NULL,
    subject VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table to store the messages inside those sessions
CREATE TABLE chat_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    sender ENUM('user', 'bot') NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES chat_sessions(id) ON DELETE CASCADE
);
INSERT INTO books (class, book, filepath) VALUES
(7, 'abc-7', 'books/abc-7.txt');

INSERT INTO books (class, book, filepath) VALUES
(7, 'amader_prithibi-7', 'books/amader_prithibi-7.txt');

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

select * from books;
select * from chat_messages;
select * from chat_sessions;
select * from users;

INSERT INTO books (class, book, filepath) VALUES
(7, 'amader_prithibi-7', 'books/amader_prithibi-7.txt'),
(5, 'amader-poribes-5', 'books/amader-poribes-5.txt'),
(7, 'blossoms-7', 'books/blossoms-7.txt'),
(6, 'bolsom-6', 'books/bolsom-6.txt'),
(6, 'Geography-6', 'books/Geography-6.txt'),
(6, 'history-6', 'books/history-6.txt'),
(7, 'history-7', 'books/history-7.txt'),
(5, 'patabahar-5', 'books/patabahar-5.txt');

-- delete from books;
-- set sql_safe_updates=0;
-- delete 
-- FROM chat_sessions 
-- WHERE user_id IS NULL;