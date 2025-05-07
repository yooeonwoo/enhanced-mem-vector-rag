"""Worker agent implementations for the Enhanced Memory-Vector RAG system."""

import os

from dotenv import load_dotenv
from langchain.agents import AgentExecutor, AgentType, initialize_agent
from langchain.schema import BaseLanguageModel
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI

from emvr.agent.base import AgentResult, BaseAgent
from emvr.memory.memory_manager import MemoryManager
from emvr.retrieval.knowledge_graph_retriever import KnowledgeGraphRetriever
from emvr.retrieval.pipeline import RetrievalPipeline

# Load environment variables
load_dotenv()


class ResearchWorkerAgent(BaseAgent):
    """Research worker agent specializing in retrieving information."""

    description = "Specialized in research tasks, information retrieval, and answering questions based on available knowledge."

    def __init__(
        self,
        llm: BaseLanguageModel | None = None,
        retrieval_pipeline: RetrievalPipeline | None = None,
    ) -> None:
        """
        Initialize the research worker agent.

        Args:
            llm: Language model for the agent
            retrieval_pipeline: Retrieval pipeline instance

        """
        # Initialize LLM
        self.llm = llm or ChatOpenAI(
            temperature=0.0,
            model=os.environ.get("WORKER_LLM_MODEL", "gpt-3.5-turbo"),
        )

        # Initialize retrieval pipeline
        self.retrieval_pipeline = retrieval_pipeline or RetrievalPipeline()

        # Initialize agent
        self.agent_executor = self._create_agent_executor()

    def _create_agent_executor(self) -> AgentExecutor:
        """
        Create an agent executor with research tools.

        Returns:
            AgentExecutor instance

        """
        # Define tools
        class SearchTool(BaseTool):
            name = "search"
            description = "Search for information on a topic"

            def _run(self, query: str, top_k: int = 5) -> str:
                """Run the tool."""
                import asyncio

                results = asyncio.run(self.retrieval_pipeline.retrieve(query, top_k=top_k))

                if not results:
                    return "No results found."

                formatted_results = []
                for i, result in enumerate(results):
                    formatted_results.append(
                        f"[{i+1}] {result.text}\n"
                        f"Source: {result.metadata.get('source', 'Unknown')}",
                    )

                return "\n\n".join(formatted_results)

            async def _arun(self, query: str, top_k: int = 5) -> str:
                """Run the tool asynchronously."""
                results = await self.retrieval_pipeline.retrieve(query, top_k=top_k)

                if not results:
                    return "No results found."

                formatted_results = []
                for i, result in enumerate(results):
                    formatted_results.append(
                        f"[{i+1}] {result.text}\n"
                        f"Source: {result.metadata.get('source', 'Unknown')}\n"
                        f"Relevance: {result.metadata.get('score', 'Unknown')}",
                    )

                return "\n\n".join(formatted_results)

        # Initialize tools with references to our objects
        search_tool = SearchTool()
        search_tool.retrieval_pipeline = self.retrieval_pipeline

        tools = [search_tool]

        # Initialize agent
        return initialize_agent(
            tools,
            self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
        )


    def get_agent_executor(self) -> AgentExecutor:
        """
        Get the agent executor.

        Returns:
            AgentExecutor instance

        """
        return self.agent_executor

    async def run(self, query: str, **kwargs) -> AgentResult:
        """
        Run the agent with a query.

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


class KnowledgeGraphWorkerAgent(BaseAgent):
    """Knowledge graph worker agent specializing in graph operations."""

    description = "Specialized in knowledge graph operations, entity management, and relationship queries."

    def __init__(
        self,
        llm: BaseLanguageModel | None = None,
        memory_manager: MemoryManager | None = None,
        kg_retriever: KnowledgeGraphRetriever | None = None,
    ) -> None:
        """
        Initialize the knowledge graph worker agent.

        Args:
            llm: Language model for the agent
            memory_manager: Memory manager instance
            kg_retriever: Knowledge graph retriever instance

        """
        # Initialize LLM
        self.llm = llm or ChatOpenAI(
            temperature=0.0,
            model=os.environ.get("WORKER_LLM_MODEL", "gpt-3.5-turbo"),
        )

        # Initialize memory manager
        self.memory_manager = memory_manager or MemoryManager()

        # Initialize knowledge graph retriever
        self.kg_retriever = kg_retriever or KnowledgeGraphRetriever()

        # Initialize agent
        self.agent_executor = self._create_agent_executor()

    def _create_agent_executor(self) -> AgentExecutor:
        """
        Create an agent executor with knowledge graph tools.

        Returns:
            AgentExecutor instance

        """
        # Define tools
        class KGSearchTool(BaseTool):
            name = "kg_search"
            description = "Search the knowledge graph for entities and relationships"

            def _run(self, query: str, top_k: int = 5) -> str:
                """Run the tool."""
                import asyncio

                results = asyncio.run(self.kg_retriever.retrieve(query, top_k=top_k))

                if not results:
                    return "No results found in the knowledge graph."

                formatted_results = []
                for i, result in enumerate(results):
                    formatted_results.append(
                        f"[{i+1}] {result.text}\n"
                        f"Source: {result.metadata.get('source', 'Unknown')}",
                    )

                return "\n\n".join(formatted_results)

            async def _arun(self, query: str, top_k: int = 5) -> str:
                """Run the tool asynchronously."""
                results = await self.kg_retriever.retrieve(query, top_k=top_k)

                if not results:
                    return "No results found in the knowledge graph."

                formatted_results = []
                for i, result in enumerate(results):
                    formatted_results.append(
                        f"[{i+1}] {result.text}\n"
                        f"Source: {result.metadata.get('source', 'Unknown')}\n"
                        f"Relevance: {result.metadata.get('score', 'Unknown')}",
                    )

                return "\n\n".join(formatted_results)

        class ReadGraphTool(BaseTool):
            name = "read_graph"
            description = "Read the knowledge graph structure to understand entity relationships"

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
                        f"{entity.get('name')} ({entity.get('entity_type')}): {observation_text}",
                    )

                relation_descriptions = []
                for relation in relations[:10]:  # Limit to 10 relations
                    relation_descriptions.append(
                        f"{relation.get('from')} --{relation.get('relation_type')}--> {relation.get('to')}",
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
                        f"{entity.get('name')} ({entity.get('entity_type')}): {observation_text}",
                    )

                relation_descriptions = []
                for relation in relations[:10]:  # Limit to 10 relations
                    relation_descriptions.append(
                        f"{relation.get('from')} --{relation.get('relation_type')}--> {relation.get('to')}",
                    )

                output = "Entities:\n" + "\n".join(entity_descriptions)
                if relations:
                    output += "\n\nRelations:\n" + "\n".join(relation_descriptions)

                if len(entities) > 10 or len(relations) > 10:
                    output += "\n\n(Showing partial results)"

                return output

        # Initialize tools with references to our objects
        kg_search_tool = KGSearchTool()
        kg_search_tool.kg_retriever = self.kg_retriever

        read_graph_tool = ReadGraphTool()
        read_graph_tool.memory_manager = self.memory_manager

        tools = [kg_search_tool, read_graph_tool]

        # Initialize agent
        return initialize_agent(
            tools,
            self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
        )


    def get_agent_executor(self) -> AgentExecutor:
        """
        Get the agent executor.

        Returns:
            AgentExecutor instance

        """
        return self.agent_executor

    async def run(self, query: str, **kwargs) -> AgentResult:
        """
        Run the agent with a query.

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


