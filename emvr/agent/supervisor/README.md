# Supervisor Agent for EMVR System

This directory contains the implementation of the supervisor agent for the Enhanced Memory-Vector RAG (EMVR) system. The supervisor agent uses LangGraph to orchestrate multiple worker agents in a supervisor-worker pattern.

## Components

- `base.py`: Base supervisor agent implementation using LangGraph
- `workers.py`: Worker agent implementations for specialized tasks
- `__init__.py`: Package exports

## Architecture

The supervisor agent implements a LangGraph-based workflow that routes tasks to specialized worker agents:

1. **Supervisor Agent**: Central coordinator that decides which worker agent should handle a given task
2. **Worker Agents**:
   - **Research Worker**: Specialized in information retrieval and search
   - **Knowledge Graph Worker**: Specialized in knowledge graph operations
   - **Memory Management Worker**: Specialized in memory system maintenance

## Usage

The supervisor agent can be used through the agent workflow:

```python
from emvr.agent.workflows import AgentWorkflowFactory

# Create a workflow
workflow = AgentWorkflowFactory.create_workflow()

# Run a query
result = await workflow.run("What information do we have about machine learning?")

# Access the result
print(result.output)
```

## State Management

The supervisor agent uses LangGraph's checkpointing mechanism to maintain conversation state, allowing for multi-turn interactions within the same thread context.