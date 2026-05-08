'use client';

import { useState, useEffect, useMemo } from 'react';
import Link from 'next/link';
import { useLang } from '@/lib/i18n';
import { API_BASE } from '@/lib/api';

/* ------------------------------------------------------------------ */
/*  Types                                                              */
/* ------------------------------------------------------------------ */

type Difficulty = 'beginner' | 'intermediate' | 'advanced';

interface Lab {
  id: string;
  title: string;
  description: string;
  difficulty: Difficulty;
  estimated_minutes: number;
  track: string;
  track_icon: string;
}

/* ------------------------------------------------------------------ */
/*  Constants                                                          */
/* ------------------------------------------------------------------ */

const DIFFICULTY_ORDER: Difficulty[] = ['beginner', 'intermediate', 'advanced'];

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

/* ------------------------------------------------------------------ */
/*  localStorage helpers                                               */
/* ------------------------------------------------------------------ */

function loadCompletedLabs(): Set<string> {
  if (typeof window === 'undefined') return new Set();
  try {
    const raw = localStorage.getItem('lab_completed');
    return raw ? new Set(JSON.parse(raw)) : new Set();
  } catch {
    return new Set();
  }
}

/* ------------------------------------------------------------------ */
/*  Component                                                          */
/* ------------------------------------------------------------------ */

