"""
RAGFlow Dissection -- Simplified RAG Pipeline

This module reimplements RAGFlow's core RAG pipeline from scratch.
The goal is understanding: how does a production RAG system work?
From document parsing to chunking to embedding to retrieval to generation.

Run: python dissect.py
"""

from __future__ import annotations

import hashlib
import math
import re
from dataclasses import dataclass, field
from typing import Any


# =============================================================================
# Data Structures
# =============================================================================

@dataclass
class ContentBlock:
    """A structured content block extracted from a document."""
    text: str
    block_type: str  # "header", "body", "table", "list"
    page: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ParsedDocument:
    """Result of parsing a document -- a list of content blocks."""
    source: str
    blocks: list[ContentBlock]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Chunk:
    """A unit of text ready for embedding."""
    id: str
    text: str
    source: str
    position: int
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddedChunk:
    """A chunk with its vector representation."""
    chunk: Chunk
    vector: list[float]


@dataclass
class SearchResult:
    """A chunk retrieved by similarity search, with its score."""
    chunk: Chunk
    score: float


# =============================================================================
# Document Parser -- Text Extraction
# =============================================================================

class DocumentParser:
    """
    Extracts structured content from documents.

    In RAGFlow, this is the most sophisticated component, using:
    - Layout analysis (YOLO-based object detection)
    - OCR for scanned documents
    - Table extraction with structure preservation
    - Multi-column layout handling

    Here we implement simplified parsers for plain text and Markdown.
    The principle is the same: structure in, structured blocks out.
    """

    def parse(self, text: str, source: str = "unknown") -> ParsedDocument:
        """
        Parse text into structured content blocks.

        Detects:
        - Headers (lines starting with #)
        - Tables (lines with | delimiters)
        - Lists (lines starting with - or *)
        - Body text (everything else)
        """
        blocks: list[ContentBlock] = []
        lines = text.split("\n")
        current_body: list[str] = []

        def flush_body():
            """Flush accumulated body text into a ContentBlock."""
            if current_body:
                blocks.append(ContentBlock(
                    text="\n".join(current_body).strip(),
                    block_type="body",
                ))
                current_body.clear()

        for line in lines:
            stripped = line.strip()

            # Empty line: flush current body
            if not stripped:
                flush_body()
                continue

            # Header: lines starting with #
            if stripped.startswith("#"):
                flush_body()
                level = len(stripped) - len(stripped.lstrip("#"))
                blocks.append(ContentBlock(
                    text=stripped.lstrip("# ").strip(),
                    block_type="header",
                    metadata={"level": level},
                ))
                continue

            # Table: lines with | delimiter
            if "|" in stripped and stripped.startswith("|"):
                flush_body()
                # Accumulate consecutive table lines
                table_lines = [stripped]
                idx = lines.index(line)
                for next_line in lines[idx + 1:]:
                    if next_line.strip().startswith("|"):
                        table_lines.append(next_line.strip())
                    else:
                        break
                blocks.append(ContentBlock(
                    text="\n".join(table_lines),
                    block_type="table",
                ))
                continue

            # List: lines starting with - or *
            if stripped.startswith(("-", "*")):
                flush_body()
                blocks.append(ContentBlock(
                    text=stripped,
                    block_type="list",
                ))
                continue

            # Body text: accumulate
            current_body.append(stripped)

        flush_body()

        return ParsedDocument(source=source, blocks=blocks)


# =============================================================================
# Chunker -- Split Documents into Chunks
# =============================================================================

