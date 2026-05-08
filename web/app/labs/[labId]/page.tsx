'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { useLang } from '@/lib/i18n';
import { API_BASE } from '@/lib/api';

/* ------------------------------------------------------------------ */
/*  Types                                                              */
/* ------------------------------------------------------------------ */

type Difficulty = 'beginner' | 'intermediate' | 'advanced';
type TabKey = 'starter' | 'test' | 'solution' | 'results';

interface LabDetail {
  id: string;
  title: string;
  description: string;
  difficulty: Difficulty;
  estimated_minutes: number;
  track: string;
  track_icon: string;
  task: string;
  acceptance_criteria: string[];
  starter_code: string;
  test_file: string;
  language?: string;
}

interface TestResult {
  passed: boolean;
  name: string;
  message?: string;
}

interface RunResponse {
  success: boolean;
  results: TestResult[];
  output?: string;
  error?: string;
}

/* ------------------------------------------------------------------ */
/*  Constants                                                          */
/* ------------------------------------------------------------------ */

const DIFFICULTY_META: Record<Difficulty, { label: { zh: string; en: string }; color: string; bg: string; border: string }> = {
  beginner: {
    label: { zh: '入门', en: 'Beginner' },
    color: 'text-green-400',
    bg: 'bg-green-900/30',
    border: 'border-green-700/50',
  },
  intermediate: {
    label: { zh: '进阶', en: 'Intermediate' },
    color: 'text-amber-400',
    bg: 'bg-amber-900/30',
    border: 'border-amber-700/50',
  },
  advanced: {
    label: { zh: '高级', en: 'Advanced' },
    color: 'text-red-400',
    bg: 'bg-red-900/30',
    border: 'border-red-700/50',
  },
};

const TAB_DEFS: { key: TabKey; label: { zh: string; en: string }; icon: string }[] = [
  { key: 'starter', label: { zh: '初始代码', en: 'Starter Code' }, icon: '📜' },
  { key: 'test', label: { zh: '测试文件', en: 'Test File' }, icon: '✅' },
  { key: 'solution', label: { zh: '我的解答', en: 'My Solution' }, icon: '✏️' },
  { key: 'results', label: { zh: '运行结果', en: 'Results' }, icon: '📊' },
];

/* ------------------------------------------------------------------ */
/*  localStorage helpers                                               */
/* ------------------------------------------------------------------ */

const SOLUTION_KEY = (labId: string) => `lab_solution_${labId}`;
const COMPLETED_KEY = 'lab_completed';

function loadSolution(labId: string): string {
  if (typeof window === 'undefined') return '';
  try {
    return localStorage.getItem(SOLUTION_KEY(labId)) ?? '';
  } catch {
    return '';
  }
}

function saveSolution(labId: string, code: string): void {
  try {
    localStorage.setItem(SOLUTION_KEY(labId), code);
  } catch {}
}

function loadCompleted(): Set<string> {
  if (typeof window === 'undefined') return new Set();
  try {
    const raw = localStorage.getItem(COMPLETED_KEY);
    return raw ? new Set(JSON.parse(raw)) : new Set();
  } catch {
    return new Set();
  }
}

function toggleCompleted(labId: string): boolean {
  const set = loadCompleted();
  const nowComplete = !set.has(labId);
  if (nowComplete) set.add(labId);
  else set.delete(labId);
  localStorage.setItem(COMPLETED_KEY, JSON.stringify([...set]));
  return nowComplete;
}

/* ------------------------------------------------------------------ */
/*  Component                                                          */
/* ------------------------------------------------------------------ */