export default function LabsPage() {
  const { lang, toggle, t } = useLang();
  const [labs, setLabs] = useState<Lab[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterTrack, setFilterTrack] = useState<string>('all');
  const [completed, setCompleted] = useState<Set<string>>(new Set());

  useEffect(() => {
    setCompleted(loadCompletedLabs());

    fetch(`${API_BASE}/api/labs`)
      .then((r) => r.json())
      .then((data) => {
        setLabs(Array.isArray(data) ? data : data.labs ?? []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  /* ---- derived ---- */
  const tracks = useMemo(() => {
    const set = new Set(labs.map((l) => l.track));
    return Array.from(set).sort();
  }, [labs]);

  const filtered = useMemo(() => {
    if (filterTrack === 'all') return labs;
    return labs.filter((l) => l.track === filterTrack);
  }, [labs, filterTrack]);

  const grouped = useMemo(() => {
    const map: Record<Difficulty, Lab[]> = {
      beginner: [],
      intermediate: [],
      advanced: [],
    };
    for (const lab of filtered) {
      const key = DIFFICULTY_ORDER.includes(lab.difficulty) ? lab.difficulty : 'beginner';
      map[key].push(lab);
    }
    return map;
  }, [filtered]);

  const completedCount = useMemo(
    () => filtered.filter((l) => completed.has(l.id)).length,
    [filtered, completed],
  );

  /* ---- format time ---- */
  function formatTime(mins: number): string {
    if (mins < 60) return lang === 'zh' ? `${mins} 分钟` : `${mins} min`;
    const h = Math.floor(mins / 60);
    const m = mins % 60;
    if (m === 0) return lang === 'zh' ? `${h} 小时` : `${h}h`;
    return lang === 'zh' ? `${h} 小时 ${m} 分` : `${h}h ${m}m`;
  }

  /* ---- loading ---- */
  if (loading) {
    return (
      <div className="min-h-screen bg-[#0a0a0a] flex items-center justify-center">
        <div className="text-gray-400 text-lg">
          {lang === 'zh' ? '加载实验列表...' : 'Loading labs...'}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0a0a0a]">
      {/* ============================================================ */}
      {/*  Header                                                       */}
      {/* ============================================================ */}
      <header className="border-b border-gray-800 bg-[#0a0a0a]/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link
              href="/"
              className="text-gray-400 hover:text-white transition-colors text-sm"
            >
              {lang === 'zh' ? '← 首页' : '← Home'}
            </Link>
            <div className="flex items-center gap-2">
              <span className="text-2xl">🧪</span>
              <h1 className="text-xl font-bold bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
                {lang === 'zh' ? '编程实验室' : 'Coding Labs'}
              </h1>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-xs text-gray-500">
              {completedCount}/{filtered.length}{' '}
              {lang === 'zh' ? '已完成' : 'completed'}
            </span>
            <button
              onClick={toggle}
              className="px-3 py-1 rounded-full text-xs font-medium bg-gray-800 text-gray-300 hover:bg-gray-700 border border-gray-700 transition-all"
            >
              {lang === 'zh' ? '中/EN' : 'EN/中'}
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-5xl mx-auto px-4 py-8">
        {/* ============================================================ */}
        {/*  Track filter                                                 */}
        {/* ============================================================ */}
        {tracks.length > 1 && (
          <div className="flex gap-2 flex-wrap mb-8">
            <button
              onClick={() => setFilterTrack('all')}
              className={`px-3 py-1.5 rounded-full text-xs font-medium transition-all ${
                filterTrack === 'all'
                  ? 'bg-white text-black'
                  : 'bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-white'
              }`}
            >
              {lang === 'zh' ? '全部' : 'All'}
            </button>
            {tracks.map((track) => (
              <button
                key={track}
                onClick={() => setFilterTrack(filterTrack === track ? 'all' : track)}
                className={`px-3 py-1.5 rounded-full text-xs font-medium transition-all ${
                  filterTrack === track
                    ? 'bg-white text-black'
                    : 'bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-white'
                }`}
              >
                {track}
              </button>
            ))}
          </div>
        )}

        {/* ============================================================ */}
        {/*  Labs grouped by difficulty                                   */}
        {/* ============================================================ */}
        {filtered.length === 0 ? (
          <div className="text-center text-gray-500 py-20">
            <span className="text-4xl block mb-4">🧪</span>
            {lang === 'zh' ? '暂无实验' : 'No labs available'}
          </div>
        ) : (
          <div className="space-y-12">
            {DIFFICULTY_ORDER.map((diff) => {
              const group = grouped[diff];
              if (group.length === 0) return null;
              const meta = DIFFICULTY_META[diff];

              return (
                <section key={diff}>
                  <div className="flex items-center gap-3 mb-5">
                    <span
                      className={`text-xs font-semibold uppercase tracking-wider px-2.5 py-1 rounded-full ${meta.bg} ${meta.color} border ${meta.border}`}
                    >
                      {meta.label[lang]}
                    </span>
                    <span className="text-xs text-gray-600">
                      {group.length} {lang === 'zh' ? '个实验' : 'labs'}
                    </span>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {group.map((lab) => {
                      const done = completed.has(lab.id);
                      return (
                        <Link
                          key={lab.id}
                          href={`/labs/${lab.id}`}
                          className="group relative block p-5 rounded-xl border border-gray-800 bg-gray-900/50 hover:border-gray-600 hover:bg-gray-900/80 transition-all duration-200"
                        >
                          {/* Completed indicator */}
                          {done && (
                            <div className="absolute top-3 right-3 w-5 h-5 rounded-full bg-green-500 flex items-center justify-center">
                              <span className="text-white text-[10px] font-bold">
                                ✓
                              </span>
                            </div>
                          )}

                          <div className="flex items-start gap-3 mb-3">
                            <span className="text-2xl flex-shrink-0">
                              {lab.track_icon || '🧪'}
                            </span>
                            <div className="min-w-0">
                              <h3 className="font-semibold text-white group-hover:text-emerald-300 transition-colors text-sm leading-tight">
                                {lab.title}
                              </h3>
                              <span className="text-[11px] text-gray-500">
                                {lab.track}
                              </span>
                            </div>
                          </div>

                          <p className="text-gray-400 text-xs leading-relaxed mb-4 line-clamp-2">
                            {lab.description}
                          </p>

                          <div className="flex items-center justify-between">
                            <span
                              className={`text-[10px] font-medium uppercase tracking-wider px-2 py-0.5 rounded-full ${meta.bg} ${meta.color}`}
                            >
                              {meta.label[lang]}
                            </span>
                            <span className="text-[11px] text-gray-500">
                              ⏱ {formatTime(lab.estimated_minutes)}
                            </span>
                          </div>
                        </Link>
                      );
                    })}
                  </div>
                </section>
              );
            })}
          </div>
        )}
      </div>

      {/* Footer */}
      <footer className="max-w-5xl mx-auto px-4 py-12 mt-8 border-t border-gray-800 text-center text-gray-600 text-xs">
        {lang === 'zh'
          ? '动手实践是掌握编程的最佳方式'
          : 'Hands-on practice is the best way to master programming'}
      </footer>
    </div>
  );
}
