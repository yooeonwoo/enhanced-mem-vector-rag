"""Base classes for retrieval."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel


class RetrievalResult(BaseModel):
    """Result of a retrieval operation."""
    
    id: str
    text: str
    score: Optional[float] = None
    metadata: Dict[str, Any]


class BaseRetriever(ABC):
    """Base class for retrievers."""
    
    @abstractmethod
    async def retrieve(
        self, query: str, top_k: int = 5, filters: Optional[Dict[str, Any]] = None
    ) -> List[RetrievalResult]:
        """Retrieve documents based on a query.
        
        Args:
            query: Query string
            top_k: Number of results to return
            filters: Optional filters to apply
            
        Returns:
            List of retrieval results
        """
        pass