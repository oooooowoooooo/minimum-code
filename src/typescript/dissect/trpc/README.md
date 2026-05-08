# tRPC — End-to-End Type Safety Without Code Generation

> GitHub Stars: 35k+ | Language: TypeScript | Category: API Framework

## What Is tRPC?

tRPC enables building fully type-safe APIs without schemas, code generation, or runtime overhead. Change a server function's return type, and your frontend code instantly knows — the TypeScript compiler catches any mismatch.

## Why We Dissect This Project

tRPC is the **pinnacle of TypeScript type-level programming** in production. It demonstrates:
- How to create end-to-end type safety without code generation
- How generics and inference eliminate boilerplate
- How the "Procedure" pattern replaces REST/GraphQL
- How TypeScript can be a build tool, not just a type checker

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                  Frontend (React)                │
│  const user = trpc.user.getProfile.useQuery({id})│
│  // TypeScript knows: user is {name: string}    │
├─────────────────────────────────────────────────┤
│              tRPC Client                        │
│  Type-safe HTTP calls, automatic serialization  │
├─────────────────────────────────────────────────┤
│              HTTP Transport                     │
├─────────────────────────────────────────────────┤
│              tRPC Server                        │
│  Router → Procedure → Handler                   │
├─────────────────────────────────────────────────┤
│              Your Backend                       │
│  Database, services, external APIs              │
└─────────────────────────────────────────────────┘
```

## Key Design Decisions

### 1. Procedures Over Endpoints
Instead of REST routes (`GET /users/:id`), you define "procedures" that are just functions with typed inputs and outputs.

### 2. Router Composition
Small routers compose into large ones. Each router is a namespace of related procedures.

### 3. Zero Code Generation
Types flow from server to client through TypeScript inference alone. No `.proto` files, no GraphQL schemas, no OpenAPI specs.

### 4. Middleware as First-Class Citizen
Procedures can be extended with middleware for auth, logging, rate limiting.

## Learning Objectives

After dissecting tRPC, you will understand:
- How TypeScript generics enable end-to-end type safety
- The "Procedure" pattern and why it's better than REST for internal APIs
- How router composition scales to large applications
- How to design APIs that are type-safe by default

## Files in This Module

| File | Description |
|------|-------------|
| [patterns.md](./patterns.md) | Core design patterns analysis |
| [dissect.ts](./dissect.ts) | Atomic code dissection with inline tests |
