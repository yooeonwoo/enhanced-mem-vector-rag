"""
Agent-related MCP server endpoints for the EMVR system.

This module implements the endpoints for agent operations in the custom 'memory' MCP server.
"""

import logging
import uuid
from typing import Annotated, Any

from fastmcp import Context, MCPServer
from pydantic import BaseModel, Field

from emvr.agent.workflows import AgentWorkflowFactory

# Configure logging
logger = logging.getLogger(__name__)


# ----- Request/Response Models -----

class AgentRunRequest(BaseModel):
    """Request schema for running an agent."""

    query: str
    thread_id: str | None = None
    context: list[dict[str, Any]] | None = None
    params: dict[str, Any] | None = None


class WorkerRunRequest(BaseModel):
    """Request schema for running a worker agent."""

    worker_name: str
    query: str
    thread_id: str | None = None
    context: list[dict[str, Any]] | None = None
    params: dict[str, Any] | None = None


# ----- MCP Endpoint Functions -----

async def register_agent_endpoints(mcp: MCPServer) -> None:
    """Register all agent MCP endpoints."""
    # Agent workflow singleton
    agent_workflow = None

    def get_agent_workflow():
        """Get or create the agent workflow."""
        nonlocal agent_workflow
        if agent_workflow is None:
            agent_workflow = AgentWorkflowFactory.create_workflow()
        return agent_workflow

    # ----- Agent Operations -----

    @mcp.tool()
    async def agent_run(
        query: Annotated[str, Field(description="The query to process")],
        thread_id: Annotated[str | None, Field(description="Optional thread ID for conversation context")] = None,
        context: Annotated[list[dict[str, Any]] | None, Field(description="Optional context for the agent")] = None,
        params: Annotated[dict[str, Any] | None, Field(description="Optional parameters for the agent")] = None,
        ctx: Context = None,
    ) -> dict[str, Any]:
        """
        Run the agent workflow on a query.

        The agent will process the query through the supervisor-worker pattern and return a response.
        """
        try:
            await ctx.info(f"Running agent workflow with query: {query}")

            # Get the agent workflow
            workflow = get_agent_workflow()

            # Process parameters
            thread_id = thread_id or str(uuid.uuid4())

            # Process context if provided
            workflow_params = params or {}
            workflow_params["thread_id"] = thread_id

            if context:
                # TODO: Handle context integration
                pass

            # Execute the workflow
            result = await workflow.run(query, **workflow_params)

            # Format response
            return {
                "success": result.success,
                "output": result.output,
                "thread_id": thread_id,
                "error": result.error,
                "status": "success" if result.success else "error",
            }
        except Exception as e:
            logger.exception(f"Agent workflow execution failed: {e}")
            await ctx.error(f"Failed to execute agent workflow: {e}")

            return {
                "success": False,
                "output": "",
                "thread_id": thread_id or str(uuid.uuid4()),
                "error": str(e),
                "status": "error",
            }

    @mcp.tool()
    async def agent_run_worker(
        worker_name: Annotated[str, Field(description="Name of the worker agent to run")],
        query: Annotated[str, Field(description="The query to process")],
        thread_id: Annotated[str | None, Field(description="Optional thread ID for conversation context")] = None,
        context: Annotated[list[dict[str, Any]] | None, Field(description="Optional context for the agent")] = None,
        params: Annotated[dict[str, Any] | None, Field(description="Optional parameters for the agent")] = None,
        ctx: Context = None,
    ) -> dict[str, Any]:
        """
        Run a specific worker agent on a query.

        Each worker agent has a specialized capability (research, knowledge_graph, memory_management).
        """
        try:
            await ctx.info(f"Running worker agent '{worker_name}' with query: {query}")

            # Get the agent workflow
            workflow = get_agent_workflow()

            # Check if worker exists
            if worker_name not in workflow.worker_agents:
                return {
                    "success": False,
                    "output": "",
                    "thread_id": thread_id or str(uuid.uuid4()),
                    "error": f"Worker agent '{worker_name}' not found",
                    "status": "error",
                }

            # Process parameters
            thread_id = thread_id or str(uuid.uuid4())

            # Process context if provided
            worker_params = params or {}
            worker_params["thread_id"] = thread_id

            if context:
                # TODO: Handle context integration
                pass

            # Execute the worker agent directly
            worker_agent = workflow.worker_agents[worker_name]
            result = await worker_agent.run(query, **worker_params)

            # Format response
            return {
                "success": result.success,
                "output": result.output,
                "thread_id": thread_id,
                "error": result.error,
                "status": "success" if result.success else "error",
            }
        except Exception as e:
            logger.exception(f"Worker agent execution failed: {e}")
            await ctx.error(f"Failed to execute worker agent: {e}")

            return {
                "success": False,
                "output": "",
                "thread_id": thread_id or str(uuid.uuid4()),
                "error": str(e),
                "status": "error",
            }


# ----- Resources (Static Knowledge) -----

async def register_agent_resources(mcp: MCPServer) -> None:
    """Register all agent MCP resources."""

    @mcp.resource(
        uri="memory://agent-guide",
        name="AgentSystemGuide",
        description="Guide for using the agent system",
        mime_type="text/markdown",
    )
    async def agent_guide() -> str:
        """Return the Agent System usage guide."""
        return """
        # Agent System Guide

        The EMVR system includes an agent orchestration framework with a supervisor agent
        and multiple specialized worker agents using LangGraph.

        ## Main Agent Workflow

        Use the main agent workflow for general queries and tasks:

        ```python
        result = await agent.run(
            query="What information do we have about machine learning?",
            thread_id="optional-conversation-id"
        )
        ```

        ## Worker Agents

        For specialized tasks, you can use specific worker agents directly:

        ### Research Agent

        Specializes in information retrieval and search:

        ```python
        result = await agent.run_worker(
            worker_name="research_agent",
            query="Find all information related to transformers architecture"
        )
        ```

        ### Knowledge Graph Agent

        Specializes in knowledge graph operations and queries:

        ```python
        result = await agent.run_worker(
            worker_name="knowledge_graph_agent",
            query="What entities are related to LlamaIndex?"
        )
        ```

        ### Memory Management Agent

        Specializes in memory operations like entity creation and observation management:

        ```python
        result = await agent.run_worker(
            worker_name="memory_management_agent",
            query="Create a new entity for the FastEmbed library"
        )
        ```

        ## Providing Context

        You can provide additional context to any agent:

        ```python
        result = await agent.run(
            query="What can you tell me about this concept?",
            context=[
                {"content": "...", "source": "..."},
                {"content": "...", "source": "..."}
            ]
        )
        ```

        ## Thread ID for Conversation Context

        Pass a thread_id to maintain conversation context across multiple requests:

        ```python
        result = await agent.run(
            query="Tell me more about that",
            thread_id="previous-conversation-id"
        )
        ```

        ## Additional Parameters

        Pass additional parameters as needed:

        ```python
        result = await agent.run(
            query="...",
            params={
                "detailed": True,
                "max_sources": 5
            }
        )
        ```
        """
