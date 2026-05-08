# Prompt Engineering for Code Generation

## Why Prompt Engineering Matters

The same AI model can produce brilliant code or garbage code depending on the prompt. Prompt engineering is not about tricks or jailbreaks -- it is about clear communication of intent, constraints, and context.

Think of it this way: if you gave the same task to two human developers, one with a clear spec and one with a vague request, who would produce better code? The AI is no different.

## The Anatomy of a Good Code Prompt

A high-quality code prompt has five components:

```
1. Context     -- What is the broader system?
2. Task         -- What specific thing should be built?
3. Constraints  -- What are the rules and limitations?
4. Examples     -- What does good output look like?
5. Format       -- How should the output be structured?
```

Not every prompt needs all five. But when the output is not what you wanted, check which component you omitted.

## System Prompts

The system prompt sets the stage for the entire conversation. For code generation, a good system prompt establishes:

### The Role

```
You are a senior software engineer working on a TypeScript backend service.
You follow these principles:
- Prefer explicit over implicit
- Use Result types for error handling
- Write self-documenting code with clear naming
- Keep functions under 30 lines
- Always handle edge cases
```

### The Codebase Context

```
Our project uses:
- TypeScript 5.x with strict mode
- Express.js for HTTP
- Prisma for database access
- Zod for validation
- Vitest for testing
- pnpm as package manager
```

### The Style Guide

```
Code style requirements:
- Use const by default, let only when reassignment is needed
- Never use var
- Prefer named exports over default exports
- Use async/await over .then() chains
- Errors should be thrown as custom Error subclasses
```

A well-crafted system prompt eliminates 80% of style inconsistencies and tooling mismatches in AI output.

## Few-Shot Examples

Few-shot examples are the most underused technique in code prompting. Showing AI what good output looks like dramatically improves its generation quality.

### Template Pattern

```
Here is an example of how our service layer functions should look:

[TYPES]
type UserId = string & { readonly __brand: "UserId" };
type User = { id: UserId; name: string; email: string; createdAt: Date };
type CreateUserInput = { name: string; email: string };
type ServiceResult<T> = { ok: true; data: T } | { ok: false; error: string };

[EXAMPLE FUNCTION]
export async function createUser(input: CreateUserInput): Promise<ServiceResult<User>> {
    const existing = await db.user.findByEmail(input.email);
    if (existing) {
        return { ok: false, error: "Email already registered" };
    }
    const user = await db.user.create({
        data: { ...input, id: generateId() },
    });
    return { ok: true, data: user };
}

Now write a function `getUserById` that fetches a user by ID and returns ServiceResult<User>.
Return { ok: false, error: "User not found" } if the ID does not exist.
```

### Why This Works

The AI now knows:
- The exact type signatures to use
- The error handling pattern (ServiceResult)
- The database access pattern (db.user.findX)
- The naming conventions
- The return value structure

Without the example, you would get a function that uses exceptions, different naming, and different types. With the example, you get a consistent extension of your codebase.

## Chain-of-Thought for Code

Chain-of-thought prompting asks the AI to think before it writes code. This is especially useful for complex logic.

### When to Use It

- Complex algorithms
- Multi-step business logic
- Code that requires careful edge case handling
- Debugging sessions

### How to Apply It

```
I need a function that calculates shipping costs. Before writing code, think through:

1. What are all the inputs? (weight, dimensions, destination, shipping speed)
2. What are the business rules? (free shipping over $50, surcharge for oversized, etc.)
3. What are the edge cases? (international vs domestic, zero weight, multiple items)
4. What should the return type be? (itemized cost breakdown, not just a number)

After thinking through these, write the function with full error handling.
```

### The Difference

Without chain-of-thought, AI might write:
```python
def calculate_shipping(weight, destination):
    return weight * 0.5
```

With chain-of-thought, AI produces a well-considered function that handles edge cases and returns a structured result.

## Prompt Patterns for Common Tasks

### Pattern 1: The Refactor Prompt

```
Here is my current code:

[paste code]

Problems with this code:
1. [specific problem 1]
2. [specific problem 2]

Refactor it to:
- [goal 1]
- [goal 2]

Do NOT change the external API (function signatures and return types must stay the same).
```

### Pattern 2: The Debug Prompt

```
This code is supposed to [expected behavior], but instead it [actual behavior].

[paste code]

I have already checked:
- [thing 1 you verified]
- [thing 2 you verified]

What are the most likely causes? For each cause, explain the mechanism and suggest a fix.
```

