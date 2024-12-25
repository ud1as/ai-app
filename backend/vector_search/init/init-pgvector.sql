CREATE EXTENSION IF NOT EXISTS vector;

DO $$ 
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'example_db') THEN
      PERFORM dblink_exec('dbname=' || current_database(), 'CREATE DATABASE example_db');
   END IF;
END $$;





-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Enable uuid-ossp extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Table: datasets
CREATE TABLE IF NOT EXISTS datasets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_by UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(0),
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(0)
);

-- Index on tenant_id for datasets
CREATE INDEX IF NOT EXISTS dataset_tenant_idx ON datasets (tenant_id);

-- Table: documents
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    dataset_id UUID NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(0),
    CONSTRAINT document_dataset_id_fk FOREIGN KEY (dataset_id) REFERENCES datasets (id) ON DELETE CASCADE
);

-- Index on dataset_id for documents
CREATE INDEX IF NOT EXISTS document_dataset_id_idx ON documents (dataset_id);

-- Table: embeddings
CREATE TABLE IF NOT EXISTS embeddings (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(255) NOT NULL,
    hash VARCHAR(64) NOT NULL,
    embedding VECTOR(1536) NOT NULL  -- Vector column with dimension 1536
);







-- Bots table
CREATE TABLE bots (
    id UUID NOT NULL DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    CONSTRAINT bot_pkey PRIMARY KEY (id)
);

-- Bot configurations table
CREATE TABLE bot_configurations (
    id UUID NOT NULL DEFAULT uuid_generate_v4(),
    bot_id UUID NOT NULL,
    prompt_template TEXT NOT NULL,
    temperature FLOAT DEFAULT 0.7,
    max_tokens INTEGER DEFAULT 1000,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT bot_config_pkey PRIMARY KEY (id),
    CONSTRAINT valid_temperature CHECK (temperature >= 0 AND temperature <= 1),
    CONSTRAINT valid_max_tokens CHECK (max_tokens > 0)
);

-- Bot datasets mapping table
CREATE TABLE bot_datasets (
    bot_id UUID NOT NULL,
    dataset_id UUID NOT NULL,
    CONSTRAINT bot_dataset_pkey PRIMARY KEY (bot_id, dataset_id)
);

-- Bot usage tracking table
CREATE TABLE bot_usage (
    id UUID NOT NULL DEFAULT uuid_generate_v4(),
    bot_id UUID NOT NULL,
    total_messages INTEGER DEFAULT 0,
    CONSTRAINT bot_usage_pkey PRIMARY KEY (id)
);