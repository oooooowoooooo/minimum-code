"""RAG Mini Pipeline Lab
Goal: Build document chunking, mock embedding, and top-k retrieval
"""
from dataclasses import dataclass
from typing import List
import hashlib
import math


@dataclass
class Chunk:
    text: str
    index: int
    embedding: List[float]


class RAGPipeline:
    def __init__(self, chunk_size: int = 200, overlap: int = 50, embedding_dim: int = 384):
        """Initialize RAG pipeline.

        Args:
            chunk_size: Maximum characters per chunk
            overlap: Number of overlapping characters between consecutive chunks
            embedding_dim: Dimension of embedding vectors
        """
        # TODO: store config
        pass

    def chunk_document(self, text: str) -> List[Chunk]:
        """Split text into overlapping chunks.

        Each chunk should be at most chunk_size characters.
        Consecutive chunks should overlap by `overlap` characters.
        Empty or whitespace-only text should return empty list.
        """
        # TODO: implement
        pass

    def embed(self, text: str) -> List[float]:
        """Generate a deterministic mock embedding vector.

        Use SHA-256 hash of the text to generate a deterministic vector.
        The vector should have `embedding_dim` dimensions.
        Values should be normalized to [-1, 1] range.
        Same text should always produce same embedding.
        """
        # TODO: implement
        pass

    def cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Compute cosine similarity between two vectors."""
        # TODO: implement
        pass

    def retrieve(self, query: str, chunks: List[Chunk], top_k: int = 3) -> List[Chunk]:
        """Retrieve top-k most similar chunks to the query.

        1. Embed the query
        2. Compute similarity with each chunk's embedding
        3. Return top-k chunks sorted by similarity (highest first)
        """
        # TODO: implement
        pass
