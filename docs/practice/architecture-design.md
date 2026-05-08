# Architecture Design

## What Architecture Is

Architecture is the set of decisions that are hard to change later. Choosing a database is architecture. Choosing a function name is not. The goal is to get the hard decisions right and leave the easy decisions flexible.

Architecture is not about diagrams and buzzwords. It is about answering three questions:
1. What are the pieces?
2. How do they communicate?
3. What are the rules?

## The System Overview

Our knowledge base application has these major components:

```
                    +-----------------+
                    |   Web Frontend  |
                    |   (Next.js)     |
                    +--------+--------+
                             |
                    +--------v--------+
                    |   API Server    |
                    |   (FastAPI)     |
                    +--------+--------+
                             |
              +--------------+--------------+
              |              |              |
     +--------v---+  +------v------+  +----v--------+
     | Document   |  | Query       |  | User        |
     | Service    |  | Service     |  | Service     |
     +--------+---+  +------+------+  +----+--------+
              |              |              |
     +--------v---+  +------v------+  +----v--------+
     | Document   |  | Vector      |  | User        |
     | Store      |  | Store       |  | Database    |
     | (files)    |  | (pgvector)  |  | (PostgreSQL)|
     +------------+  +-------------+  +-------------+
```

## Component Responsibilities

### API Server (FastAPI)

The API server is the entry point. It handles HTTP requests, authentication, and routing. It does NOT contain business logic -- it delegates to services.

```
Responsibilities:
- Route HTTP requests to the appropriate service
- Validate request data (using Pydantic models)
- Authenticate requests (JWT tokens)
- Serialize responses
- Handle CORS, rate limiting, and error formatting
```

### Document Service

Handles document lifecycle: upload, processing, storage, and deletion.

```
Responsibilities:
- Accept file uploads
- Extract text from different file formats (PDF, Markdown, text)
- Chunk text into appropriate segments
- Generate embeddings for each chunk
- Store document metadata and chunks
- Track processing status
```

### Query Service

Handles the AI-powered question-answering pipeline.

```
Responsibilities:
- Accept natural language queries
- Generate query embedding
- Find relevant document chunks (semantic search)
- Construct prompt with context
- Call LLM to generate answer
- Return answer with citations
- Store conversation history
```

### User Service

Handles authentication, authorization, and user management.

```
Responsibilities:
- User registration and login
- JWT token generation and validation
- Password hashing and verification
- User profile management
- Role-based access control (admin vs regular user)
```

## Data Model

### Core Entities

```python
# User
class User:
    id: UUID
    email: str              # unique, indexed
    name: str
    hashed_password: str
    role: UserRole          # admin | member
    created_at: datetime
    updated_at: datetime
    is_active: bool

# Document
class Document:
    id: UUID
    user_id: UUID           # FK -> User, indexed
    title: str
    filename: str
    file_type: FileType     # pdf | markdown | text
    file_size: int          # bytes
    status: DocumentStatus  # uploading | processing | ready | failed
    chunk_count: int
    created_at: datetime
    updated_at: datetime

# DocumentChunk
class DocumentChunk:
    id: UUID
    document_id: UUID       # FK -> Document, indexed
    chunk_index: int        # order within document
    content: str            # the actual text
    embedding: vector(1536) # embedding vector (dimension depends on model)
    metadata: JSON          # page number, section title, etc.

# Conversation
class Conversation:
    id: UUID
    user_id: UUID           # FK -> User, indexed
    title: str
    created_at: datetime
    updated_at: datetime

# Message
class Message:
    id: UUID
    conversation_id: UUID   # FK -> Conversation, indexed
    role: MessageRole       # user | assistant
    content: str
    citations: JSON         # list of {document_id, chunk_id, text_snippet}
    created_at: datetime
```

### Database Schema Decisions

**Why PostgreSQL with pgvector?**
- Single database for both relational data and vector search
- Proven, reliable, well-documented
- pgvector is mature and performant for our scale
- Avoids the operational cost of running a separate vector database

