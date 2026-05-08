# AI-Driven Development: The Complete Workflow

## Overview

This chapter presents a complete workflow for building software with AI as a core collaborator at every stage. This is not about AI replacing you. It is about you directing AI to do what it does best, while you focus on what only humans can do.

The workflow has five stages:

```
Problem Definition → Architecture → Implementation → Review → Deploy
```

At each stage, you lead. AI assists. The quality of the result depends on how well you direct the process.

## Stage 1: Problem Definition

### What You Do

Before touching any code or AI tool, define the problem clearly. This is the most important stage. A well-defined problem is half-solved.

### Your Checklist

- **Who has the problem?** (Users, stakeholders, systems)
- **What is the current state?** (What exists now? What is broken or missing?)
- **What is the desired state?** (What does success look like?)
- **What are the constraints?** (Time, budget, team, technology)
- **What are the non-goals?** (What are you explicitly NOT building?)

### How AI Helps

Use AI to refine your problem definition:

```
I am building [feature/system]. Here is my initial problem statement:

[paste your problem statement]

Challenge this definition:
1. What assumptions am I making?
2. What edge cases am I ignoring?
3. What is the simplest version of this problem that still delivers value?
4. What questions should I ask my stakeholders before proceeding?
```

AI will surface assumptions you did not realize you were making. This is valuable.

### Real Example

**Vague problem:** "We need a notification system."

**AI-refined problem:** "Users need to receive real-time alerts when specific events occur in their projects. The current system sends email only, with 5-minute delays. Users want instant delivery via their preferred channel (email, SMS, push, in-app). Constraints: existing email infrastructure must be preserved, team has no mobile development experience, budget is $500/month for external services."

The refined problem is actionable. The vague problem leads to building the wrong thing.

## Stage 2: Architecture

### What You Do

Design the system structure. Define components, their responsibilities, how they communicate, and how data flows. This is where you make the big decisions that are expensive to change later.

### Your Checklist

- **Components** -- What are the major pieces? What does each one do?
- **Data flow** -- How does information move through the system?
- **Technology choices** -- What tools and frameworks? Why?
- **Boundaries** -- Where does one component end and another begin?
- **Failure modes** -- What happens when each component fails?

### How AI Helps

Use AI for design exploration (see [AI-Assisted Architecture](ai-assisted-architecture.md) for detailed templates). The key interaction pattern:

```
You: "Here is the problem. Here are my constraints. Propose 3 approaches."
AI: [proposes 3 approaches with tradeoffs]
You: "Approach 2 is closest. But what about [concern]?"
AI: [addresses concern, refines approach]
You: "Good. Now challenge this design. What are the weaknesses?"
AI: [identifies weaknesses]
You: "I accept weakness 1 (we can live with it). Fix weakness 2 and 3."
AI: [provides mitigations]
```

### Architecture Decision Records

Document every significant decision:

```markdown
# ADR-001: Use WebSocket for Real-Time Notifications

## Status: Accepted

## Context
Users need to receive notifications within 2 seconds. HTTP polling at this
interval creates excessive server load for 50K concurrent users.

## Decision
Use WebSocket connections for real-time delivery. Fall back to SSE for
environments where WebSocket is blocked (corporate firewalls).

## Consequences
- Positive: Sub-second delivery, lower bandwidth than polling
- Negative: Requires connection state management, more complex deployment
- Risk: WebSocket connections consume server memory; need connection limits
```

AI can help draft ADRs:

```
I made this architecture decision: [describe decision and reasoning]

Draft an ADR (Architecture Decision Record) for this decision.
Include: Status, Context, Decision, Consequences (positive and negative), and Risks.
```

## Stage 3: Implementation

### What You Do

Direct AI to write the code, piece by piece. You break the architecture into implementable units and guide AI through each one.

### The Implementation Sequence

Do not build everything at once. Follow this order:

```
1. Data model / types (the contracts)
2. Core business logic (the brain)
3. Data access layer (the persistence)
4. API / interface layer (the face)
5. Integration layer (the connections)
6. Error handling and validation (the safety net)
7. Tests (the verification)
```

### How AI Helps

**For each unit, use this pattern:**

```
Here is the context for what I am building:
- Architecture: [brief description of the system]
- This component's role: [what this specific piece does]
- Inputs: [what it receives]
- Outputs: [what it produces]
- Dependencies: [what it calls and what calls it]
- Error cases: [what can go wrong]

Here are the types/interfaces it works with:
[paste relevant type definitions]

Here is an example of a similar component in this codebase:
[paste a representative example if available]

Implement this component. Follow the patterns shown in the example.
```

**For iterating on AI output:**

```
This is close, but:
1. [specific issue 1]
2. [specific issue 2]

Fix these without changing anything else.
```

### Real Example: Building a User Service

**Step 1 -- Types:**
```
Define the TypeScript types for a user management system.
Users have: id, name, email, role (admin/member/viewer), createdAt, updatedAt.
Include types for: User, CreateUserInput, UpdateUserInput, UserFilter, UserListResult.
Use branded types for IDs. Use Result types for operations that can fail.
```

**Step 2 -- Business Logic:**
```
Now implement the UserService class using these types.
Methods needed:
- createUser(input: CreateUserInput): Promise<Result<User, CreateUserError>>
- getUser(id: UserId): Promise<Result<User, NotFoundError>>
- updateUser(id: UserId, input: UpdateUserInput): Promise<Result<User, UpdateUserError>>
- listUsers(filter: UserFilter): Promise<UserListResult>

Business rules:
- Email must be unique (check before creation)
- Only admins can change user roles
- Users cannot be deleted, only deactivated (set status to inactive)
- Name must be 1-100 characters

Use the repository pattern for data access (inject a UserRepository interface).
```