class MemoryManagementWorkerAgent(BaseAgent):
    """Memory management worker agent specializing in memory operations."""

    description = "Specialized in memory management, entity creation, and memory system maintenance."

    def __init__(
        self,
        llm: BaseLanguageModel | None = None,
        memory_manager: MemoryManager | None = None,
    ) -> None:
        """
        Initialize the memory management worker agent.

        Args:
            llm: Language model for the agent
            memory_manager: Memory manager instance

        """
        # Initialize LLM
        self.llm = llm or ChatOpenAI(
            temperature=0.0,
            model=os.environ.get("WORKER_LLM_MODEL", "gpt-3.5-turbo"),
        )

        # Initialize memory manager
        self.memory_manager = memory_manager or MemoryManager()

        # Initialize agent
        self.agent_executor = self._create_agent_executor()

    def _create_agent_executor(self) -> AgentExecutor:
        """
        Create an agent executor with memory management tools.

        Returns:
            AgentExecutor instance

        """
        # Define tools
        class CreateEntityTool(BaseTool):
            name = "create_entity"
            description = "Create a new entity in the memory system"

            def _run(self, name: str, entity_type: str, observations: list[str]) -> str:
                """Run the tool."""
                import asyncio

                asyncio.run(self.memory_manager.create_entities([
                    {
                        "name": name,
                        "entity_type": entity_type,
                        "observations": observations,
                    },
                ]))

                return f"Entity created: {name} ({entity_type})"

            async def _arun(self, name: str, entity_type: str, observations: list[str]) -> str:
                """Run the tool asynchronously."""
                await self.memory_manager.create_entities([
                    {
                        "name": name,
                        "entity_type": entity_type,
                        "observations": observations,
                    },
                ])

                return f"Entity created: {name} ({entity_type})"

        class CreateRelationTool(BaseTool):
            name = "create_relation"
            description = "Create a new relation between entities in the memory system"

            def _run(self, from_entity: str, relation_type: str, to_entity: str) -> str:
                """Run the tool."""
                import asyncio

                asyncio.run(self.memory_manager.create_relations([
                    {
                        "from": from_entity,
                        "relation_type": relation_type,
                        "to": to_entity,
                    },
                ]))

                return f"Relation created: {from_entity} --{relation_type}--> {to_entity}"

            async def _arun(self, from_entity: str, relation_type: str, to_entity: str) -> str:
                """Run the tool asynchronously."""
                await self.memory_manager.create_relations([
                    {
                        "from": from_entity,
                        "relation_type": relation_type,
                        "to": to_entity,
                    },
                ])

                return f"Relation created: {from_entity} --{relation_type}--> {to_entity}"

        class AddObservationsTool(BaseTool):
            name = "add_observations"
            description = "Add observations to an existing entity in the memory system"

            def _run(self, entity_name: str, observations: list[str]) -> str:
                """Run the tool."""
                import asyncio

                asyncio.run(self.memory_manager.add_observations([
                    {
                        "entity_name": entity_name,
                        "contents": observations,
                    },
                ]))

                return f"Observations added to entity: {entity_name}"

            async def _arun(self, entity_name: str, observations: list[str]) -> str:
                """Run the tool asynchronously."""
                await self.memory_manager.add_observations([
                    {
                        "entity_name": entity_name,
                        "contents": observations,
                    },
                ])

                return f"Observations added to entity: {entity_name}"

        class SearchNodesTool(BaseTool):
            name = "search_nodes"
            description = "Search for nodes in the memory system based on a query"

            def _run(self, query: str) -> str:
                """Run the tool."""
                import asyncio

                result = asyncio.run(self.memory_manager.search_nodes(query))

                nodes = result.get("nodes", [])

                if not nodes:
                    return "No nodes found."

                node_descriptions = []
                for node in nodes[:10]:  # Limit to 10 nodes for readability
                    observations = node.get("observations", [])
                    observation_text = ", ".join(observations[:3])
                    if len(observations) > 3:
                        observation_text += f" (and {len(observations)-3} more)"

                    node_descriptions.append(
                        f"{node.get('name')} ({node.get('entity_type')}): {observation_text}",
                    )

                output = "Nodes:\n" + "\n".join(node_descriptions)

                if len(nodes) > 10:
                    output += "\n\n(Showing top 10 results)"

                return output

            async def _arun(self, query: str) -> str:
                """Run the tool asynchronously."""
                result = await self.memory_manager.search_nodes(query)

                nodes = result.get("nodes", [])

                if not nodes:
                    return "No nodes found."

                node_descriptions = []
                for node in nodes[:10]:  # Limit to 10 nodes for readability
                    observations = node.get("observations", [])
                    observation_text = ", ".join(observations[:3])
                    if len(observations) > 3:
                        observation_text += f" (and {len(observations)-3} more)"

                    node_descriptions.append(
                        f"{node.get('name')} ({node.get('entity_type')}): {observation_text}",
                    )

                output = "Nodes:\n" + "\n".join(node_descriptions)

                if len(nodes) > 10:
                    output += "\n\n(Showing top 10 results)"

                return output

        # Initialize tools with references to our objects
        create_entity_tool = CreateEntityTool()
        create_entity_tool.memory_manager = self.memory_manager

        create_relation_tool = CreateRelationTool()
        create_relation_tool.memory_manager = self.memory_manager

        add_observations_tool = AddObservationsTool()
        add_observations_tool.memory_manager = self.memory_manager

        search_nodes_tool = SearchNodesTool()
        search_nodes_tool.memory_manager = self.memory_manager

        tools = [
            create_entity_tool,
            create_relation_tool,
            add_observations_tool,
            search_nodes_tool,
        ]

        # Initialize agent
        return initialize_agent(
            tools,
            self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
        )


    def get_agent_executor(self) -> AgentExecutor:
        """
        Get the agent executor.

        Returns:
            AgentExecutor instance

        """
        return self.agent_executor

    async def run(self, query: str, **kwargs) -> AgentResult:
        """
        Run the agent with a query.

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
