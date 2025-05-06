# Custom Memory MCP Server

This directory contains the implementation of the custom `memory` MCP server using the FastMCP framework. 

## Endpoints

- `/search.hybrid`: Hybrid search across vector and graph stores
- `/graph.query`: Knowledge graph queries
- `/memory.*`: Memory management operations
- `/rules.validate`: Rule validation
- `/ingest.*`: Data ingestion endpoints

## Implementation

The MCP server leverages LlamaIndex as the central orchestration framework to connect to and query the following backend components:

- Qdrant: Vector storage for semantic search
- Neo4j/Graphiti: Graph database for structured knowledge
- Mem0: Memory interface for personalization
- Supabase: Metadata storage

## Usage with Claude Code

This MCP server is designed to be used with Claude Code. See [CLAUDE.md](../../CLAUDE.md) for detailed usage instructions.

## Development

See the Dockerfile.dev and docker-compose.dev.yml files for setting up the development environment.

```bash
# Start the development environment
docker-compose -f docker-compose.dev.yml up
```