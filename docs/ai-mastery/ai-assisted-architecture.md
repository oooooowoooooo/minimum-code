# AI-Assisted Architecture

## What AI Can and Cannot Do for Architecture

AI cannot design your system. But it can be an exceptional thinking partner for exploring design options, identifying risks, and stress-testing your decisions.

Think of AI as a senior engineer you can brainstorm with at any time, who has seen thousands of systems and can instantly recall patterns, tradeoffs, and failure modes. The final decision is still yours.

## The Right Mindset

Architecture is about tradeoffs, not solutions. There is no "correct" architecture -- there are architectures that optimize for different constraints. AI helps you enumerate and evaluate those tradeoffs faster than you could alone.

## Prompt Template: Initial Design Exploration

Use this when starting a new system or major feature:

```
I am designing [system/feature description].

Context:
- Team size: [number]
- Expected scale: [users/requests/data volume]
- Timeline: [duration]
- Key constraint: [the one thing that cannot be compromised]
- Tech stack: [current technologies]

Before diving into implementation, I need to explore the design space.

Please:
1. Propose 3 distinct architectural approaches
2. For each approach, list:
   - Key components and their responsibilities
   - Data flow (how information moves through the system)
   - Strengths (what this approach handles well)
   - Weaknesses (where this approach struggles)
   - Operational complexity (deployment, monitoring, debugging)
3. For the approach that best fits my constraints, identify the top 3 risks
4. Suggest mitigation strategies for each risk
```

### Example Usage

```
I am designing a real-time notification system.

Context:
- Team size: 3 developers
- Expected scale: 50K concurrent users, 100K notifications/hour
- Timeline: 6 weeks
- Key constraint: notifications must arrive within 2 seconds
- Tech stack: TypeScript, PostgreSQL, Redis, deployed on AWS

Before diving into implementation, I need to explore the design space.

Please:
1. Propose 3 distinct architectural approaches
2. For each approach, list:
   - Key components and their responsibilities
   - Data flow
   - Strengths
   - Weaknesses
   - Operational complexity
3. For the approach that best fits my constraints, identify the top 3 risks
4. Suggest mitigation strategies for each risk
```

## Prompt Template: Design Critique

Use this when you already have a design and want it challenged:

```
Here is my current architecture design:

[describe your architecture: components, data flow, technology choices]

I want you to challenge this design. Be critical. Specifically:

1. What are the single points of failure?
2. Where will this break first as scale increases?
3. What happens when [specific component] goes down?
4. Are there any circular dependencies or tight couplings?
5. What would a senior engineer with 15 years of experience criticize?
6. What would you change if the team doubled in size? What if it halved?
```

## Prompt Template: Technology Selection

```
I need to choose a [database/message queue/cache/etc.] for my project.

Requirements:
- [requirement 1]
- [requirement 2]
- [requirement 3]

Constraints:
- [constraint 1, e.g., must run on a single server]
- [constraint 2, e.g., budget for managed service is $X/month]

Compare the top 3 options for my use case. For each option:
1. How well does it meet my requirements?
2. What is the operational burden? (setup, maintenance, monitoring)
3. What is the learning curve for a team that has not used it?
4. What are the failure modes?
5. When would you NOT choose this option?

Recommend one and explain why.
```

## Prompt Template: Data Model Design

```
I am building [system description].

The core entities are:
- [Entity 1]: [brief description and key attributes]
- [Entity 2]: [brief description and key attributes]
- [Entity 3]: [brief description and key attributes]

Key relationships:
- [Entity 1] has many [Entity 2]
- [Entity 2] belongs to [Entity 3]

Key queries I need to support:
- [query 1]
- [query 2]
- [query 3]

Design the data model. For each decision:
1. Explain why you chose that structure
2. Identify the tradeoffs of that choice
3. Note any queries that will be expensive and suggest optimizations

Use [PostgreSQL/MongoDB/etc.] conventions.
```

## Prompt Template: API Design

