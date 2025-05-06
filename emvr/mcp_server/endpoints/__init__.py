"""MCP server endpoints for EMVR."""

from emvr.mcp_server.endpoints.agent_endpoints import register_agent_endpoints, register_agent_resources
from emvr.mcp_server.endpoints.retrieval_endpoints import register_retrieval_endpoints
from emvr.mcp_server.endpoints.ingestion_endpoints import register_ingestion_endpoints

__all__ = [
    "register_agent_endpoints", 
    "register_agent_resources",
    "register_retrieval_endpoints",
    "register_ingestion_endpoints",
]