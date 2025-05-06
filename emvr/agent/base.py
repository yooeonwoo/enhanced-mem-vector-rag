"""Base classes for agents."""

from abc import ABC, abstractmethod
from typing import Any

from langchain.agents import AgentExecutor
from pydantic import BaseModel


class AgentResult(BaseModel):
    """Result of an agent operation."""

    success: bool
    output: str
    intermediate_steps: list[dict[str, Any]] | None = None
    error: str | None = None


class BaseAgent(ABC):
    """Base class for agents."""

    @abstractmethod
    def get_agent_executor(self) -> AgentExecutor:
        """Get the agent executor.
        
        Returns:
            AgentExecutor instance
        """
        pass

    @abstractmethod
    async def run(self, query: str, **kwargs) -> AgentResult:
        """Run the agent with a query.
        
        Args:
            query: Query string
            **kwargs: Additional keyword arguments
            
        Returns:
            Agent result
        """
        pass
