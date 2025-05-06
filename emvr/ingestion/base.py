"""Base classes for the ingestion pipeline."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel


class Document(BaseModel):
    """Document representation for ingestion."""
    
    content: str
    metadata: Dict[str, Any]
    id: Optional[str] = None


class IngestResult(BaseModel):
    """Result of an ingestion operation."""
    
    document_id: str
    success: bool
    message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class BaseIngestionConnector(ABC):
    """Base class for ingestion connectors."""
    
    @abstractmethod
    async def ingest(self, documents: List[Document]) -> List[IngestResult]:
        """Ingest documents into the system.
        
        Args:
            documents: List of documents to ingest
            
        Returns:
            List of ingestion results
        """
        pass
    
    @abstractmethod
    async def delete(self, document_ids: List[str]) -> List[IngestResult]:
        """Delete documents from the system.
        
        Args:
            document_ids: List of document IDs to delete
            
        Returns:
            List of deletion results
        """
        pass