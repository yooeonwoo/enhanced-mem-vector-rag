#!/usr/bin/env python
"""
Script to update the memory system with our implementation progress.
This uses HTTP requests to interact with our MCP server endpoints directly.
"""

import asyncio
import os
import sys
from datetime import datetime

import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MCP server endpoint for memory operations
MCP_HOST = os.environ.get("MCP_HOST", "localhost")
MCP_PORT = os.environ.get("MCP_PORT", "8000")
BASE_URL = f"http://{MCP_HOST}:{MCP_PORT}"
HEADERS = {"Content-Type": "application/json"}


async def create_entities():
    """Create entities for new components."""
    url = f"{BASE_URL}/memory.create_entities"

    # Get today's date for progress entity
    today = datetime.now().strftime("%Y-%m-%d")

    data = {
        "entities": [
            {
                "name": f"Implementation Progress - {today}",
                "entity_type": "Progress",
                "observations": [
                    "Added Docker and Docker Compose configuration for all system components",
                    "Implemented a comprehensive setup script for initial project setup",
                    "Added environment configuration templates and documentation",
                    "Implemented monitoring with Prometheus and Grafana",
                    "Completed Docker configurations and orchestration in Phase 8",
                    "Next focus on testing implementation and documentation",
                ],
            },
            {
                "name": "Decision - Deployment Strategy",
                "entity_type": "Decision",
                "observations": [
                    "Using Docker Compose for local development and deployment",
                    "Containerized all components: MCP Server, Chainlit UI, Qdrant, Neo4j, Supabase, Grafana, Prometheus",
                    "Implemented persistent volumes for all storage components",
                    "Added monitoring and observability with Prometheus/Grafana stack",
                    "Created environment-specific setup scripts",
                ],
            },
            {
                "name": "DockerConfiguration",
                "entity_type": "Component",
                "observations": [
                    "Created Docker Compose configuration with service dependencies",
                    "Implemented environment variable passing from host to containers",
                    "Set up container networking for internal communication",
                    "Added persistent volumes for data storage",
                    "Created Dockerfiles for custom services (MCP Server, Chainlit UI)",
                    "Added Grafana dashboards for monitoring",
                ],
            },
            {
                "name": "SetupScript",
                "entity_type": "Component",
                "observations": [
                    "Created comprehensive setup script for initial project setup",
                    "Checks for required dependencies (Python 3.11+, Docker, Docker Compose)",
                    "Sets up virtual environment using uv",
                    "Installs project dependencies",
                    "Creates environment configuration from template",
                    "Provides option to start Docker containers",
                ],
            },
        ],
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=HEADERS)
            print(f"Create entities response: {response.status_code}")
            if response.status_code == 200:
                print("Successfully created entities")
            else:
                print(f"Error creating entities: {response.text}")
    except Exception as e:
        print(f"Error creating entities: {e}")


async def create_relations():
    """Create relations between components."""
    url = f"{BASE_URL}/memory.create_relations"

    data = {
        "relations": [
            {
                "from": "DockerConfiguration",
                "relation_type": "implements",
                "to": "Decision - Deployment Strategy",
            },
            {
                "from": "DockerConfiguration",
                "relation_type": "part_of",
                "to": "Phase 8: Deployment & Testing",
            },
            {
                "from": "SetupScript",
                "relation_type": "part_of",
                "to": "Phase 8: Deployment & Testing",
            },
            {
                "from": "Implementation Progress - " + datetime.now().strftime("%Y-%m-%d"),
                "relation_type": "documents",
                "to": "Phase 8: Deployment & Testing",
            },
            {
                "from": "DockerConfiguration",
                "relation_type": "depends_on",
                "to": "MCP Server",
            },
            {
                "from": "DockerConfiguration",
                "relation_type": "depends_on",
                "to": "AgentSystem",
            },
            {
                "from": "DockerConfiguration",
                "relation_type": "connects",
                "to": "Chainlit UI",
            },
        ],
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=HEADERS)
            print(f"Create relations response: {response.status_code}")
            if response.status_code == 200:
                print("Successfully created relations")
            else:
                print(f"Error creating relations: {response.text}")
    except Exception as e:
        print(f"Error creating relations: {e}")


async def add_observations():
    """Add observations to existing entities."""
    url = f"{BASE_URL}/memory.add_observations"

    data = {
        "observations": [
            {
                "entity_name": "Project Status",
                "contents": [
                    "Phases 1-7 are fully completed",
                    "Phase 8 (Deployment & Testing) partially completed with Docker configurations",
                    "Next focus is on testing implementation and documentation",
                    "Unit tests development is the next priority",
                ],
            },
            {
                "entity_name": "EMVR System",
                "contents": [
                    "Added Docker and Docker Compose support for all components",
                    "Created setup script for easy initialization",
                    "Completed the deployment architecture",
                    "Implemented monitoring and observability with Prometheus/Grafana",
                ],
            },
            {
                "entity_name": "Recent Decisions",
                "contents": [
                    "Decided to use Docker Compose for deployment orchestration",
                    "Implemented Prometheus/Grafana for monitoring and observability",
                    "Created detailed setup script for easier onboarding",
                    "Next focus will be on comprehensive testing and documentation",
                ],
            },
        ],
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=HEADERS)
            print(f"Add observations response: {response.status_code}")
            if response.status_code == 200:
                print("Successfully added observations")
            else:
                print(f"Error adding observations: {response.text}")
    except Exception as e:
        print(f"Error adding observations: {e}")


async def main():
    """Main function to update memory."""
    print("Updating memory with implementation progress...")

    try:
        # Check if the MCP server is running
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{BASE_URL}/memory.read_graph", timeout=5.0)
                if response.status_code != 200:
                    print(f"Error: MCP server not available at {BASE_URL}")
                    print("Please make sure the MCP server is running.")
                    sys.exit(1)
            except httpx.RequestError:
                print(f"Error: Could not connect to MCP server at {BASE_URL}")
                print("Please make sure the MCP server is running.")
                sys.exit(1)

        await create_entities()
        await create_relations()
        await add_observations()

        print("Memory update completed successfully")
    except Exception as e:
        print(f"Error updating memory: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
