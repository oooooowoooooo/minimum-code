<div align="center">

# minimum-code

**AI App Engineer Minimum Engineering Capability Training System.**

Not syntax tutorials — an engineering training ground for AI app development jobs.
From LLM API calls, FastAPI services, RAG retrieval, Agent tool calling, to Docker deployment, CI testing, and interview expression.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB.svg?logo=python&logoColor=white)](https://python.org)
[![TypeScript 5+](https://img.shields.io/badge/TypeScript-5+-3178C6.svg?logo=typescript&logoColor=white)](https://typescriptlang.org)
[![Next.js 14](https://img.shields.io/badge/Next.js-14-000000.svg?logo=next.js&logoColor=white)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)

[Quick Start](#quick-start) · [Why This Matters](#why-this-matters) · [Six Modules](#six-capability-modules) · [Architecture](#architecture) · [Contributing](CONTRIBUTING.md)

</div>

---

## Why This Matters

Most AI tutorials teach you to write `openai.ChatCompletion.create(...)`.
None teach you what happens when the API times out, returns a 500, or gives a malformed response.

This project fills that gap: **the minimum engineering code you need to actually ship AI applications.**

The industry does not need more people who can copy-paste an LLM API call from a blog post. It needs engineers who understand retry logic, schema validation, dependency injection, containerization, and how to verify that their code actually works — not just that it runs once on their laptop.

> You don't get hired for knowing the syntax.
> You get hired for knowing what to do when things go wrong.

---

## Who This Is For

| Who | Why This Helps |
|-----|----------------|
| **Aspiring AI Application Developers** with incomplete engineering skills | Fill the gap between "I can call an API" and "I can ship a service" |
| **Backend engineers** transitioning to AI application development | Map your existing skills to LLM-specific patterns (streaming, retries, token limits) |
| **CS students** preparing for AI application developer interviews | Build a portfolio of verified, runnable engineering labs — not toy scripts |
| **Self-taught programmers** who can write code but can't ship production systems | Learn the engineering layer that tutorials skip: testing, deployment, observability |

---

## Core Training Loop

Every module follows the same five-step loop. This is not a passive course. You write code, it gets verified, and you learn to explain it.

```
 1. Capability Assessment  -->  identify your engineering skill gaps
 2. Minimum Code Patterns  -->  understand mechanisms through shortest possible code
 3. Engineering Labs       -->  complete runnable tasks with real acceptance criteria
 4. Auto-Verification      -->  pytest / vitest / schema validation proves your code works
 5. Interview Expression   -->  convert code capability into project narrative
```

**Step 1** tells you what you don't know.
**Step 2** shows you the minimum viable implementation.
**Step 3** makes you build it yourself.
**Step 4** removes all ambiguity — your code either passes or it doesn't.
**Step 5** teaches you to articulate your decisions under pressure.

---

## Six Capability Modules

Each module targets a specific engineering capability required for AI application development roles. Labs are not exercises — they are production-like tasks with real acceptance criteria.

| Module | Training Goal | Lab Count |
|--------|--------------|-----------|
| **Python Engineering** | Packages, modules, types, async, config, exceptions | 1 |
| **FastAPI Services** | API design, Pydantic validation, dependency injection, middleware, SSE | 1 |
| **LLM API Client** | OpenAI-compatible API, timeout handling, retry logic, error classification | 1 |
| **RAG System** | Document parsing, chunking, embedding, retrieval, rerank, evaluation | 1 |
| **Agent Engineering** | Tool calling, skill registration, planner, executor, guardrails | 1 |
| **Deployment & Quality** | Docker, CI pipelines, structured logging, config management, testing, observability | 1 |

### What makes these labs different?

- **No hand-holding.** You get a spec and acceptance criteria, not a step-by-step tutorial.
- **Auto-verified.** Every lab has a test suite. Your code passes the tests or it doesn't ship.
- **Interview-ready.** Every lab includes interview prompts — explain your design decisions as you would in a technical screen.

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+

### 1. Clone

```bash
git clone https://github.com/your-username/minimum-code.git
cd minimum-code
```

### 2. Start Backend

```bash
cd web/backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Backend runs at **http://localhost:8000**

### 3. Start Frontend

```bash
# New terminal
cd web
npm install
npm run dev
```

Open **http://localhost:3000** — you're in.

### 4. Run Tests

```bash
# Backend
cd web/backend && pytest tests/ -v

# Frontend
cd web && npm test

# Full verification
python verify_all.py
```

---

## Project Structure

```
minimum-code/
├── web/                                  # Web application
│   ├── app/                              # Next.js 14 App Router
│   │   ├── page.tsx                      # Home — dashboard + module entry
│   │   ├── assessment/                   # Capability assessment flow
│   │   ├── knowledge/                    # Knowledge browser — search, filter, games
│   │   ├── learn/[id]/                   # Module learning — sections + quiz
│   │   ├── module/[id]/                  # Module detail page
│   │   ├── fundamentals/                 # Python & TypeScript fundamentals
│   │   ├── patterns/                     # Design pattern modules
│   │   ├── dissect/                      # Project dissection (FastAPI, LangChain, etc.)
│   │   ├── practice/                     # Engineering lab workspace
│   │   └── ai-mastery/                   # AI-specific capability training
│   ├── components/
│   │   └── games/                        # 4 interactive game components
│   │       ├── PredictOutput.tsx         # "What will this code output?"
│   │       ├── FindBug.tsx               # "Click the buggy line"
│   │       ├── FillBlank.tsx             # "Complete the missing code"
│   │       └── CodeOrder.tsx             # "Put lines in correct order"
│   ├── lib/
│   │   ├── i18n.ts                       # Bilingual system (zh/en)
│   │   ├── api.ts                        # API client
│   │   └── progress.ts                   # LocalStorage progress tracking
│   └── backend/                          # FastAPI server
│       ├── main.py                       # API server
│       ├── data/                         # Knowledge points (JSON)
│       └── verify_all.py                 # Data integrity verification
├── src/                                  # Course source files
│   ├── python/                           # Python fundamentals + project dissections
│   ├── typescript/                       # TypeScript fundamentals + project dissections
│   └── patterns/                         # 8 universal design patterns
├── tests/                                # Unit tests (Python + TypeScript)
├── docs/                                 # Guides: cognitive, AI mastery, practice
├── labs/                                 # Engineering lab definitions + acceptance tests
└── tracks/                               # Capability module tracks
```

---

## Architecture

```
┌─────────────┐     HTTP/JSON      ┌─────────────┐     Service Layer    ┌──────────────┐
│   Frontend   │ ─────────────────▶ │   FastAPI    │ ──────────────────▶ │  Repository   │
│  (Next.js)   │ ◀───────────────── │   Backend    │ ◀────────────────── │   (JSON)      │
└─────────────┘     SSE / REST     └─────────────┘                     └──────────────┘
       │                                   │
       │                                   │
       ▼                                   ▼
  ┌──────────┐                      ┌──────────────┐
  │ Vitest   │                      │   pytest     │
  │ (75 tests)│                     │  (85 tests)  │
  └──────────┘                      └──────────────┘
```

**Data flow:** Frontend sends requests via REST/SSE to the FastAPI backend. The backend processes requests through a service layer and reads/writes JSON data files. No database required — clone and run.

---

## What You'll Be Able To Do After Completing All Labs

- **Confidently call any LLM API** with proper error handling, timeout configuration, and retry logic — not just the happy path
- **Build a FastAPI service** with Pydantic schema validation, dependency injection, and middleware — production-grade, not tutorial-grade
- **Implement a RAG pipeline** with document parsing, chunking strategies, embedding generation, retrieval, and reranking
- **Create an Agent** with tool calling, skill registration, a planner-executor loop, and safety guardrails
- **Deploy with Docker** and verify with CI — your code works in a container, not just on your machine
- **Articulate your engineering decisions** in technical interviews — explain the why, not just the what

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, React 18, Tailwind CSS, Vitest |
| Backend | FastAPI, uvicorn, pytest |
| Data | JSON files (zero database — clone and run) |
| Testing | Vitest (frontend), pytest (backend), schema validation |
| Deployment | Docker, CI pipelines |

---

## Contributing

We welcome contributions of all kinds:

- Add new knowledge points or engineering labs
- Fix bugs or improve existing content
- Improve documentation
- Add new capability modules or game types

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## License

[MIT](LICENSE) — free for personal and commercial use.

---

<div align="center">

**Star this repo if it helps you ship your first production AI application.**

*"The minimum code is not the least code. It is the code that teaches you the most."*

</div>
