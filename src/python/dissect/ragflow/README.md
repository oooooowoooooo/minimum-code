# RAGFlow -- RAG Engine with Deep Document Understanding

## Project Overview

RAGFlow is an open-source RAG (Retrieval-Augmented Generation) engine that
emphasizes deep document understanding. With 30,000+ GitHub stars, it stands
out by focusing on the hardest part of RAG: parsing real-world documents
accurately before feeding them to an LLM.

- **Repository:** https://github.com/infiniflow/ragflow
- **Language:** Python (backend), TypeScript (frontend)
- **Stars:** 30k+
- **License:** Apache 2.0
- **Core Idea:** RAG is only as good as your document parsing. Garbage in,
  garbage out. RAGFlow invests heavily in document understanding to ensure
  high-quality retrieval.

## Why RAGFlow Exists

Most RAG tutorials treat document parsing as an afterthought: split text by
paragraphs, embed, done. This works for clean Markdown files. It fails
spectacularly for:

- **PDFs with tables** -- naive text extraction destroys table structure
- **Scanned documents** -- OCR errors propagate through the pipeline
- **Multi-column layouts** -- text ordering gets scrambled
- **Mixed content** -- images, charts, and text need different handling
- **Legal/financial documents** -- precise structure matters

RAGFlow addresses this by investing in deep document understanding:
layout analysis, table extraction, OCR, and intelligent chunking that
preserves document structure.

## Architecture

### Document Parser

The parser is RAGFlow's crown jewel. It handles:

- **PDF parsing** with layout analysis (detect columns, headers, footers)
- **Table extraction** preserving row/column structure
- **OCR** for scanned documents and images within PDFs
- **Format-specific parsers** for DOCX, HTML, Markdown, Excel, etc.
- **Layout detection** using computer vision models (YOLO-based)

The parser produces structured output: text blocks, tables, images, and
their spatial relationships.

### Chunking

After parsing, documents are split into chunks for embedding. RAGFlow
supports multiple strategies:

- **Fixed-size chunking** -- split by character/token count with overlap
- **Semantic chunking** -- split at natural boundaries (paragraphs, sections)
- **Document-aware chunking** -- respect table boundaries, heading hierarchy
- **Agentic chunking** -- use an LLM to determine optimal split points

Chunk quality directly determines retrieval quality. This is why RAGFlow
invests so heavily here.

### Embedding

Chunks are converted to dense vectors using embedding models:

- Built-in support for multiple embedding providers
- Configurable embedding dimensions
- Batch processing for efficiency
- Caching to avoid re-embedding unchanged content

### Vector Store

Embeddings are stored in a vector database for fast similarity search:

- Built-in Elasticsearch integration (default)
- Support for external vector databases
- Hybrid search: vector similarity + BM25 keyword matching
- Filtering by metadata (document source, date, etc.)

### Retriever

The retriever finds relevant chunks for a given query:

- **Vector search** -- cosine similarity between query embedding and chunk embeddings
- **Keyword search** -- BM25 text matching
- **Hybrid search** -- combine vector + keyword with configurable weights
- **Reranking** -- use a cross-encoder to reorder results for precision
- **Multi-turn** -- consider conversation history for context-aware retrieval

### Generator

The generator produces the final answer:

- Takes retrieved chunks as context
- Generates a grounded response via LLM
- Supports citation tracking (which chunk supports which claim)
- Configurable prompt templates

## Key Design Decisions

### Parse First, Embed Second

RAGFlow's core philosophy: the quality of your RAG system is determined by
your document parsing, not your embedding model or vector database. A perfect
embedding of garbage text is still garbage.

### Hybrid Search by Default

Pure vector search misses exact keyword matches. Pure keyword search misses
semantic similarity. RAGFlow uses hybrid search by default, combining both
approaches for robust retrieval.

### Document Pipeline as DAG

The document processing pipeline is a directed acyclic graph:
```
Parse -> Chunk -> Embed -> Store
```
Each stage is independent and can be configured separately. Re-running a
stage does not require re-running prior stages (results are cached).

## When to Use RAGFlow

- Building RAG systems over complex documents (PDFs, scanned files)
- Need high-accuracy table extraction
- Enterprise document Q&A
- When document quality is more important than agent capabilities

## When NOT to Use RAGFlow

- Simple RAG over clean text files (use Dify or LangChain instead)
- Need multi-agent capabilities (use CrewAI)
- Real-time chatbot without document retrieval
- When you want full control over every pipeline stage

## Key Files in This Module

| File | Purpose |
|------|---------|
| `README.md` | This file -- project overview and architecture |
| `patterns.md` | Core design patterns extracted from RAGFlow |
| `dissect.py` | Simplified reimplementation of RAGFlow's RAG pipeline |

## Learning Objectives

After studying this module, you should be able to:

1. Explain why document parsing is the most critical stage of RAG
2. Implement multiple chunking strategies and understand their tradeoffs
3. Build a vector store with similarity search
4. Construct a complete RAG pipeline from parse to generate
5. Understand hybrid search (vector + keyword) and when to use it
6. Evaluate RAG system quality and identify bottlenecks
