-- Create a database named sp_db
CREATE DATABASE sp_db;

-- Connect to the sp_db database
\c sp_db

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(120) UNIQUE,
    password VARCHAR(80),
    fullname VARCHAR(80),
    photo VARCHAR(120)
);

CREATE TABLE publication (
    id SERIAL PRIMARY KEY,
    title VARCHAR(80),
    description TEXT,
    priority INTEGER,
    status VARCHAR(80),
    time_since_published INTERVAL,
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE access_tokens (
    id SERIAL PRIMARY KEY,
    access_token TEXT,
    user_id INTEGER REFERENCES users(id)
);
