# shadcn/ui — Component Design at Its Finest

> GitHub Stars: 80k+ | Language: TypeScript/React | Category: UI Components

## What Is shadcn/ui?

Not a component library. A collection of reusable components you copy into your project and own. Built on Radix UI primitives + Tailwind CSS.

## Why It Matters

1. **You own the code** — no version updates breaking your app
2. **Composable** — small primitives combine into complex UIs
3. **Accessible by default** — Radix handles ARIA, keyboard nav
4. **Themed via CSS variables** — one file controls entire look

## Architecture

```
Your Project
├── components/ui/        ← You OWN these files
│   ├── button.tsx
│   ├── dialog.tsx
│   └── form.tsx
├── lib/utils.ts
└── tailwind.config.ts

Dependencies:
├── @radix-ui/react-*     ← Headless primitives (accessibility)
├── tailwind-merge        ← Smart class merging
└── class-variance-authority ← Variant management
```

## Key Patterns

| # | Pattern | What It Does |
|---|---------|-------------|
| 1 | Copy-paste ownership | You own the code, not a dependency |
| 2 | Variant system | One component, many styles via props |
| 3 | Composition | Small pieces build complex UIs |
| 4 | CSS variables theming | One config file, infinite themes |
| 5 | Slot pattern | Radix's `asChild` for polymorphic components |

## Files

| File | Description |
|------|-------------|
| [patterns.md](./patterns.md) | Core design patterns |
| [dissect.tsx](./dissect.tsx) | Atomic code dissection |
