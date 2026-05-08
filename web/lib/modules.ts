export type ModuleCategory =
  | 'cognitive'
  | 'python-fundamentals'
  | 'typescript-fundamentals'
  | 'patterns'
  | 'python-dissect'
  | 'typescript-dissect'
  | 'ai-mastery'
  | 'practice';

export type ModuleStatus = 'locked' | 'available' | 'in-progress' | 'complete';

export interface Module {
  id: string;
  title: string;
  category: ModuleCategory;
  order: number;
  prerequisites: string[];
  description: string;
  icon: string;
  path: string;
}

export const CATEGORY_META: Record<ModuleCategory, { label: string; color: string; week: number }> = {
  'cognitive':               { label: 'Cognitive Foundation',       color: '#8b5cf6', week: 1 },
  'python-fundamentals':     { label: 'Python Fundamentals',        color: '#3b82f6', week: 2 },
  'typescript-fundamentals': { label: 'TypeScript Fundamentals',    color: '#06b6d4', week: 3 },
  'patterns':                { label: 'Industrial Patterns',        color: '#f59e0b', week: 4 },
  'python-dissect':          { label: 'Python Project Dissection',  color: '#22c55e', week: 5 },
  'typescript-dissect':      { label: 'TS Project Dissection',      color: '#10b981', week: 6 },
  'ai-mastery':              { label: 'AI Mastery',                 color: '#ec4899', week: 7 },
  'practice':                { label: 'Practice Projects',          color: '#ef4444', week: 8 },
};

// ──────────────────────────────────────────────
//  Cognitive Foundation  (Week 1)
// ──────────────────────────────────────────────
const cognitive: Module[] = [
  {
    id: 'cog-1',
    title: 'AI Era Thinking',
    category: 'cognitive',
    order: 1,
    prerequisites: [],
    description: 'How AI reshapes the software industry and what it means for developers.',
    icon: '🧠',
    path: '/module/cog-1',
  },
  {
    id: 'cog-2',
    title: 'Why Learn Programming',
    category: 'cognitive',
    order: 2,
    prerequisites: ['cog-1'],
    description: 'The enduring value of programming skills in the age of AI.',
    icon: '💡',
    path: '/module/cog-2',
  },
  {
    id: 'cog-3',
    title: 'Why Python + TypeScript',
    category: 'cognitive',
    order: 3,
    prerequisites: ['cog-2'],
    description: 'Strategic language selection for maximum career leverage.',
    icon: '🎯',
    path: '/module/cog-3',
  },
];

// ──────────────────────────────────────────────
//  Python Fundamentals  (Week 2)
// ──────────────────────────────────────────────
const pythonFundamentals: Module[] = [
  {
    id: 'py-f-1',
    title: 'Variables & Types',
    category: 'python-fundamentals',
    order: 4,
    prerequisites: ['cog-3'],
    description: 'Python type system, variables, and type annotations.',
    icon: '📦',
    path: '/module/py-f-1',
  },
  {
    id: 'py-f-2',
    title: 'Functions',
    category: 'python-fundamentals',
    order: 5,
    prerequisites: ['py-f-1'],
    description: 'Function definitions, arguments, return types, and decorators.',
    icon: '⚡',
    path: '/module/py-f-2',
  },
  {
    id: 'py-f-3',
    title: 'Classes & OOP',
    category: 'python-fundamentals',
    order: 6,
    prerequisites: ['py-f-2'],
    description: 'Object-oriented programming in Python: classes, inheritance, protocols.',
    icon: '🏗️',
    path: '/module/py-f-3',
  },
  {
    id: 'py-f-4',
    title: 'Modules & Packages',
    category: 'python-fundamentals',
    order: 7,
    prerequisites: ['py-f-3'],
    description: 'Module system, imports, package structure, and virtual environments.',
    icon: '📚',
    path: '/module/py-f-4',
  },
  {
    id: 'py-f-5',
    title: 'Async I/O',
    category: 'python-fundamentals',
    order: 8,
    prerequisites: ['py-f-4'],
    description: 'asyncio, coroutines, event loops, and concurrent execution.',
    icon: '🔄',
    path: '/module/py-f-5',
  },
  {
    id: 'py-f-6',
    title: 'Type System Deep Dive',
    category: 'python-fundamentals',
    order: 9,
    prerequisites: ['py-f-5'],
    description: 'Advanced typing: generics, TypeVar, Protocol, and type narrowing.',
    icon: '🔬',
    path: '/module/py-f-6',
  },
];

