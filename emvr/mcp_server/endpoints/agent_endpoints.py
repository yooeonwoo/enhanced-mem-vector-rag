"""
Agent-related MCP server endpoints for the EMVR system.

This module implements the endpoints for agent operations in the custom 'memory' MCP server.
"""

import logging
from typing import Dict, List, Optional, Any, Union, Annotated

from fastmcp import MCPServer, Context
from pydantic import Field, BaseModel

from emvr.agents.orchestration import get_orchestrator
from emvr.config import get_settings

# Configure logging
logger = logging.getLogger(__name__)


# ----- Request/Response Models -----

class AgentRunRequest(BaseModel):
    """Request schema for running an agent."""
    query: str
    context: Optional[List[Dict[str, Any]]] = None
    params: Optional[Dict[str, Any]] = None


class WorkerRunRequest(BaseModel):
    """Request schema for running a worker agent."""
    worker_name: str
    query: str
    context: Optional[List[Dict[str, Any]]] = None
    params: Optional[Dict[str, Any]] = None


# ----- MCP Endpoint Functions -----

async def register_agent_endpoints(mcp: MCPServer) -> None:
    """Register all agent MCP endpoints."""
    
    # ----- Agent Operations -----
    
    @mcp.tool()
    async def agent_run(
        query: Annotated[str, Field(description="The query to process")],
        context: Annotated[Optional[List[Dict[str, Any]]], Field(description="Optional context for the agent")] = None,
        params: Annotated[Optional[Dict[str, Any]], Field(description="Optional parameters for the agent")] = None,
        ctx: Context = None
    ) -> Dict[str, Any]:
        """
        Run the main agent system on a query.
        
        The agent will process the query and return a response based on its capabilities.
        """
        try:
            await ctx.info(f"Running agent with query: {query}")
            
            # Get the orchestrator
            orchestrator = get_orchestrator()
            if orchestrator is None:
                return {
                    "error": "Agent system not initialized",
                    "status": "error"
                }
            
            # Execute the agent
            params = params or {}
            if context:
                params["context"] = context
            
            result = await orchestrator.run(query, **params)
            
            return result
        except Exception as e:
            logger.error(f"Agent execution failed: {e}")
            await ctx.error(f"Failed to execute agent: {e}")
            raise
    
    @mcp.tool()
    async def agent_run_worker(
        worker_name: Annotated[str, Field(description="Name of the worker agent to run")],
        query: Annotated[str, Field(description="The query to process")],
        context: Annotated[Optional[List[Dict[str, Any]]], Field(description="Optional context for the agent")] = None,
        params: Annotated[Optional[Dict[str, Any]], Field(description="Optional parameters for the agent")] = None,
        ctx: Context = None
    ) -> Dict[str, Any]:
        """
        Run a specific worker agent on a query.
        
        Each worker agent has a specialized capability (research, ingestion, analysis, creative).
        """
        try:
            await ctx.info(f"Running worker agent '{worker_name}' with query: {query}")
            
            # Get the orchestrator
            orchestrator = get_orchestrator()
            if orchestrator is None:
                return {
                    "error": "Agent system not initialized",
                    "status": "error"
                }
            
            # Execute the worker agent
            params = params or {}
            if context:
                params["context"] = context
            
            result = await orchestrator.run_worker(worker_name, query, **params)
            
            return result
        except Exception as e:
            logger.error(f"Worker agent execution failed: {e}")
            await ctx.error(f"Failed to execute worker agent: {e}")
            raise


# ----- Resources (Static Knowledge) -----

async def register_agent_resources(mcp: MCPServer) -> None:
    """Register all agent MCP resources."""
    
    @mcp.resource(
        uri="memory://agent-guide",
        name="AgentSystemGuide",
        description="Guide for using the agent system",
        mime_type="text/markdown"
    )
    async def agent_guide() -> str:
        """Return the Agent System usage guide."""
        return """
        # Agent System Guide
        
        The EMVR system includes an agent orchestration framework with a supervisor agent
        and multiple specialized worker agents.
        
        ## Main Agent
        
        Use the main agent for general queries and tasks:
        
        ```python
        result = await agent.run("What information do we have about machine learning?")
        ```
        
        ## Worker Agents
        
        For specialized tasks, you can use specific worker agents:
        
        ### Research Agent
        
        Specializes in information gathering and synthesis:
        
        ```python
        result = await agent.run_worker(
            worker_name="research",
            query="Find all information related to transformers architecture"
        )
        ```
        
        ### Ingestion Agent
        
        Specializes in data processing and storage:
        
        ```python
        result = await agent.run_worker(
            worker_name="ingestion",
            query="Process this research paper and extract key information"
        )
        ```
        
        ### Analysis Agent
        
        Specializes in data analysis and pattern recognition:
        
        ```python
        result = await agent.run_worker(
            worker_name="analysis",
            query="Analyze these sales figures and identify trends"
        )
        ```
        
        ### Creative Agent
        
        Specializes in idea generation and creative solutions:
        
        ```python
        result = await agent.run_worker(
            worker_name="creative",
            query="Generate ideas for improving our product"
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