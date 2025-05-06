"""Memory-augmented agent implementation."""

import os

from dotenv import load_dotenv
from langchain.agents import AgentExecutor, AgentType, initialize_agent
from langchain.schema import BaseLanguageModel
from langchain_openai import ChatOpenAI

from emvr.agent.base import AgentResult, BaseAgent
from emvr.memory.memory_manager import MemoryManager
from emvr.retrieval.hybrid_retriever import HybridRetriever

# Load environment variables
load_dotenv()


class MemoryAgent(BaseAgent):
    """Memory-augmented agent for the Enhanced Memory-Vector RAG system."""

    def __init__(
        self,
        llm: BaseLanguageModel | None = None,
        memory_manager: MemoryManager | None = None,
        retriever: HybridRetriever | None = None,
    ):
        """Initialize the memory agent.
        
        Args:
            llm: Language model for the agent
            memory_manager: Memory manager instance
            retriever: Retriever instance
        """
        # Initialize LLM
        self.llm = llm or ChatOpenAI(
            temperature=0.0,
            model=os.environ.get("LLM_MODEL", "gpt-3.5-turbo"),
        )

        # Initialize memory manager
        self.memory_manager = memory_manager or MemoryManager()

        # Initialize retriever
        self.retriever = retriever or HybridRetriever()

        # Initialize agent
        self.agent_executor = self._create_agent_executor()

    def _create_agent_executor(self) -> AgentExecutor:
        """Create an agent executor with memory tools.
        
        Returns:
            AgentExecutor instance
        """
        # Define tools
        from langchain.tools import BaseTool

        class MemorySearchTool(BaseTool):
            name = "memory_search"
            description = "Search for information in memory"

            def _run(self, query: str, top_k: int = 5) -> str:
                """Run the tool."""
                import asyncio

                results = asyncio.run(self.retriever.retrieve(query, top_k=top_k))

                if not results:
                    return "No results found."

                formatted_results = []
                for i, result in enumerate(results):
                    formatted_results.append(
                        f"[{i+1}] {result.text}\n"
                        f"Source: {result.metadata.get('source', 'Unknown')}"
                    )

                return "\n\n".join(formatted_results)

            async def _arun(self, query: str, top_k: int = 5) -> str:
                """Run the tool asynchronously."""
                results = await self.retriever.retrieve(query, top_k=top_k)

                if not results:
                    return "No results found."

                formatted_results = []
                for i, result in enumerate(results):
                    formatted_results.append(
                        f"[{i+1}] {result.text}\n"
                        f"Source: {result.metadata.get('source', 'Unknown')}"
                    )

                return "\n\n".join(formatted_results)

        class MemoryReadTool(BaseTool):
            name = "memory_read_graph"
            description = "Read the knowledge graph to understand entity relationships"

            def _run(self) -> str:
                """Run the tool."""
                import asyncio

                result = asyncio.run(self.memory_manager.read_graph())

                entities = result.get("entities", [])
                relations = result.get("relations", [])

                if not entities and not relations:
                    return "Knowledge graph is empty."

                entity_descriptions = []
                for entity in entities[:10]:  # Limit to 10 entities for readability
                    observations = entity.get("observations", [])
                    observation_text = ", ".join(observations[:3])
                    if len(observations) > 3:
                        observation_text += f" (and {len(observations)-3} more)"

                    entity_descriptions.append(
                        f"{entity.get('name')} ({entity.get('entity_type')}): {observation_text}"
                    )

                relation_descriptions = []
                for relation in relations[:10]:  # Limit to 10 relations
                    relation_descriptions.append(
                        f"{relation.get('from')} --{relation.get('relation')}--> {relation.get('to')}"
                    )

                output = "Entities:\n" + "\n".join(entity_descriptions)
                if relations:
                    output += "\n\nRelations:\n" + "\n".join(relation_descriptions)

                if len(entities) > 10 or len(relations) > 10:
                    output += "\n\n(Showing partial results)"

                return output

            async def _arun(self) -> str:
                """Run the tool asynchronously."""
                result = await self.memory_manager.read_graph()

                entities = result.get("entities", [])
                relations = result.get("relations", [])

                if not entities and not relations:
                    return "Knowledge graph is empty."

                entity_descriptions = []
                for entity in entities[:10]:  # Limit to 10 entities for readability
                    observations = entity.get("observations", [])
                    observation_text = ", ".join(observations[:3])
                    if len(observations) > 3:
                        observation_text += f" (and {len(observations)-3} more)"

                    entity_descriptions.append(
                        f"{entity.get('name')} ({entity.get('entity_type')}): {observation_text}"
                    )

                relation_descriptions = []
                for relation in relations[:10]:  # Limit to 10 relations
                    relation_descriptions.append(
                        f"{relation.get('from')} --{relation.get('relation')}--> {relation.get('to')}"
                    )

                output = "Entities:\n" + "\n".join(entity_descriptions)
                if relations:
                    output += "\n\nRelations:\n" + "\n".join(relation_descriptions)

                if len(entities) > 10 or len(relations) > 10:
                    output += "\n\n(Showing partial results)"

                return output

        # Initialize tools with references to our objects
        memory_search_tool = MemorySearchTool()
        memory_search_tool.retriever = self.retriever

        memory_read_tool = MemoryReadTool()
        memory_read_tool.memory_manager = self.memory_manager

        tools = [memory_search_tool, memory_read_tool]

        # Initialize agent
        agent = initialize_agent(
            tools,
            self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
        )

        return agent

    def get_agent_executor(self) -> AgentExecutor:
        """Get the agent executor.
        
        Returns:
            AgentExecutor instance
        """
        return self.agent_executor

    async def run(self, query: str, **kwargs) -> AgentResult:
        """Run the agent with a query.
        
        Args:
            query: Query string
            **kwargs: Additional keyword arguments
            
        Returns:
            Agent result
        """
        try:
            # Initialize agent input
            agent_input = {
                "input": query,
                "chat_history": kwargs.get("chat_history", []),
            }

            # Run agent
            agent_output = await self.agent_executor.ainvoke(agent_input)

            return AgentResult(
                success=True,
                output=agent_output["output"],
                intermediate_steps=agent_output.get("intermediate_steps"),
            )
        except Exception as e:
            return AgentResult(
                success=False,
                output="",
                error=str(e),
            )
