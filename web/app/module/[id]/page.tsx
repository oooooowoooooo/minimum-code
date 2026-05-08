'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useLang } from '@/lib/i18n';

// Module content mapping
const MODULE_CONTENT: Record<string, { title: string; category: string; icon: string; sections: Array<{ title: string; content: string }> }> = {
  'cognitive-why': {
    title: 'Why Learn Programming',
    category: 'cognitive',
    icon: '🧠',
    sections: [
      { title: 'The Wrong Question', content: '"But ChatGPT writes code. Why learn?" This is like asking "Calculators exist. Why learn math?" The answer isn\'t about computation — it\'s about understanding what to compute.' },
      { title: 'What AI Can and Cannot Do', content: 'AI CAN: Generate boilerplate, translate languages, write tests, debug simple errors.\nAI CANNOT: Decide what to build, design architecture, judge tradeoffs, understand requirements.' },
      { title: 'The Skill Hierarchy', content: 'Level 1: Writing code ← AI does this\nLevel 2: Reading code ← You need this to verify AI\nLevel 3: Designing systems ← You need this to direct AI\nLevel 4: Making tradeoffs ← You need this to lead projects\nLevel 5: Defining problems ← You need this to create value' },
      { title: 'Key Insight', content: 'If you only learn to write code → replaced by AI.\nIf you learn to think about code → you become the person who makes AI useful.' },
    ],
  },
  'py-variables': {
    title: 'Variables & Types',
    category: 'python',
    icon: '📦',
    sections: [
      { title: 'Variables Are References', content: 'In Python, a variable is a NAME bound to an OBJECT in memory. Multiple names can point to the same object.' },
      { title: 'Mutable vs Immutable', content: 'Immutable: int, str, tuple, frozenset, bytes, None, bool\nMutable: list, dict, set, bytearray, custom objects' },
      { title: 'Code Example', content: 'a = [1, 2, 3]\nb = a  # b points to the SAME list\nb.append(4)\nprint(a)  # [1, 2, 3, 4] — a changed too!' },
      { title: 'Transferability', content: 'TypeScript: let x: number = 42 is a typed box; x = "hello" is a compile error.\nPython\'s x is more like TypeScript\'s let x: unknown.' },
    ],
  },
  'ts-types': {
    title: 'Type System',
    category: 'typescript',
    icon: '🔷',
    sections: [
      { title: 'Basic Types', content: 'string, number, boolean, null, undefined, symbol, bigint\nArrays: number[], Array<string>\nTuples: [string, number]' },
      { title: 'Interface vs Type', content: 'interface User { name: string; age: number }\ntype User = { name: string; age: number }\nInterfaces can be merged; types can use union/intersection.' },
      { title: 'Type Narrowing', content: 'function process(value: string | number) {\n  if (typeof value === "string") {\n    return value.toUpperCase(); // TypeScript knows it\'s string\n  }\n  return value.toFixed(2); // TypeScript knows it\'s number\n}' },
      { title: 'Discriminated Unions', content: 'type Shape =\n  | { kind: "circle"; radius: number }\n  | { kind: "rectangle"; width: number; height: number };\nThe "kind" field discriminates between variants.' },
    ],
  },
  'pat-di': {
    title: 'Dependency Injection',
    category: 'patterns',
    icon: '💉',
    sections: [
      { title: 'What It Is', content: 'Instead of creating dependencies inside a function, you PASS them in from outside.' },
      { title: 'Python Example (FastAPI)', content: 'def get_user(db: Database = Depends(get_database)):\n    return db.query("SELECT * FROM users")' },
      { title: 'TypeScript Example (tRPC)', content: 'const userRouter = router({\n  getProfile: publicProcedure\n    .query(({ ctx }) => {\n      return ctx.db.user.findUnique({ where: { id: ctx.userId } });\n    }),\n});' },
      { title: 'Why It Matters', content: 'Testable: mock the dependency, test the function.\nFlexible: swap implementations without changing code.\nDecoupled: function doesn\'t know about concrete implementation.' },
    ],
  },
  'py-fastapi': {
    title: 'FastAPI',
    category: 'python-dissect',
    icon: '🚀',
    sections: [
      { title: 'What Is FastAPI', content: 'Modern Python web framework. GitHub 80k+ stars. Async-first, type-safe, automatic API documentation.' },
      { title: 'Key Pattern: Dependency Injection', content: 'def get_user(db: Session = Depends(get_db)):\n    return db.query(User).all()\n\nDependencies are declared as function parameters. FastAPI resolves them automatically.' },
      { title: 'Key Pattern: Middleware', content: '@app.middleware("http")\nasync def add_timing(request, call_next):\n    start = time.time()\n    response = await call_next(request)\n    response.headers["X-Process-Time"] = str(time.time() - start)\n    return response' },
      { title: 'Key Pattern: Lifecycle', content: '@asynccontextmanager\nasync def lifespan(app):\n    # Startup\n    await connect_to_db()\n    yield\n    # Shutdown\n    await disconnect_from_db()' },
    ],
  },
  'ts-nextjs': {
    title: 'Next.js',
    category: 'typescript-dissect',
    icon: '▲',
    sections: [
      { title: 'What Is Next.js', content: 'Production-grade React framework. GitHub 130k+ stars. SSR, SSG, App Router.' },
      { title: 'Key Pattern: File-Based Routing', content: 'app/blog/[slug]/page.tsx → /blog/:slug\n\nThe file system IS the router. Zero configuration.' },
      { title: 'Key Pattern: Server/Client Boundary', content: '// Server Component (default)\nexport default async function Page() {\n  const data = await db.query(); // Direct DB access\n  return <List data={data} />;\n}\n\n// Client Component\n"use client"\nexport function Counter() {\n  const [count, setCount] = useState(0);\n  return <button onClick={() => setCount(c => c+1)}>{count}</button>;\n}' },
      { title: 'Key Pattern: Middleware', content: 'export function middleware(request: NextRequest) {\n  const token = request.cookies.get("auth-token");\n  if (!token) {\n    return NextResponse.redirect(new URL("/login", request.url));\n  }\n}' },
    ],
  },
};

