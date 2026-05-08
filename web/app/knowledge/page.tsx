'use client';

import { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import Link from 'next/link';
import PredictOutput from '@/components/games/PredictOutput';
import FindBug from '@/components/games/FindBug';
import FillBlank from '@/components/games/FillBlank';
import CodeOrder from '@/components/games/CodeOrder';
import { useLang } from '@/lib/i18n';

const API = 'http://localhost:8000';

/* ------------------------------------------------------------------ */
/*  Types                                                              */
/* ------------------------------------------------------------------ */

interface QuizQuestion {
  question: string;
  options: string[];
  correct: number;
  explanation: string;
}

interface KnowledgePoint {
  id: string;
  week: number;
  module: string;
  title: string;
  explanation: string;
  code: string;
  game: { type: string; title: string; instructions: string; content: Record<string, unknown> } | string;
  quiz: QuizQuestion;
}

interface WeekModule {
  module: string;
  count: number;
}

interface WeekInfo {
  week: number;
  modules: WeekModule[];
  total_points: number;
}

type GameType = 'predict_output' | 'find_bug' | 'fill_blank' | 'code_order';

/* ------------------------------------------------------------------ */
/*  localStorage helpers                                               */
/* ------------------------------------------------------------------ */

const STORAGE_KEY = 'kp_completed';

function loadCompleted(): Set<string> {
  if (typeof window === 'undefined') return new Set();
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? new Set(JSON.parse(raw)) : new Set();
  } catch {
    return new Set();
  }
}

function saveCompleted(ids: Set<string>) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify([...ids]));
}

/* ------------------------------------------------------------------ */
/*  Debounce hook                                                      */
/* ------------------------------------------------------------------ */

function useDebouncedCallback(fn: (q: string) => void, delay: number) {
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  return useCallback(
    (q: string) => {
      if (timerRef.current) clearTimeout(timerRef.current);
      timerRef.current = setTimeout(() => fn(q), delay);
    },
    [fn, delay],
  );
}

/* ------------------------------------------------------------------ */
/*  Sidebar virtualization constants                                   */
/* ------------------------------------------------------------------ */

const SIDEBAR_ITEM_H = 40;
const SIDEBAR_BUFFER = 10;
const SIDEBAR_VISIBLE_H = 480;

/* ------------------------------------------------------------------ */
/*  Game type detection                                                */
/* ------------------------------------------------------------------ */

function getGameType(game: KnowledgePoint['game']): GameType | null {
  if (!game) return null;
  try {
    const obj = typeof game === 'string' ? JSON.parse(game) : game;
    if (obj && typeof obj === 'object' && obj.type) {
      const t = obj.type as string;
      if (['predict_output', 'find_bug', 'fill_blank', 'code_order'].includes(t)) {
        return t as GameType;
      }
    }
  } catch {
    // not valid JSON
  }
  return null;
}

/* ------------------------------------------------------------------ */
/*  Component                                                          */
/* ------------------------------------------------------------------ */

