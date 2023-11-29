-- Table for Guilds (Servers)
CREATE TABLE guilds (
    id BIGINT PRIMARY KEY,           -- Discord Guild (Server) ID
    name TEXT NOT NULL,              -- Guild Name
    created_at TIMESTAMP NOT NULL    -- Timestamp when the Guild was created
);