**Step 3 -- Data Access:**
```
Implement UserRepository using Prisma with PostgreSQL.
Methods: findById, findByEmail, create, update, findByFilter.
Map between Prisma models and domain types.
Handle database errors by wrapping them in domain-specific errors.
```

**Step 4 -- API Layer:**
```
Create Express.js routes for the user service:
- POST /users -- create user
- GET /users/:id -- get user by ID
- PATCH /users/:id -- update user
- GET /users -- list users with filtering and pagination

Use Zod for request validation.
Return appropriate HTTP status codes.
Include request logging middleware.
```

## Stage 4: Review

### What You Do

Review the code AI generated. This is not optional. Every line of AI output needs human verification.

### The Review Process

```
1. Run the code. Does it work?
2. Read the code. Does it make sense?
3. Test edge cases. Does it handle them?
4. Check security. Is it safe?
5. Check performance. Is it efficient enough?
6. Check consistency. Does it match the rest of the codebase?
```

### How AI Helps

Use AI as a first-pass reviewer (see [AI Code Review](ai-code-review.md) for detailed templates):

```
I just implemented [component name]. Here is the code:

[paste code]

Review it for:
1. Bugs I might have missed
2. Edge cases not handled
3. Security issues
4. Performance concerns
5. Consistency with the architecture we designed

Be specific. Point to exact lines.
```

### The Verification Loop

```
AI: "There is a race condition in the user creation flow.
     If two requests with the same email arrive simultaneously,
     both could pass the uniqueness check."

You: "Good catch. How should I fix this?"

AI: "Add a unique constraint on the email column in the database,
     and handle the Prisma unique constraint violation error.
     The check-then-insert pattern is not sufficient for concurrency."

You: "Makes sense. Show me the fix."

AI: [shows fix with database constraint and error handling]

You: [verify the fix, run tests, confirm it works]
```

## Stage 5: Deploy

### What You Do

Prepare the code for production. This includes configuration, infrastructure, monitoring, and documentation.

### Your Checklist

- **Configuration** -- Environment variables, secrets management
- **Infrastructure** -- Servers, databases, networking
- **CI/CD** -- Automated build, test, and deploy pipeline
- **Monitoring** -- Logs, metrics, alerts
- **Documentation** -- API docs, runbooks, architecture diagrams

### How AI Helps

**Dockerfile generation:**
```
Generate a production-ready Dockerfile for this Node.js application:
- Multi-stage build (build stage + production stage)
- Non-root user
- Only production dependencies in final image
- Health check endpoint
- Proper signal handling for graceful shutdown

[paste package.json and any relevant config]
```

**CI/CD pipeline:**
```
Generate a GitHub Actions workflow for this project:
- Trigger on push to main and on pull requests
- Steps: install dependencies, lint, type-check, test, build
- Deploy to [platform] on merge to main
- Cache node_modules between runs
- Environment variables from GitHub secrets
```

**Monitoring setup:**
```
I need to add observability to this service. Generate:
1. Structured logging (JSON format, with request ID, user ID, duration)
2. Key metrics to track (request count, error rate, latency percentiles)
3. Health check endpoint (check database connectivity, external service reachability)
4. Alert rules for critical issues (error rate spike, high latency, service down)

Use [Prometheus/Winston/etc.] conventions.
```

## Putting It All Together: A Day in the Life

Here is what a typical development session looks like:

**Morning -- Planning (30 minutes)**
```
You: Define today's task. Write it down clearly.
You: Ask AI to challenge your plan and surface risks.
You: Adjust plan based on AI's feedback.
```

**Morning -- Architecture (1 hour)**
```
You: Break the task into components.
AI: Help design interfaces between components.
You: Make decisions. Document them in ADRs.
```

**Midday -- Implementation (3 hours)**
```
You: Write types and interfaces.
AI: Generate implementation code, unit by unit.
You: Review each piece. Request fixes for issues.
AI: Apply fixes.
You: Run tests. Verify behavior.
```

**Afternoon -- Review and Polish (2 hours)**
```
AI: Perform automated code review.
You: Evaluate findings. Apply justified fixes.
You: Manual review for design and intent.
AI: Generate missing tests.
You: Verify test coverage and quality.
```

**End of Day -- Deploy Prep (30 minutes)**
```
AI: Generate/update Dockerfile, CI config, documentation.
You: Verify deployment configuration.
You: Run full test suite.
You: Merge and deploy.
```

## Key Principles

1. **You architect, AI implements.** Never let AI make design decisions. Never waste your time on boilerplate.

2. **Small, focused prompts beat large, vague ones.** Ask for one thing at a time. Review it. Then ask for the next thing.

3. **Always provide context.** AI works best when it understands the surrounding code, the business rules, and the constraints.

4. **Iterate, do not batch.** Build in small increments. Review each increment before moving on.

5. **Trust but verify.** AI output needs testing and review. Always.

6. **Document decisions.** Use ADRs, comments, and commit messages to capture the "why" behind choices.

7. **Keep a learning loop.** After each project, reflect: what worked? What did not? How can you direct AI better next time?

## Summary

AI-driven development is not about pressing a button and getting a finished product. It is about a structured collaboration where you bring the judgment, context, and decisions, and AI brings the speed, knowledge, and tirelessness.

Master this workflow, and you will build better software faster than either you or AI could alone.
