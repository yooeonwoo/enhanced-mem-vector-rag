"""Factory for creating agent workflows."""

import os

from dotenv import load_dotenv
from langchain.schema import BaseLanguageModel
from langchain_openai import ChatOpenAI

from emvr.agent.workflows.agent_workflow import AgentWorkflow
from emvr.memory.memory_manager import MemoryManager
from emvr.retrieval.pipeline import RetrievalPipeline

# Load environment variables
load_dotenv()


class AgentWorkflowFactory:
    """Factory for creating agent workflows."""

    @staticmethod
    def create_workflow(
        supervisor_llm: BaseLanguageModel | None = None,
        worker_llm: BaseLanguageModel | None = None,
        memory_manager: MemoryManager | None = None,
        retrieval_pipeline: RetrievalPipeline | None = None,
    ) -> AgentWorkflow:
        """
        Create an agent workflow.

        Args:
            supervisor_llm: Language model for the supervisor agent
            worker_llm: Language model for worker agents
            memory_manager: Memory manager instance
            retrieval_pipeline: Retrieval pipeline instance

        Returns:
            AgentWorkflow instance

        """
        # Initialize components if not provided
        if supervisor_llm is None:
            supervisor_llm = ChatOpenAI(
                temperature=0.2,
                model=os.environ.get("SUPERVISOR_LLM_MODEL", "gpt-4o"),
            )

        if worker_llm is None:
            worker_llm = ChatOpenAI(
                temperature=0.0,
                model=os.environ.get("WORKER_LLM_MODEL", "gpt-3.5-turbo"),
            )

        if memory_manager is None:
            memory_manager = MemoryManager()

        if retrieval_pipeline is None:
            retrieval_pipeline = RetrievalPipeline()

        # Create and return workflow
        return AgentWorkflow(
            supervisor_llm=supervisor_llm,
            worker_llm=worker_llm,
            memory_manager=memory_manager,
            retrieval_pipeline=retrieval_pipeline,
        )
