# Enhanced Memory-Vector RAG Deployment

This directory contains deployment configurations for the Enhanced Memory-Vector RAG system.

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your system
- API keys for OpenAI and other necessary services
- At least 8GB of RAM available for running all containers

### Setup

1. Create a `.env` file based on the provided `.env.example`:

```bash
cp .env.example .env
```

2. Edit the `.env` file and add your API keys and configuration settings.

### Running the System

To start all components:

```bash
docker-compose up -d
```

To stop the system:

```bash
docker-compose down
```

To stop the system and remove all data volumes:

```bash
docker-compose down -v
```

## Components

The deployment includes the following components:

- **MCP Server**: The custom FastMCP server that provides the API for interacting with the system
- **Chainlit UI**: The web user interface built with Chainlit
- **Qdrant**: Vector database for semantic search, accessed via Mem0
- **Neo4j**: Graph database for knowledge graphs, accessed via Graphiti
- **Supabase**: PostgreSQL database for structured data and metadata
- **Grafana**: Monitoring dashboard
- **Prometheus**: Metrics collection

## Monitoring

The system includes comprehensive monitoring with Grafana and Prometheus:

- Grafana dashboard: http://localhost:3000 (default credentials: admin/admin)
- Prometheus metrics: http://localhost:9090

## Ports

The following ports are exposed on the host machine:

- 8000: MCP Server API
- 8501: Chainlit UI
- 6333: Qdrant API
- 7474: Neo4j Browser
- 7687: Neo4j Bolt
- 5432: PostgreSQL
- 3000: Grafana
- 9090: Prometheus

## Security

Important security considerations:

1. Never commit your `.env` file to version control
2. Rotate the JWT and session secrets regularly
3. Use strong passwords for database access
4. Consider network segregation for production deployments
5. Enable TLS for all external-facing services in production

## Scaling

To scale the system:

1. Increase the number of MCP Server instances:
   ```bash
   docker-compose up -d --scale mcp-server=3
   ```

2. Add a load balancer in front of the MCP Server instances

3. Consider using dedicated instances for Neo4j and Qdrant in production environments

## Backup

To backup the system data:

1. For Neo4j:
   ```bash
   docker-compose exec neo4j neo4j-admin dump --database=neo4j --to=/backup/neo4j.dump
   ```

2. For Qdrant:
   ```bash
   # Qdrant data is stored in the qdrant_storage volume
   # Use docker volume backup strategies
   ```

3. For Supabase/PostgreSQL:
   ```bash
   docker-compose exec supabase pg_dump -U postgres -d postgres > backup.sql
   ```