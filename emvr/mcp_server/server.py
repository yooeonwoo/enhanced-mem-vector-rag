"""
MCP server implementation for the EMVR system.

This module implements the main FastMCP server for the EMVR system.
"""

import logging
import sys
import os
import signal
import asyncio
from typing import Optional, Dict, Any

from fastmcp import MCPServer

from emvr.config import get_settings
from emvr.core.db_connections import initialize_connections, close_connections
from emvr.memory.memory_manager import memory_manager
from emvr.ingestion.pipeline import ingestion_pipeline
from emvr.mcp_server.endpoints import register_endpoints, register_resources

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


class MemoryMCPServer:
    """
    MCP server for the EMVR system.
    
    Provides memory operations, search, and ingestion capabilities.
    """
    
    def __init__(self):
        """Initialize the MCP server."""
        self._settings = get_settings()
        self._mcp_server = MCPServer(
            name="memory",
            description="EMVR Memory MCP Server",
            version="0.1.0"
        )
        self._initialized = False
    
    async def initialize(self):
        """Initialize the server and all dependencies."""
        if self._initialized:
            return
        
        try:
            logger.info("Initializing MCP server")
            
            # Initialize database connections
            initialize_connections()
            
            # Initialize memory manager
            await memory_manager.initialize()
            
            # Initialize ingestion pipeline
            await ingestion_pipeline.initialize()
            
            # Register endpoints and resources
            await register_endpoints(self._mcp_server)
            await register_resources(self._mcp_server)
            
            # Setup signal handlers for graceful shutdown
            self._setup_signal_handlers()
            
            self._initialized = True
            logger.info("MCP server initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize MCP server: {e}")
            raise
    
    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""
        def handle_exit_signal(sig, frame):
            logger.info(f"Received signal {sig}, shutting down...")
            self.cleanup()
            sys.exit(0)
        
        # Register signal handlers
        signal.signal(signal.SIGINT, handle_exit_signal)
        signal.signal(signal.SIGTERM, handle_exit_signal)
    
    async def run_stdio(self):
        """Run the server in stdio mode."""
        try:
            await self.initialize()
            logger.info("Starting MCP server in stdio mode")
            await self._mcp_server.start_stdio()
        except Exception as e:
            logger.error(f"Error running MCP server in stdio mode: {e}")
            self.cleanup()
            raise
    
    async def run_http(self, host: Optional[str] = None, port: Optional[int] = None):
        """
        Run the server in HTTP mode.
        
        Args:
            host: Host to bind to (defaults to settings)
            port: Port to bind to (defaults to settings)
        """
        try:
            await self.initialize()
            
            host = host or self._settings.mcp_host
            port = port or self._settings.mcp_port
            
            logger.info(f"Starting MCP server on {host}:{port}")
            await self._mcp_server.start_http(host=host, port=port)
        except Exception as e:
            logger.error(f"Error running MCP server in HTTP mode: {e}")
            self.cleanup()
            raise
    
    def cleanup(self):
        """Clean up resources before shutdown."""
        logger.info("Cleaning up resources...")
        
        # Close memory manager connections
        memory_manager.close()
        
        # Close database connections
        close_connections()
        
        logger.info("Cleanup complete")


# Main entry point
async def main():
    """Main entry point for the MCP server."""
    server = MemoryMCPServer()
    
    # Determine server mode based on environment variable
    server_mode = os.environ.get("MCP_SERVER_MODE", "stdio")
    
    if server_mode.lower() == "http":
        await server.run_http()
    else:
        await server.run_stdio()


if __name__ == "__main__":
    asyncio.run(main())