// ──────────────────────────────────────────────
//  TypeScript Fundamentals  (Week 3)
// ──────────────────────────────────────────────
const tsFundamentals: Module[] = [
  {
    id: 'ts-f-1',
    title: 'Types & Interfaces',
    category: 'typescript-fundamentals',
    order: 10,
    prerequisites: ['cog-3'],
    description: 'Core type system: primitives, interfaces, type aliases, and unions.',
    icon: '🔷',
    path: '/module/ts-f-1',
  },
  {
    id: 'ts-f-2',
    title: 'Functions & Overloads',
    category: 'typescript-fundamentals',
    order: 11,
    prerequisites: ['ts-f-1'],
    description: 'Typed functions, overloads, generics, and higher-order functions.',
    icon: '⚡',
    path: '/module/ts-f-2',
  },
  {
    id: 'ts-f-3',
    title: 'Interfaces & Classes',
    category: 'typescript-fundamentals',
    order: 12,
    prerequisites: ['ts-f-2'],
    description: 'Advanced interfaces, class patterns, and implementation strategies.',
    icon: '🏗️',
    path: '/module/ts-f-3',
  },
  {
    id: 'ts-f-4',
    title: 'Modules & ESM',
    category: 'typescript-fundamentals',
    order: 13,
    prerequisites: ['ts-f-3'],
    description: 'ES modules, import/export patterns, and module resolution.',
    icon: '📚',
    path: '/module/ts-f-4',
  },
  {
    id: 'ts-f-5',
    title: 'Async Patterns',
    category: 'typescript-fundamentals',
    order: 14,
    prerequisites: ['ts-f-4'],
    description: 'Promises, async/await, error handling, and concurrency patterns.',
    icon: '🔄',
    path: '/module/ts-f-5',
  },
  {
    id: 'ts-f-6',
    title: 'Advanced Types',
    category: 'typescript-fundamentals',
    order: 15,
    prerequisites: ['ts-f-5'],
    description: 'Conditional types, mapped types, template literals, and type guards.',
    icon: '🔬',
    path: '/module/ts-f-6',
  },
];

// ──────────────────────────────────────────────
//  Industrial Patterns  (Week 4)
// ──────────────────────────────────────────────
const patterns: Module[] = [
  {
    id: 'pat-1',
    title: 'Builder Pattern',
    category: 'patterns',
    order: 16,
    prerequisites: ['py-f-6', 'ts-f-6'],
    description: 'Step-by-step construction of complex objects.',
    icon: '🔨',
    path: '/module/pat-1',
  },
  {
    id: 'pat-2',
    title: 'Factory Pattern',
    category: 'patterns',
    order: 17,
    prerequisites: ['pat-1'],
    description: 'Object creation without specifying exact classes.',
    icon: '🏭',
    path: '/module/pat-2',
  },
  {
    id: 'pat-3',
    title: 'Strategy Pattern',
    category: 'patterns',
    order: 18,
    prerequisites: ['pat-2'],
    description: 'Encapsulating algorithms and making them interchangeable.',
    icon: '♟️',
    path: '/module/pat-3',
  },
  {
    id: 'pat-4',
    title: 'Observer Pattern',
    category: 'patterns',
    order: 19,
    prerequisites: ['pat-3'],
    description: 'Event-driven communication between decoupled components.',
    icon: '👁️',
    path: '/module/pat-4',
  },
  {
    id: 'pat-5',
    title: 'Middleware Pattern',
    category: 'patterns',
    order: 20,
    prerequisites: ['pat-4'],
    description: 'Request/response processing pipelines.',
    icon: '🔗',
    path: '/module/pat-5',
  },
  {
    id: 'pat-6',
    title: 'Repository Pattern',
    category: 'patterns',
    order: 21,
    prerequisites: ['pat-5'],
    description: 'Abstracting data access behind a clean interface.',
    icon: '🗄️',
    path: '/module/pat-6',
  },
  {
    id: 'pat-7',
    title: 'Pipeline Pattern',
    category: 'patterns',
    order: 22,
    prerequisites: ['pat-6'],
    description: 'Chaining transformations through sequential stages.',
    icon: '🔧',
    path: '/module/pat-7',
  },
  {
    id: 'pat-8',
    title: 'Dependency Injection',
    category: 'patterns',
    order: 23,
    prerequisites: ['pat-7'],
    description: 'Inversion of control for testable, modular architectures.',
    icon: '💉',
    path: '/module/pat-8',
  },
];

