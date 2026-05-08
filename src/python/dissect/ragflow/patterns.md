# RAGFlow Core Design Patterns

## Pattern 1: Document Parsing Pattern

**Intent:** Extract structured content from unstructured documents while
preserving layout, tables, and semantic structure.

**Approach:**
```
Document (PDF/DOCX/HTML)
  |
  v
Layout Analysis (detect columns, headers, body, tables)
  |
  v
Content Extraction (text blocks, tables, images)
  |
  v
Structure Mapping (parent-child relationships, reading order)
  |
  v
Structured Output (list of content blocks with metadata)
```

**Content block types:**
```
TextBlock
  text: str              -- the extracted text
  bbox: tuple[int, ...]  -- bounding box on the page
  type: str              -- "header", "body", "footer", "caption"
  page: int              -- page number

TableBlock
  rows: list[list[str]]  -- table data as 2D array
  bbox: tuple[int, ...]  -- bounding box on the page
  page: int              -- page number

ImageBlock
  path: str              -- path to extracted image file
  bbox: tuple[int, ...]  -- bounding box on the page
  caption: str           -- associated caption text
  page: int              -- page number
```

**Why it matters:** Naive text extraction (copy-paste from PDF) destroys
structure. Tables become garbled text. Multi-column layouts get interleaved.
Headers and footers contaminate body text. The Document Parsing Pattern
preserves structure so downstream stages receive clean input.

**Key insight:** Parsing is not a solved problem. Different document types
require different strategies. RAGFlow uses multiple parsers and selects the
best one per document type. This is why the parser is a pluggable component.

---

## Pattern 2: Chunking Pattern

**Intent:** Split parsed documents into semantically meaningful chunks that
are optimal for embedding and retrieval.

**Strategies:**

### Fixed-Size Chunking
```
Input:  "AAAA BBBB CCCC DDDD EEEE"  (25 chars)
Chunk size: 10, Overlap: 3

Output:
  Chunk 1: "AAAA BBBB C"
  Chunk 2: "B CCCC DDD"
  Chunk 3: "C DDDD EEE"
  Chunk 4: "D EEEE"
```
- Simple, fast, predictable
- Problem: splits mid-word, mid-sentence, mid-paragraph

### Semantic Chunking
```
Input:  [Para 1] [Para 2] [Para 3]

Output:
  Chunk 1: [Para 1]
  Chunk 2: [Para 2]
  Chunk 3: [Para 3]
```
- Respects natural boundaries
- Problem: chunk sizes vary wildly

### Document-Aware Chunking
```
Input:  [Header] [Body paragraph] [Table] [Body paragraph]

Output:
  Chunk 1: "[Header]\n[Body paragraph]"
  Chunk 2: "[Table]" (tables always get their own chunk)
  Chunk 3: "[Body paragraph]"
```
- Preserves table integrity
- Groups related content (header + following body)
- Best for structured documents

**Why it matters:** Chunk quality directly determines retrieval quality. A
chunk that splits a table in half is useless. A chunk that contains three
unrelated paragraphs retrieves poorly. The chunking pattern must balance:
- Chunk size (too small = no context, too large = diluted relevance)
- Boundary respect (do not split tables, sentences, or logical units)
- Overlap (adjacent chunks should share some context)

---

## Pattern 3: Embedding Pattern

**Intent:** Convert text chunks into dense vector representations that capture
semantic meaning for similarity-based retrieval.

**Pipeline:**
```
Text chunk
  |
  v
Preprocessing (normalize, truncate to max tokens)
  |
  v
Embedding Model (e.g., text-embedding-ada-002, BGE, E5)
  |
  v
Float vector (768 or 1536 dimensions)
  |
  v
Store with metadata (chunk ID, document ID, position)
```

**Why it matters:** Embeddings are the bridge between human language and
mathematical similarity. Two chunks with similar meanings produce vectors
that are close in embedding space, even if they share no words.

**Key decisions:**
- **Model choice** -- larger models produce better embeddings but cost more
- **Dimension** -- 768 is common, 1536 for OpenAI, 384 for lightweight models
- **Batch processing** -- embed multiple chunks in one API call for efficiency
- **Caching** -- re-embed only when content changes

---

## Pattern 4: Vector Search Pattern

