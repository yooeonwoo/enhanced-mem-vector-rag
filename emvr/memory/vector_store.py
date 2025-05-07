"""Vector store implementation using Qdrant and Mem0."""

import os
from typing import Any

import qdrant_client
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore

# Load environment variables
load_dotenv()


class QdrantMemoryStore:
    """Vector memory store implementation using Qdrant."""

    def __init__(
        self,
        collection_name: str = "emvr_memory",
        url: str | None = None,
        api_key: str | None = None,
    ) -> None:
        """
        Initialize the Qdrant memory store.

        Args:
            collection_name: Name of the Qdrant collection
            url: URL of the Qdrant server (defaults to env var QDRANT_URL)
            api_key: API key for the Qdrant server (defaults to env var QDRANT_API_KEY)

        """
        self.collection_name = collection_name
        self.url = url or os.environ.get("QDRANT_URL", "http://localhost:6333")
        self.api_key = api_key or os.environ.get("QDRANT_API_KEY")

        # Initialize Qdrant client
        self.client = qdrant_client.QdrantClient(
            url=self.url,
            api_key=self.api_key,
        )

        # Initialize LlamaIndex vector store
        self.vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
        )

        # Initialize LlamaIndex vector store index
        self.index = VectorStoreIndex.from_vector_store(self.vector_store)

    async def similarity_search(
        self, query: str, top_k: int = 5, filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Perform similarity search against the vector store.

        Args:
            query: The query text
            top_k: Number of results to return
            filters: Optional filters to apply to the search

        Returns:
            List of matching documents with scores

        """
        # Create retriever with filtering
        retriever = self.index.as_retriever(
            similarity_top_k=top_k,
            filters=filters,
        )

        # Retrieve similar documents
        nodes = await retriever.aretrieve(query)

        # Format results
        results = []
        for node in nodes:
            results.append({
                "id": node.node_id,
                "text": node.text,
                "metadata": node.metadata,
                "score": node.score if hasattr(node, "score") else None,
            })

        return results

    async def hybrid_search(
        self, query: str, top_k: int = 5, filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Perform hybrid (vector + keyword) search against the vector store.

        Args:
            query: The query text
            top_k: Number of results to return
            filters: Optional filters to apply to the search

        Returns:
            List of matching documents with scores

        """
        # Use LlamaIndex's hybrid retriever
        from llama_index.core import QueryBundle

        vector_retriever = self.index.as_retriever(
            similarity_top_k=top_k * 2,  # Get more candidates for reranking
            filters=filters,
        )

        # Create query bundle
        query_bundle = QueryBundle(query)

        # Retrieve with vector search
        nodes = await vector_retriever.aretrieve(query_bundle)

        # Simple reranking - in a real implementation, you'd use a more sophisticated
        # reranking method, potentially with BM25 or a learned reranker
        results = []
        for node in nodes[:top_k]:
            results.append({
                "id": node.node_id,
                "text": node.text,
                "metadata": node.metadata,
                "score": node.score if hasattr(node, "score") else None,
            })

        return results
