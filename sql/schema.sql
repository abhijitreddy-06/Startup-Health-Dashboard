-- In sql/schema.sql
CREATE TABLE startups (
    id SERIAL PRIMARY KEY,
    startup_name VARCHAR(255), -- Note: your data may not have this, which is fine
    year INT,
    state VARCHAR(100),
    industry VARCHAR(100),
    count INT, -- <-- ADD THIS LINE
    last_update VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);