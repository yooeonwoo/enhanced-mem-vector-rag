"""LangGraph workflow implementation for the Enhanced Memory-Vector RAG system."""

import os
import uuid
from typing import Any

from dotenv import load_dotenv
from langchain.schema import BaseLanguageModel
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from emvr.agent.supervisor import (
    KnowledgeGraphWorkerAgent,
    MemoryManagementWorkerAgent,
    ResearchWorkerAgent,
    SupervisorAgent,
)
from emvr.memory.memory_manager import MemoryManager
from emvr.retrieval.pipeline import RetrievalPipeline

# Load environment variables
load_dotenv()


class WorkflowOutput(BaseModel):
    """Output from the agent workflow."""

    success: bool
    output: str
    intermediate_steps: list[dict[str, Any]] | None = None
    error: str | None = None


class AgentWorkflow:
    """Agent workflow for the Enhanced Memory-Vector RAG system."""

    def __init__(
        self,
        supervisor_llm: BaseLanguageModel | None = None,
        worker_llm: BaseLanguageModel | None = None,
        memory_manager: MemoryManager | None = None,
        retrieval_pipeline: RetrievalPipeline | None = None,
    ):
        """
        Initialize the agent workflow.
        
        Args:
            supervisor_llm: Language model for the supervisor agent
            worker_llm: Language model for worker agents
            memory_manager: Memory manager instance
            retrieval_pipeline: Retrieval pipeline instance

        """
        # Initialize LLMs
        self.supervisor_llm = supervisor_llm or ChatOpenAI(
            temperature=0.2,
            model=os.environ.get("SUPERVISOR_LLM_MODEL", "gpt-4o"),
        )

        self.worker_llm = worker_llm or ChatOpenAI(
            temperature=0.0,
            model=os.environ.get("WORKER_LLM_MODEL", "gpt-3.5-turbo"),
        )

        # Initialize components
        self.memory_manager = memory_manager or MemoryManager()
        self.retrieval_pipeline = retrieval_pipeline or RetrievalPipeline()

        # Initialize worker agents
        self.worker_agents = self._create_worker_agents()

        # Initialize supervisor agent
        self.supervisor_agent = self._create_supervisor_agent()

    def _create_worker_agents(self) -> dict[str, Any]:
        """
        Create worker agents.
        
        Returns:
            Dictionary of worker agents

        """
        return {
            "research_agent": ResearchWorkerAgent(
                llm=self.worker_llm,
                retrieval_pipeline=self.retrieval_pipeline,
            ),
            "knowledge_graph_agent": KnowledgeGraphWorkerAgent(
                llm=self.worker_llm,
                memory_manager=self.memory_manager,
            ),
            "memory_management_agent": MemoryManagementWorkerAgent(
                llm=self.worker_llm,
                memory_manager=self.memory_manager,
            ),
        }

    def _create_supervisor_agent(self) -> SupervisorAgent:
        """
        Create supervisor agent.
        
        Returns:
            SupervisorAgent instance

        """
        return SupervisorAgent(
            llm=self.supervisor_llm,
            worker_agents=self.worker_agents,
        )

    async def run(self, query: str, **kwargs) -> WorkflowOutput:
        """
        Run the agent workflow with a query.
        
        Args:
            query: Query string
            **kwargs: Additional keyword arguments
            
        Returns:
            WorkflowOutput instance

        """
        # Run memory-related operations to track the interaction
        try:
            # Add observation about the query
            await self.memory_manager.add_observations([
                {
                    "entity_name": f"Query - {uuid.uuid4()}",
                    "contents": [query],
                },
            ])

            # Get thread ID if available
            thread_id = kwargs.get("thread_id", str(uuid.uuid4()))

            # Run the supervisor agent
            result = await self.supervisor_agent.run(query, thread_id=thread_id)

            # Record the result in memory
            if result.success:
                await self.memory_manager.add_observations([
                    {
                        "entity_name": "Agent Workflow Results",
                        "contents": [f"Successfully processed query: {query}", f"Output: {result.output}"],
                    },
                ])
            else:
                await self.memory_manager.add_observations([
                    {
                        "entity_name": "Agent Workflow Errors",
                        "contents": [f"Failed to process query: {query}", f"Error: {result.error}"],
                    },
                ])

            # Return workflow output
            return WorkflowOutput(
                success=result.success,
                output=result.output,
                intermediate_steps=result.intermediate_steps,
                error=result.error,
            )
        except Exception as e:
            # Record error in memory
            await self.memory_manager.add_observations([
                {
                    "entity_name": "Agent Workflow Errors",
                    "contents": [f"Exception while processing query: {query}", f"Error: {e!s}"],
                },
            ])

            # Return error output
            return WorkflowOutput(
                success=False,
                output="",
                error=str(e),
            )