export default function KnowledgePage() {
  const { lang, toggle, t } = useLang();
  /* ---- state ---- */
  const [weeks, setWeeks] = useState<WeekInfo[]>([]);
  const [points, setPoints] = useState<KnowledgePoint[]>([]);
  const [completed, setCompleted] = useState<Set<string>>(new Set());
  const [activeWeek, setActiveWeek] = useState(1);
  const [activeModule, setActiveModule] = useState<string | null>(null);
  const [activePointIdx, setActivePointIdx] = useState(0);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<KnowledgePoint[] | null>(null);
  const [expandedExplanations, setExpandedExplanations] = useState<Set<string>>(new Set());
  const [quizAnswers, setQuizAnswers] = useState<Record<string, Record<number, number>>>({});
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<{ total: number; completed: number } | null>(null);
  const [gameTypeFilter, setGameTypeFilter] = useState<GameType | null>(null);
  const [randomPool, setRandomPool] = useState<KnowledgePoint[] | null>(null);
  const [sidebarScrollTop, setSidebarScrollTop] = useState(0);
  const sidebarRef = useRef<HTMLDivElement>(null);

  /* ---- load weeks on mount ---- */
  useEffect(() => {
    setCompleted(loadCompleted());

    Promise.all([
      fetch(`${API}/api/weeks`).then((r) => r.json()),
      fetch(`${API}/api/knowledge-points/stats`).then((r) => r.json()).catch(() => null),
    ])
      .then(([w, s]) => {
        setWeeks(w);
        setStats(s);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  /* ---- load points when week / module changes ---- */
  useEffect(() => {
    if (searchQuery || randomPool) return;
    setLoading(true);
    const params = new URLSearchParams({ week: String(activeWeek) });
    if (activeModule) params.set('module', activeModule);

    fetch(`${API}/api/knowledge-points?${params}`)
      .then((r) => r.json())
      .then((data) => {
        const raw = data.points || data;
        const pts: KnowledgePoint[] = Array.isArray(raw)
          ? raw.map((p: Record<string, unknown>, i: number) => ({
              ...p,
              id: p.id || `${p.week}-${p.module}-${i}`,
            }) as KnowledgePoint)
          : [];
        setPoints(pts);
        setActivePointIdx(0);
        setExpandedExplanations(new Set(pts.map((p) => p.id)));
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [activeWeek, activeModule, searchQuery, randomPool]);

  /* ---- search (with debounce) ---- */
  const doSearch = useCallback(
    async (q: string) => {
      setSearchQuery(q);
      setRandomPool(null);
      if (!q.trim()) {
        setSearchResults(null);
        return;
      }
      const res = await fetch(`${API}/api/knowledge-points?per_page=1000`);
      const data = await res.json();
      const raw = data.points || data || [];
      const all: KnowledgePoint[] = Array.isArray(raw)
        ? raw.map((p: Record<string, unknown>, i: number) => ({
            ...p,
            id: p.id || `${p.week}-${p.module}-${i}`,
          }) as KnowledgePoint)
        : [];
      const lower = q.toLowerCase();
      setSearchResults(
        all.filter(
          (p) =>
            p.title.toLowerCase().includes(lower) ||
            p.explanation.toLowerCase().includes(lower) ||
            p.module.toLowerCase().includes(lower),
        ),
      );
    },
    [],
  );

  const debouncedSearch = useDebouncedCallback(doSearch, 300);

  /* ---- random review ---- */
  const pickRandom = useCallback(() => {
    const source = searchResults ?? points;
    if (source.length === 0) return;
    const shuffled = [...source].sort(() => Math.random() - 0.5);
    const picked = shuffled.slice(0, Math.min(10, shuffled.length));
    setRandomPool(picked);
    setSearchResults(null);
    setSearchQuery('');
    setActivePointIdx(0);
    setExpandedExplanations(new Set(picked.map((p) => p.id)));
  }, [points, searchResults]);

  const clearRandom = useCallback(() => {
    setRandomPool(null);
    setActivePointIdx(0);
  }, []);

  /* ---- toggle completed ---- */
  const toggleCompleted = useCallback((id: string) => {
    setCompleted((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      saveCompleted(next);
      return next;
    });
  }, []);

  /* ---- toggle explanation collapse ---- */
  const toggleExplanation = useCallback((id: string) => {
    setExpandedExplanations((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }, []);

  /* ---- quiz answer ---- */
  const handleQuizAnswer = useCallback((pointId: string, qi: number, answer: number) => {
    setQuizAnswers((prev) => ({
      ...prev,
      [pointId]: { ...(prev[pointId] || {}), [qi]: answer },
    }));
  }, []);

  /* ---- derived data ---- */
  const displayPoints = useMemo(() => {
    let list = randomPool ?? searchResults ?? points;
    if (gameTypeFilter && !randomPool && !searchResults) {
      list = list.filter((p) => getGameType(p.game) === gameTypeFilter);
    }
    return list;
  }, [randomPool, searchResults, points, gameTypeFilter]);

  const currentPoint = displayPoints[activePointIdx] ?? null;

  const modulesForWeek = useMemo(() => {
    const wi = weeks.find((w) => w.week === activeWeek);
    return wi?.modules ?? [];
  }, [weeks, activeWeek]);

  const weekProgress = useMemo(() => {
    const ids = points.map((p) => p.id);
    const done = ids.filter((id) => completed.has(id)).length;
    return { done, total: ids.length };
  }, [points, completed]);

  const weekComplete = weekProgress.total > 0 && weekProgress.done === weekProgress.total;

  const progressPct = weekProgress.total
    ? Math.round((weekProgress.done / weekProgress.total) * 100)
    : 0;

  /* ---- navigation helpers ---- */
  const goPrev = () => setActivePointIdx((i) => Math.max(0, i - 1));
  const goNext = () => setActivePointIdx((i) => Math.min(displayPoints.length - 1, i + 1));

  /* ---- keyboard nav: j/k/Enter ---- */
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;
      switch (e.key) {
        case 'ArrowLeft':
        case 'k':
          e.preventDefault();
          goPrev();
          break;
        case 'ArrowRight':
        case 'j':
          e.preventDefault();
          goNext();
          break;
        case 'Enter':
          e.preventDefault();
          if (currentPoint) toggleExplanation(currentPoint.id);
          break;
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [displayPoints.length, currentPoint, toggleExplanation]);

  /* ---- sidebar virtualization ---- */
  const startIdx = Math.max(0, Math.floor(sidebarScrollTop / SIDEBAR_ITEM_H) - SIDEBAR_BUFFER);
  const endIdx = Math.min(
    displayPoints.length,
    Math.ceil((sidebarScrollTop + SIDEBAR_VISIBLE_H) / SIDEBAR_ITEM_H) + SIDEBAR_BUFFER,
  );
  const visibleSidebarItems = displayPoints.slice(startIdx, endIdx);

  /* ---------------------------------------------------------------- */
  /*  Render                                                           */
  /* ---------------------------------------------------------------- */

  if (loading && weeks.length === 0) {
    return (
      <div className="min-h-screen bg-[#0a0a0a] flex items-center justify-center">
        <div className="text-gray-400 text-lg">{t('kp.loading')}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0a0a0a]">
      {/* ============================================================ */}
      {/*  Header                                                       */}
      {/* ============================================================ */}
      <header className="border-b border-gray-800 bg-[#0a0a0a]/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link
              href="/"
              className="text-gray-400 hover:text-white transition-colors text-sm"
            >
              {t('nav.home')}
            </Link>
            <h1 className="text-lg font-bold bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
              {t('kp.title')}
            </h1>
          </div>

          <div className="flex items-center gap-3">
            {/* Language toggle */}
            <button
              onClick={toggle}
              className="px-3 py-1 rounded-full text-xs font-medium bg-gray-800 text-gray-300 hover:bg-gray-700 border border-gray-700 transition-all"
            >
              {lang === 'zh' ? '中/EN' : 'EN/中'}
            </button>

            {/* Random Review button */}
            {randomPool ? (
              <button
                onClick={clearRandom}
                className="px-3 py-1.5 rounded-lg text-xs font-medium bg-amber-600 text-white hover:bg-amber-700 transition-colors"
              >
                {t('kp.exit_random')} ({randomPool.length})
              </button>
            ) : (
              <button
                onClick={pickRandom}
                disabled={points.length === 0}
                className="px-3 py-1.5 rounded-lg text-xs font-medium bg-gray-800 text-gray-300 hover:bg-gray-700 disabled:opacity-30 transition-colors"
              >
                {t('kp.random')}
              </button>
            )}

            {/* Search with debounce */}
            <div className="relative w-64">
              <input
                type="text"
                placeholder={t('kp.search')}
                value={searchQuery}
                onChange={(e) => debouncedSearch(e.target.value)}
                className="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-1.5 text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:border-cyan-500 transition-colors"
              />
              {searchQuery && (
                <button
                  onClick={() => debouncedSearch('')}
                  className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-500 hover:text-white text-xs"
                >
                  ✕
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Progress bar with percentage */}
        <div className="h-1 bg-gray-800 relative">
          <div
            className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 transition-all duration-500"
            style={{ width: `${progressPct}%` }}
          />
          <span className="absolute right-2 -top-5 text-[10px] text-gray-500 tabular-nums">
            {progressPct}%
          </span>
        </div>
      </header>

      {/* ============================================================ */}
      {/*  Congratulations banner                                       */}
      {/* ============================================================ */}
      {weekComplete && !randomPool && !searchResults && (
        <div className="max-w-7xl mx-auto px-4 pt-4">
          <div className="rounded-xl border border-green-600/40 bg-green-900/20 px-6 py-4 flex items-center gap-3 animate-fade-in">
            <span className="text-2xl">&#127881;</span>
            <div>
              <p className="text-green-300 font-semibold">{lang === 'zh' ? `第 ${activeWeek} 周完成！` : `Week ${activeWeek} Complete!`}</p>
              <p className="text-green-400/70 text-sm">
                {lang === 'zh' ? `所有 ${weekProgress.total} 个知识点已掌握，做得好！` : `All ${weekProgress.total} knowledge points mastered. Great work!`}
              </p>
            </div>
          </div>
        </div>
      )}

      <div className="max-w-7xl mx-auto px-4 py-6">
        {/* ============================================================ */}
        {/*  Week Selector                                                */}
        {/* ============================================================ */}
        {!searchResults && !randomPool && (
          <div className="flex gap-2 overflow-x-auto pb-2 mb-4 scrollbar-hide">
            {weeks.map((w) => (
              <button
                key={w.week}
                onClick={() => {
                  setActiveWeek(w.week);
                  setActiveModule(null);
                  setSearchQuery('');
                  setSearchResults(null);
                  setGameTypeFilter(null);
                }}
                className={`flex-shrink-0 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  activeWeek === w.week
                    ? 'bg-cyan-600 text-white shadow-lg shadow-cyan-500/20'
                    : 'bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-white'
                }`}
              >
                {lang === 'zh' ? `第 ${w.week} 周` : `Week ${w.week}`}
              </button>
            ))}
          </div>
        )}

        {/* ============================================================ */}
        {/*  Module Filter + Game Type Filter                             */}
        {/* ============================================================ */}
        {!searchResults && !randomPool && modulesForWeek.length > 0 && (
          <div className="flex gap-2 flex-wrap mb-6">
            <button
              onClick={() => setActiveModule(null)}
              className={`px-3 py-1.5 rounded-full text-xs transition-all ${
                !activeModule
                  ? 'bg-white text-black font-medium'
                  : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
              }`}
            >
              {t('cat.all')}
            </button>
            {modulesForWeek.map((mod) => {
              const count = points.filter((p) => p.module === mod.module).length;
              const done = points.filter((p) => p.module === mod.module && completed.has(p.id)).length;
              return (
                <button
                  key={mod.module}
                  onClick={() => setActiveModule(activeModule === mod.module ? null : mod.module)}
                  className={`px-3 py-1.5 rounded-full text-xs transition-all ${
                    activeModule === mod.module
                      ? 'bg-white text-black font-medium'
                      : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                  }`}
                >
                  {mod.module} ({done}/{count})
                </button>
              );
            })}

            {/* Game type filters */}
            <span className="border-l border-gray-700 mx-1 self-stretch" />
            {(['predict_output', 'find_bug', 'fill_blank', 'code_order'] as GameType[]).map((gt) => {
              const labels: Record<GameType, string> = {
                predict_output: t('game.predict'),
                find_bug: t('game.find_bug'),
                fill_blank: t('game.fill_blank'),
                code_order: t('game.code_order'),
              };
              return (
                <button
                  key={gt}
                  onClick={() => setGameTypeFilter(gameTypeFilter === gt ? null : gt)}
                  className={`px-3 py-1.5 rounded-full text-xs transition-all ${
                    gameTypeFilter === gt
                      ? 'bg-amber-600 text-white font-medium'
                      : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                  }`}
                >
                  {labels[gt]}
                </button>
              );
            })}
          </div>
        )}

        {/* Random review label */}
        {randomPool && (
          <div className="flex items-center gap-2 mb-4">
            <span className="text-xs px-2 py-0.5 rounded-full bg-amber-900/50 text-amber-300 border border-amber-700/50">
              {lang === 'zh' ? '随机复习' : 'Random Review'}
            </span>
            <span className="text-xs text-gray-500">
              {lang === 'zh' ? `已选 ${randomPool.length} 个知识点` : `${randomPool.length} points selected`}
            </span>
          </div>
        )}

        {/* ============================================================ */}
        {/*  Main Layout: sidebar + content                               */}
        {/* ============================================================ */}
        <div className="flex gap-6">
          {/* ---- Sidebar: point list (virtualized) ---- */}
          <aside className="w-64 flex-shrink-0 hidden lg:block">
            <div className="sticky top-28">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-2 px-2">
                {randomPool
                  ? `${lang === 'zh' ? '随机' : 'Random'} (${displayPoints.length})`
                  : searchResults
                  ? `${lang === 'zh' ? '搜索结果' : 'Search Results'} (${searchResults.length})`
                  : `${lang === 'zh' ? `第 ${activeWeek} 周` : `Week ${activeWeek}`}`}
              </div>
              <div
                ref={sidebarRef}
                className="space-y-0 overflow-y-auto"
                style={{ maxHeight: `${SIDEBAR_VISIBLE_H}px` }}
                onScroll={(e) => setSidebarScrollTop((e.target as HTMLDivElement).scrollTop)}
              >
                {/* Top spacer */}
                <div style={{ height: `${startIdx * SIDEBAR_ITEM_H}px` }} />
                {visibleSidebarItems.map((p) => {
                  const i = displayPoints.indexOf(p);
                  return (
                    <button
                      key={p.id}
                      onClick={() => setActivePointIdx(i)}
                      style={{ height: `${SIDEBAR_ITEM_H}px` }}
                      className={`w-full text-left px-3 rounded-lg text-sm transition-all flex items-center gap-2 ${
                        activePointIdx === i
                          ? 'bg-cyan-600/20 text-cyan-300 border border-cyan-600/40'
                          : 'text-gray-400 hover:text-white hover:bg-gray-800'
                      }`}
                    >
                      <span
                        className={`w-4 h-4 rounded-full flex-shrink-0 flex items-center justify-center text-[10px] border ${
                          completed.has(p.id)
                            ? 'bg-green-500 border-green-500 text-white'
                            : 'border-gray-600'
                        }`}
                      >
                        {completed.has(p.id) && '✓'}
                      </span>
                      <span className="truncate">{p.title}</span>
                    </button>
                  );
                })}
                {/* Bottom spacer */}
                <div
                  style={{
                    height: `${Math.max(0, (displayPoints.length - endIdx) * SIDEBAR_ITEM_H)}px`,
                  }}
                />
                {displayPoints.length === 0 && !loading && (
                  <div className="text-gray-500 text-sm px-2 py-4">{t('kp.no_points')}</div>
                )}
              </div>
            </div>
          </aside>

          {/* ---- Main content ---- */}
          <main className="flex-1 min-w-0">
            {currentPoint ? (
              <div className="animate-fade-in" key={currentPoint.id}>
                {/* Top bar */}
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <span className="text-xs px-2 py-0.5 rounded-full bg-cyan-900/50 text-cyan-300 border border-cyan-700/50">
                      Week {currentPoint.week}
                    </span>
                    <span className="text-xs px-2 py-0.5 rounded-full bg-gray-800 text-gray-400">
                      {currentPoint.module}
                    </span>
                  </div>
                  <button
                    onClick={() => toggleCompleted(currentPoint.id)}
                    className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-all ${
                      completed.has(currentPoint.id)
                        ? 'bg-green-500 text-white'
                        : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                    }`}
                  >
                    {completed.has(currentPoint.id) ? t('action.completed') : t('action.mark_complete')}
                  </button>
                </div>

                {/* Title */}
                <h2 className="text-2xl font-bold text-white mb-6">{currentPoint.title}</h2>

                {/* ---- Explanation (collapsible) ---- */}
                <section className="rounded-xl border border-gray-800 bg-gray-900/50 mb-4">
                  <button
                    onClick={() => toggleExplanation(currentPoint.id)}
                    className="w-full flex items-center justify-between px-6 py-4 text-left"
                  >
                    <h3 className="font-semibold text-gray-200">{t('section.explanation')}</h3>
                    <span className="text-gray-500 text-sm">
                      {expandedExplanations.has(currentPoint.id) ? '▲' : '▼'}
                    </span>
                  </button>
                  {expandedExplanations.has(currentPoint.id) && (
                    <div className="px-6 pb-5 text-gray-300 leading-relaxed text-sm whitespace-pre-line border-t border-gray-800 pt-4">
                      {currentPoint.explanation}
                    </div>
                  )}
                </section>

                {/* ---- Code Example ---- */}
                {currentPoint.code && (
                  <section className="rounded-xl border border-gray-800 bg-gray-900/50 mb-4 overflow-hidden">
                    <div className="px-6 py-3 border-b border-gray-800 flex items-center justify-between">
                      <h3 className="font-semibold text-gray-200">{t('section.code')}</h3>
                    </div>
                    <pre className="p-6 overflow-x-auto text-sm">
                      <code className="text-gray-300 font-mono leading-relaxed">
                        {currentPoint.code}
                      </code>
                    </pre>
                  </section>
                )}

                {/* ---- Mini-game / Puzzle ---- */}
                {currentPoint.game && (() => {
                  const gameObj = typeof currentPoint.game === 'string'
                    ? null
                    : currentPoint.game as { type: string; content?: Record<string, unknown>; instructions?: string };
                  const gameType = gameObj?.type;
                  const c = (gameObj?.content || {}) as Record<string, unknown>;

                  if (!gameType || !['predict_output', 'find_bug', 'fill_blank', 'code_order'].includes(gameType)) {
                    return (
                      <section className="rounded-xl border border-amber-700/50 bg-amber-900/10 mb-4 overflow-hidden">
                        <div className="px-6 py-3 border-b border-amber-700/40 flex items-center gap-2">
                          <span className="text-base">&#129513;</span>
                          <h3 className="font-semibold text-amber-200">{t('game.challenge')}</h3>
                        </div>
                        <div className="p-6 text-gray-300 text-sm leading-relaxed whitespace-pre-line">
                          {typeof currentPoint.game === 'string'
                            ? currentPoint.game
                            : gameObj?.instructions || ''}
                        </div>
                      </section>
                    );
                  }

                  return (
                    <section className="rounded-xl border border-amber-700/50 bg-amber-900/10 mb-4 overflow-hidden">
                      <div className="px-6 py-3 border-b border-amber-700/40 flex items-center gap-2">
                        <span className="text-base">&#129513;</span>
                        <h3 className="font-semibold text-amber-200">Mini Challenge</h3>
                      </div>
                      <div className="p-6">
                        {gameType === 'predict_output' && (
                          <PredictOutput
                            code={String(c.code || '')}
                            options={Array.isArray(c.options) ? c.options as string[] : []}
                            correctIndex={Number(c.correct ?? 0)}
                            explanation={String(c.explanation || '')}
                          />
                        )}
                        {gameType === 'find_bug' && (
                          <FindBug
                            code={Array.isArray(c.code_lines) ? (c.code_lines as string[]).join('\n') : String(c.code || '')}
                            bugLineIndex={Number(c.bug_line ?? 0)}
                            explanation={String(c.explanation || '')}
                          />
                        )}
                        {gameType === 'fill_blank' && (() => {
                          const rawBlanks = Array.isArray(c.blanks) ? c.blanks as Record<string, unknown>[] : [];
                          const blanks = rawBlanks.map((b, i) => ({
                            id: String(b.position ?? i),
                            answer: String(b.answer || ''),
                            hint: String(b.hint || ''),
                          }));
                          // Preprocess template: replace each ___ with ___ID___
                          let template = String(c.code || '');
                          let blankIdx = 0;
                          template = template.replace(/___/g, () => {
                            const id = String(blankIdx < blanks.length ? blankIdx : blanks.length);
                            blankIdx++;
                            return `___${id}___`;
                          });
                          return (
                            <FillBlank
                              template={template}
                              blanks={blanks}
                              explanation={String(c.explanation || '')}
                            />
                          );
                        })()}
                        {gameType === 'code_order' && (
                          <CodeOrder
                            lines={Array.isArray(c.lines) ? c.lines as string[] : []}
                            explanation={String(c.explanation || '')}
                          />
                        )}
                      </div>
                    </section>
                  );
                })()}

                {/* ---- Quiz ---- */}
                {currentPoint.quiz && currentPoint.quiz.question && (
                  <section className="rounded-xl border border-purple-700/50 bg-purple-900/10 mb-4 overflow-hidden">
                    <div className="px-6 py-3 border-b border-purple-700/40">
                      <h3 className="font-semibold text-purple-200">{t('quiz.title')}</h3>
                    </div>
                    <div className="p-6 space-y-6">
                      {(() => {
                        const q = currentPoint.quiz;
                        const pointAnswers = quizAnswers[currentPoint.id] || {};
                        const answered = pointAnswers[0] !== undefined;
                        const selected = pointAnswers[0];

                        return (
                          <div>
                            <p className="font-medium text-gray-200 mb-3">{q.question}</p>
                            <div className="space-y-2">
                              {q.options.map((opt, oi) => {
                                const isCorrect = oi === q.correct;
                                let cls = 'bg-gray-800 hover:bg-gray-700 border-transparent';
                                if (answered) {
                                  if (selected === oi && isCorrect)
                                    cls = 'bg-green-800/60 border-green-500';
                                  else if (selected === oi && !isCorrect)
                                    cls = 'bg-red-800/60 border-red-500';
                                  else if (isCorrect)
                                    cls = 'bg-green-800/20 border-green-700/50';
                                }

                                return (
                                  <button
                                    key={oi}
                                    disabled={answered}
                                    onClick={() => handleQuizAnswer(currentPoint.id, 0, oi)}
                                    className={`w-full text-left px-4 py-3 rounded-lg border text-sm transition-all ${cls}`}
                                  >
                                    <span className="font-mono text-gray-500 mr-2">
                                      {String.fromCharCode(65 + oi)}.
                                    </span>
                                    {opt}
                                    {answered && isCorrect && (
                                      <span className="ml-2 text-green-400">✓</span>
                                    )}
                                    {answered && selected === oi && !isCorrect && (
                                      <span className="ml-2 text-red-400">✗</span>
                                    )}
                                  </button>
                                );
                              })}
                            </div>
                            {answered && (
                              <div className="mt-3 p-3 rounded-lg bg-gray-800/50 text-sm text-gray-300">
                                <strong>{t('quiz.explanation')}</strong> {q.explanation}
                              </div>
                            )}
                          </div>
                        );
                      })()}
                    </div>
                  </section>
                )}

                {/* ---- Navigation ---- */}
                <div className="flex items-center justify-between pt-2 pb-8">
                  <button
                    onClick={goPrev}
                    disabled={activePointIdx === 0}
                    className="px-4 py-2 rounded-lg bg-gray-800 text-gray-300 hover:bg-gray-700 disabled:opacity-30 text-sm transition-all"
                  >
                    {t('nav.prev')}
                  </button>
                  <span className="text-xs text-gray-500">
                    {activePointIdx + 1} / {displayPoints.length}
                  </span>
                  <button
                    onClick={goNext}
                    disabled={activePointIdx >= displayPoints.length - 1}
                    className="px-4 py-2 rounded-lg bg-cyan-600 text-white hover:bg-cyan-700 disabled:opacity-30 text-sm transition-all"
                  >
                    {t('nav.next')}
                  </button>
                </div>
              </div>
            ) : (
              <div className="text-center text-gray-500 py-20">
                {loading ? t('kp.loading') : t('kp.no_points')}
              </div>
            )}
          </main>

          {/* ---- Right sidebar: progress summary ---- */}
          <aside className="w-48 flex-shrink-0 hidden xl:block">
            <div className="sticky top-28 space-y-4">
              <div className="p-4 rounded-xl bg-gray-900 border border-gray-800">
                <div className="text-xs text-gray-500 mb-1">{t('kp.week_progress')}</div>
                <div className="text-2xl font-bold text-white">
                  {weekProgress.done}/{weekProgress.total}
                </div>
                <div className="text-xs text-gray-500 mt-0.5">{progressPct}%</div>
                <div className="h-2 bg-gray-800 rounded-full mt-2">
                  <div
                    className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full transition-all"
                    style={{ width: `${progressPct}%` }}
                  />
                </div>
              </div>

              {stats && (
                <div className="p-4 rounded-xl bg-gray-900 border border-gray-800">
                  <div className="text-xs text-gray-500 mb-1">{t('kp.total')}</div>
                  <div className="text-lg font-bold text-white">
                    {stats.completed}/{stats.total}
                  </div>
                </div>
              )}

              {/* Keyboard hints */}
              <div className="p-4 rounded-xl bg-gray-900 border border-gray-800">
                <div className="text-xs text-gray-500 mb-2">{t('kb.title')}</div>
                <div className="space-y-1 text-[11px] text-gray-600">
                  <div><kbd className="bg-gray-800 px-1.5 py-0.5 rounded text-gray-400">j</kbd> / <kbd className="bg-gray-800 px-1.5 py-0.5 rounded text-gray-400">→</kbd> {t('kb.next')}</div>
                  <div><kbd className="bg-gray-800 px-1.5 py-0.5 rounded text-gray-400">k</kbd> / <kbd className="bg-gray-800 px-1.5 py-0.5 rounded text-gray-400">←</kbd> {t('kb.prev')}</div>
                  <div><kbd className="bg-gray-800 px-1.5 py-0.5 rounded text-gray-400">Enter</kbd> {t('kb.toggle')}</div>
                </div>
              </div>

              {/* Mini-map */}
              <div className="p-4 rounded-xl bg-gray-900 border border-gray-800">
                <div className="text-xs text-gray-500 mb-2">{t('map.title')}</div>
                <div className="flex flex-wrap gap-1">
                  {displayPoints.map((p, i) => (
                    <button
                      key={p.id}
                      onClick={() => setActivePointIdx(i)}
                      className={`w-3 h-3 rounded-sm transition-all ${
                        i === activePointIdx
                          ? 'bg-cyan-400 scale-125'
                          : completed.has(p.id)
                          ? 'bg-green-500'
                          : 'bg-gray-700 hover:bg-gray-600'
                      }`}
                      title={p.title}
                    />
                  ))}
                </div>
              </div>
            </div>
          </aside>
        </div>
      </div>

      {/* ---- Mobile bottom nav ---- */}
      <div className="lg:hidden fixed bottom-0 left-0 right-0 bg-[#0a0a0a]/95 backdrop-blur-sm border-t border-gray-800 px-4 py-2 flex items-center justify-between z-50">
        <button
          onClick={goPrev}
          disabled={activePointIdx === 0}
          className="px-3 py-1.5 rounded bg-gray-800 text-gray-300 text-sm disabled:opacity-30"
        >
          {t('nav.prev')}
        </button>
        <span className="text-xs text-gray-500">
          {activePointIdx + 1}/{displayPoints.length}
        </span>
        <button
          onClick={goNext}
          disabled={activePointIdx >= displayPoints.length - 1}
          className="px-3 py-1.5 rounded bg-cyan-600 text-white text-sm disabled:opacity-30"
        >
          {t('nav.next')}
        </button>
      </div>
    </div>
  );
}
