# Project Planning

## Why Planning Matters

The biggest mistake in software development is jumping straight to code. The second biggest is planning so much that you never start. The goal is to plan enough to avoid major mistakes, but not so much that you delay learning.

Planning is where you apply every mental model from the Cognitive Upgrade module:
- **Pattern Recognition** -- What kind of system is this?
- **Abstraction Levels** -- At what level do I plan?
- **Separation of Concerns** -- How do I break this into manageable pieces?
- **Type Safety** -- What are the inputs and outputs of each piece?
- **Error Handling** -- What can go wrong at each stage?

## Step 1: Requirements Gathering

Before writing a single requirement, ask: **Who cares about this project, and what do they need?**

For our knowledge base application, the stakeholders are:

- **End users** -- People who want to ask questions and get answers from documents
- **Admin users** -- People who manage the document library
- **You, the developer** -- You need a system you can understand, maintain, and extend

### Functional Requirements

Write requirements as user stories. Each story should be testable -- you should be able to verify whether it is done.

```
As a user, I can:
- Upload a document (PDF, Markdown, or text file) to the knowledge base
- Ask a question in natural language and receive an answer based on the documents
- See which documents were used to generate the answer (citations)
- View my conversation history

As an admin, I can:
- See all uploaded documents and their processing status
- Delete documents from the knowledge base
- View usage statistics (number of queries, popular topics)
- Manage user accounts (create, deactivate)
```

### Non-Functional Requirements

These are the "-ilities" -- the quality attributes:

```
Performance:
- Document ingestion: process a 100-page PDF in under 60 seconds
- Query response: return an answer within 5 seconds for 95% of queries
- Search: semantic search returns results in under 1 second

Scalability:
- Support 100 concurrent users
- Handle a knowledge base of up to 10,000 documents
- Store up to 1 million text chunks

Security:
- User authentication via email/password
- Users can only access their own documents and conversations
- Admins can access all documents but not user conversations
- All API endpoints require authentication
- Input validation on all user-provided data

Reliability:
- 99% uptime during business hours
- Graceful degradation when the LLM service is unavailable
- Automatic retry for transient failures
```

### Using AI to Refine Requirements

```
I am building an AI-powered knowledge base application. Here are my initial requirements:

[paste requirements above]

Review these requirements:
1. What am I missing?
2. Which requirements are ambiguous and need clarification?
3. Which requirements conflict with each other?
4. What should I cut to reduce scope for a first version?
5. What are the hidden assumptions I am making?
```

AI will often surface requirements you did not consider: What happens when two users upload the same document? What is the maximum file size? How long do you retain conversation history?

## Step 2: Scope Definition

You cannot build everything at once. Scope management is the art of deciding what to build now, what to build later, and what to never build.

### The MoSCoW Method

Categorize every requirement:

- **Must Have** -- The product is useless without these
- **Should Have** -- Important but the product works without them
- **Could Have** -- Nice to have, adds value, but not essential
- **Won't Have** -- Explicitly out of scope for this version

For our project:

```
Must Have (Version 0.1):
- Document upload and processing (PDF, Markdown, text)
- Text chunking and embedding generation
- Semantic search over document chunks
- Conversational query interface (CLI)
- Basic authentication (single user, API key)

Should Have (Version 0.2):
- Web interface for queries
- Multi-user support with email/password auth
- Conversation history
- Citation display (show source documents)

Could Have (Version 0.3):
- Admin panel
- Usage statistics
- Document management (delete, re-process)
- Multiple LLM provider support

Won't Have (for now):
- Real-time collaboration
- Mobile app
- Multi-language support
- Voice interface
```

### Using AI to Challenge Scope

```
Here is my scope definition for version 0.1:

[paste the Must Have list]

Challenge this scope:
1. Is this achievable in [your timeline]?
2. Are there dependencies between these items that affect the order?
3. Is there anything in "Must Have" that could be moved to "Should Have"?
4. Is there anything in "Should Have" that is actually essential for a usable product?
```

## Step 3: Timeline and Phases

Break the project into phases, each delivering working software:

```
Phase 1: Foundation (Days 1-3)
- Project setup (structure, dependencies, configuration)
- Data model design and implementation
- Basic document processing pipeline (upload -> chunk -> store)

Phase 2: Core AI (Days 4-6)
- Embedding generation and storage
- Semantic search implementation
- LLM integration for answer generation
- Basic query interface (CLI)

Phase 3: Web Interface (Days 7-9)
- API design and implementation
- Web frontend (React or Next.js)
- Authentication system
- Conversation UI

Phase 4: Polish and Deploy (Days 10-12)
- Admin features
- Error handling and edge cases
- Docker containerization
- CI/CD pipeline
- Documentation
```

### Realistic Estimation

Software estimation is notoriously difficult. AI can help:

