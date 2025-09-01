
CREATE TABLE startups (
    id SERIAL PRIMARY KEY,
    startup_name VARCHAR(255), 
    year INT,
    state VARCHAR(100),
    industry VARCHAR(100),
    count INT, 
    last_update VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);