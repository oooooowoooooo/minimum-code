import pytest
from starter import RAGPipeline, Chunk


@pytest.fixture
def pipeline():
    return RAGPipeline(chunk_size=100, overlap=20, embedding_dim=64)


def test_chunk_document_basic(pipeline):
    """Should split text into chunks of specified size."""
    text = "A" * 250
    chunks = pipeline.chunk_document(text)
    assert len(chunks) > 1
    for chunk in chunks:
        assert len(chunk.text) <= 100


def test_chunk_document_overlap(pipeline):
    """Consecutive chunks should overlap."""
    text = "ABCDEFGHIJ" * 30  # 300 chars
    chunks = pipeline.chunk_document(text)
    if len(chunks) >= 2:
        # Check overlap exists
        end_of_first = chunks[0].text[-20:]
        start_of_second = chunks[1].text[:20]
        # They should share some characters
        assert any(c in start_of_second for c in end_of_first[:5])


def test_chunk_document_empty(pipeline):
    """Empty text should return empty list."""
    assert pipeline.chunk_document("") == []
    assert pipeline.chunk_document("   ") == []


def test_chunk_indices(pipeline):
    """Chunks should have sequential indices."""
    text = "A" * 250
    chunks = pipeline.chunk_document(text)
    for i, chunk in enumerate(chunks):
        assert chunk.index == i


def test_embed_deterministic(pipeline):
    """Same text should always produce same embedding."""
    e1 = pipeline.embed("hello world")
    e2 = pipeline.embed("hello world")
    assert e1 == e2


def test_embed_dimension(pipeline):
    """Embedding should have correct dimension."""
    e = pipeline.embed("test")
    assert len(e) == 64


def test_embed_range(pipeline):
    """Embedding values should be in [-1, 1]."""
    e = pipeline.embed("some text for embedding")
    for val in e:
        assert -1 <= val <= 1


def test_embed_different_texts(pipeline):
    """Different texts should produce different embeddings."""
    e1 = pipeline.embed("hello")
    e2 = pipeline.embed("world")
    assert e1 != e2


def test_cosine_similarity_same(pipeline):
    """Cosine similarity of same vector should be 1.0."""
    v = [1.0, 0.0, 0.0]
    assert abs(pipeline.cosine_similarity(v, v) - 1.0) < 1e-6


def test_cosine_similarity_orthogonal(pipeline):
    """Cosine similarity of orthogonal vectors should be 0.0."""
    a = [1.0, 0.0, 0.0]
    b = [0.0, 1.0, 0.0]
    assert abs(pipeline.cosine_similarity(a, b)) < 1e-6


def test_retrieve_returns_top_k(pipeline):
    """Should return exactly top_k chunks."""
    text = "Machine learning is great. " * 50
    chunks = pipeline.chunk_document(text)
    for c in chunks:
        c.embedding = pipeline.embed(c.text)

    results = pipeline.retrieve("machine learning", chunks, top_k=2)
    assert len(results) == 2


def test_retrieve_relevance(pipeline):
    """Most relevant chunk should be first."""
    c1 = Chunk(text="Python is a programming language", index=0, embedding=pipeline.embed("Python is a programming language"))
    c2 = Chunk(text="Cooking pasta with tomato sauce", index=1, embedding=pipeline.embed("Cooking pasta with tomato sauce"))
    c3 = Chunk(text="Python decorators and context managers", index=2, embedding=pipeline.embed("Python decorators and context managers"))

    results = pipeline.retrieve("Python programming", [c1, c2, c3], top_k=2)
    # Python-related chunks should rank higher
    texts = [r.text for r in results]
    assert any("Python" in t for t in texts)
