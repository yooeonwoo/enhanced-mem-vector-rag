"""Base memory interface for the Enhanced Memory-Vector RAG system."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel


class Entity(BaseModel):
    """Entity representation in the knowledge graph."""
    
    name: str
    entity_type: str
    observations: List[str]


class Relation(BaseModel):
    """Relation between entities in the knowledge graph."""
    
    from_entity: str
    relation_type: str
    to_entity: str


class MemoryInterface(ABC):
    """Abstract base class for memory interfaces."""
    
    @abstractmethod
    async def create_entities(self, entities: List[Entity]) -> Dict[str, Any]:
        """Create multiple new entities in the knowledge graph."""
        pass
    
    @abstractmethod
    async def create_relations(self, relations: List[Relation]) -> Dict[str, Any]:
        """Create multiple new relations between entities in the knowledge graph."""
        pass
    
    @abstractmethod
    async def add_observations(self, entity_name: str, observations: List[str]) -> Dict[str, Any]:
        """Add new observations to an existing entity in the knowledge graph."""
        pass
    
    @abstractmethod
    async def delete_entities(self, entity_names: List[str]) -> Dict[str, Any]:
        """Delete multiple entities and their associated relations from the knowledge graph."""
        pass
    
    @abstractmethod
    async def delete_observations(
        self, entity_name: str, observations: List[str]
    ) -> Dict[str, Any]:
        """Delete specific observations from an entity in the knowledge graph."""
        pass
    
    @abstractmethod
    async def delete_relations(self, relations: List[Relation]) -> Dict[str, Any]:
        """Delete multiple relations from the knowledge graph."""
        pass
    
    @abstractmethod
    async def read_graph(self) -> Dict[str, Any]:
        """Read the entire knowledge graph."""
        pass
    
    @abstractmethod
    async def search_nodes(self, query: str) -> Dict[str, Any]:
        """Search for nodes in the knowledge graph based on a query."""
        pass
    
    @abstractmethod
    async def open_nodes(self, names: List[str]) -> Dict[str, Any]:
        """Open specific nodes in the knowledge graph by their names."""
        pass