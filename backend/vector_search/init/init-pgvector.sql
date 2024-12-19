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
