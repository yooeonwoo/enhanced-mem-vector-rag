"""Base supervisor agent implementation using LangGraph."""

import os
import uuid
from collections.abc import Callable
from typing import Any, Dict

from dotenv import load_dotenv
from langchain.agents import AgentExecutor
from langchain.schema import BaseLanguageModel
from langchain_core.messages import HumanMessage
from langchain_core.tools import Tool, tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, MessagesState, StateGraph, add_messages
from langgraph.prebuilt import create_react_agent
from pydantic import Field

from emvr.agent.base import AgentResult, BaseAgent

# Load environment variables
load_dotenv()


class SupervisorAgentState(MessagesState):
    """State for the supervisor agent graph."""

    next_agent: str | None = None
    execution_state: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None


class SupervisorAgent(BaseAgent):
    """Supervisor agent that orchestrates worker agents."""

    def __init__(
        self,
        llm: BaseLanguageModel | None = None,
        worker_agents: dict[str, BaseAgent] | None = None,
    ) -> None:
        """
        Initialize the supervisor agent.

        Args:
            llm: Language model for the agent
            worker_agents: Dictionary of worker agents keyed by agent name

        """
        # Initialize LLM
        self.llm = llm or ChatOpenAI(
            temperature=0.2,
            model=os.environ.get("SUPERVISOR_LLM_MODEL", "gpt-4o"),
        )

        # Initialize worker agents
        self.worker_agents = worker_agents or {}

        # Initialize state storage
        self.checkpointer = MemorySaver()

        # Initialize graph
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """
        Build the supervisor graph.

        Returns:
            StateGraph instance

        """
        # Create supervisor node
        supervisor_node = self._create_supervisor_node()

        # Initialize graph builder
        builder = StateGraph(SupervisorAgentState)

        # Add supervisor node
        builder.add_node("supervisor", supervisor_node)

        # Set supervisor as the entry node
        builder.add_edge("START", "supervisor")

        # Add worker agents and connect them to the supervisor
        worker_destinations = {}
        for agent_name, agent in self.worker_agents.items():
            # Add worker node
            builder.add_node(agent_name, self._create_worker_node(agent_name, agent))

            # Create edges: Supervisor to worker and worker back to supervisor
            builder.add_edge("supervisor", agent_name)
            builder.add_edge(agent_name, "supervisor")

            # Add worker to destinations
            worker_destinations[agent_name] = agent_name

        # Add END as a possible destination from supervisor
        worker_destinations["END"] = END

        # Update supervisor node destinations
        builder.update_node("supervisor", destinations=worker_destinations)

        # Compile graph with checkpointing
        return builder.compile(checkpointer=self.checkpointer)

    def _create_supervisor_node(self) -> Callable:
        """
        Create the supervisor node function.

        Returns:
            Supervisor node function

        """
        # Create handoff tools for each worker agent
        handoff_tools = [
            self._create_handoff_tool(agent_name) for agent_name in self.worker_agents
        ]

        # Create the supervisor agent
        supervisor_agent = create_react_agent(
            self.llm,
            handoff_tools,
            system_message=(
                "You are a supervisor managing multiple specialist agents "
                "for the Enhanced Memory-Vector RAG system. "
                "Based on the user request, decide which specialist agent to route the task to. "
                "Available agents:\n"
                + "\n".join(
                    [
                        f"- {agent_name}: "
                        f"{agent.description if hasattr(agent, 'description') else 'Specialist agent'}"
                        for agent_name, agent in self.worker_agents.items()
                    ],
                )
                + "\n\nIf the task is complete or doesn't require a specialist, you can finish."
            ),
        )

        # Create the supervisor node function
        def supervisor_node(state: SupervisorAgentState) -> dict[str, Any]:
            """Supervisor node function."""
            # Run the supervisor agent
            result = supervisor_agent.invoke(state)

            # Extract messages and tool calls
            messages = result.get("messages", [])

            # Determine next agent
            next_agent = "END"  # Default to END

            # Check for handoff tool calls
            for message in messages:
                if message.get("tool_calls"):
                    for tool_call in message.get("tool_calls", []):
                        if tool_call.get("name", "").startswith("transfer_to_"):
                            # Extract agent name from tool call
                            next_agent = tool_call.get("name").replace(
                                "transfer_to_", "",
                            )
                            break

            # Update state with new information
            state = add_messages(state, messages)
            state["next_agent"] = next_agent

            return state

        return supervisor_node

    def _create_worker_node(self, agent_name: str, agent: BaseAgent) -> Callable:
        """
        Create a worker node function.

        Args:
            agent_name: Name of the worker agent
            agent: Worker agent instance

        Returns:
            Worker node function

        """

        def worker_node(state: SupervisorAgentState) -> dict[str, Any]:
            """Worker node function."""
            # Extract the last user message
            user_messages = [
                m
                for m in state.get("messages", [])
                if m.get("role") == "user" or isinstance(m, HumanMessage)
            ]

            if not user_messages:
                # No user message, return to supervisor
                return add_messages(
                    state,
                    [
                        {
                            "role": "system",
                            "content": "No user message found. Returning to supervisor.",
                        },
                    ],
                )

            # Get the last user message
            last_message = user_messages[-1]
            query = (
                last_message.get("content")
                if isinstance(last_message, dict)
                else last_message.content
            )

            try:
                # Run the worker agent
                import asyncio

                result = asyncio.run(agent.run(query))

                # Update state with agent result
                messages = [{"role": "assistant", "content": result.output}]

                return add_messages(state, messages)
            except (RuntimeError, asyncio.TimeoutError) as e:
                # Handle specific runtime errors
                error_message = f"Error in {agent_name}: {e!s}"
                state["error"] = error_message

                return add_messages(
                    state, [{"role": "system", "content": error_message}],
                )
            except ValueError as e:
                # Handle value errors
                error_message = f"Value error in {agent_name}: {e!s}"
                state["error"] = error_message

                return add_messages(
                    state, [{"role": "system", "content": error_message}],
                )

        return worker_node

    def _create_handoff_tool(self, agent_name: str) -> Tool:
        """
        Create a handoff tool for a worker agent.

        Args:
            agent_name: Name of the worker agent

        Returns:
            Handoff tool

        """
        agent = self.worker_agents[agent_name]
        description = getattr(
            agent, "description", f"Specialist agent for {agent_name} tasks",
        )

        @tool(
            f"transfer_to_{agent_name}",
            description=f"Transfer task to {agent_name}. {description}",
        )
        def handoff_tool(task_description: str) -> str:
            """Handoff tool to transfer tasks to worker agents."""
            return f"Task transferred to {agent_name}: {task_description}"

        return handoff_tool

    def get_agent_executor(self) -> AgentExecutor:
        """
        Get the agent executor.

        Returns:
            AgentExecutor instance

        """
        msg = "Supervisor agent doesn't use AgentExecutor"
        raise NotImplementedError(msg)

    async def run(self, query: str, **kwargs: Dict[str, Any]) -> AgentResult:
        """
        Run the agent with a query.

        Args:
            query: Query string
            **kwargs: Additional keyword arguments

        Returns:
            Agent result

        """
        try:
            # Generate a thread ID if not provided
            thread_id = kwargs.get("thread_id", str(uuid.uuid4()))

            # Set up configuration
            config = {
                "configurable": {
                    "thread_id": thread_id,
                },
            }

            # Initialize state
            state = {
                "messages": [{"role": "user", "content": query}],
                "next_agent": None,
                "execution_state": {},
                "error": None,
            }

            # Run the graph
            final_state = None
            intermediate_steps = []

            # Process the graph stream
            for step in self.graph.stream(state, config, stream_mode="values"):
                intermediate_steps.append(step)
                final_state = step

            # Extract final output
            if final_state:
                assistant_messages = [
                    m
                    for m in final_state.get("messages", [])
                    if m.get("role") == "assistant"
                ]

                output = ""
                if assistant_messages:
                    # Get the content of the last assistant message
                    output = assistant_messages[-1].get("content", "")

            return AgentResult(
                success=not final_state.get("error"),
                output=output,
                intermediate_steps=intermediate_steps,
                error=final_state.get("error"),
            )
        except (ValueError, KeyError) as e:
            return AgentResult(
                success=False,
                output="",
                error=str(e),
            )
