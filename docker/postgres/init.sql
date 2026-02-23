CREATE USER langflow WITH PASSWORD 'langflow';
create database langflow OWNER langflow;

CREATE USER flowise WITH PASSWORD 'flowise';
create database flowise OWNER flowise;
\c flowise
CREATE EXTENSION IF NOT EXISTS vector;