### Pattern 3: The Test Generation Prompt

```
Here is a function:

[paste function]

Generate tests that cover:
1. The happy path (normal valid inputs)
2. Edge cases (empty input, boundary values, special characters)
3. Error cases (invalid types, missing required fields)
4. Integration concerns (what if the database is down?)

Use [testing framework] conventions.
For each test, explain what scenario it covers and why it matters.
```

### Pattern 4: The Migration Prompt

```
I need to migrate this code from [old technology] to [new technology].

Current code:
[paste code]

Constraints:
- Must preserve all existing behavior
- Must maintain the same external API
- Can take advantage of [new technology] features where appropriate
- Must handle the following edge cases: [list]

Show me the migrated code, and explain each significant change.
```

### Pattern 5: The Architecture Exploration Prompt

```
I need to build [system description].

Before writing code, help me explore the design space:
1. What are 3 different approaches to this problem?
2. For each approach, what are the tradeoffs? (complexity, performance, maintainability)
3. Which approach would you recommend for a team of [size] with a timeline of [duration]?
4. What are the risks of that approach?

Do not write implementation code yet. Focus on the design decision.
```

## Common Pitfalls

### Pitfall 1: The Vague Prompt

**Bad:** "Write me a user authentication system."

**Why it fails:** AI does not know your tech stack, your security requirements, your user model, or your deployment environment. You get generic code that does not fit your project.

**Good:** "Write a user authentication module for a Node.js Express app using JWT tokens. Users are stored in PostgreSQL via Prisma. Include registration, login, token refresh, and logout. Use bcrypt for password hashing. Return proper HTTP status codes and error messages."

### Pitfall 2: The Overloaded Prompt

**Bad:** "Build me a complete e-commerce platform with user auth, product catalog, shopping cart, payment processing, order management, admin panel, and email notifications."

**Why it fails:** Even the best AI produces poor results when asked to generate everything at once. The output will be inconsistent, incomplete, and full of gaps between the pieces.

**Good:** Break it into focused prompts: "First, design the data model for the product catalog. Then, implement the product listing API. Next, build the shopping cart service."

### Pitfall 3: The Trust-But-Don't-Verify

**Bad:** Copying AI output directly into production without review.

**Why it fails:** AI generates plausible code, not necessarily correct code. It may use deprecated APIs, have subtle bugs, or miss security considerations.

**Good:** Review every AI output. Run it. Test it. Read it line by line. If you do not understand what a line does, ask AI to explain it.

### Pitfall 4: The Context-Free Prompt

**Bad:** "Fix this bug" (without showing the surrounding code, error messages, or what you already tried).

**Why it fails:** AI cannot debug what it cannot see. Without context, it guesses -- and the guess is often wrong.

**Good:** Include the code, the error message, what you expected, what actually happened, and what you have already tried.

### Pitfall 5: Ignoring the System Prompt

**Bad:** Starting a new chat for every question, losing all context.

**Why it fails:** AI treats each conversation independently. Without accumulated context, it does not know your codebase, your conventions, or your constraints.

**Good:** Maintain a long-running conversation with context. Or, use tools that provide codebase-aware context automatically (like Claude Code or Cursor).

## Advanced Technique: Iterative Refinement

The best code rarely comes from a single prompt. Use an iterative approach:

```
Round 1: "Here is the problem. Propose a design."
Round 2: "The design is good, but [concern]. Address that."
Round 3: "Now implement the core logic."
Round 4: "Add error handling and edge cases."
Round 5: "Write tests for this."
Round 6: "Review this code for security issues."
```

Each round builds on the previous one. The AI has full context from earlier rounds. This produces better code than asking for everything in one shot.

## Measuring Prompt Quality

How do you know if your prompts are good? Measure:

1. **First-try accuracy** -- How often does the AI output work without modification?
2. **Consistency** -- Does the AI follow your conventions every time?
3. **Completeness** -- Does the AI handle edge cases you did not explicitly mention?
4. **Fit** -- Does the generated code feel like it belongs in your codebase?

If any of these are low, improve your prompts -- usually by adding more context, examples, or constraints.

## Summary

Good prompt engineering is good communication. Be specific. Provide context. Show examples. Set constraints. Review the output. Iterate.

The goal is not to trick AI into producing good code. The goal is to communicate clearly enough that good code is the natural result.
