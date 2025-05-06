"""
Memory tools for EMVR agents.

This module implements tools for interacting with the memory system.
"""

from typing import Dict, List, Optional, Any, Type
import logging

from langchain.tools import BaseTool, StructuredTool, tool
from pydantic import BaseModel, Field

from emvr.memory.memory_manager import memory_manager

# Configure logging
logger = logging.getLogger(__name__)


# ----- Tool Input/Output Schemas -----

class SearchNodesInput(BaseModel):
    """Input schema for search_nodes tool."""
    query: str = Field(..., description="The search query string")
    limit: int = Field(10, description="Maximum number of results to return")


class CreateEntitiesInput(BaseModel):
    """Input schema for create_entities tool."""
    entities: List[Dict[str, Any]] = Field(..., description="List of entities to create")


class CreateRelationsInput(BaseModel):
    """Input schema for create_relations tool."""
    relations: List[Dict[str, Any]] = Field(..., description="List of relations to create")


class AddObservationsInput(BaseModel):
    """Input schema for add_observations tool."""
    observations: List[Dict[str, Any]] = Field(..., description="List of observations to add")


class DeleteEntitiesInput(BaseModel):
    """Input schema for delete_entities tool."""
    entity_names: List[str] = Field(..., description="List of entity names to delete")


# ----- Memory Tools -----

@tool
async def search_memory(
    query: str,
    limit: int = 10,
) -> Dict[str, Any]:
    """
    Search the memory system for nodes matching the query.
    
    Args:
        query: The search query string
        limit: Maximum number of results to return
        
    Returns:
        Dict containing search results
    """
    try:
        # Initialize memory manager if needed
        await memory_manager.initialize()
        
        # Execute the search
        result = await memory_manager.search_nodes(query, limit)
        
        return result
    except Exception as e:
        logger.error(f"Memory search failed: {e}")
        return {
            "error": str(e),
            "status": "error"
        }


@tool
async def read_memory_graph() -> Dict[str, Any]:
    """
    Read the entire memory graph.
    
    Returns:
        Dict containing the complete graph structure
    """
    try:
        # Initialize memory manager if needed
        await memory_manager.initialize()
        
        # Read the graph
        result = await memory_manager.read_graph()
        
        return result
    except Exception as e:
        logger.error(f"Reading memory graph failed: {e}")
        return {
            "error": str(e),
            "status": "error"
        }


@tool
async def create_memory_entities(entities: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Create new entities in the memory system.
    
    Args:
        entities: List of entities to create, each with name, entityType, and observations
        
    Returns:
        Dict containing the result of the operation
    """
    try:
        # Initialize memory manager if needed
        await memory_manager.initialize()
        
        # Create the entities
        result = await memory_manager.create_entities(entities)
        
        return result
    except Exception as e:
        logger.error(f"Entity creation failed: {e}")
        return {
            "error": str(e),
            "status": "error"
        }


@tool
async def create_memory_relations(relations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Create new relations between entities in the memory system.
    
    Args:
        relations: List of relations to create, each with from, to, and relationType
        
    Returns:
        Dict containing the result of the operation
    """
    try:
        # Initialize memory manager if needed
        await memory_manager.initialize()
        
        # Create the relations
        result = await memory_manager.create_relations(relations)
        
        return result
    except Exception as e:
        logger.error(f"Relation creation failed: {e}")
        return {
            "error": str(e),
            "status": "error"
        }


@tool
async def add_memory_observations(observations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Add new observations to existing entities in the memory system.
    
    Args:
        observations: List of observations to add, each with entityName and contents
        
    Returns:
        Dict containing the result of the operation
    """
    try:
        # Initialize memory manager if needed
        await memory_manager.initialize()
        
        # Add the observations
        result = await memory_manager.add_observations(observations)
        
        return result
    except Exception as e:
        logger.error(f"Adding observations failed: {e}")
        return {
            "error": str(e),
            "status": "error"
        }


@tool
async def delete_memory_entities(entity_names: List[str]) -> Dict[str, Any]:
    """
    Delete entities from the memory system.
    
    Args:
        entity_names: List of entity names to delete
        
    Returns:
        Dict containing the result of the operation
    """
    try:
        # Initialize memory manager if needed
        await memory_manager.initialize()
        
        # Delete the entities
        result = await memory_manager.delete_entities(entity_names)
        
        return result
    except Exception as e:
        logger.error(f"Entity deletion failed: {e}")
        return {
            "error": str(e),
            "status": "error"
        }


# ----- Tool Collection -----

def get_memory_tools() -> List[BaseTool]:
    """
    Get all memory tools.
    
    Returns:
        List of memory tools
    """
    return [
        search_memory,
        read_memory_graph,
        create_memory_entities,
        create_memory_relations,
        add_memory_observations,
        delete_memory_entities,
    ]