# Enhanced Memory Vector RAG

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/BjornMelin/enhanced-mem-vector-rag/graphs/commit-activity)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://makeapullrequest.com)
[![Documentation Status](https://img.shields.io/badge/docs-in%20progress-orange)](https://github.com/BjornMelin/enhanced-mem-vector-rag/wiki)

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

## Architecture

EMVR implements a layered architecture:

1. **Storage Layer**
   - Vector Database (Qdrant)
   - Graph Database (Neo4j via Graphiti)
   - Memory System (mem0)

2. **Integration Layer**
   - LlamaIndex Connectors
   - LangChain Components

3. **Orchestration Layer**
   - Hybrid Retrieval Manager
   - Context Fusion Engine
   - Knowledge Graph Traversal

4. **Application Layer**
   - Query Interfaces
   - Response Generation
   - Custom Agent Workflows

## Getting Started

### Prerequisites

- Python 3.9+
- Docker (recommended for Neo4j and Qdrant)
- Basic understanding of RAG systems

### Installation

```bash
# Clone the repository
git clone https://github.com/BjornMelin/enhanced-mem-vector-rag.git
cd enhanced-mem-vector-rag

# Install dependencies
pip install -e .
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

### Graph Knowledge Base (Graphiti/Neo4j)

The graph component uses Graphiti with Neo4j to:

- Store structured relationships between entities
- Enable complex traversal queries
- Support reasoning about interconnected concepts
- Provide explicit knowledge paths

### Vector Storage (Qdrant)

The vector component uses Qdrant to:

- Store and retrieve document embeddings
- Perform efficient similarity search
- Support semantic matching
- Handle large-scale vector operations

### Framework Integration (LlamaIndex & LangChain)

EMVR integrates with both major RAG frameworks:

- **LlamaIndex** - For advanced indexing and retrieval operations
- **LangChain** - For agent-based workflows and tool integration

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

- [ ] Initial release with core functionality
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