**Intent:** Find the most relevant chunks for a query by comparing vector
representations.

**Pure vector search:**
```
Query -> Embed -> query_vector
                    |
                    v
        Vector Store: [chunk_1_vec, chunk_2_vec, ..., chunk_n_vec]
                    |
                    v
        Compute cosine_similarity(query_vector, each chunk_vector)
                    |
                    v
        Return top-K chunks by similarity score
```

**Hybrid search (vector + keyword):**
```
Query
  |                |
  v                v
Embed query    Tokenize query
  |                |
  v                v
Vector search   BM25 keyword search
  |                |
  v                v
Scores (0-1)    Scores (0-1)
  |                |
  v                v
  Combine: final_score = alpha * vector_score + (1-alpha) * bm25_score
                    |
                    v
            Return top-K by final_score
```

**Why it matters:** Pure vector search is great for semantic similarity but
misses exact matches. If someone searches for "Python 3.11", a vector search
might return chunks about "programming languages" rather than the specific
version. BM25 catches exact keyword matches that vectors miss.

**Reranking:**
```
Top-K from hybrid search
  |
  v
Cross-encoder model (scores each query-chunk pair)
  |
  v
Re-sort by cross-encoder score
  |
  v
Return re-ranked top-K
```

Reranking is expensive (O(K) model calls) but significantly improves
precision. It is the final quality gate before generation.

---

## Pattern 5: RAG Pipeline Pattern

**Intent:** End-to-end pipeline that parses documents, stores knowledge, and
generates grounded answers.

**Full pipeline:**
```
=== Ingestion Phase (offline) ===

Document
  |
  v
Parse (extract text, tables, images)
  |
  v
Chunk (split into embeddable units)
  |
  v
Embed (convert chunks to vectors)
  |
  v
Store (save to vector database)

=== Query Phase (online) ===

User Question
  |
  v
Embed Question
  |
  v
Retrieve (vector + keyword search)
  |
  v
Rerank (cross-encoder)
  |
  v
Build Prompt (question + retrieved chunks)
  |
  v
Generate (LLM produces answer)
  |
  v
Return Answer + Citations
```

**Why it matters:** RAG is a pipeline, not a single step. Each stage has its
own failure modes. A bug in parsing corrupts all downstream stages. A bad
chunking strategy makes retrieval useless. A poor prompt wastes good retrieval.

**Key insight:** The two phases (ingestion and query) are independent.
Ingestion happens once per document. Query happens many times. Optimizing
ingestion quality has multiplicative returns because every query benefits.

---

## Pattern 6: Citation Pattern

**Intent:** Track which retrieved chunks support which claims in the generated
answer.

**Mechanism:**
```
1. Each chunk has a unique ID and source metadata
2. The prompt instructs the LLM to cite sources: [1], [2], etc.
3. The LLM generates an answer with inline citations
4. Post-processing maps [1] -> chunk_id -> document + page number
5. The UI displays citations as clickable links
```

**Why it matters:** Without citations, users cannot verify the answer. RAG
systems that lack citations are black boxes. Citations build trust and enable
fact-checking.

---

## Pattern 7: Feedback Loop Pattern

**Intent:** Use retrieval and generation quality signals to improve the
pipeline over time.

**Signals:**
```
- Retrieval relevance: did the retrieved chunks contain the answer?
- Answer quality: was the generated answer correct and complete?
- User feedback: thumbs up/down on answers
- Query analysis: what types of questions fail most often?
```

**Improvement actions:**
```
- Adjust chunking strategy (smaller/larger chunks)
- Tune hybrid search weights (more vector vs. more keyword)
- Update embedding model
- Improve prompt templates
- Add document preprocessing (better OCR, table extraction)
```

---

## Summary Table

| Pattern | Purpose | Key Insight |
|---------|---------|-------------|
| Document Parsing | Extract structure | Garbage in = garbage out |
| Chunking | Split for embedding | Respect boundaries, balance size |
| Embedding | Text to vectors | Model choice matters |
| Vector Search | Find relevant chunks | Hybrid > pure vector |
| RAG Pipeline | End-to-end flow | Ingestion quality has multiplicative returns |
| Citation | Source tracking | Trust requires verifiability |
| Feedback Loop | Continuous improvement | Measure, analyze, iterate |
