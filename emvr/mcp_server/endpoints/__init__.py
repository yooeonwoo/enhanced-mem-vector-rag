"""MCP server endpoints for EMVR."""

from emvr.mcp_server.endpoints.agent_endpoints import register_agent_endpoints, register_agent_resources

__all__ = ["register_agent_endpoints", "register_agent_resources"]