# Enhanced Memory Vector RAG

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/BjornMelin/enhanced-mem-vector-rag/graphs/commit-activity)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://makeapullrequest.com)
[![Documentation Status](https://img.shields.io/badge/docs-in%20progress-orange)](https://github.com/BjornMelin/enhanced-mem-vector-rag/wiki)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Ready-purple.svg)](https://github.com/BjornMelin/enhanced-mem-vector-rag/blob/main/CLAUDE.md)

⚡ Developer-friendly hybrid-RAG toolkit merging Graphiti, Qdrant, mem0, LlamaIndex, and LangChain into one powerful engine.

This implementation creates a sophisticated knowledge retrieval system by integrating KAG methodologies with traditional RAG approaches. It seamlessly combines Graphiti's graph intelligence, Qdrant's vector capabilities, and mem0's memory persistence - all accessible through flexible LlamaIndex and LangChain interfaces for applications requiring both factual accuracy and contextual understanding.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Quick Start](#quick-start)
- [Components](#components)
  - [Memory System (mem0)](#memory-system-mem0)
  - [Graph Knowledge Base (Graphiti/Neo4j)](#graph-knowledge-base-graphitineo4j)
  - [Vector Storage (Qdrant)](#vector-storage-qdrant)
  - [Framework Integration (LlamaIndex & LangChain)](#framework-integration-llamaindex--langchain)
- [Usage Examples](#usage-examples)
- [Configuration](#configuration)
- [Benchmarks](#benchmarks)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [How to Cite](#how-to-cite)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Claude Code Development](#claude-code-development)
- [Deployment](#deployment)

## Overview

Enhanced Memory Vector RAG (EMVR) is a comprehensive framework that combines the strengths of multiple retrieval methodologies to create a more robust, accurate, and contextually aware knowledge system. By integrating graph-based Knowledge-Augmented Generation (KAG) with traditional vector-based Retrieval-Augmented Generation (RAG), EMVR provides superior performance in complex knowledge retrieval tasks.

The system leverages:
- **Graphiti/Neo4j** for structured knowledge representation and graph traversal
- **Qdrant** for efficient vector similarity search
- **mem0** for persistent memory and context management
- **LlamaIndex & LangChain** for flexible orchestration and agent-based workflows

## Features

- 🔄 **Hybrid Retrieval System** - Combines vector similarity search with graph-based knowledge retrieval
- 🧠 **Persistent Memory** - Maintains context and relationships across sessions
- 🔍 **Multi-modal Search** - Query across different data types and structures
- 🔗 **Knowledge Graph Integration** - Leverages structured relationships for improved context
- 🚀 **Framework Flexibility** - Works with both LlamaIndex and LangChain
- 📊 **Extensible Architecture** - Easy to customize and extend for specific use cases
- 🛠️ **Developer-Friendly APIs** - Simple interfaces for complex retrieval operations
- 📈 **Performance Optimization** - Efficient retrieval strategies for reduced latency
- 🐳 **Docker Deployment** - Containerized architecture for easy deployment

## Architecture

EMVR implements a comprehensive layered architecture integrating multiple components for advanced retrieval:

### Layered Architecture

```mermaid
graph TD
    subgraph "Application Layer"
        QueryInterface("Query Interfaces")
        ResponseGen("Response Generation")
        AgentWorkflows("Custom Agent Workflows")
        MCP("Model Context Protocol (MCP)")
    end

    subgraph "Orchestration Layer"
        HybridManager("Hybrid Retrieval Manager")
        ContextFusion("Context Fusion Engine")
        GraphTraversal("Knowledge Graph Traversal")
        LangGraph("LangGraph Orchestration")
    end

    subgraph "Integration Layer"
        LlamaIndexConn("LlamaIndex Connectors")
        LangChainComp("LangChain Components")
        FastEmbed("FastEmbed Integration")
        FastMCP("FastMCP Framework")
    end

    subgraph "Storage Layer"
        Qdrant("Vector Database (Qdrant)")
        Neo4j("Graph Database (Neo4j/Graphiti)")
        Mem0("Memory System (mem0)")
        Supabase("Metadata Storage (Supabase)")
    end

    QueryInterface --> HybridManager
    ResponseGen --> ContextFusion
    AgentWorkflows --> GraphTraversal
    AgentWorkflows --> HybridManager
    MCP --> FastMCP
    
    LangGraph --> LangChainComp
    HybridManager --> LlamaIndexConn
    HybridManager --> LangChainComp
    ContextFusion --> LlamaIndexConn
    ContextFusion --> LangChainComp
    GraphTraversal --> LlamaIndexConn
    FastMCP --> LlamaIndexConn
    
    FastEmbed -.-> Qdrant
    LlamaIndexConn --> Qdrant
    LlamaIndexConn --> Neo4j
    LlamaIndexConn --> Mem0
    LlamaIndexConn --> Supabase
    LangChainComp --> Qdrant
    LangChainComp --> Neo4j
    LangChainComp --> Mem0
    LangChainComp --> Supabase
```

### Comprehensive System Architecture

```mermaid
graph TB
    User([User]) <--> ClaudeCode["Claude Code & MCP Tools"]
    ClaudeCode <--> CustomMCP["Custom 'memory' MCP Server\n(FastMCP Framework)"]
    ClaudeCode <--> ExternalMCP["External MCP Servers\n(tavily, firecrawl, context7, etc.)"]
    
    subgraph "Agent System"
        LangGraph["LangGraph\n(Agent Orchestration)"]
        LangChain["LangChain\n(Agent Tools & Planning)"]
        Agents["Specialized Agents\n(Supervisor-Worker Pattern)"]
        
        LangGraph --> LangChain
        LangGraph --> Agents
    end
    
    subgraph "RAG Framework"
        LlamaIndex["LlamaIndex\n(Core RAG Framework)"]
        QueryEngines["Query Engines\n(Vector, Graph, Hybrid)"]
        Retrievers["Specialized Retrievers"]
        DataLoaders["Data Loaders & Indexers"]
        
        LlamaIndex --> QueryEngines
        LlamaIndex --> Retrievers
        LlamaIndex --> DataLoaders
    end
    
    subgraph "Memory & Storage"
        Qdrant[(Qdrant\nVector Store)]
        Neo4j[(Neo4j\nGraph Database)]
        Mem0["Mem0\n(Memory Interface)"]
        Graphiti["Graphiti\n(Graph Interface)"]
        Supabase[(Supabase\nMetadata & Documents)]
        S3[(AWS S3\nOriginal Documents)]
        
        Mem0 -.-> Qdrant
        Graphiti -.-> Neo4j
    end
    
    subgraph "Embedding & Ingestion"
        FastEmbed["FastEmbed\nEmbedding Generation"]
        WebCrawlers["Web Crawlers\n(Crawl4AI, Firecrawl)"]
        ConnectorAPIs["Connector APIs\n(GitHub, Reddit, etc.)"]
        
        FastEmbed --> Qdrant
        WebCrawlers --> DataLoaders
        ConnectorAPIs --> DataLoaders
    end
    
    CustomMCP <--> LangGraph
    CustomMCP <--> LlamaIndex
    
    LangGraph <--> LlamaIndex
    
    LlamaIndex <--> Qdrant
    LlamaIndex <--> Neo4j
    LlamaIndex <--> Mem0
    LlamaIndex <--> Graphiti
    LlamaIndex <--> Supabase
    
    DataLoaders --> S3
    DataLoaders --> Supabase
    DataLoaders --> Qdrant
    DataLoaders --> Neo4j
    
    style CustomMCP fill:#f9d6ff,stroke:#9333ea,stroke-width:2px
    style LlamaIndex fill:#d1fae5,stroke:#059669,stroke-width:2px
    style LangGraph fill:#dbeafe,stroke:#3b82f6,stroke-width:2px
    style Qdrant fill:#fee2e2,stroke:#ef4444,stroke-width:2px
    style Neo4j fill:#ffedd5,stroke:#f97316,stroke-width:2px
```

## Data Flow

```mermaid
flowchart LR
    classDef userInteraction fill:#f9d6ff,stroke:#9333ea,stroke-width:2px
    classDef retrieval fill:#dbeafe,stroke:#3b82f6,stroke-width:2px
    classDef processing fill:#d1fae5,stroke:#059669,stroke-width:2px
    classDef storage fill:#fee2e2,stroke:#ef4444,stroke-width:2px
    classDef fusion fill:#ffedd5,stroke:#f97316,stroke-width:2px
    
    Input("User Query/Task") --> ClaudeCode("Claude Code\nMCP Interface")
    ClaudeCode --> MemoryMCP("Custom 'memory'\nMCP Server")
    
    MemoryMCP --> Agent("Agent System\n(LangChain/LangGraph)")
    
    Agent --> VR("Vector Retrieval\n(Qdrant via LlamaIndex)")
    Agent --> GR("Graph Retrieval\n(Neo4j/Graphiti via LlamaIndex)")
    Agent --> MR("Memory Retrieval\n(mem0)")
    Agent --> WS("Web Search\n(Tavily/Firecrawl)")
    
    VR --> CF("Context Fusion\n(LlamaIndex Orchestration)")
    GR --> CF
    MR --> CF
    WS --> CF
    
    CF --> QP("Query Planning\n(LangGraph)")
    QP --> RT("Response Templates")
    
    CF --> LLM("Large Language Model")
    RT --> LLM
    LLM --> Response("Enhanced Response")
    
    Response --> MemUpdate("Memory Update\n(mem0)")
    Response --> KGUpdate("Knowledge Graph Update\n(Neo4j)")
    Response --> MetaUpdate("Metadata Update\n(Supabase)")
    
    Response --> ClaudeCode
    ClaudeCode --> User([User])
    
    class Input,ClaudeCode,User userInteraction
    class VR,GR,MR,WS retrieval
    class QP,RT,LLM processing
    class MemUpdate,KGUpdate,MetaUpdate storage
    class CF fusion
```

### MCP Interaction Flow

```mermaid
sequenceDiagram
    participant User
    participant Claude as Claude Code
    participant Memory as custom 'memory' MCP
    participant External as External MCP Servers
    participant LlamaIdx as LlamaIndex
    participant Storage as Storage Systems
    
    User->>Claude: Query or Task
    Claude->>Memory: memory.read_graph()
    Memory->>LlamaIdx: Query through LlamaIndex
    LlamaIdx->>Storage: Fetch from Qdrant/Neo4j/Supabase
    Storage-->>LlamaIdx: Return relevant data
    LlamaIdx-->>Memory: Process & return results
    Memory-->>Claude: Return graph state
    
    Claude->>External: context7.get_library_docs()
    External-->>Claude: Return documentation
    
    Note over Claude,Memory: Agent Planning & Execution
    
    Claude->>Memory: Execute retrieval/update
    Memory->>LlamaIdx: Orchestrate operations
    LlamaIdx->>Storage: Execute operations
    Storage-->>LlamaIdx: Return operation results
    LlamaIdx-->>Memory: Process & return results
    Memory-->>Claude: Return operation status/results
    
    Claude->>Memory: memory.add_observations()
    Memory->>Storage: Update memory state
    
    Claude-->>User: Deliver response/results
```

## Getting Started

### Prerequisites

- Python 3.11+
- Docker (recommended for Neo4j, Qdrant, and Supabase)
- `uv` for Python package management
- Basic understanding of RAG systems

### Installation

#### Local Development

```bash
# Clone the repository
git clone https://github.com/BjornMelin/enhanced-mem-vector-rag.git
cd enhanced-mem-vector-rag

# Install dependencies using uv
uv pip install -r requirements.txt
```

#### Docker Deployment

```bash
# Navigate to deployment directory
cd emvr/deployment

# Setup environment
./setup_local.sh

# Start services
docker compose up -d
```

### Quick Start

```python
from emvr import EmvrSystem

# Initialize the system
system = EmvrSystem()

# Load data
system.load_documents("path/to/documents")
system.build_knowledge_graph()

# Query the system
response = system.query("What is the relationship between X and Y?")
print(response)
```

## Components

### Memory System (mem0)

The memory component leverages mem0 to maintain persistent context across queries and sessions. This allows the system to:

- Remember previous interactions
- Build cumulative knowledge
- Maintain entity relationships
- Support temporal reasoning

```mermaid
graph LR
    Query("User Query") --> Memory("mem0 Memory System")
    Memory --> Scoring("Relevance Scoring")
    Memory --> Personalization("Personalization Layer")
    Memory --> Context("Contextual History")
    
    Scoring --> Retrieval("Enhanced Retrieval")
    Personalization --> Retrieval
    Context --> Retrieval
    
    Retrieval --> LLM("Large Language Model")
    LLM --> Response("Enhanced Response")
    Response --> Memory
```

### Graph Knowledge Base (Graphiti/Neo4j)

The graph component uses Graphiti with Neo4j to:

- Store structured relationships between entities
- Enable complex traversal queries
- Support reasoning about interconnected concepts
- Provide explicit knowledge paths

```mermaid
graph TD
    subgraph "Knowledge Graph (Neo4j/Graphiti)"
        Entity1("Entity A")
        Entity2("Entity B")
        Entity3("Entity C")
        Entity4("Entity D")
        
        Entity1 -- "relates_to" --> Entity2
        Entity2 -- "depends_on" --> Entity3
        Entity1 -- "creates" --> Entity4
        Entity3 -- "part_of" --> Entity4
    end
    
    Query("Knowledge Query") --> GraphTraversal("Graph Traversal (Graphiti)")
    GraphTraversal --> Neo4j("Neo4j Database")
    Neo4j --> Results("Structured Results")
    Results --> LLM("LLM for Reasoning")
```

### Vector Storage (Qdrant)

The vector component uses Qdrant to:

- Store and retrieve document embeddings
- Perform efficient similarity search
- Support semantic matching
- Handle large-scale vector operations

```mermaid
graph TD
    Documents["Input Documents"] --> TextChunker["Text Chunker"]
    TextChunker --> EmbeddingGen["Embedding Generation"]
    EmbeddingGen --> VectorDB["Qdrant Vector Database"]
    
    Query["User Query"] --> QueryEmbed["Query Embedding"]
    QueryEmbed --> SearchVec["Vector Search"]
    SearchVec --> VectorDB
    VectorDB --> TopMatches["Top K Matches"]
    TopMatches --> Reranker["Reranker"]
    Reranker --> ContextGen["Context Generation"]
```

### Framework Integration (LlamaIndex & LangChain)

EMVR integrates with both major RAG frameworks:

- **LlamaIndex** - For advanced indexing and retrieval operations
- **LangChain** - For agent-based workflows and tool integration

```mermaid
graph TD
    subgraph "LlamaIndex Integration"
        Docs[("Documents")] --> Loaders["Data Loaders"]
        Loaders --> Indexing["Indexing Pipelines"]
        Indexing --> QueryEngines["Query Engines"]
        QueryEngines --> RetFramework["Retrieval Framework"]
    end
    
    subgraph "LangChain Integration"
        Agents["Agent Framework"] --> Planning["Planning Modules"]
        Planning --> Tools["Tool Integration"]
        Tools --> Memory["Memory Components"]
        Memory --> Callbacks["Callback Handlers"]
    end
    
    RetFramework <--> Tools
    QueryEngines <--> Agents
```

## Usage Examples

Examples are coming soon. They will demonstrate:

- Basic RAG workflows
- Knowledge graph integration
- Multi-hop reasoning
- Custom retrieval strategies
- Agent-based applications

## Configuration

EMVR can be configured through:

- Configuration files
- Environment variables
- Programmatic settings

Detailed configuration options will be provided in the upcoming documentation.

## Benchmarks

Performance benchmarks comparing EMVR to traditional RAG systems will be available soon.

## Roadmap

- [x] Initial release with core functionality
- [x] Basic documentation
- [x] Agent orchestration implementation
- [x] UI implementation with Chainlit
- [x] Docker containerization and deployment
- [ ] Comprehensive documentation
- [ ] Performance benchmarks
- [ ] Advanced examples
- [ ] Cloud deployment guides
- [ ] Additional vector database integrations
- [ ] Custom agent templates

## Contributing

Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines.

## How to Cite

If you use EMVR in your research, please cite:

```bibtex
@software{emvr2025,
  author = {Melin, Bjorn},
  title = {Enhanced Memory Vector RAG: A Hybrid Retrieval Framework},
  year = {2025},
  url = {https://github.com/BjornMelin/enhanced-mem-vector-rag},
  version = {0.1.0}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Graphiti](https://github.com/neo4j/graphiti) for Neo4j integration
- [Qdrant](https://github.com/qdrant/qdrant) for vector database capabilities
- [mem0](https://github.com/mem0ai/mem0) for memory systems
- [LlamaIndex](https://github.com/run-llama/llama_index) for indexing frameworks
- [LangChain](https://github.com/langchain-ai/langchain) for agent orchestration

## Custom MCP Server Implementation

This project implements a custom `memory` MCP server using the FastMCP framework that serves as the central interface between Claude Code and the system's backend components:

```mermaid
flowchart TD
    classDef mcp fill:#f9d6ff,stroke:#9333ea,stroke-width:2px
    classDef frameworks fill:#d1fae5,stroke:#059669,stroke-width:2px
    classDef storage fill:#fee2e2,stroke:#ef4444,stroke-width:2px
    
    Claude([Claude Code]) --> MCP["Custom 'memory' MCP Server\n(FastMCP Framework)"]
    
    subgraph "MCP Endpoints"
        SearchHybrid["/search.hybrid"]
        GraphQuery["/graph.query"]
        MemoryOps["/memory.*"]
        RulesValidate["/rules.validate"]
        IngestOps["/ingest.*"]
    end
    
    MCP --> SearchHybrid
    MCP --> GraphQuery
    MCP --> MemoryOps
    MCP --> RulesValidate
    MCP --> IngestOps
    
    SearchHybrid --> LlamaIndex["LlamaIndex\nRAG Orchestration"]
    GraphQuery --> LlamaIndex
    MemoryOps --> LlamaIndex
    RulesValidate --> APOC["Neo4j APOC\nRules Engine"]
    IngestOps --> LlamaIndex
    
    LlamaIndex --> Qdrant[(Qdrant)]
    LlamaIndex --> Neo4j[(Neo4j)]
    LlamaIndex --> Supabase[(Supabase)]
    APOC --> Neo4j
    
    Mem0["Mem0 SDK"] --> Qdrant
    Graphiti["Graphiti Client"] --> Neo4j
    
    class MCP,SearchHybrid,GraphQuery,MemoryOps,RulesValidate,IngestOps mcp
    class LlamaIndex,APOC,Mem0,Graphiti frameworks
    class Qdrant,Neo4j,Supabase storage
```

### Key MCP Endpoints

| Endpoint | Description | Implementation |
|----------|-------------|----------------|
| `/search.hybrid` | Performs hybrid search across vector and graph stores | Uses LlamaIndex for orchestrating hybrid search across Qdrant and Neo4j |
| `/graph.query` | Executes knowledge graph queries | Translates natural language to Cypher using LlamaIndex's `KnowledgeGraphQueryEngine` |
| `/memory.*` | Operations for memory management | Includes CRUD operations for graph entities and observations |
| `/rules.validate` | Validates operations against defined rules | Uses Neo4j APOC for rule enforcement |
| `/ingest.*` | Handles data ingestion from various sources | Utilizes LlamaIndex data loaders and FastEmbed for embedding generation |

## Claude Code Development

This project provides a detailed development guide for Claude Code users. The guide includes:

- Project overview and technical architecture
- Development workflow and memory protocol
- Coding standards and practices
- Git workflow
- MCP server documentation and usage
- Key architectural components and their roles

For Claude Code development, please refer to [CLAUDE.md](CLAUDE.md) for comprehensive guidelines.

## Deployment

The project includes a complete deployment system using Docker Compose:

### Docker Components

- **MCP Server**: FastAPI server implementing the Model Context Protocol
- **Chainlit UI**: Web interface for user interaction
- **Qdrant**: Vector database for semantic search
- **Neo4j**: Graph database for knowledge graphs
- **Supabase**: PostgreSQL for structured data and metadata
- **Grafana/Prometheus**: Monitoring and observability

### Deployment Options

#### Local Deployment

```bash
# Navigate to deployment directory
cd emvr/deployment

# Set up environment
./setup_local.sh

# Start services using docker-compose
docker compose up -d
```

#### Using Makefile

```bash
cd emvr/deployment
make setup    # Run setup script
make up       # Start all services
```

### Security

The deployment includes comprehensive security features:

- JWT-based authentication
- Role-Based Access Control (RBAC)
- Secure environment variable management
- Container-based isolation

### Monitoring & Observability

Access system metrics and logs through:

- Grafana dashboard: http://localhost:3000
- Prometheus metrics: http://localhost:9090

### Backup & Restore

The system includes scripts for data backup and restoration:

```bash
# Create backup
./scripts/backup.sh

# Restore from backup
./scripts/restore.sh ./backups/emvr_backup_20250506_120000.tar.gz
```

For detailed deployment instructions, see the [deployment README](emvr/deployment/README.md).