// ──────────────────────────────────────────────
//  Python Project Dissection  (Week 5)
//  Each project has 3 sub-modules: README, dissect.py, patterns.md
// ──────────────────────────────────────────────
const pythonDissectProjects = [
  { slug: 'fastapi',  title: 'FastAPI',  icon: '🚀' },
  { slug: 'langchain', title: 'LangChain', icon: '🦜' },
  { slug: 'crewai',   title: 'CrewAI',   icon: '👥' },
  { slug: 'dify',     title: 'Dify',     icon: '🔮' },
  { slug: 'ragflow',  title: 'RAGFlow',  icon: '📖' },
];

const pythonDissect: Module[] = pythonDissectProjects.flatMap((proj, pi) => {
  const base = pi === 0 ? ['pat-8'] : [`py-d-${pythonDissectProjects[pi - 1].slug}-3`];
  return [
    {
      id: `py-d-${proj.slug}-1`,
      title: `${proj.title} — Overview`,
      category: 'python-dissect' as ModuleCategory,
      order: 24 + pi * 3,
      prerequisites: base,
      description: `Architecture overview and key decisions in ${proj.title}.`,
      icon: proj.icon,
      path: `/module/py-d-${proj.slug}-1`,
    },
    {
      id: `py-d-${proj.slug}-2`,
      title: `${proj.title} — Code Walkthrough`,
      category: 'python-dissect' as ModuleCategory,
      order: 25 + pi * 3,
      prerequisites: [`py-d-${proj.slug}-1`],
      description: `Line-by-line dissection of ${proj.title} core source code.`,
      icon: proj.icon,
      path: `/module/py-d-${proj.slug}-2`,
    },
    {
      id: `py-d-${proj.slug}-3`,
      title: `${proj.title} — Patterns Extracted`,
      category: 'python-dissect' as ModuleCategory,
      order: 26 + pi * 3,
      prerequisites: [`py-d-${proj.slug}-2`],
      description: `Reusable patterns and anti-patterns found in ${proj.title}.`,
      icon: proj.icon,
      path: `/module/py-d-${proj.slug}-3`,
    },
  ];
});

// ──────────────────────────────────────────────
//  TypeScript Project Dissection  (Week 6)
// ──────────────────────────────────────────────
const tsDissectProjects = [
  { slug: 'nextjs',     title: 'Next.js',     icon: '▲' },
  { slug: 'trpc',       title: 'tRPC',        icon: '📡' },
  { slug: 'tauri',      title: 'Tauri',       icon: '🦀' },
  { slug: 'shadcn-ui',  title: 'shadcn/ui',   icon: '🎨' },
  { slug: 'bun',        title: 'Bun',         icon: '🍞' },
];

const tsDissect: Module[] = tsDissectProjects.flatMap((proj, pi) => {
  const base = pi === 0
    ? [`py-d-${pythonDissectProjects[pythonDissectProjects.length - 1].slug}-3`]
    : [`ts-d-${tsDissectProjects[pi - 1].slug}-3`];
  return [
    {
      id: `ts-d-${proj.slug}-1`,
      title: `${proj.title} — Overview`,
      category: 'typescript-dissect' as ModuleCategory,
      order: 39 + pi * 3,
      prerequisites: base,
      description: `Architecture overview and key decisions in ${proj.title}.`,
      icon: proj.icon,
      path: `/module/ts-d-${proj.slug}-1`,
    },
    {
      id: `ts-d-${proj.slug}-2`,
      title: `${proj.title} — Code Walkthrough`,
      category: 'typescript-dissect' as ModuleCategory,
      order: 40 + pi * 3,
      prerequisites: [`ts-d-${proj.slug}-1`],
      description: `Line-by-line dissection of ${proj.title} core source code.`,
      icon: proj.icon,
      path: `/module/ts-d-${proj.slug}-2`,
    },
    {
      id: `ts-d-${proj.slug}-3`,
      title: `${proj.title} — Patterns Extracted`,
      category: 'typescript-dissect' as ModuleCategory,
      order: 41 + pi * 3,
      prerequisites: [`ts-d-${proj.slug}-2`],
      description: `Reusable patterns and anti-patterns found in ${proj.title}.`,
      icon: proj.icon,
      path: `/module/ts-d-${proj.slug}-3`,
    },
  ];
});

