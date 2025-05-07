# EMVR Retrievers

This directory contains the implementation of custom retriever components for the EMVR system.

## Components

- `hybrid_retriever.py`: Implementation of the hybrid retrieval system combining Qdrant vector search with Neo4j graph traversal
- `memory_retriever.py`: Retriever for accessing memory using mem0
- `context_aware_retriever.py`: Retriever that takes context into account during retrieval

## Usage

These retrievers are used by the MCP server and can also be used directly in Python code:

```python
from emvr.retrievers.hybrid_retriever import HybridRetriever

# Initialize the retriever
retriever = HybridRetriever(
    qdrant_collection="emvr_vectors",
    neo4j_uri="bolt://localhost:7687",
    neo4j_user="neo4j",
    neo4j_password="password",
)

# Perform a hybrid search
results = retriever.retrieve("What is the relationship between X and Y?")
```
