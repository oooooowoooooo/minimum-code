# AI Code Review

## Why AI Code Review Is Valuable

Code review is one of the most effective quality assurance practices in software engineering. But human code review has limitations: reviewers get tired, miss details, and have limited time. AI code review complements human review by catching issues that are easy to overlook.

AI excels at:
- Checking every line with the same attention (no fatigue)
- Finding patterns that match known vulnerability classes
- Identifying inconsistencies across large diffs
- Suggesting improvements based on best practices

AI does not replace human review. It augments it.

## The Review Workflow

```
1. AI performs initial review (automated, fast)
2. You evaluate AI findings (judgment required)
3. Human reviewer performs deep review (context, design, intent)
4. Final decision by the team
```

AI handles the mechanical checks. Humans handle the judgment calls.

## Prompt Template: General Code Review

```
Review the following code. Check for:

1. Bugs and logic errors
2. Security vulnerabilities
3. Performance issues
4. Error handling gaps
5. Code clarity and maintainability
6. Edge cases not handled
7. Type safety issues
8. Naming and convention issues

For each finding:
- Severity: critical / high / medium / low / nit
- Category: bug / security / performance / style / design
- Location: exact line or range
- Explanation: what is wrong and why it matters
- Suggestion: how to fix it (with code)

Code to review:
[paste code]
```

## Prompt Template: Security-Focused Review

```
Perform a security review of the following code.

Check specifically for:
1. SQL injection
2. Cross-site scripting (XSS)
3. Cross-site request forgery (CSRF)
4. Authentication bypass
5. Authorization bypass (accessing other users' data)
6. Sensitive data exposure (logging secrets, returning too much data)
7. Input validation gaps
8. Insecure cryptographic practices
9. Race conditions that could lead to security issues
10. Dependency vulnerabilities

For each finding:
- Severity: critical / high / medium / low
- Attack vector: how an attacker would exploit this
- Impact: what happens if exploited
- Fix: specific code change to resolve

Code to review:
[paste code]
```

## Prompt Template: Performance Review

```
Review the following code for performance issues.

Check for:
1. Unnecessary database queries (N+1 problem)
2. Missing or incorrect database indexes
3. Inefficient algorithms (unnecessary loops, redundant computation)
4. Memory leaks or excessive memory allocation
5. Blocking operations in async contexts
6. Missing caching opportunities
7. Unbounded data fetching (no pagination, no limits)
8. Expensive operations that could be batched

For each finding:
- Impact: high / medium / low
- Frequency: how often this code path is hit
- Current cost: estimated impact on response time / memory / CPU
- Optimization: specific change to improve performance
- Tradeoff: what you sacrifice (readability, complexity, etc.)

Code to review:
[paste code]
```

## Prompt Template: Refactoring Review

```
Review the following code for maintainability and design issues.

Check for:
1. Functions that are too long (doing too many things)
2. Deep nesting (callback hell, deeply nested if/else)
3. Duplicated logic that should be extracted
4. Poor separation of concerns
5. Missing abstractions (or unnecessary abstractions)
6. Tight coupling between components
7. Magic numbers and hard-coded values
8. Missing or misleading comments/names

For each finding:
- What: describe the issue
- Why: why it makes the code harder to maintain
- Suggestion: how to restructure (with code sketch)
- Priority: refactor now / refactor later / acceptable as-is

Code to review:
[paste code]
```

## How to Verify AI Review Suggestions

AI code review suggestions are hypotheses, not verdicts. Always verify before applying them.

### 1. Check if the suggestion is correct

AI sometimes flags things that are not actually problems. For example:

- AI might flag a "SQL injection" that is actually using parameterized queries correctly
- AI might suggest a "performance optimization" that makes no measurable difference
- AI might recommend a pattern that is inappropriate for your context

**Verification step:** Read the flagged code carefully. Does the issue actually exist?

### 2. Check if the fix introduces new problems

AI's suggested fix might:
- Break existing functionality
- Introduce a new bug
- Violate your project's conventions
- Add unnecessary complexity

**Verification step:** Apply the fix mentally. Does it create any new issues?

### 3. Check if the fix is proportionate

Not every issue needs to be fixed. A "low" severity style issue in a prototype is not worth the effort. A "medium" performance issue in code that runs once a day is not urgent.

**Verification step:** Does fixing this issue provide value proportional to the effort?

### 4. Test the fix

Never apply AI suggestions without testing:
- Run existing tests
- Write new tests for the specific case
- Test edge cases related to the change
- Test the exact scenario the AI flagged

## The Human-AI Review Partnership

The best review process uses both AI and humans:

### AI Handles:
- Pattern-based checks (security vulnerabilities, performance anti-patterns)
- Consistency checks (naming conventions, style guide compliance)
- Completeness checks (error handling, input validation)
- Exhaustive line-by-line inspection

### Humans Handle:
- Design intent (is this the right approach?)
- Business logic correctness (does this match the requirements?)
- Contextual judgment (is this complexity justified?)
- Code readability (does this make sense to the next developer?)
- Architecture alignment (does this fit the system's design?)

### The Division of Labor

```
AI:  "This function has 4 nested if statements and no error handling for the API call."

Human: "Agreed on the nesting -- I will extract the validation logic.
        The missing error handling is intentional -- there is a global error boundary.
        But you are right that the API call should have a retry."

AI:  "Here is the refactored version with extracted validation and API retry logic."

Human: "The retry logic is good, but use exponential backoff instead of fixed delay.
        Also, the extracted function should live in the utils module, not inline."
```

This back-and-forth produces better code than either AI or human alone.

## Anti-Patterns to Avoid

### Anti-Pattern 1: Blindly Applying All AI Suggestions

Not every suggestion is worth implementing. AI does not understand your priorities, your deadlines, or your team's standards. Apply judgment.

### Anti-Pattern 2: Using AI Review as a Replacement for Human Review

AI catches patterns. Humans catch intent. You need both.

### Anti-Pattern 3: Reviewing Too Much at Once

Do not paste 500 lines and ask for a review. AI (and humans) produce better reviews on smaller chunks. Review one function, one module, one feature at a time.

### Anti-Pattern 4: Ignoring AI Suggestions You Disagree With

When you disagree with an AI suggestion, articulate why. This forces you to understand the tradeoff and makes you a better reviewer.

### Anti-Pattern 5: Not Providing Context

Without context -- what the code is supposed to do, what the business requirements are, what the architecture looks like -- AI can only check for generic issues. Provide the context that helps AI find real problems.

## Building a Review Checklist

Use AI to build a project-specific review checklist:

```
Based on the following codebase and its common issues, generate a code review checklist specific to this project.

[paste a few representative code files]
[paste a few known past bugs or issues]

Create a checklist organized by:
1. Project-specific patterns to check for
2. Common mistakes in this codebase
3. Technology-specific gotchas
4. Business logic validations
```

This checklist becomes a reusable tool that improves over time as you add more project-specific items.

## Summary

AI code review is a force multiplier, not a replacement for human judgment. Use it for the mechanical work. Reserve human attention for the design decisions.

Always verify AI findings. Always provide context. Always apply judgment. The goal is not to find every possible issue -- it is to find the issues that matter and fix them efficiently.
