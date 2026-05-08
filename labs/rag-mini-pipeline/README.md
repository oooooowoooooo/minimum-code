# Lab 4: RAG Mini Pipeline

## Objective

Build the core components of a Retrieval-Augmented Generation pipeline: document chunking with overlap, deterministic mock embeddings, cosine similarity, and top-k retrieval.

## Skills Practiced

- Text chunking with sliding windows
- Hash-based deterministic vector generation
- Cosine similarity computation
- Sorting and ranking results
- Dataclass usage

## Getting Started

```bash
pip install pytest
```

1. Open `starter.py`
2. Implement all methods in `RAGPipeline`
3. Run tests: `pytest test_rag_pipeline.py -v`

## Key Algorithms

### Chunking

Split text into windows of `chunk_size` characters, advancing by `chunk_size - overlap` each step. Skip whitespace-only chunks.

### Mock Embedding

Use SHA-256 hash bytes, map each byte pair to a value in [-1, 1]. This gives a deterministic, reproducible vector for any input text -- useful for testing without real embedding models.

### Retrieval

Embed the query, compute cosine similarity against all chunk embeddings, sort descending, return top-k.

## Solution

See `solution.py` when you're ready to check your work.
