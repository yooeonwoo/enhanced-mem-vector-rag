"""Tests for the MCP server."""

import pytest
from fastapi.testclient import TestClient

from emvr.mcp_server.server import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_read_graph(client):
    """Test the /memory.read_graph endpoint."""
    response = client.post("/memory.read_graph", json={})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "graph" in response.json()


def test_search_nodes(client):
    """Test the /memory.search_nodes endpoint."""
    response = client.post(
        "/memory.search_nodes",
        json={
            "query": "test query",
            "limit": 5,
        },
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "results" in response.json()


def test_create_entities(client):
    """Test the /memory.create_entities endpoint."""
    response = client.post(
        "/memory.create_entities",
        json={
            "entities": [
                {
                    "name": "Test Entity",
                    "entityType": "Test",
                    "observations": ["Test observation"],
                },
            ],
        },
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_create_relations(client):
    """Test the /memory.create_relations endpoint."""
    response = client.post(
        "/memory.create_relations",
        json={
            "relations": [
                {
                    "from_": "Entity A",
                    "to": "Entity B",
                    "relationType": "related_to",
                },
            ],
        },
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_add_observations(client):
    """Test the /memory.add_observations endpoint."""
    response = client.post(
        "/memory.add_observations",
        json={
            "observations": [
                {
                    "entityName": "Test Entity",
                    "contents": ["New observation"],
                },
            ],
        },
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_hybrid_search(client):
    """Test the /search.hybrid endpoint."""
    response = client.post(
        "/search.hybrid",
        json={
            "query": "test query",
            "limit": 5,
        },
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "results" in response.json()


def test_graph_query(client):
    """Test the /graph.query endpoint."""
    response = client.post(
        "/graph.query",
        json={
            "query": "MATCH (n) RETURN n LIMIT 10",
        },
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "results" in response.json()