```
I need to design the API for [feature/system].

Users of this API:
- [type of consumer, e.g., mobile app, web frontend, third-party integrators]

Operations needed:
- [operation 1 with brief description]
- [operation 2 with brief description]
- [operation 3 with brief description]

Design the API endpoints following REST/GraphQL conventions. For each endpoint:
1. Method, path, and purpose
2. Request format (headers, body, query params)
3. Response format (success and error cases)
4. Authentication and authorization requirements
5. Rate limiting considerations
6. Pagination strategy (if applicable)

Flag any design decisions where there are meaningful tradeoffs.
```

## How to Evaluate AI Architecture Suggestions

AI architecture suggestions are starting points, not final decisions. Evaluate them against these criteria:

### 1. Does it solve YOUR problem, or a generic problem?

AI tends to suggest "best practice" architectures that assume ideal conditions. Your conditions are not ideal. Push back: "That works at scale, but my team is 3 people and my budget is $200/month. Simplify."

### 2. What is the operational cost?

Every architectural choice has an operational cost: another service to monitor, another database to back up, another failure mode to handle. AI often suggests adding components without accounting for the operational burden. Ask: "What does my team need to do to keep this running at 3 AM?"

### 3. Does it match your team's skills?

A microservices architecture with Kubernetes and service mesh is elegant -- but if your team has never operated containers, it is a disaster waiting to happen. Tell AI your team's actual skill level.

### 4. Can you start simple and evolve?

The best architecture is one that starts simple and can evolve as needs change. Ask AI: "What is the simplest version of this that works? What are the upgrade paths when I need more scale?"

### 5. What are the failure modes?

Ask AI specifically: "When this system fails, how does it fail? What does the user see? What does the operator see? How long does recovery take?"

## Real-World Example: Designing a Content Management System

Here is how a conversation with AI might flow:

**Round 1 -- Exploration:**
"I need a CMS for a blog platform. Team of 2, expected 10K articles, 100K monthly visitors. What are my architectural options?"

**Round 2 -- Narrowing:**
"I like the API-first approach. But I want to avoid a separate admin frontend. Can the API serve both the admin and the public site? What are the tradeoffs?"

**Round 3 -- Data Model:**
"Design the data model for articles, categories, tags, and authors. I need to support: full-text search, versioning, and scheduled publishing."

**Round 4 -- API Design:**
"Design the REST API. Focus on the article CRUD operations. Include pagination, filtering by category/tag, and full-text search."

**Round 5 -- Stress Testing:**
"Challenge this design. What breaks at 10x the traffic? What if I need to add multi-language support later? What if I need to support images and videos?"

**Round 6 -- Implementation Plan:**
"Given all the decisions we have made, create an implementation plan. Break it into phases that each deliver working functionality."

This iterative approach uses AI as a sounding board at each stage. The human makes the decisions. AI provides options, analysis, and challenges.

## Red Flags in AI Architecture Suggestions

Watch out for these patterns:

**Over-engineering.** AI suggests event sourcing, CQRS, and a message queue for a CRUD app. If your system does not need the complexity, do not add it.

**Resume-driven architecture.** AI suggests trendy technologies (Kubernetes, GraphQL, microservices) without justifying why they fit your constraints. Make it justify every choice.

**Ignoring the boring option.** AI sometimes overlooks simple, proven solutions in favor of more interesting ones. Explicitly ask: "What is the simplest approach that works?"

**Missing the human factor.** AI designs systems for machines, not for the humans who operate them. Ask: "How does a developer debug this at 2 AM? How does the ops team monitor this?"

## Summary

Use AI as a thinking partner, not an architect. Your job is to ask the right questions, evaluate tradeoffs, and make decisions. AI's job is to provide options, surface risks, and challenge your assumptions.

The best architecture conversations with AI are iterative: explore, narrow, challenge, decide, implement. Never accept the first suggestion. Always push back. Always ask "what could go wrong?"