```
I am planning to build [project description].

Here are the phases I have defined:
[paste phases]

For each phase:
1. Estimate the effort in developer-days for a solo developer
2. Identify the highest-risk tasks (most likely to take longer)
3. Suggest which tasks can be parallelized with AI assistance
4. Recommend which tasks to do first (highest learning value, lowest risk)
```

### The Buffer Rule

Whatever timeline AI suggests, add 50%. Not because AI is wrong about the tasks, but because:
- You will encounter unexpected problems
- You will learn things that change your approach
- You will want to refactor when you see how the pieces fit together
- You are learning, not just producing

## Step 4: Technical Decisions

Before implementation, make key technical decisions:

### Language Choices

```
Backend: Python (for AI/ML libraries) or TypeScript (for full-stack consistency)?
Decision: [make a choice and document why]

Frontend: React? Next.js? Plain HTML?
Decision: [make a choice and document why]

Database: PostgreSQL for relational data, plus a vector database for embeddings.
Vector DB options: Pinecone, Weaviate, Qdrant, pgvector
Decision: [make a choice and document why]
```

### Using AI for Technical Decisions

```
I need to choose a vector database for my knowledge base project.

Requirements:
- Must be self-hostable (no cloud-only services)
- Must support [embedding dimensions] vectors
- Must handle [expected scale] documents
- Must integrate with Python
- Should have a simple API

Options I am considering: pgvector, Qdrant, Weaviate, Chroma

Compare these options for my use case. For each:
1. How well does it meet my requirements?
2. What is the operational complexity?
3. What is the performance characteristics?
4. What is the community and ecosystem like?
5. What is the risk of choosing this option?
```

### Document Your Decisions

Create an ADR for each significant decision:

```markdown
# ADR-002: Use Python for Backend, TypeScript for Frontend

## Status: Accepted

## Context
We need to choose languages for the backend and frontend.
Python has the best AI/ML ecosystem (LangChain, LlamaIndex, sentence-transformers).
TypeScript has the best frontend ecosystem (React, Next.js).

## Decision
Use Python for the backend (API server, document processing, AI integration).
Use TypeScript for the frontend (Next.js for the web interface).

## Consequences
- Positive: Best tool for each job, access to both ecosystems
- Negative: Two languages to maintain, two build systems, two dependency managers
- Mitigation: Clear API boundary between frontend and backend; each is independently deployable
```

## Step 5: Risk Assessment

Identify what could go wrong before it does:

```
Technical risks:
1. LLM API costs exceed budget
   Mitigation: Implement caching, use smaller models for simple queries, set usage limits

2. Document processing is too slow for large files
   Mitigation: Async processing, progress tracking, chunked upload

3. Semantic search quality is poor
   Mitigation: Experiment with different embedding models, hybrid search (semantic + keyword)

Operational risks:
4. Single developer gets stuck on a problem
   Mitigation: Use AI as a pair programmer, set time limits on problems before asking for help

5. Scope creep (adding features during implementation)
   Mitigation: Strict adherence to MoSCoW prioritization, defer new ideas to backlog
```

### AI-Assisted Risk Assessment

```
I am planning to build [project description]. Here are the key technical choices:
- [choice 1]
- [choice 2]
- [choice 3]

Identify the top 5 risks for this project. For each risk:
1. How likely is it? (high / medium / low)
2. What is the impact if it occurs? (high / medium / low)
3. What are early warning signs?
4. What is the mitigation strategy?
5. What is the fallback plan if mitigation fails?
```

## Step 6: Project Setup

Before writing any application code, set up the project structure:

```bash
knowledge-base/
  backend/
    src/
      api/            # HTTP routes and controllers
      services/       # Business logic
      models/         # Data models and database schemas
      processing/     # Document processing pipeline
      ai/             # LLM and embedding integration
      config/         # Configuration management
    tests/
    pyproject.toml
    Dockerfile
  frontend/
    src/
      components/     # React components
      pages/          # Next.js pages
      hooks/          # Custom React hooks
      services/       # API client
      types/          # TypeScript type definitions
    package.json
    tsconfig.json
    Dockerfile
  docs/
    architecture/     # ADRs and architecture diagrams
  docker-compose.yml
  .github/
    workflows/        # CI/CD pipelines
  README.md
```

## Using AI for the Entire Planning Process

You can use AI as a planning partner throughout:

```
I am starting a new project: an AI-powered knowledge base.

Help me plan this project step by step:
1. First, help me refine my requirements
2. Then, help me define scope for version 0.1
3. Then, help me create a realistic timeline
4. Then, help me make technical decisions
5. Finally, help me identify risks

I will make the final decisions at each step. Your job is to provide options,
surface issues, and challenge my thinking.
```

This iterative planning conversation with AI produces better plans than planning alone -- because AI catches gaps, suggests alternatives, and forces you to justify your choices.

## Summary

Good planning is not about predicting the future. It is about making informed decisions, identifying risks, and setting yourself up to learn efficiently. Use AI as a planning partner, but remember: the decisions are yours.

Next: [Architecture Design](architecture-design.md)
