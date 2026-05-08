/**
 * Tests for Module Registry
 * ==========================
 * Validates module definitions, categories, and structure.
 */

import { describe, it, expect } from 'vitest';

// Module data (same as in page.tsx)
interface Module {
  id: string;
  title: string;
  category: string;
  icon: string;
  description: string;
  week: number;
  order: number;
}

const MODULES: Module[] = [
  // Week 1: Cognitive + Fundamentals
  { id: 'cognitive-why', title: 'Why Learn Programming', category: 'cognitive', icon: '🧠', description: 'Understand why programming matters in the AI era', week: 1, order: 1 },
  { id: 'cognitive-thinking', title: 'AI-Era Thinking', category: 'cognitive', icon: '💡', description: 'Mental models that make you irreplaceable', week: 1, order: 2 },
  { id: 'cognitive-languages', title: 'Why Python + TypeScript', category: 'cognitive', icon: '🐍', description: 'The two languages you actually need', week: 1, order: 3 },
  { id: 'py-variables', title: 'Variables & Types', category: 'python', icon: '📦', description: 'Name binding, mutability, references', week: 1, order: 4 },
  { id: 'py-functions', title: 'Functions & Decorators', category: 'python', icon: '⚡', description: 'First-class functions, closures, decorators', week: 1, order: 5 },
  { id: 'py-classes', title: 'Classes & Inheritance', category: 'python', icon: '🏗️', description: 'OOP, dataclasses, protocols', week: 1, order: 6 },
  { id: 'py-async', title: 'Async Programming', category: 'python', icon: '🔄', description: 'Coroutines, gather, TaskGroup', week: 1, order: 7 },
  { id: 'py-types', title: 'Type Annotations', category: 'python', icon: '🏷️', description: 'Generics, TypeVar, Literal', week: 1, order: 8 },
  { id: 'py-modules', title: 'Modules & Packages', category: 'python', icon: '📚', description: 'Import system, package structure', week: 1, order: 9 },
  { id: 'ts-types', title: 'Type System', category: 'typescript', icon: '🔷', description: 'Primitives, interfaces, narrowing', week: 1, order: 10 },
  { id: 'ts-functions', title: 'Functions & Generics', category: 'typescript', icon: '⚙️', description: 'Generics, overloads, currying', week: 1, order: 11 },
  { id: 'ts-interfaces', title: 'Interfaces & Type Manipulation', category: 'typescript', icon: '🔧', description: 'Mapped types, conditional types, utility types', week: 1, order: 12 },
  { id: 'ts-async', title: 'Async Programming', category: 'typescript', icon: '⏳', description: 'Promises, async/await, AbortController', week: 1, order: 13 },
  { id: 'ts-modules', title: 'Module System', category: 'typescript', icon: '📁', description: 'ES modules, dynamic import, barrel files', week: 1, order: 14 },
  { id: 'ts-decorators', title: 'Decorators & Metaprogramming', category: 'typescript', icon: '🎨', description: 'Class/method/property decorators', week: 1, order: 15 },
  { id: 'pat-di', title: 'Dependency Injection', category: 'patterns', icon: '💉', description: 'Inversion of control', week: 1, order: 16 },
  { id: 'pat-middleware', title: 'Middleware', category: 'patterns', icon: '🔗', description: 'Request interception chain', week: 1, order: 17 },
  { id: 'pat-builder', title: 'Builder', category: 'patterns', icon: '🔨', description: 'Step-by-step construction', week: 1, order: 18 },
  { id: 'pat-strategy', title: 'Strategy', category: 'patterns', icon: '🎯', description: 'Interchangeable algorithms', week: 1, order: 19 },
  { id: 'pat-observer', title: 'Observer', category: 'patterns', icon: '👁️', description: 'Event notification', week: 1, order: 20 },
  { id: 'pat-factory', title: 'Factory', category: 'patterns', icon: '🏭', description: 'Object creation', week: 1, order: 21 },
  { id: 'pat-repository', title: 'Repository', category: 'patterns', icon: '🗄️', description: 'Data access abstraction', week: 1, order: 22 },
  { id: 'pat-pipeline', title: 'Pipeline', category: 'patterns', icon: '🔧', description: 'Sequential processing', week: 1, order: 23 },
  { id: 'py-fastapi', title: 'FastAPI', category: 'python-dissect', icon: '🚀', description: 'Dependency injection, middleware, lifecycle', week: 2, order: 24 },
  { id: 'py-langchain', title: 'LangChain', category: 'python-dissect', icon: '🦜', description: 'Chain pattern, Agent, RAG', week: 2, order: 25 },
  { id: 'py-crewai', title: 'CrewAI', category: 'python-dissect', icon: '👥', description: 'Multi-agent collaboration', week: 2, order: 26 },
  { id: 'py-dify', title: 'Dify', category: 'python-dissect', icon: '🔄', description: 'Workflow engine, plugin system', week: 2, order: 27 },
  { id: 'py-ragflow', title: 'RAGFlow', category: 'python-dissect', icon: '📖', description: 'Document parsing, vector retrieval', week: 2, order: 28 },
  { id: 'ts-nextjs', title: 'Next.js', category: 'typescript-dissect', icon: '▲', description: 'SSR/SSG, App Router, middleware', week: 3, order: 29 },
  { id: 'ts-trpc', title: 'tRPC', category: 'typescript-dissect', icon: '🔌', description: 'End-to-end type safety', week: 3, order: 30 },
  { id: 'ts-tauri', title: 'Tauri', category: 'typescript-dissect', icon: '🖥️', description: 'Cross-platform desktop', week: 3, order: 31 },
  { id: 'ts-shadcn', title: 'shadcn/ui', category: 'typescript-dissect', icon: '🎨', description: 'Component design, theming', week: 3, order: 32 },
  { id: 'ts-bun', title: 'Bun', category: 'typescript-dissect', icon: '🍞', description: 'Runtime, bundler, test runner', week: 3, order: 33 },
  { id: 'ai-prompt', title: 'Prompt Engineering', category: 'ai-mastery', icon: '✍️', description: 'System prompts, few-shot, chain-of-thought', week: 4, order: 34 },
  { id: 'ai-architecture', title: 'AI-Assisted Architecture', category: 'ai-mastery', icon: '🏛️', description: 'Design decisions with AI', week: 4, order: 35 },
  { id: 'ai-review', title: 'AI Code Review', category: 'ai-mastery', icon: '🔍', description: 'Find bugs, security, performance', week: 4, order: 36 },
  { id: 'ai-development', title: 'AI-Driven Development', category: 'ai-mastery', icon: '🤖', description: 'Complete workflow with AI', week: 4, order: 37 },
  { id: 'practice-planning', title: 'Project Planning', category: 'practice', icon: '📋', description: 'Requirements, scope, timeline', week: 4, order: 38 },
  { id: 'practice-architecture', title: 'Architecture Design', category: 'practice', icon: '🏗️', description: 'Patterns, boundaries, data flow', week: 4, order: 39 },
  { id: 'practice-implementation', title: 'Implementation', category: 'practice', icon: '💻', description: 'Build the complete project', week: 4, order: 40 },
  { id: 'practice-deployment', title: 'Deployment', category: 'practice', icon: '🚀', description: 'Docker, CI/CD, monitoring', week: 4, order: 41 },
];


