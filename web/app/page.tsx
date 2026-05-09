'use client';

import { useState, useEffect, useMemo } from 'react';
import Link from 'next/link';
import { useLang } from '@/lib/i18n';
import { API_BASE } from '@/lib/api';

// ──────────────────────────────────────────────
//  Types
// ──────────────────────────────────────────────

interface Track {
  id: string;
  title: string;
  title_zh: string;
  icon: string;
  description: string;
  description_zh: string;
  skill_count: number;
}

interface ProgressMap {
  [trackId: string]: {
    completed: number;
    total: number;
  };
}

// ──────────────────────────────────────────────
//  Default tracks (fallback if API unavailable)
// ──────────────────────────────────────────────

const DEFAULT_TRACKS: Track[] = [
  {
    id: 'python-engineering',
    title: 'Python Engineering',
    title_zh: 'Python 工程化',
    icon: '🐍',
    description: 'Type hints, testing, packaging, project structure',
    description_zh: '类型标注、测试、打包、工程结构',
    skill_count: 24,
  },
  {
    id: 'fastapi-services',
    title: 'FastAPI Services',
    title_zh: 'FastAPI 服务',
    icon: '⚡',
    description: 'REST APIs, middleware, auth, database integration',
    description_zh: 'REST API、中间件、认证、数据库集成',
    skill_count: 20,
  },
  {
    id: 'llm-api-client',
    title: 'LLM API Client',
    title_zh: 'LLM API 客户端',
    icon: '🤖',
    description: 'OpenAI/Claude SDK, streaming, prompt engineering',
    description_zh: 'OpenAI/Claude SDK、流式调用、Prompt 工程',
    skill_count: 18,
  },
  {
    id: 'rag-system',
    title: 'RAG System',
    title_zh: 'RAG 系统',
    icon: '📚',
    description: 'Embeddings, vector DB, retrieval, chunking strategies',
    description_zh: 'Embedding、向量库、检索、分块策略',
    skill_count: 22,
  },
  {
    id: 'agent-engineering',
    title: 'Agent Engineering',
    title_zh: 'Agent 工程',
    icon: '🛠️',
    description: 'Tool use, planning, memory, multi-agent orchestration',
    description_zh: '工具调用、规划、记忆、多 Agent 编排',
    skill_count: 20,
  },
  {
    id: 'deployment-quality',
    title: 'Deployment & Quality',
    title_zh: '部署与质量',
    icon: '🚀',
    description: 'Docker, CI/CD, monitoring, observability, testing',
    description_zh: 'Docker、CI/CD、监控、可观测性、测试',
    skill_count: 16,
  },
];

// ──────────────────────────────────────────────
//  localStorage helpers
// ──────────────────────────────────────────────

const STORAGE_KEY = 'competency_progress';

function loadProgress(): ProgressMap {
  if (typeof window === 'undefined') return {};
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
}

function saveProgress(p: ProgressMap) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(p));
  } catch {}
}

// ──────────────────────────────────────────────
//  Component
// ──────────────────────────────────────────────

