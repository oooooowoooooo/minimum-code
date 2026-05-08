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
    def __init__(self, chunk_size=200, overlap=50, embedding_dim=384):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.embedding_dim = embedding_dim

    def chunk_document(self, text):
        text = text.strip()
        if not text:
            return []
        chunks = []
        idx = 0
        start = 0
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunk_text = text[start:end]
            if chunk_text.strip():
                chunks.append(Chunk(text=chunk_text, index=idx, embedding=[]))
                idx += 1
            start += self.chunk_size - self.overlap
        return chunks

    def embed(self, text):
        h = hashlib.sha256(text.encode()).hexdigest()
        values = []
        for i in range(self.embedding_dim):
            byte_pair = h[(i * 2) % len(h):(i * 2 + 2) % len(h) + 1]
            if len(byte_pair) < 2:
                byte_pair = h[-2:]
            val = int(byte_pair, 16) / 255.0 * 2 - 1
            values.append(val)
        return values

    def cosine_similarity(self, a, b):
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    def retrieve(self, query, chunks, top_k=3):
        if not chunks:
            return []
        q_embed = self.embed(query)
        scored = []
        for chunk in chunks:
            sim = self.cosine_similarity(q_embed, chunk.embedding)
            scored.append((sim, chunk))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [chunk for _, chunk in scored[:top_k]]
