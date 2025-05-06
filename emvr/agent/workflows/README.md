# Agent Workflows for EMVR System

This directory contains the implementation of agent workflows for the Enhanced Memory-Vector RAG (EMVR) system. These workflows leverage LangGraph to create sophisticated agent orchestration patterns.

## Components

- `agent_workflow.py`: Main agent workflow implementation
- `factory.py`: Factory for creating agent workflows
- `__init__.py`: Package exports

## Architecture

The agent workflow system implements a supervisor-worker pattern using LangGraph:

1. **Agent Workflow**: The main entry point that manages the entire agent ecosystem
2. **Supervisor Agent**: Coordinates and routes tasks to worker agents
3. **Worker Agents**:
   - **Research Worker**: For information retrieval and search
   - **Knowledge Graph Worker**: For knowledge graph operations
   - **Memory Management Worker**: For memory system maintenance

## Usage

The agent workflow can be used directly or through the MCP server:

```python
from emvr.agent.workflows import AgentWorkflowFactory

# Create a workflow
workflow = AgentWorkflowFactory.create_workflow()

# Run a query with thread tracking
result = await workflow.run(
    query="What information do we have about machine learning?",
    thread_id="conversation-123"
)

# Access the result
print(result.output)
```

## State Management

The workflow uses LangGraph's checkpointing mechanism to maintain conversation state, allowing for multi-turn interactions within the same thread context.