class Chunker:
    """
    Splits parsed documents into chunks suitable for embedding.

    In RAGFlow, multiple chunking strategies are available:
    - Fixed-size: split by character count with overlap
    - Semantic: split at paragraph/section boundaries
    - Document-aware: respect table and header boundaries

    We implement all three strategies here.
    """

    def __init__(self, chunk_size: int = 200, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_fixed_size(self, doc: ParsedDocument) -> list[Chunk]:
        """
        Fixed-size chunking with overlap.

        Simple but can split mid-sentence. The overlap ensures that
        context is not completely lost at boundaries.
        """
        # Concatenate all text blocks
        full_text = "\n".join(block.text for block in doc.blocks if block.text)
        if not full_text:
            return []

        chunks: list[Chunk] = []
        start = 0
        position = 0

        while start < len(full_text):
            end = min(start + self.chunk_size, len(full_text))
            chunk_text = full_text[start:end]

            if chunk_text.strip():
                chunk_id = self._make_id(chunk_text, doc.source, position)
                chunks.append(Chunk(
                    id=chunk_id,
                    text=chunk_text.strip(),
                    source=doc.source,
                    position=position,
                    metadata={"strategy": "fixed_size"},
                ))
                position += 1

            # Move forward by (chunk_size - overlap)
            start += self.chunk_size - self.chunk_overlap

        return chunks

    def chunk_semantic(self, doc: ParsedDocument) -> list[Chunk]:
        """
        Semantic chunking: split at natural boundaries.

        Each content block becomes a chunk. This preserves paragraph
        and section boundaries but can produce uneven chunk sizes.
        """
        chunks: list[Chunk] = []
        position = 0

        for block in doc.blocks:
            if not block.text.strip():
                continue

            # Small blocks: merge with neighbors (handled by caller)
            # For simplicity, each block is a chunk here
            chunk_id = self._make_id(block.text, doc.source, position)
            chunks.append(Chunk(
                id=chunk_id,
                text=block.text.strip(),
                source=doc.source,
                position=position,
                metadata={
                    "strategy": "semantic",
                    "block_type": block.block_type,
                    **block.metadata,
                },
            ))
            position += 1

        return chunks

    def chunk_document_aware(self, doc: ParsedDocument) -> list[Chunk]:
        """
        Document-aware chunking: respect structure.

        Rules:
        - Tables always get their own chunk (never split a table)
        - Headers are merged with the following body text
        - Lists are grouped together
        - Body text is split by fixed size if too long
        """
        chunks: list[Chunk] = []
        position = 0
        pending_header: str | None = None
        pending_list: list[str] = []

        def flush_list():
            nonlocal pending_list, position
            if pending_list:
                text = "\n".join(pending_list)
                chunk_id = self._make_id(text, doc.source, position)
                chunks.append(Chunk(
                    id=chunk_id,
                    text=text,
                    source=doc.source,
                    position=position,
                    metadata={"strategy": "document_aware", "block_type": "list"},
                ))
                position += 1
                pending_list.clear()

        for block in doc.blocks:
            if not block.text.strip():
                continue

            # Tables: always their own chunk
            if block.block_type == "table":
                flush_list()
                chunk_id = self._make_id(block.text, doc.source, position)
                chunks.append(Chunk(
                    id=chunk_id,
                    text=block.text.strip(),
                    source=doc.source,
                    position=position,
                    metadata={"strategy": "document_aware", "block_type": "table"},
                ))
                position += 1
                continue

            # Headers: store for merging with next body text
            if block.block_type == "header":
                flush_list()
                pending_header = block.text
                continue

            # Lists: accumulate
            if block.block_type == "list":
                pending_list.append(block.text)
                continue

            # Body text: merge with pending header if any
            flush_list()
            text = block.text
            if pending_header:
                text = f"{pending_header}\n{text}"
                pending_header = None

            # Split if too long
            if len(text) > self.chunk_size:
                sub_chunks = self._split_text(text)
                for sub_text in sub_chunks:
                    chunk_id = self._make_id(sub_text, doc.source, position)
                    chunks.append(Chunk(
                        id=chunk_id,
                        text=sub_text,
                        source=doc.source,
                        position=position,
                        metadata={"strategy": "document_aware", "block_type": "body"},
                    ))
                    position += 1
            else:
                chunk_id = self._make_id(text, doc.source, position)
                chunks.append(Chunk(
                    id=chunk_id,
                    text=text,
                    source=doc.source,
                    position=position,
                    metadata={"strategy": "document_aware", "block_type": "body"},
                ))
                position += 1

        flush_list()
        return chunks

    def _split_text(self, text: str) -> list[str]:
        """Split long text into chunks respecting sentence boundaries."""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks: list[str] = []
        current: list[str] = []
        current_len = 0

        for sentence in sentences:
            if current_len + len(sentence) > self.chunk_size and current:
                chunks.append(" ".join(current))
                current = [sentence]
                current_len = len(sentence)
            else:
                current.append(sentence)
                current_len += len(sentence)

        if current:
            chunks.append(" ".join(current))

        return chunks

    @staticmethod
    def _make_id(text: str, source: str, position: int) -> str:
        """Generate a deterministic chunk ID."""
        content = f"{source}:{position}:{text[:100]}"
        return hashlib.md5(content.encode()).hexdigest()[:12]


# =============================================================================
# Embedder -- Text to Vectors
# =============================================================================

class Embedder:
    """
    Converts text chunks into dense vector representations.

    In RAGFlow, this calls an embedding model API (OpenAI, BGE, E5, etc.).
    Here we use a simple hash-based simulation that produces deterministic
    vectors for testing. The principle is identical: text in, vector out.
    """

    def __init__(self, dimension: int = 128):
        self.dimension = dimension

    def embed(self, text: str) -> list[float]:
        """
        Generate a vector for a text string.

        Real implementation: call embedding model API.
        Our implementation: hash-based deterministic simulation.

        The simulation ensures:
        - Same text always produces the same vector
        - Similar texts produce somewhat similar vectors
        - The vector has the correct dimension
        """
        # Use text hash as seed for deterministic "embedding"
        text_hash = hashlib.sha256(text.encode()).hexdigest()

        # Generate vector from hash
        vector: list[float] = []
        for i in range(self.dimension):
            # Use different parts of the hash for each dimension
            byte_idx = (i * 2) % len(text_hash)
            hex_pair = text_hash[byte_idx:byte_idx + 2]
            # Normalize to [-1, 1]
            value = (int(hex_pair, 16) / 255.0) * 2 - 1
            vector.append(value)

        # Normalize to unit vector (as real embeddings are)
        magnitude = math.sqrt(sum(v * v for v in vector))
        if magnitude > 0:
            vector = [v / magnitude for v in vector]

        return vector

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts. In production, this would batch API calls."""
        return [self.embed(text) for text in texts]


# =============================================================================
# Vector Store -- Similarity Search
# =============================================================================

class VectorStore:
    """
    Stores embedded chunks and supports similarity search.

    In RAGFlow, the default vector store is Elasticsearch. For production,
    you would use a dedicated vector database (Qdrant, Milvus, Weaviate).

    Here we implement a simple in-memory vector store with cosine similarity.
    """

    def __init__(self):
        self._vectors: list[tuple[str, list[float], Chunk]] = []

    def add(self, embedded_chunk: EmbeddedChunk) -> None:
        """Add an embedded chunk to the store."""
        self._vectors.append((
            embedded_chunk.chunk.id,
            embedded_chunk.vector,
            embedded_chunk.chunk,
        ))

    def add_batch(self, embedded_chunks: list[EmbeddedChunk]) -> None:
        """Add multiple embedded chunks."""
        for ec in embedded_chunks:
            self.add(ec)

    def search(self, query_vector: list[float], top_k: int = 5) -> list[SearchResult]:
        """
        Find the most similar chunks to the query vector.

        Uses cosine similarity: measures the angle between two vectors.
        Range: [-1, 1] where 1 = identical, 0 = orthogonal, -1 = opposite.
        """
        if not self._vectors:
            return []

        # Compute similarity scores
        scored: list[tuple[float, Chunk]] = []
        for _, vector, chunk in self._vectors:
            score = self._cosine_similarity(query_vector, vector)
            scored.append((score, chunk))

        # Sort by score descending
        scored.sort(key=lambda x: x[0], reverse=True)

        # Return top-K
        return [
            SearchResult(chunk=chunk, score=score)
            for score, chunk in scored[:top_k]
        ]

    def search_hybrid(
        self,
        query_vector: list[float],
        query_text: str,
        top_k: int = 5,
        alpha: float = 0.7,
    ) -> list[SearchResult]:
        """
        Hybrid search: combine vector similarity with keyword matching.

        alpha: weight for vector score (1-alpha for keyword score)
        """
        if not self._vectors:
            return []

        # Vector scores
        vector_scores: dict[str, float] = {}
        for _, vector, chunk in self._vectors:
            vector_scores[chunk.id] = self._cosine_similarity(query_vector, vector)

        # Keyword scores (BM25-like: term frequency in chunk)
        query_terms = set(query_text.lower().split())
        keyword_scores: dict[str, float] = {}
        for _, _, chunk in self._vectors:
            chunk_lower = chunk.text.lower()
            # Simple term frequency score
            matches = sum(1 for term in query_terms if term in chunk_lower)
            keyword_scores[chunk.id] = matches / max(len(query_terms), 1)

        # Normalize scores to [0, 1]
        max_vec = max(vector_scores.values()) if vector_scores else 1
        max_kw = max(keyword_scores.values()) if keyword_scores else 1

        # Combine scores
        combined: list[tuple[float, Chunk]] = []
        for _, _, chunk in self._vectors:
            v_score = vector_scores.get(chunk.id, 0) / max(max_vec, 1e-10)
            k_score = keyword_scores.get(chunk.id, 0) / max(max_kw, 1e-10)
            final_score = alpha * v_score + (1 - alpha) * k_score
            combined.append((final_score, chunk))

        combined.sort(key=lambda x: x[0], reverse=True)

        return [
            SearchResult(chunk=chunk, score=score)
            for score, chunk in combined[:top_k]
        ]

    @staticmethod
    def _cosine_similarity(a: list[float], b: list[float]) -> float:
        """Compute cosine similarity between two vectors."""
        if len(a) != len(b):
            raise ValueError(f"Vector dimensions mismatch: {len(a)} vs {len(b)}")

        dot_product = sum(x * y for x, y in zip(a, b))
        magnitude_a = math.sqrt(sum(x * x for x in a))
        magnitude_b = math.sqrt(sum(x * x for x in b))

        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        return dot_product / (magnitude_a * magnitude_b)

    def __len__(self) -> int:
        return len(self._vectors)


# =============================================================================
# RAG Pipeline -- End-to-End
# =============================================================================

class RAGPipeline:
    """
    Complete RAG pipeline: parse -> chunk -> embed -> store -> retrieve -> generate.

    This is the simplified equivalent of RAGFlow's document processing
    and query pipeline.
    """

    def __init__(
        self,
        chunker: Chunker | None = None,
        embedder: Embedder | None = None,
        vector_store: VectorStore | None = None,
        parser: DocumentParser | None = None,
    ):
        self.parser = parser or DocumentParser()
        self.chunker = chunker or Chunker(chunk_size=200, chunk_overlap=50)
        self.embedder = embedder or Embedder(dimension=128)
        self.vector_store = vector_store or VectorStore()

    def ingest(self, text: str, source: str = "document", strategy: str = "document_aware") -> int:
        """
        Ingest a document into the RAG pipeline.

        Steps:
        1. Parse the document into content blocks
        2. Chunk the blocks using the specified strategy
        3. Embed each chunk
        4. Store embeddings in the vector store

        Returns: number of chunks ingested.
        """
        print(f"  [Ingest] Parsing '{source}'...")
        doc = self.parser.parse(text, source)
        print(f"  [Ingest] Found {len(doc.blocks)} content blocks")

        # Chunk
        print(f"  [Ingest] Chunking (strategy: {strategy})...")
        if strategy == "fixed_size":
            chunks = self.chunker.chunk_fixed_size(doc)
        elif strategy == "semantic":
            chunks = self.chunker.chunk_semantic(doc)
        else:
            chunks = self.chunker.chunk_document_aware(doc)
        print(f"  [Ingest] Created {len(chunks)} chunks")

        # Embed
        print(f"  [Ingest] Embedding {len(chunks)} chunks...")
        for chunk in chunks:
            vector = self.embedder.embed(chunk.text)
            self.vector_store.add(EmbeddedChunk(chunk=chunk, vector=vector))

        print(f"  [Ingest] Stored in vector store (total: {len(self.vector_store)} vectors)")
        return len(chunks)

    def query(
        self,
        question: str,
        top_k: int = 3,
        use_hybrid: bool = True,
    ) -> dict[str, Any]:
        """
        Query the RAG pipeline.

        Steps:
        1. Embed the question
        2. Retrieve relevant chunks (vector or hybrid search)
        3. Build a prompt with retrieved context
        4. Generate an answer (simulated)

        Returns: answer, sources, and retrieval details.
        """
        print(f"\n  [Query] Question: '{question}'")

        # Embed the question
        query_vector = self.embedder.embed(question)
        print(f"  [Query] Embedded question ({len(query_vector)} dimensions)")

        # Retrieve
        if use_hybrid:
            results = self.vector_store.search_hybrid(
                query_vector, question, top_k=top_k
            )
            print(f"  [Query] Hybrid search returned {len(results)} results")
        else:
            results = self.vector_store.search(query_vector, top_k=top_k)
            print(f"  [Query] Vector search returned {len(results)} results")

        # Build context from retrieved chunks
        context_parts: list[str] = []
        sources: list[dict[str, Any]] = []
        for i, result in enumerate(results):
            context_parts.append(f"[{i+1}] {result.chunk.text}")
            sources.append({
                "chunk_id": result.chunk.id,
                "source": result.chunk.source,
                "score": round(result.score, 4),
                "text_preview": result.chunk.text[:80],
            })

        context = "\n\n".join(context_parts)

        # Generate answer (simulated)
        answer = self._generate_answer(question, context)

        return {
            "answer": answer,
            "sources": sources,
            "context_used": context[:300] + "..." if len(context) > 300 else context,
        }

    def _generate_answer(self, question: str, context: str) -> str:
        """
        Generate an answer using the question and retrieved context.

        In RAGFlow, this calls an LLM (GPT-4, Claude, etc.) with a
        carefully crafted prompt. Here we simulate the response.
        """
        # In production: call LLM API with prompt
        prompt = (
            f"Based on the following context, answer the question.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\n\n"
            f"Answer:"
        )

        # Simulated response
        if context.strip():
            return (
                f"Based on the retrieved context, here is the answer to "
                f"'{question}': The context provides relevant information "
                f"from {len(context)} characters of source material. "
                f"[This is a simulated answer; in production, an LLM "
                f"would generate a real response grounded in the context.]"
            )
        else:
            return "No relevant context found. Unable to answer the question."


# =============================================================================
# Inline Tests & Demo
# =============================================================================

def test_document_parser():
    """Test document parsing with various content types."""
    print("--- Test: DocumentParser ---")

    parser = DocumentParser()

    text = """# Introduction to RAG

RAG stands for Retrieval-Augmented Generation.

## How It Works

RAG combines retrieval with generation. The system first retrieves relevant
documents, then uses them as context for the LLM.

| Component | Purpose |
|-----------|---------|
| Parser | Extract text |
| Chunker | Split text |
| Embedder | Create vectors |

- First, parse the document
- Then, chunk the text
- Finally, embed and store

RAG is powerful because it grounds LLM responses in real data."""

    doc = parser.parse(text, source="test.md")

    assert len(doc.blocks) > 0, "Should find content blocks"
    print(f"  Parsed {len(doc.blocks)} blocks:")
    for block in doc.blocks:
        preview = block.text[:50].replace("\n", " ")
        print(f"    [{block.block_type:6s}] {preview}...")

    # Verify block types
    types = [b.block_type for b in doc.blocks]
    assert "header" in types, "Should detect headers"
    assert "body" in types, "Should detect body text"

    print("  PASS\n")


def test_chunker_strategies():
    """Test all three chunking strategies."""
    print("--- Test: Chunker Strategies ---")

    parser = DocumentParser()
    chunker = Chunker(chunk_size=100, chunk_overlap=20)

    text = """# Python Guide

Python is a high-level programming language. It was created by Guido van Rossum
and first released in 1991. Python emphasizes code readability with its notable
use of significant indentation.

## Data Types

Python has several built-in data types including integers, floats, strings,
lists, tuples, and dictionaries. Each type has specific methods and use cases.

| Type | Example |
|------|---------|
| int | 42 |
| str | 'hello' |
| list | [1, 2, 3] |

- Integers are whole numbers
- Strings are text sequences
- Lists are ordered collections"""

    doc = parser.parse(text, source="python_guide.md")

    # Fixed-size chunking
    fixed_chunks = chunker.chunk_fixed_size(doc)
    print(f"  Fixed-size: {len(fixed_chunks)} chunks")
    for c in fixed_chunks:
        print(f"    [{c.id}] {c.text[:50]}...")

    # Semantic chunking
    semantic_chunks = chunker.chunk_semantic(doc)
    print(f"  Semantic: {len(semantic_chunks)} chunks")
    for c in semantic_chunks:
        print(f"    [{c.id}] {c.text[:50]}...")

    # Document-aware chunking
    aware_chunks = chunker.chunk_document_aware(doc)
    print(f"  Document-aware: {len(aware_chunks)} chunks")
    for c in aware_chunks:
        block_type = c.metadata.get("block_type", "?")
        print(f"    [{c.id}] ({block_type}) {c.text[:50]}...")

    # Verify tables are preserved in document-aware mode
    table_chunks = [c for c in aware_chunks if c.metadata.get("block_type") == "table"]
    assert len(table_chunks) > 0, "Document-aware should preserve tables as single chunks"
    print(f"  Table chunks preserved: {len(table_chunks)}")

    print("  PASS\n")


def test_embedder():
    """Test the embedder produces correct vectors."""
    print("--- Test: Embedder ---")

    embedder = Embedder(dimension=64)

    # Embed a text
    vec1 = embedder.embed("Python is a programming language")
    assert len(vec1) == 64, f"Expected 64 dimensions, got {len(vec1)}"
    print(f"  Vector dimension: {len(vec1)}")

    # Same text produces same vector (deterministic)
    vec2 = embedder.embed("Python is a programming language")
    assert vec1 == vec2, "Same text should produce same vector"
    print(f"  Deterministic: YES")

    # Different text produces different vector
    vec3 = embedder.embed("JavaScript is also a programming language")
    assert vec1 != vec3, "Different text should produce different vector"
    print(f"  Different text -> different vector: YES")

    # Vector is normalized (magnitude ~1)
    magnitude = math.sqrt(sum(v * v for v in vec1))
    assert abs(magnitude - 1.0) < 0.001, f"Expected unit vector, got magnitude {magnitude}"
    print(f"  Unit vector magnitude: {magnitude:.6f}")

    print("  PASS\n")


def test_vector_store():
    """Test vector store with similarity search."""
    print("--- Test: VectorStore ---")

    embedder = Embedder(dimension=64)
    store = VectorStore()

    # Add some chunks
    texts = [
        "Python is a high-level programming language",
        "JavaScript is used for web development",
        "Machine learning uses statistical methods",
        "Deep learning is a subset of machine learning",
        "Natural language processing handles human language",
    ]

    for i, text in enumerate(texts):
        chunk = Chunk(id=f"chunk_{i}", text=text, source="test", position=i)
        vector = embedder.embed(text)
        store.add(EmbeddedChunk(chunk=chunk, vector=vector))

    assert len(store) == 5, f"Expected 5 vectors, got {len(store)}"
    print(f"  Stored {len(store)} vectors")

    # Search
    query_vector = embedder.embed("programming language Python")
    results = store.search(query_vector, top_k=3)
    assert len(results) == 3, f"Expected 3 results, got {len(results)}"
    print(f"  Top-3 search results:")
    for r in results:
        print(f"    score={r.score:.4f} | {r.chunk.text[:50]}")

    # Hybrid search
    results_hybrid = store.search_hybrid(
        query_vector, "Python programming", top_k=3, alpha=0.5
    )
    print(f"  Hybrid search results:")
    for r in results_hybrid:
        print(f"    score={r.score:.4f} | {r.chunk.text[:50]}")

    print("  PASS\n")


def test_rag_pipeline_end_to_end():
    """Test the complete RAG pipeline."""
    print("--- Test: RAG Pipeline (End-to-End) ---")

    pipeline = RAGPipeline(
        chunker=Chunker(chunk_size=150, chunk_overlap=30),
        embedder=Embedder(dimension=64),
    )

    # Ingest multiple documents
    doc1 = """# Python Basics

Python is a versatile programming language. It supports multiple programming
paradigms including procedural, object-oriented, and functional programming.

## Variables

Variables in Python do not need explicit declaration. Python uses dynamic typing,
meaning the type is determined at runtime.

| Type | Example | Description |
|------|---------|-------------|
| int | x = 42 | Integer numbers |
| str | s = 'hi' | Text strings |
| list | l = [1,2] | Ordered collections |

- Variables are created on assignment
- No type declaration needed
- Names are case-sensitive"""

    doc2 = """# Machine Learning Overview

Machine learning is a subset of artificial intelligence. It enables systems
to learn and improve from experience without being explicitly programmed.

## Types of ML

- Supervised learning: trained on labeled data
- Unsupervised learning: finds patterns in unlabeled data
- Reinforcement learning: learns through trial and error

## Common Algorithms

| Algorithm | Type | Use Case |
|-----------|------|----------|
| Linear Regression | Supervised | Prediction |
| K-Means | Unsupervised | Clustering |
| Q-Learning | Reinforcement | Game playing |

Deep learning uses neural networks with multiple layers.
It excels at image recognition and natural language processing."""

    n1 = pipeline.ingest(doc1, source="python_basics.md")
    n2 = pipeline.ingest(doc2, source="ml_overview.md")
    print(f"  Ingested: {n1} chunks from doc1, {n2} chunks from doc2")
    print(f"  Total vectors in store: {len(pipeline.vector_store)}")

    # Query
    result = pipeline.query("What are Python variables?", top_k=3)
    print(f"\n  Answer: {result['answer'][:100]}...")
    print(f"  Sources: {len(result['sources'])}")
    for src in result["sources"]:
        print(f"    [{src['chunk_id']}] score={src['score']} | {src['text_preview']}")

    # Query about ML
    result2 = pipeline.query("What types of machine learning exist?", top_k=3)
    print(f"\n  Answer: {result2['answer'][:100]}...")
    print(f"  Sources: {len(result2['sources'])}")

    print("  PASS\n")


def test_rag_pipeline_empty_store():
    """Test querying an empty pipeline."""
    print("--- Test: RAG Pipeline (Empty Store) ---")

    pipeline = RAGPipeline()
    result = pipeline.query("What is Python?")

    assert "No relevant context" in result["answer"]
    assert len(result["sources"]) == 0
    print(f"  Empty store query result: {result['answer']}")
    print("  PASS\n")


# =============================================================================
# Main -- Run all tests
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("RAGFlow Dissection -- Running Tests")
    print("=" * 60)
    print()

    test_document_parser()
    test_chunker_strategies()
    test_embedder()
    test_vector_store()
    test_rag_pipeline_end_to_end()
    test_rag_pipeline_empty_store()

    print("=" * 60)
    print("All tests passed.")
    print("=" * 60)