**Why store embeddings in the database instead of a separate vector store?**
- Simpler architecture (one database instead of two)
- Transactional consistency (document and its chunks are in the same database)
- At our scale (up to 1M vectors), pgvector performs well
- Tradeoff: at much larger scale (10M+ vectors), a dedicated vector database would be better

**Why store file content in chunks instead of the original file?**
- Semantic search operates on chunks, not whole documents
- Chunks are the unit of retrieval
- Original files can be re-processed if chunking strategy changes
- Store original files separately (filesystem or object storage) for reference

## API Design

### Endpoints

```
Authentication:
POST   /api/auth/register     - Create account
POST   /api/auth/login        - Get JWT token
POST   /api/auth/refresh      - Refresh JWT token

Documents:
POST   /api/documents         - Upload document
GET    /api/documents         - List user's documents
GET    /api/documents/:id     - Get document details
DELETE /api/documents/:id     - Delete document and its chunks

Query:
POST   /api/query             - Ask a question
GET    /api/conversations     - List conversations
GET    /api/conversations/:id - Get conversation with messages

Admin:
GET    /api/admin/documents   - List all documents
GET    /api/admin/users       - List all users
GET    /api/admin/stats       - Usage statistics
DELETE /api/admin/users/:id   - Deactivate user
```

### Request/Response Examples

```
POST /api/query
Request:
{
    "question": "What is the company's refund policy?",
    "conversation_id": "optional-existing-conversation-id"
}

Response:
{
    "answer": "According to the company policy document, refunds...",
    "citations": [
        {
            "document_id": "abc-123",
            "document_title": "Company Policy 2024",
            "chunk_text": "Customers may request a refund within 30 days...",
            "relevance_score": 0.92
        }
    ],
    "conversation_id": "conv-456"
}
```

## The Processing Pipeline

Document processing is the most complex part of the system. Here is the pipeline:

```
Upload -> Validate -> Extract Text -> Chunk -> Embed -> Store -> Index
```

### Step 1: Upload and Validate

```
Input: File upload (multipart form data)
Validation:
- File type is allowed (PDF, MD, TXT)
- File size is under limit (50MB)
- User has not exceeded their document limit
Output: Document record with status "uploading"
```

### Step 2: Extract Text

```
Input: File on disk
Processing:
- PDF: Use PyMuPDF or pdfplumber to extract text
- Markdown: Parse and extract text (preserve structure)
- Text: Read file content
Output: Raw text with metadata (page numbers for PDF)
```

### Step 3: Chunk Text

```
Input: Raw text
Strategy: Recursive character splitting
- Split by paragraphs first
- If a paragraph is too long, split by sentences
- If a sentence is too long, split by words
- Maintain overlap between chunks (for context continuity)
Parameters:
- Chunk size: 500 tokens (approximately 2000 characters)
- Overlap: 50 tokens (approximately 200 characters)
Output: List of text chunks with metadata
```

### Step 4: Generate Embeddings

```
Input: List of text chunks
Processing:
- Call embedding API (e.g., OpenAI text-embedding-3-small)
- Batch requests (send multiple chunks per API call)
- Handle rate limits and errors
Output: List of vectors (one per chunk)
```

### Step 5: Store and Index

```
Input: Chunks with embeddings
Processing:
- Insert chunks into document_chunks table
- Update document status to "ready"
- Update chunk_count on document
Output: Document is searchable
```

### Error Handling in the Pipeline

```
Each step can fail. The pipeline handles failures gracefully:

- Upload fails: Return error to user, no database record created
- Text extraction fails: Mark document as "failed", log error
- Chunking fails: Mark document as "failed", log error
- Embedding fails: Retry up to 3 times with exponential backoff
  - If all retries fail: Mark document as "failed", keep extracted text
  - User can re-process the document later
- Storage fails: Retry once, then mark as "failed"

Failed documents can be re-processed without re-uploading.
```

