"""
Chainlit UI application for EMVR.

This module implements the main Chainlit UI for the EMVR system.
"""

import os
import logging
import asyncio
from typing import Dict, List, Optional, Any, Union

import chainlit as cl
from chainlit.playground.providers import ChatOpenAI
from chainlit.types import FileDict
from langchain_openai import ChatOpenAI

from emvr.config import get_settings
from emvr.memory.memory_manager import memory_manager
from emvr.retrievers.retrieval_pipeline import retrieval_pipeline
from emvr.ingestion.pipeline import ingestion_pipeline
from emvr.agents.orchestration import initialize_orchestration, get_orchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


# ----- Initialization -----

@cl.on_app_start
async def setup():
    """Initialize the EMVR components."""
    try:
        settings = get_settings()
        
        # Initialize memory manager
        await memory_manager.initialize()
        cl.user_session.set("memory_manager", memory_manager)
        
        # Initialize retrieval pipeline
        await retrieval_pipeline.initialize()
        cl.user_session.set("retrieval_pipeline", retrieval_pipeline)
        
        # Initialize ingestion pipeline
        await ingestion_pipeline.initialize()
        cl.user_session.set("ingestion_pipeline", ingestion_pipeline)
        
        # Initialize LLM
        llm = ChatOpenAI(
            temperature=0.0,
            model=settings.openai_model,
        )
        cl.user_session.set("llm", llm)
        
        # Register with playground
        actions = [
            cl.Action(name="search", label="🔍 Search", description="Search for information"),
            cl.Action(name="ingest", label="📤 Ingest", description="Add information to the system"),
            cl.Action(name="analyze", label="🔬 Analyze", description="Analyze information"),
        ]
        
        cl.init_chat(
            actions=actions,
            playground=ChatOpenAI(
                model=settings.openai_model,
                temperature=0.0,
            ),
        )
        
        # Initialize agent orchestration
        orchestrator = await initialize_orchestration(llm=llm)
        cl.user_session.set("orchestrator", orchestrator)
        
        # Send welcome message
        await cl.Message(
            content="👋 Welcome to Enhanced Mem-Vector RAG! How can I assist you today?",
            author="EMVR System",
        ).send()
    
    except Exception as e:
        logger.error(f"Failed to initialize UI: {e}")
        await cl.Message(
            content=f"❌ Error initializing system: {str(e)}",
            author="System",
        ).send()


# ----- Message Handling -----

@cl.on_message
async def on_message(message: cl.Message):
    """
    Process user messages.
    
    Args:
        message: The user message
    """
    try:
        # Get components from session
        orchestrator = cl.user_session.get("orchestrator")
        
        if orchestrator is None:
            await cl.Message(
                content="System not initialized. Please refresh the page.",
                author="System",
            ).send()
            return
        
        # Get uploaded files if any
        files = None
        if message.elements:
            files = [e for e in message.elements if isinstance(e, cl.File)]
        
        # Process the message
        thinking_msg = cl.Message(content="", author="EMVR")
        await thinking_msg.send()
        
        async with thinking_msg.content_thread() as content_stream:
            await content_stream.append("🧠 Thinking...")
            
            # Run the query through the agent orchestrator
            results = await orchestrator.run(message.content)
            
            # Clear the thinking message
            await content_stream.clear()
            
            # Show the agent response
            await content_stream.append(results["response"])
            
            # If there's a workflow trace, add it to the message steps
            if "workflow_trace" in results:
                trace = results["workflow_trace"]
                
                # Add steps for the planning, retrieval, execution, etc.
                steps = []
                
                if trace.get("plan"):
                    steps.append(
                        cl.Step(
                            name="Planning",
                            type="planning",
                            content="\n".join(trace["plan"].get("steps", [])),
                        )
                    )
                
                if trace.get("context"):
                    context_str = "\n\n".join([
                        f"Document {i+1}:\n{doc.get('content', '')}"
                        for i, doc in enumerate(trace.get("context", []))
                    ])
                    steps.append(
                        cl.Step(
                            name="Retrieval",
                            type="retrieval",
                            content=context_str,
                        )
                    )
                
                if trace.get("execution_result"):
                    steps.append(
                        cl.Step(
                            name="Execution",
                            type="execution",
                            content=trace["execution_result"],
                        )
                    )
                
                if trace.get("reflection"):
                    steps.append(
                        cl.Step(
                            name="Reflection",
                            type="thinking",
                            content=trace["reflection"],
                        )
                    )
                
                # Add the steps to the message
                thinking_msg.steps = steps
    
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await cl.Message(
            content=f"❌ Error: {str(e)}",
            author="System",
        ).send()


# ----- File Handling -----

@cl.on_file
async def on_file(file: FileDict):
    """
    Process uploaded files.
    
    Args:
        file: The uploaded file
    """
    try:
        # Get ingestion pipeline from session
        pipeline = cl.user_session.get("ingestion_pipeline")
        
        if pipeline is None:
            await cl.Message(
                content="Ingestion pipeline not initialized.",
                author="System",
            ).send()
            return
        
        # Process the file
        file_path = file["path"]
        file_name = file["name"]
        file_type = file["type"]
        
        ingestion_msg = cl.Message(content="", author="EMVR")
        await ingestion_msg.send()
        
        async with ingestion_msg.content_thread() as content_stream:
            await content_stream.append(f"📤 Processing file: `{file_name}`...")
            
            # Ingest the file
            result = await pipeline.ingest_file(file_path, metadata={"source": file_name})
            
            # Show the ingestion result
            if result.get("status") == "success":
                await content_stream.clear()
                chunks = result.get("chunks", 0)
                await content_stream.append(
                    f"✅ Successfully ingested `{file_name}` ({chunks} chunks created)\n\n"
                    f"The file content is now available in the knowledge base."
                )
            else:
                await content_stream.clear()
                await content_stream.append(
                    f"❌ Failed to ingest `{file_name}`: {result.get('error', 'Unknown error')}"
                )
    
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        await cl.Message(
            content=f"❌ Error processing file: {str(e)}",
            author="System",
        ).send()


# ----- Action Handlers -----

@cl.action_callback("search")
async def on_search(action):
    """
    Handle search action.
    
    Args:
        action: The action
    """
    # Get search query
    await cl.Message(
        content="🔍 What would you like to search for?",
        author="EMVR",
    ).send()


@cl.action_callback("ingest")
async def on_ingest(action):
    """
    Handle ingest action.
    
    Args:
        action: The action
    """
    # Prompt for ingestion source
    await cl.Message(
        content="📤 Please provide a URL or upload a file to ingest:",
        author="EMVR",
    ).send()


@cl.action_callback("analyze")
async def on_analyze(action):
    """
    Handle analyze action.
    
    Args:
        action: The action
    """
    # Prompt for analysis content
    await cl.Message(
        content="🔬 What would you like me to analyze?",
        author="EMVR",
    ).send()


# ----- UI Customization -----

@cl.on_settings_update
async def on_settings_update(settings: Dict[str, Any]):
    """
    Handle settings updates.
    
    Args:
        settings: The new settings
    """
    # Update user preferences
    cl.user_session.set("settings", settings)
    
    # Confirm update
    await cl.Message(
        content="✅ Settings updated",
        author="System",
    ).send()


# ----- Shutdown -----

@cl.on_app_stop
async def shutdown():
    """Clean up resources when app is shutting down."""
    try:
        # Get orchestrator and close connections
        orchestrator = cl.user_session.get("orchestrator")
        if orchestrator:
            await orchestrator.shutdown()
        
        # Close other connections as needed
        memory_manager.close()
        
        logger.info("UI shutdown successfully")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")