// Default content for modules without specific content
function getDefaultContent(id: string) {
  const parts = id.split('-');
  const category = parts[0];
  const name = parts.slice(1).join('-');
  return {
    title: name.replace(/-/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase()),
    category: category,
    icon: '📖',
    sections: [
      { title: 'Overview', content: `This module covers ${name.replace(/-/g, ' ')}. Refer to the source files in the project for detailed content.` },
      { title: 'Key Concepts', content: 'Each module includes:\n1. Architecture explanation\n2. Code patterns with I/O examples\n3. Transferability notes\n4. Mini-exercises\n5. Key takeaways' },
      { title: 'Source Files', content: 'Check the src/ directory for the corresponding .py or .ts files with comprehensive inline comments.' },
    ],
  };
}

export default function ModulePage({ params }: { params: { id: string } }) {
  const { lang, toggle, t } = useLang();
  const [isComplete, setIsComplete] = useState(false);
  const content = MODULE_CONTENT[params.id] || getDefaultContent(params.id);

  useEffect(() => {
    const stored = localStorage.getItem('ai-era-progress');
    if (stored) {
      const completed = new Set(JSON.parse(stored));
      setIsComplete(completed.has(params.id));
    }
  }, [params.id]);

  const toggleComplete = () => {
    const stored = localStorage.getItem('ai-era-progress');
    const completed = stored ? new Set(JSON.parse(stored)) : new Set<string>();
    if (completed.has(params.id)) {
      completed.delete(params.id);
    } else {
      completed.add(params.id);
    }
    setIsComplete(!isComplete);
    localStorage.setItem('ai-era-progress', JSON.stringify([...completed]));
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a]">
      {/* Header */}
      <header className="border-b border-gray-800 bg-[#0a0a0a]/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors">
            <span>←</span>
            <span className="text-sm">{t('nav.home')}</span>
          </Link>
          <div className="flex items-center gap-3">
            <button
              onClick={toggle}
              className="px-3 py-1 rounded-full text-xs font-medium bg-gray-800 text-gray-300 hover:bg-gray-700 border border-gray-700 transition-all"
            >
              {lang === 'zh' ? '中/EN' : 'EN/中'}
            </button>
            <button
              onClick={toggleComplete}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                isComplete
                  ? 'bg-green-500 text-white'
                  : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
              }`}
            >
              {isComplete ? t('action.completed') : t('action.mark_complete')}
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Module Header */}
        <div className="mb-8">
          <div className="flex items-center gap-4 mb-4">
            <span className="text-4xl">{content.icon}</span>
            <div>
              <h1 className="text-2xl font-bold">{content.title}</h1>
              <span className="text-sm text-gray-500 capitalize">{content.category.replace(/-/g, ' ')}</span>
            </div>
          </div>
        </div>

        {/* Content Sections */}
        <div className="space-y-6">
          {content.sections.map((section, i) => (
            <div key={i} className="p-6 rounded-xl bg-gray-900 border border-gray-800">
              <h2 className="text-lg font-bold mb-3 text-blue-400">{section.title}</h2>
              <div className="text-gray-300 text-sm leading-relaxed whitespace-pre-line">
                {section.content}
              </div>
            </div>
          ))}
        </div>

        {/* Navigation */}
        <div className="mt-12 flex justify-between">
          <Link
            href="/"
            className="px-4 py-2 rounded-lg bg-gray-800 text-gray-300 hover:bg-gray-700 transition-colors text-sm"
          >
            ← {t('nav.home')}
          </Link>
        </div>
      </div>
    </div>
  );
}
