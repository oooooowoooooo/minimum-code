# Next.js — React Framework at Industrial Scale

> GitHub Stars: 130k+ | Language: TypeScript | Category: Web Framework

## What Is Next.js?

Next.js is the production-grade React framework created by Vercel. It introduced server-side rendering (SSR), static site generation (SSG), and the App Router to the React ecosystem. Every major company using React in production uses or has used Next.js.

## Why We Dissect This Project

Next.js represents the **ceiling of TypeScript framework design**. Its architecture demonstrates:
- How to build a framework that's both powerful and approachable
- How TypeScript types create a self-documenting API
- How middleware works at the framework level
- How server and client code coexist in one codebase

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                   Next.js App                    │
├─────────────────────────────────────────────────┤
│  App Router (file-based routing)                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│  │ Layout   │ │ Page     │ │ Loading  │        │
│  │ (server) │ │ (server/ │ │ (client) │        │
│  │          │ │  client) │ │          │        │
│  └──────────┘ └──────────┘ └──────────┘        │
├─────────────────────────────────────────────────┤
│  Server Components │ Client Components          │
│  (RSC - zero JS)   │ (interactive, hydrated)    │
├─────────────────────────────────────────────────┤
│  Middleware (edge runtime, request interception) │
├─────────────────────────────────────────────────┤
│  Data Layer (server actions, fetch, cache)      │
├─────────────────────────────────────────────────┤
│  Build System (Turbopack, webpack)              │
└─────────────────────────────────────────────────┘
```

## Key Design Decisions

### 1. File-Based Routing
Routes are defined by the file system structure, not configuration files.
```
app/
├── page.tsx          → /
├── about/
│   └── page.tsx      → /about
└── blog/
    ├── page.tsx      → /blog
    └── [slug]/
        └── page.tsx  → /blog/:slug
```

### 2. Server Components by Default
Components are server-rendered by default. You opt into client-side behavior with `"use client"`.

### 3. Middleware at the Edge
Request interception before the route handler runs — for auth, redirects, logging.

## Learning Objectives

After dissecting Next.js, you will understand:
- How file-based routing works internally
- The Server/Client component boundary
- How middleware intercepts requests
- How TypeScript types enforce framework contracts
- How build systems optimize for production

## Prerequisites

- TypeScript fundamentals
- Basic React knowledge
- Understanding of HTTP (requests, responses, cookies)

## Files in This Module

| File | Description |
|------|-------------|
| [patterns.md](./patterns.md) | Core design patterns analysis |
| [dissect.ts](./dissect.ts) | Atomic code dissection with inline tests |