// ──────────────────────────────────────────────
//  AI Mastery  (Week 7)
// ──────────────────────────────────────────────
const aiMastery: Module[] = [
  {
    id: 'ai-1',
    title: 'Prompt Engineering',
    category: 'ai-mastery',
    order: 54,
    prerequisites: [`ts-d-${tsDissectProjects[tsDissectProjects.length - 1].slug}-3`],
    description: 'Crafting effective prompts for code generation and analysis.',
    icon: '🤖',
    path: '/module/ai-1',
  },
  {
    id: 'ai-2',
    title: 'AI-Assisted Architecture',
    category: 'ai-mastery',
    order: 55,
    prerequisites: ['ai-1'],
    description: 'Using AI to design and evaluate software architectures.',
    icon: '🏛️',
    path: '/module/ai-2',
  },
  {
    id: 'ai-3',
    title: 'AI Code Review',
    category: 'ai-mastery',
    order: 56,
    prerequisites: ['ai-2'],
    description: 'Automated code review workflows with LLM-powered analysis.',
    icon: '🔍',
    path: '/module/ai-3',
  },
  {
    id: 'ai-4',
    title: 'AI-Driven Development',
    category: 'ai-mastery',
    order: 57,
    prerequisites: ['ai-3'],
    description: 'Full development lifecycle with AI as a copilot.',
    icon: '🚀',
    path: '/module/ai-4',
  },
];

// ──────────────────────────────────────────────
//  Practice Projects  (Week 8)
// ──────────────────────────────────────────────
const practice: Module[] = [
  {
    id: 'prac-1',
    title: 'Project Planning',
    category: 'practice',
    order: 58,
    prerequisites: ['ai-4'],
    description: 'Requirements gathering, tech stack selection, and roadmap creation.',
    icon: '📋',
    path: '/module/prac-1',
  },
  {
    id: 'prac-2',
    title: 'Architecture Design',
    category: 'practice',
    order: 59,
    prerequisites: ['prac-1'],
    description: 'Designing scalable, maintainable system architecture.',
    icon: '🏗️',
    path: '/module/prac-2',
  },
  {
    id: 'prac-3',
    title: 'Implementation',
    category: 'practice',
    order: 60,
    prerequisites: ['prac-2'],
    description: 'Building the project with industrial-grade patterns.',
    icon: '⌨️',
    path: '/module/prac-3',
  },
  {
    id: 'prac-4',
    title: 'Deployment',
    category: 'practice',
    order: 61,
    prerequisites: ['prac-3'],
    description: 'CI/CD, containerization, monitoring, and production deployment.',
    icon: '🌐',
    path: '/module/prac-4',
  },
];

// ──────────────────────────────────────────────
//  All modules combined
// ──────────────────────────────────────────────
export const modules: Module[] = [
  ...cognitive,
  ...pythonFundamentals,
  ...tsFundamentals,
  ...patterns,
  ...pythonDissect,
  ...tsDissect,
  ...aiMastery,
  ...practice,
];

/** Get a module by id. Throws if not found. */
export function getModuleById(id: string): Module {
  const mod = modules.find((m) => m.id === id);
  if (!mod) throw new Error(`Module not found: ${id}`);
  return mod;
}

/** Get all modules for a given category. */
export function getModulesByCategory(category: ModuleCategory): Module[] {
  return modules.filter((m) => m.category === category);
}

/** Get all unique categories in display order. */
export function getCategories(): ModuleCategory[] {
  return [
    'cognitive',
    'python-fundamentals',
    'typescript-fundamentals',
    'patterns',
    'python-dissect',
    'typescript-dissect',
    'ai-mastery',
    'practice',
  ];
}