## Security Architecture

### Authentication Flow

```
1. User registers with email and password
2. Password is hashed with bcrypt (cost factor 12)
3. User logs in, receives JWT access token (15 min expiry) and refresh token (7 day expiry)
4. Access token is sent in Authorization header for each request
5. Refresh token is used to get new access tokens
6. Tokens are stored in httpOnly cookies (web) or localStorage (API clients)
```

### Authorization Rules

```
- Regular users can:
  - Upload, view, and delete their own documents
  - Query their own documents
  - View their own conversations

- Admin users can additionally:
  - View and delete any document
  - View all users
  - Deactivate user accounts
  - View usage statistics

- Unauthenticated users can:
  - Register
  - Login
  - Nothing else
```

### Input Validation

```
Every API input is validated:
- Request body: Pydantic models with strict type checking
- Path parameters: UUID format validation
- Query parameters: Type and range validation
- File uploads: Type, size, and content validation
- SQL injection: Use parameterized queries (ORM handles this)
- XSS: Sanitize all user input before rendering
```

## Architecture Decision Records

Create an ADR for each significant decision. Here are the key ones for this project:

### ADR-003: Use FastAPI for Backend

```
## Context
Need a Python web framework that supports async, has good OpenAPI support,
and is modern and well-maintained.

## Decision
Use FastAPI.

## Consequences
- Positive: Async support, automatic OpenAPI docs, Pydantic integration, fast
- Negative: Smaller ecosystem than Django, less built-in functionality
- Tradeoff: We build more from scratch, but get a cleaner, faster API
```

### ADR-004: Use pgvector Instead of Dedicated Vector Database

```
## Context
Need to store and search document embeddings. Options: pgvector, Qdrant,
Weaviate, Pinecone.

## Decision
Use pgvector (PostgreSQL extension).

## Consequences
- Positive: Single database, transactional consistency, simpler operations
- Negative: Less optimized than dedicated vector DBs at very large scale
- Mitigation: Monitor query performance; migrate to dedicated vector DB
  if we exceed 5M vectors or need sub-10ms search latency
```

### ADR-005: Use JWT for Authentication

```
## Context
Need stateless authentication for the API server. Options: JWT, session-based,
API keys.

## Decision
Use JWT with short-lived access tokens and longer-lived refresh tokens.

## Consequences
- Positive: Stateless, works across services, no server-side session storage
- Negative: Tokens cannot be revoked (must wait for expiry)
- Mitigation: Short access token expiry (15 min), refresh token rotation
```

## Using AI for Architecture Design

Use these prompts to work through the architecture with AI:

### Exploring Alternatives

```
I am designing a document processing pipeline. My current approach is
synchronous: upload -> process -> return. But processing takes 30-60 seconds
for large documents.

What are the alternatives? Compare:
1. Synchronous processing (current)
2. Async processing with a task queue (Celery/RQ)
3. Event-driven processing (message queue + workers)

For each approach, evaluate: complexity, user experience, scalability, and
operational cost.
```

### Stress Testing the Design

```
Here is my current architecture:
[paste architecture description]

Challenge this design at 10x scale (100K documents, 10K daily active users):
1. Where does it break first?
2. What is the cheapest fix for each bottleneck?
3. What would need to be completely redesigned?
```

### Validating Decisions

```
I chose [technology/approach] for [purpose]. My reasoning is [reasoning].

Is my reasoning sound? What am I not considering? What would change your
recommendation?
```

## Summary

Architecture is about making the decisions that are expensive to change. For our knowledge base, the key decisions are:

1. **PostgreSQL with pgvector** -- single database for simplicity
2. **FastAPI** -- modern, fast, async Python framework
3. **Next.js** -- full-stack React framework for the frontend
4. **JWT authentication** -- stateless, scalable
5. **Async document processing** -- good user experience for slow operations

Each decision has tradeoffs. Document them in ADRs. Revisit them when constraints change.

Next: [Implementation](implementation.md)
