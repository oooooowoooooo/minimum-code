<div align="center">

# minimum-code

### AI Era: Write Less Code. Learn Stronger Architecture.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB.svg?logo=python&logoColor=white)](https://python.org)
[![TypeScript 5+](https://img.shields.io/badge/TypeScript-5+-3178C6.svg?logo=typescript&logoColor=white)](https://typescriptlang.org)
[![Next.js 14](https://img.shields.io/badge/Next.js-14-000000.svg?logo=next.js&logoColor=white)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Tests Passing](https://img.shields.io/badge/Tests-160%20passed-brightgreen.svg)](#testing)
[![Knowledge Points](https://img.shields.io/badge/Points-892-orange.svg)](#features)

**An open-source programming education platform for the AI era.**

*892 interactive knowledge points. 4 game types. 10 industrial project dissections. 30 days.*

[Quick Start](#quick-start) · [Why This Matters](#why-this-matters) · [Features](#features) · [Architecture](#architecture) · [Roadmap](#roadmap) · [Contributing](CONTRIBUTING.md)

</div>

---

## Why This Matters

The AI revolution has changed *what* programmers do. Writing boilerplate code is now automated. But the skills that **cannot** be automated — system design, architectural thinking, code quality judgment — are more valuable than ever.

**This project exists to fill that gap.**

Most programming courses teach you syntax. This project teaches you **thinking**. By dissecting 10 of the most popular open-source projects on GitHub (FastAPI, LangChain, Next.js, tRPC, Tauri, and more), you absorb the architectural patterns and design decisions that make these projects successful.

> You don't need to write 10,000 lines of code to become a great engineer.
> You need to **read** 10,000 lines of *great* code.

### Who Is This For?

- **Beginners** who want to fast-track from zero to AI-proficient developer
- **Experienced developers** who want to quickly learn the latest frameworks at source-code level
- **AI practitioners** who want to understand the tools they use daily
- **Career switchers** who need a structured, project-based learning path
- **Anyone** who believes that code quality matters in the age of AI

### What You'll Learn

After completing this 30-day program, you will be able to:

| Skill | Description |
|-------|-------------|
| **Python Mastery** | Variables, types, data structures, OOP, async, modules — the full language |
| **TypeScript Mastery** | Types, interfaces, generics, decorators, async patterns — production-grade TS |
| **Design Patterns** | 8 universal patterns (Builder, Factory, Observer, Strategy, etc.) in both languages |
| **Architecture Thinking** | How to design systems, not just write functions |
| **Project Dissection** | How to read and understand any open-source codebase |
| **AI Tool Proficiency** | Prompt engineering, AI-assisted development, RAG architecture |
| **Code Quality Judgment** | The ability to spot good and bad design decisions in code reviews |
| **Full-Stack Capability** | Build complete applications with FastAPI (Python) + Next.js (TypeScript) |

### What Makes This Different?

| Traditional Courses | minimum-code |
|-------------------|--------------|
| Teach syntax in isolation | Teach through real project dissection |
| "How to use X" | "Why X is designed this way" |
| Passive video watching | Interactive games and quizzes |
| One language at a time | Python + TypeScript side by side |
| No architecture focus | Architecture-first, language-second |
| Outdated examples | Projects active in last 2 years, 25k+ stars |

## Features

| Feature | Description |
|---------|-------------|
| **892 Knowledge Points** | Bite-sized concepts with clear explanations and code examples |
| **4 Interactive Games** | Predict Output · Find Bug · Fill Blank · Code Order |
| **892 Quizzes** | One per knowledge point, instant feedback |
| **12-Week Roadmap** | Structured path from beginner to architect-level thinking |
| **Bilingual** | 中文 / English — switch with one click |
| **10 Project Dissections** | FastAPI, LangChain, CrewAI, Dify, RAGFlow, Next.js, tRPC, Tauri, shadcn/ui, Bun |
| **8 Design Patterns** | Builder, Factory, Observer, Strategy, Middleware, DI, Pipeline, Repository |
| **Zero Database** | JSON files only — clone and run, no setup needed |
| **Keyboard-First** | `j`/`k` navigate, `Enter` toggles, `/` searches |
| **Progress Tracking** | LocalStorage-based, no account required |

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+

### 1. Clone

```bash
git clone https://github.com/oooooowoooooo/minimum-code.git
cd minimum-code
```

### 2. Start Backend

```bash
cd web/backend
pip install fastapi uvicorn
python -m uvicorn main:app --reload --port 8000
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
# Frontend tests (75 tests)
cd web && npm test

# Backend tests (85 tests)
cd web/backend && python -m pytest test_knowledge_api.py -v

# Verify all 892 knowledge points
cd web/backend && python verify_all.py
```

## Architecture

```
minimum-code/
├── web/                              # Web application
│   ├── app/                          # Next.js 14 App Router
│   │   ├── page.tsx                  # Home — stats + knowledge entry
│   │   ├── knowledge/page.tsx        # Knowledge browser — search, filter, games
│   │   ├── learn/[id]/page.tsx       # Module learning — sections + quiz
│   │   └── module/[id]/page.tsx      # Module detail page
│   ├── components/games/             # 4 interactive game components
│   │   ├── PredictOutput.tsx         # "What will this code output?"
│   │   ├── FindBug.tsx               # "Click the buggy line"
│   │   ├── FillBlank.tsx             # "Complete the missing code"
│   │   └── CodeOrder.tsx             # "Put lines in correct order"
│   ├── lib/
│   │   ├── i18n.ts                   # Bilingual system (zh/en)
│   │   ├── api.ts                    # API client
│   │   └── progress.ts               # LocalStorage progress tracking
│   └── backend/                      # FastAPI server
│       ├── main.py                   # API server
│       ├── data/knowledge_points.json  # 892 knowledge points
│       └── test_knowledge_api.py     # 85 API tests
├── src/                              # Course source files
│   ├── python/                       # Python fundamentals + 5 project dissections
│   ├── typescript/                   # TypeScript fundamentals + 5 project dissections
│   └── patterns/                     # 8 universal design patterns
├── tests/                            # 212 Python/TS unit tests
└── docs/                             # Guides: cognitive, AI mastery, practice
```

## Roadmap

| Week | Focus | What You'll Learn |
|------|-------|-------------------|
| 1–2 | Python Fundamentals | Variables, types, data structures, control flow, functions, classes, async |
| 3–4 | TypeScript Fundamentals | Types, interfaces, functions, async, decorators, modules |
| 5–6 | Design Patterns | Builder, Factory, Observer, Strategy, Middleware, DI, Pipeline, Repository |
| 7–8 | Python Project Dissection | FastAPI, LangChain, CrewAI, Dify, RAGFlow |
| 9–10 | TypeScript Project Dissection | Next.js, tRPC, Tauri, shadcn/ui, Bun |
| 11–12 | AI Mastery + Capstone | Prompt engineering, AI-assisted architecture, build your own project |

## Testing

```bash
# All tests
cd web && npm test                    # 75 frontend tests
cd web/backend && python -m pytest   # 85 backend tests
cd web/backend && python verify_all.py  # Data integrity check
```

| Suite | Count | Status |
|-------|-------|--------|
| Frontend (Vitest) | 75 | Passing |
| Backend (pytest) | 85 | Passing |
| Python course | 212 | Passing |
| Data verification | 892 points | Passing |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, React 18, Tailwind CSS |
| Backend | FastAPI, uvicorn |
| Data | JSON files (no database required) |
| Testing | Vitest (frontend), pytest (backend) |
| Package | npm (frontend), pip (backend) |

## Project Selection Criteria

Every project we dissect meets these standards:

1. **25k+ GitHub Stars** — proven community value
2. **Active in last 2 years** — represents current industry practices
3. **Architecturally rich** — contains design patterns worth studying
4. **High code quality** — written by top-tier engineers

## Contributing

We welcome contributions of all kinds:

- Add new knowledge points
- Fix bugs or improve existing content
- Improve documentation
- Add new game types or project dissections

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## License

[MIT](LICENSE) — free for personal and commercial use.

---

<div align="center">

**If this project helped you learn something new, give it a star.**

It helps others find it, and it keeps us motivated to add more content.

*"Programs must be written for people to read, and only incidentally for machines to execute."*
— Harold Abelson, *Structure and Interpretation of Computer Programs*

</div>
