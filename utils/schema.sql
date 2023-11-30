-- Servers
CREATE TABLE IF NOT EXISTS Servers (
    ServerID INT PRIMARY KEY,           -- Discord Guild (Server) ID
    ServerName VARCHAR(255)             -- Guild Name
);
-- Temp Voicce
CREATE TABLE IF NOT EXISTS temp_voice_config (
    ServerID INT,
    RoomId INT,
    RoomName VARCHAR(255),
    RoomPrefix varchar(255),
    FOREIGN KEY (ServerID) REFERENCES Servers(ServerID)
);
CREATE TABLE IF NOT EXISTS temp_room (
    ServerID INT,
    RoomId INT,
    OwnerId VARCHAR(255),
    FOREIGN KEY (ServerID) REFERENCES Servers(ServerID)
);