export default function HomePage() {
  const { lang, toggle, t } = useLang();
  const [tracks, setTracks] = useState<Track[]>(DEFAULT_TRACKS);
  const [progress, setProgress] = useState<ProgressMap>({});
  const [loading, setLoading] = useState(true);

  // Fetch tracks from API + progress from localStorage
  useEffect(() => {
    setProgress(loadProgress());

    let cancelled = false;
    fetch(`${API_BASE}/api/tracks`)
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((data: Track[]) => {
        if (!cancelled && Array.isArray(data) && data.length > 0) {
          setTracks(data);
        }
      })
      .catch(() => {
        // API unavailable — keep defaults
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, []);

  // Persist progress whenever it changes (after initial load)
  useEffect(() => {
    if (!loading) saveProgress(progress);
  }, [progress, loading]);

  // ── Derived stats ──

  const stats = useMemo(() => {
    const totalSkills = tracks.reduce((sum, t) => sum + t.skill_count, 0);
    const completedSkills = Object.values(progress).reduce(
      (sum, p) => sum + p.completed,
      0,
    );
    const overallPct = totalSkills > 0 ? Math.round((completedSkills / totalSkills) * 100) : 0;
    return { totalSkills, completedSkills, overallPct };
  }, [tracks, progress]);

  // ── Loading state ──

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0a0a0a] flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
          <span className="text-gray-400 text-sm">
            {lang === 'zh' ? '加载中...' : 'Loading...'}
          </span>
        </div>
      </div>
    );
  }

  // ── Helpers ──

  function getTrackTitle(track: Track): string {
    return lang === 'zh' ? track.title_zh : track.title;
  }

  function getTrackDesc(track: Track): string {
    return lang === 'zh' ? track.description_zh : track.description;
  }

  function getProgress(trackId: string): number {
    const p = progress[trackId];
    if (!p || p.total === 0) return 0;
    return Math.round((p.completed / p.total) * 100);
  }

  // ── Render ──

  return (
    <div className="min-h-screen bg-[#0a0a0a]">
      {/* ── Header ── */}
      <header className="border-b border-gray-800 bg-[#0a0a0a]/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-3 group">
            <span className="text-2xl">🧠</span>
            <div>
              <h1 className="text-lg font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                {lang === 'zh' ? 'minimum-code' : 'minimum-code'}
              </h1>
              <p className="text-xs text-gray-500">
                {lang === 'zh' ? '源码阅读与架构训练' : 'Source Reading & Architecture'}
              </p>
            </div>
          </Link>
          <button
            onClick={toggle}
            className="px-3 py-1.5 rounded-full text-xs font-medium bg-gray-800 text-gray-300 hover:bg-gray-700 border border-gray-700 transition-all"
          >
            {lang === 'zh' ? '中 / EN' : 'EN / 中'}
          </button>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 sm:px-6 py-10 sm:py-16">
        {/* ── Hero ── */}
        <section className="mb-12">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-3">
            {lang === 'zh'
              ? 'AI 时代源码阅读与架构训练平台'
              : 'Source Code Reading and Architecture Training for the AI Era'}
          </h2>
          <p className="text-gray-400 text-base sm:text-lg max-w-2xl">
            {lang === 'zh'
              ? 'AI 会写代码，但你要会读代码、评审代码、设计架构。用最少时间读懂 Python + TypeScript 主流开源项目的核心边界。'
              : 'AI can write code, but you still need to read code, review tradeoffs, and design architecture across mainstream Python and TypeScript projects.'}
          </p>
        </section>

        {/* ── Quick Actions ── */}
        <section className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-12">
          <Link
            href="/assessment"
            className="group flex items-center gap-4 p-5 rounded-xl border border-blue-500/30 bg-blue-500/5 hover:bg-blue-500/10 hover:border-blue-500/50 transition-all duration-200"
          >
            <span className="text-2xl">📝</span>
            <div>
              <div className="text-sm font-semibold text-blue-400 group-hover:text-blue-300 transition-colors">
                {lang === 'zh' ? '开始评估' : 'Start Assessment'}
              </div>
              <div className="text-xs text-gray-500 mt-0.5">
                {lang === 'zh'
                  ? '测一测你当前的能力水平'
                  : 'Test your current skill level'}
              </div>
            </div>
          </Link>
          <Link
            href="/tracks/python-engineering"
            className="group flex items-center gap-4 p-5 rounded-xl border border-purple-500/30 bg-purple-500/5 hover:bg-purple-500/10 hover:border-purple-500/50 transition-all duration-200"
          >
            <span className="text-2xl">▶️</span>
            <div>
              <div className="text-sm font-semibold text-purple-400 group-hover:text-purple-300 transition-colors">
                {lang === 'zh' ? '继续训练' : 'Continue Training'}
              </div>
              <div className="text-xs text-gray-500 mt-0.5">
                {lang === 'zh'
                  ? '从上次中断的地方继续'
                  : 'Pick up where you left off'}
              </div>
            </div>
          </Link>
          <Link
            href="/labs"
            className="group flex items-center gap-4 p-5 rounded-xl border border-green-500/30 bg-green-500/5 hover:bg-green-500/10 hover:border-green-500/50 transition-all duration-200"
          >
            <span className="text-2xl">🧪</span>
            <div>
              <div className="text-sm font-semibold text-green-400 group-hover:text-green-300 transition-colors">
                {lang === 'zh' ? '查看实验' : 'View Labs'}
              </div>
              <div className="text-xs text-gray-500 mt-0.5">
                {lang === 'zh'
                  ? '动手实战项目与练习'
                  : 'Hands-on projects and exercises'}
              </div>
            </div>
          </Link>
        </section>

        {/* ── Stats Row ── */}
        <section className="grid grid-cols-3 gap-4 mb-12">
          <div className="p-5 rounded-xl border border-gray-800 bg-gray-900/50 text-center">
            <div className="text-xs text-gray-500 mb-1">
              {lang === 'zh' ? '技能总数' : 'Total Skills'}
            </div>
            <div className="text-2xl sm:text-3xl font-bold text-white">
              {stats.totalSkills}
            </div>
          </div>
          <div className="p-5 rounded-xl border border-gray-800 bg-gray-900/50 text-center">
            <div className="text-xs text-gray-500 mb-1">
              {lang === 'zh' ? '已完成' : 'Completed'}
            </div>
            <div className="text-2xl sm:text-3xl font-bold text-green-400">
              {stats.completedSkills}
            </div>
          </div>
          <div className="p-5 rounded-xl border border-gray-800 bg-gray-900/50 text-center">
            <div className="text-xs text-gray-500 mb-1">
              {lang === 'zh' ? '总体进度' : 'Overall Progress'}
            </div>
            <div className="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              {stats.overallPct}%
            </div>
          </div>
        </section>

        {/* ── Capability Tracks ── */}
        <section>
          <h3 className="text-lg font-semibold text-white mb-6">
            {lang === 'zh' ? '六大能力赛道' : 'Six Capability Tracks'}
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {tracks.map((track) => {
              const pct = getProgress(track.id);
              return (
                <Link
                  key={track.id}
                  href={`/tracks/${track.id}`}
                  className="group block p-6 rounded-xl border border-gray-800 bg-gray-900/50 hover:border-blue-500/50 hover:bg-gray-900/80 transition-all duration-200"
                >
                  <div className="flex items-start justify-between mb-3">
                    <span className="text-3xl">{track.icon}</span>
                    <span className="text-xs text-gray-500 bg-gray-800 px-2 py-0.5 rounded-full">
                      {track.skill_count} {lang === 'zh' ? '项技能' : 'skills'}
                    </span>
                  </div>
                  <h4 className="text-base font-semibold text-white group-hover:text-blue-400 transition-colors mb-1">
                    {getTrackTitle(track)}
                  </h4>
                  <p className="text-xs text-gray-500 mb-4 line-clamp-2">
                    {getTrackDesc(track)}
                  </p>
                  {/* Progress bar */}
                  <div className="w-full h-1.5 bg-gray-800 rounded-full overflow-hidden">
                    <div
                      className="h-full rounded-full bg-gradient-to-r from-blue-500 to-purple-500 transition-all duration-500"
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                  <div className="flex justify-between mt-2">
                    <span className="text-xs text-gray-500">
                      {lang === 'zh' ? '进度' : 'Progress'}
                    </span>
                    <span className="text-xs font-medium text-gray-400">
                      {pct}%
                    </span>
                  </div>
                </Link>
              );
            })}
          </div>
        </section>

        {/* ── Footer ── */}
        <footer className="mt-16 pt-8 border-t border-gray-800 text-center text-gray-500 text-sm">
          <p>
            {lang === 'zh'
              ? 'AI 时代，代码廉价，品味昂贵。'
              : 'In the AI era, code is cheap. Taste is expensive.'}
          </p>
        </footer>
      </main>
    </div>
  );
}