export default function LabDetailPage() {
  const params = useParams();
  const labId = params.labId as string;
  const { lang, toggle, t } = useLang();

  const [lab, setLab] = useState<LabDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [activeTab, setActiveTab] = useState<TabKey>('starter');
  const [solution, setSolution] = useState('');
  const [isComplete, setIsComplete] = useState(false);
  const [criteriaChecked, setCriteriaChecked] = useState<Record<number, boolean>>({});

  const [running, setRunning] = useState(false);
  const [runResult, setRunResult] = useState<RunResponse | null>(null);
  const [copied, setCopied] = useState(false);

  const textareaRef = useRef<HTMLTextAreaElement>(null);

  /* ---- fetch lab detail ---- */
  useEffect(() => {
    if (!labId) return;

    fetch(`${API_BASE}/api/labs/${encodeURIComponent(labId)}`)
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((data) => {
        setLab(data);
        setSolution(loadSolution(labId));
        setIsComplete(loadCompleted().has(labId));
        // Initialize all criteria as unchecked
        if (data.acceptance_criteria) {
          const init: Record<number, boolean> = {};
          data.acceptance_criteria.forEach((_: string, i: number) => { init[i] = false; });
          setCriteriaChecked(init);
        }
        setLoading(false);
      })
      .catch((e) => {
        setError(e.message);
        setLoading(false);
      });
  }, [labId]);

  /* ---- persist solution ---- */
  const handleSolutionChange = useCallback(
    (val: string) => {
      setSolution(val);
      saveSolution(labId, val);
    },
    [labId],
  );

  /* ---- toggle criterion ---- */
  const toggleCriterion = useCallback((idx: number) => {
    setCriteriaChecked((prev) => ({ ...prev, [idx]: !prev[idx] }));
  }, []);

  /* ---- mark complete ---- */
  const handleMarkComplete = useCallback(() => {
    const nowComplete = toggleCompleted(labId);
    setIsComplete(nowComplete);
  }, [labId]);

  /* ---- run tests ---- */
  const handleRunTests = useCallback(async () => {
    if (!solution.trim()) return;
    setRunning(true);
    setActiveTab('results');
    setRunResult(null);

    try {
      const res = await fetch(`${API_BASE}/api/labs/${encodeURIComponent(labId)}/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ solution }),
      });
      const data: RunResponse = await res.json();
      setRunResult(data);
    } catch (e) {
      setRunResult({
        success: false,
        results: [],
        error: e instanceof Error ? e.message : 'Network error',
      });
    } finally {
      setRunning(false);
    }
  }, [labId, solution]);

  /* ---- copy to clipboard ---- */
  const handleCopy = useCallback(async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {}
  }, []);

  /* ---- format time ---- */
  function formatTime(mins: number): string {
    if (mins < 60) return lang === 'zh' ? `${mins} 分钟` : `${mins} min`;
    const h = Math.floor(mins / 60);
    const m = mins % 60;
    if (m === 0) return lang === 'zh' ? `${h} 小时` : `${h}h`;
    return lang === 'zh' ? `${h} 小时 ${m} 分` : `${h}h ${m}m`;
  }

  /* ---- keyboard: Tab in textarea ---- */
  const handleTextareaKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
      if (e.key === 'Tab') {
        e.preventDefault();
        const ta = e.currentTarget;
        const start = ta.selectionStart;
        const end = ta.selectionEnd;
        const val = ta.value;
        const newVal = val.substring(0, start) + '  ' + val.substring(end);
        setSolution(newVal);
        saveSolution(labId, newVal);
        // Restore cursor position after React re-renders
        requestAnimationFrame(() => {
          ta.selectionStart = ta.selectionEnd = start + 2;
        });
      }
    },
    [labId],
  );

  /* ================================================================ */
  /*  Loading / Error                                                  */
  /* ================================================================ */

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0a0a0a] flex items-center justify-center">
        <div className="text-gray-400 text-lg">
          {lang === 'zh' ? '加载实验...' : 'Loading lab...'}
        </div>
      </div>
    );
  }

  if (error || !lab) {
    return (
      <div className="min-h-screen bg-[#0a0a0a] flex items-center justify-center">
        <div className="text-center">
          <div className="text-4xl mb-4">⚠️</div>
          <div className="text-gray-400 text-lg mb-2">
            {lang === 'zh' ? '无法加载实验' : 'Failed to load lab'}
          </div>
          <div className="text-gray-600 text-sm mb-6">{error}</div>
          <Link
            href="/labs"
            className="px-4 py-2 rounded-lg bg-gray-800 text-gray-300 hover:bg-gray-700 text-sm transition-colors"
          >
            {lang === 'zh' ? '← 返回实验列表' : '← Back to Labs'}
          </Link>
        </div>
      </div>
    );
  }

  const diffMeta = DIFFICULTY_META[lab.difficulty] ?? DIFFICULTY_META.beginner;
  const criteriaDone = Object.values(criteriaChecked).filter(Boolean).length;
  const criteriaTotal = lab.acceptance_criteria?.length ?? 0;
  const allCriteriaMet = criteriaTotal > 0 && criteriaDone === criteriaTotal;
  const passedCount = runResult?.results?.filter((r) => r.passed).length ?? 0;
  const totalTests = runResult?.results?.length ?? 0;

  /* ================================================================ */
  /*  Render                                                           */
  /* ================================================================ */

  return (
    <div className="min-h-screen bg-[#0a0a0a]">
      {/* ============================================================ */}
      {/*  Header                                                       */}
      {/* ============================================================ */}
      <header className="border-b border-gray-800 bg-[#0a0a0a]/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link
              href="/labs"
              className="text-gray-400 hover:text-white transition-colors text-sm"
            >
              {lang === 'zh' ? '← 实验列表' : '← Labs'}
            </Link>
            <span className="text-gray-700">|</span>
            <span className="text-sm text-gray-500">{lab.track}</span>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={toggle}
              className="px-3 py-1 rounded-full text-xs font-medium bg-gray-800 text-gray-300 hover:bg-gray-700 border border-gray-700 transition-all"
            >
              {lang === 'zh' ? '中/EN' : 'EN/中'}
            </button>
            <button
              onClick={handleMarkComplete}
              className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-all ${
                isComplete
                  ? 'bg-green-500 text-white'
                  : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
              }`}
            >
              {isComplete
                ? lang === 'zh'
                  ? '✓ 已完成'
                  : '✓ Completed'
                : lang === 'zh'
                  ? '标记完成'
                  : 'Mark Complete'}
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-4 py-6">
        {/* ============================================================ */}
        {/*  Top: Lab meta info                                           */}
        {/* ============================================================ */}
        <div className="mb-6">
          <div className="flex items-center gap-3 mb-2">
            <span className="text-3xl">{lab.track_icon || '🧪'}</span>
            <div>
              <h1 className="text-2xl font-bold text-white">{lab.title}</h1>
              <div className="flex items-center gap-2 mt-1">
                <span
                  className={`text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded-full ${diffMeta.bg} ${diffMeta.color} border ${diffMeta.border}`}
                >
                  {diffMeta.label[lang]}
                </span>
                <span className="text-xs text-gray-500">
                  ⏱ {formatTime(lab.estimated_minutes)}
                </span>
              </div>
            </div>
          </div>
          <p className="text-gray-400 text-sm leading-relaxed mt-2 ml-11">
            {lab.description}
          </p>
        </div>

        {/* ============================================================ */}
        {/*  Two-column layout                                            */}
        {/* ============================================================ */}
        <div className="flex flex-col lg:flex-row gap-6">
          {/* ======================================================== */}
          {/*  Left panel: task + acceptance criteria                    */}
          {/* ======================================================== */}
          <aside className="lg:w-[380px] flex-shrink-0 space-y-4">
            {/* Task description */}
            <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-5">
              <h2 className="text-sm font-semibold text-gray-200 mb-3 flex items-center gap-2">
                <span>🎯</span>
                {lang === 'zh' ? '任务描述' : 'Task'}
              </h2>
              <div className="text-gray-300 text-sm leading-relaxed whitespace-pre-line">
                {lab.task}
              </div>
            </div>

            {/* Acceptance criteria */}
            {lab.acceptance_criteria && lab.acceptance_criteria.length > 0 && (
              <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-5">
                <div className="flex items-center justify-between mb-3">
                  <h2 className="text-sm font-semibold text-gray-200 flex items-center gap-2">
                    <span>✅</span>
                    {lang === 'zh' ? '验收标准' : 'Acceptance Criteria'}
                  </h2>
                  <span className="text-[11px] text-gray-500 tabular-nums">
                    {criteriaDone}/{criteriaTotal}
                  </span>
                </div>
                <div className="h-1 bg-gray-800 rounded-full mb-4">
                  <div
                    className="h-full bg-emerald-500 rounded-full transition-all duration-300"
                    style={{
                      width: criteriaTotal ? `${(criteriaDone / criteriaTotal) * 100}%` : '0%',
                    }}
                  />
                </div>
                <ul className="space-y-2">
                  {lab.acceptance_criteria.map((criterion, i) => (
                    <li key={i}>
                      <button
                        onClick={() => toggleCriterion(i)}
                        className="w-full text-left flex items-start gap-2.5 group"
                      >
                        <span
                          className={`mt-0.5 w-4 h-4 rounded flex-shrink-0 flex items-center justify-center text-[10px] border transition-all ${
                            criteriaChecked[i]
                              ? 'bg-green-500 border-green-500 text-white'
                              : 'border-gray-600 group-hover:border-gray-400'
                          }`}
                        >
                          {criteriaChecked[i] && '✓'}
                        </span>
                        <span
                          className={`text-sm leading-relaxed transition-colors ${
                            criteriaChecked[i]
                              ? 'text-gray-500 line-through'
                              : 'text-gray-300'
                          }`}
                        >
                          {criterion}
                        </span>
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Progress summary */}
            <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-5">
              <h2 className="text-sm font-semibold text-gray-200 mb-3">
                {lang === 'zh' ? '进度' : 'Progress'}
              </h2>
              <div className="space-y-2 text-xs text-gray-400">
                <div className="flex justify-between">
                  <span>{lang === 'zh' ? '验收标准' : 'Criteria'}</span>
                  <span className={allCriteriaMet ? 'text-green-400' : 'text-gray-400'}>
                    {criteriaDone}/{criteriaTotal}
                  </span>
                </div>
                {runResult && (
                  <div className="flex justify-between">
                    <span>{lang === 'zh' ? '测试通过' : 'Tests Passed'}</span>
                    <span
                      className={
                        runResult.success && passedCount === totalTests
                          ? 'text-green-400'
                          : 'text-red-400'
                      }
                    >
                      {passedCount}/{totalTests}
                    </span>
                  </div>
                )}
                <div className="flex justify-between">
                  <span>{lang === 'zh' ? '状态' : 'Status'}</span>
                  <span className={isComplete ? 'text-green-400' : 'text-amber-400'}>
                    {isComplete
                      ? lang === 'zh'
                        ? '已完成'
                        : 'Completed'
                      : lang === 'zh'
                        ? '进行中'
                        : 'In Progress'}
                  </span>
                </div>
              </div>
            </div>

            {/* Back to track */}
            {lab.track && (
              <Link
                href="/"
                className="block text-center text-xs text-gray-500 hover:text-gray-300 transition-colors py-2"
              >
                {lang === 'zh'
                  ? `← 返回 ${lab.track}`
                  : `← Back to ${lab.track}`}
              </Link>
            )}
          </aside>

          {/* ======================================================== */}
          {/*  Right panel: code tabs                                    */}
          {/* ======================================================== */}
          <div className="flex-1 min-w-0">
            {/* Tab bar */}
            <div className="flex border-b border-gray-800 mb-0">
              {TAB_DEFS.map((tab) => (
                <button
                  key={tab.key}
                  onClick={() => setActiveTab(tab.key)}
                  className={`px-4 py-2.5 text-sm font-medium transition-all relative ${
                    activeTab === tab.key
                      ? 'text-white'
                      : 'text-gray-500 hover:text-gray-300'
                  }`}
                >
                  <span className="mr-1.5">{tab.icon}</span>
                  {tab.label[lang]}
                  {activeTab === tab.key && (
                    <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-emerald-500" />
                  )}
                  {tab.key === 'results' && runResult && (
                    <span
                      className={`ml-2 text-[10px] px-1.5 py-0.5 rounded-full ${
                        runResult.success
                          ? 'bg-green-900/50 text-green-400'
                          : 'bg-red-900/50 text-red-400'
                      }`}
                    >
                      {passedCount}/{totalTests}
                    </span>
                  )}
                </button>
              ))}
            </div>

            {/* Tab content */}
            <div className="rounded-b-xl border border-t-0 border-gray-800 bg-[#1a1a2e] min-h-[400px]">
              {/* ---- Starter Code tab ---- */}
              {activeTab === 'starter' && (
                <div className="relative">
                  <div className="flex items-center justify-between px-4 py-2 border-b border-gray-800/60">
                    <span className="text-xs text-gray-500 font-mono">
                      {lab.language || 'code'}
                    </span>
                    <button
                      onClick={() => handleCopy(lab.starter_code || '')}
                      className="px-2.5 py-1 rounded text-[11px] text-gray-400 hover:text-white hover:bg-gray-700/50 transition-all"
                    >
                      {copied
                        ? lang === 'zh'
                          ? '已复制'
                          : 'Copied'
                        : lang === 'zh'
                          ? '复制'
                          : 'Copy'}
                    </button>
                  </div>
                  <pre className="p-5 overflow-x-auto text-sm font-mono text-gray-300 leading-relaxed">
                    <code>{lab.starter_code || (lang === 'zh' ? '// 暂无初始代码' : '// No starter code provided')}</code>
                  </pre>
                </div>
              )}

              {/* ---- Test File tab ---- */}
              {activeTab === 'test' && (
                <div className="relative">
                  <div className="flex items-center justify-between px-4 py-2 border-b border-gray-800/60">
                    <span className="text-xs text-gray-500 font-mono">
                      test
                    </span>
                    <button
                      onClick={() => handleCopy(lab.test_file || '')}
                      className="px-2.5 py-1 rounded text-[11px] text-gray-400 hover:text-white hover:bg-gray-700/50 transition-all"
                    >
                      {lang === 'zh' ? '复制' : 'Copy'}
                    </button>
                  </div>
                  <pre className="p-5 overflow-x-auto text-sm font-mono text-gray-300 leading-relaxed">
                    <code>{lab.test_file || (lang === 'zh' ? '// 暂无测试文件' : '// No test file provided')}</code>
                  </pre>
                </div>
              )}

              {/* ---- Solution tab ---- */}
              {activeTab === 'solution' && (
                <div className="flex flex-col">
                  <div className="flex items-center justify-between px-4 py-2 border-b border-gray-800/60">
                    <span className="text-xs text-gray-500">
                      {lang === 'zh'
                        ? '在此编写或粘贴你的解答'
                        : 'Write or paste your solution below'}
                    </span>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => {
                          if (lab.starter_code && !solution.trim()) {
                            handleSolutionChange(lab.starter_code);
                          }
                        }}
                        className="px-2.5 py-1 rounded text-[11px] text-gray-400 hover:text-white hover:bg-gray-700/50 transition-all"
                      >
                        {lang === 'zh' ? '填入初始代码' : 'Load Starter'}
                      </button>
                      <button
                        onClick={() => handleCopy(solution)}
                        className="px-2.5 py-1 rounded text-[11px] text-gray-400 hover:text-white hover:bg-gray-700/50 transition-all"
                      >
                        {lang === 'zh' ? '复制' : 'Copy'}
                      </button>
                    </div>
                  </div>
                  <textarea
                    ref={textareaRef}
                    value={solution}
                    onChange={(e) => handleSolutionChange(e.target.value)}
                    onKeyDown={handleTextareaKeyDown}
                    spellCheck={false}
                    className="w-full flex-1 min-h-[400px] bg-transparent p-5 text-sm font-mono text-gray-300 leading-relaxed resize-none focus:outline-none placeholder-gray-600"
                    placeholder={
                      lang === 'zh'
                        ? '# 在此编写你的代码...\n# 按 Tab 插入两个空格'
                        : '# Write your code here...\n# Press Tab to insert two spaces'
                    }
                  />
                </div>
              )}

              {/* ---- Results tab ---- */}
              {activeTab === 'results' && (
                <div className="p-5">
                  {running ? (
                    <div className="flex items-center gap-3 text-gray-400 py-10 justify-center">
                      <div className="w-4 h-4 border-2 border-gray-600 border-t-emerald-400 rounded-full animate-spin" />
                      {lang === 'zh' ? '正在运行测试...' : 'Running tests...'}
                    </div>
                  ) : runResult ? (
                    <div className="space-y-4">
                      {/* Overall status */}
                      <div
                        className={`flex items-center gap-3 px-4 py-3 rounded-lg border ${
                          runResult.success && passedCount === totalTests
                            ? 'bg-green-900/20 border-green-700/50'
                            : 'bg-red-900/20 border-red-700/50'
                        }`}
                      >
                        <span className="text-lg">
                          {runResult.success && passedCount === totalTests
                            ? '✅'
                            : '❌'}
                        </span>
                        <div>
                          <div
                            className={`font-semibold text-sm ${
                              runResult.success && passedCount === totalTests
                                ? 'text-green-300'
                                : 'text-red-300'
                            }`}
                          >
                            {runResult.success && passedCount === totalTests
                              ? lang === 'zh'
                                ? '全部通过!'
                                : 'All tests passed!'
                              : lang === 'zh'
                                ? `${totalTests - passedCount} 个测试未通过`
                                : `${totalTests - passedCount} test(s) failed`}
                          </div>
                          <div className="text-xs text-gray-500">
                            {passedCount}/{totalTests}{' '}
                            {lang === 'zh' ? '通过' : 'passed'}
                          </div>
                        </div>
                      </div>

                      {/* Console output */}
                      {runResult.output && (
                        <div className="rounded-lg border border-gray-800 overflow-hidden">
                          <div className="px-4 py-2 bg-gray-900/80 border-b border-gray-800">
                            <span className="text-xs text-gray-500 font-mono">
                              {lang === 'zh' ? '控制台输出' : 'Console Output'}
                            </span>
                          </div>
                          <pre className="p-4 text-xs font-mono text-gray-400 overflow-x-auto">
                            {runResult.output}
                          </pre>
                        </div>
                      )}

                      {/* Individual test results */}
                      {runResult.results.length > 0 && (
                        <div className="space-y-2">
                          {runResult.results.map((r, i) => (
                            <div
                              key={i}
                              className={`rounded-lg border px-4 py-3 ${
                                r.passed
                                  ? 'border-green-800/40 bg-green-900/10'
                                  : 'border-red-800/40 bg-red-900/10'
                              }`}
                            >
                              <div className="flex items-center gap-2">
                                <span className={r.passed ? 'text-green-400' : 'text-red-400'}>
                                  {r.passed ? '✓' : '✗'}
                                </span>
                                <span className="text-sm text-gray-200 font-mono">
                                  {r.name}
                                </span>
                              </div>
                              {r.message && (
                                <div className="mt-1.5 text-xs text-gray-400 ml-5">
                                  {r.message}
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      )}

                      {/* Error */}
                      {runResult.error && (
                        <div className="rounded-lg border border-red-800/40 bg-red-900/10 px-4 py-3">
                          <div className="text-sm text-red-300 font-mono whitespace-pre-wrap">
                            {runResult.error}
                          </div>
                        </div>
                      )}
                    </div>
                  ) : (
                    <div className="text-center text-gray-500 py-16">
                      <span className="text-3xl block mb-3">🚀</span>
                      {lang === 'zh'
                        ? '点击下方「运行测试」按钮开始验证'
                        : 'Click "Run Tests" below to verify your solution'}
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* ======================================================== */}
            {/*  Bottom action bar                                         */}
            {/* ======================================================== */}
            <div className="mt-4 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <button
                  onClick={handleRunTests}
                  disabled={running || !solution.trim()}
                  className="px-5 py-2.5 rounded-lg bg-emerald-600 text-white text-sm font-medium hover:bg-emerald-700 disabled:opacity-40 disabled:cursor-not-allowed transition-all flex items-center gap-2"
                >
                  {running ? (
                    <>
                      <div className="w-3.5 h-3.5 border-2 border-emerald-300 border-t-transparent rounded-full animate-spin" />
                      {lang === 'zh' ? '运行中...' : 'Running...'}
                    </>
                  ) : (
                    <>
                      <span>▶</span>
                      {lang === 'zh' ? '运行测试' : 'Run Tests'}
                    </>
                  )}
                </button>

                <button
                  onClick={handleMarkComplete}
                  className={`px-5 py-2.5 rounded-lg text-sm font-medium transition-all ${
                    isComplete
                      ? 'bg-green-500 text-white'
                      : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                  }`}
                >
                  {isComplete
                    ? lang === 'zh'
                      ? '✓ 已完成'
                      : '✓ Completed'
                    : lang === 'zh'
                      ? '标记完成'
                      : 'Mark Complete'}
                </button>
              </div>

              {/* Solution length indicator */}
              <span className="text-[11px] text-gray-600 tabular-nums">
                {solution.length}{' '}
                {lang === 'zh' ? '字符' : 'chars'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