// ============================================================================
// TESTS
// ============================================================================

describe('Module Registry', () => {
  describe('Module count', () => {
    it('has 41 total modules', () => {
      expect(MODULES).toHaveLength(41);
    });

    it('has unique IDs', () => {
      const ids = MODULES.map((m) => m.id);
      const uniqueIds = new Set(ids);
      expect(uniqueIds.size).toBe(ids.length);
    });
  });

  describe('Categories', () => {
    it('has 8 categories', () => {
      const categories = new Set(MODULES.map((m) => m.category));
      expect(categories.size).toBe(8);
    });

    it('has correct category distribution', () => {
      const counts: Record<string, number> = {};
      MODULES.forEach((m) => {
        counts[m.category] = (counts[m.category] || 0) + 1;
      });
      expect(counts['cognitive']).toBe(3);
      expect(counts['python']).toBe(6);
      expect(counts['typescript']).toBe(6);
      expect(counts['patterns']).toBe(8);
      expect(counts['python-dissect']).toBe(5);
      expect(counts['typescript-dissect']).toBe(5);
      expect(counts['ai-mastery']).toBe(4);
      expect(counts['practice']).toBe(4);
    });
  });

  describe('Weeks', () => {
    it('has 4 weeks', () => {
      const weeks = new Set(MODULES.map((m) => m.week));
      expect(weeks.size).toBe(4);
    });

    it('Week 1 has the most modules', () => {
      const weekCounts: Record<number, number> = {};
      MODULES.forEach((m) => {
        weekCounts[m.week] = (weekCounts[m.week] || 0) + 1;
      });
      expect(weekCounts[1]).toBeGreaterThan(weekCounts[2]);
      expect(weekCounts[1]).toBeGreaterThan(weekCounts[3]);
      expect(weekCounts[1]).toBeGreaterThan(weekCounts[4]);
    });
  });

  describe('Module structure', () => {
    it('every module has required fields', () => {
      MODULES.forEach((m) => {
        expect(m.id).toBeTruthy();
        expect(m.title).toBeTruthy();
        expect(m.category).toBeTruthy();
        expect(m.icon).toBeTruthy();
        expect(m.description).toBeTruthy();
        expect(m.week).toBeGreaterThanOrEqual(1);
        expect(m.week).toBeLessThanOrEqual(4);
        expect(m.order).toBeGreaterThanOrEqual(1);
      });
    });

    it('modules are ordered correctly', () => {
      const orders = MODULES.map((m) => m.order);
      const sorted = [...orders].sort((a, b) => a - b);
      expect(orders).toEqual(sorted);
    });
  });

  describe('Project dissection modules', () => {
    it('has 5 Python projects', () => {
      const pythonProjects = MODULES.filter((m) => m.category === 'python-dissect');
      expect(pythonProjects).toHaveLength(5);
    });

    it('has 5 TypeScript projects', () => {
      const tsProjects = MODULES.filter((m) => m.category === 'typescript-dissect');
      expect(tsProjects).toHaveLength(5);
    });

    it('Python projects are in Week 2', () => {
      const pythonProjects = MODULES.filter((m) => m.category === 'python-dissect');
      pythonProjects.forEach((m) => {
        expect(m.week).toBe(2);
      });
    });

    it('TypeScript projects are in Week 3', () => {
      const tsProjects = MODULES.filter((m) => m.category === 'typescript-dissect');
      tsProjects.forEach((m) => {
        expect(m.week).toBe(3);
      });
    });
  });
});
