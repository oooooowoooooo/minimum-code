'use client';

import { useState, useEffect, useCallback } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { useLang } from '@/lib/i18n';
import { API_BASE } from '@/lib/api';

interface Skill {
  id: string;
  title: string;
  title_zh?: string;
  why: string;
  why_zh?: string;
  code: string;
  language?: string;
  lab_id?: string | null;
}

interface Track {
  id: string;
  icon: string;
  title: string;
  title_zh?: string;
  goal: string;
  goal_zh?: string;
  level?: string;
  skills: Skill[];
}

const PROGRESS_KEY = 'track_progress';

function getCompletedSkills(trackId: string): Set<string> {
  try {
    const stored = localStorage.getItem(PROGRESS_KEY);
    if (!stored) return new Set();
    const map = JSON.parse(stored) as Record<string, string[]>;
    return new Set(map[trackId] || []);
  } catch {
    return new Set();
  }
}

function saveCompletedSkills(trackId: string, completed: Set<string>) {
  try {
    const stored = localStorage.getItem(PROGRESS_KEY);
    const map = stored ? (JSON.parse(stored) as Record<string, string[]>) : {};
    map[trackId] = Array.from(completed);
    localStorage.setItem(PROGRESS_KEY, JSON.stringify(map));
  } catch {
    // ignore
  }
}

// Minimal syntax highlighting for code blocks (reuses the same patterns as CodeViewer)
function highlightCode(code: string, language: string): React.ReactNode {
  const lines = code.split('\n');
  const patterns: { regex: RegExp; className: string }[] = [
    { regex: /(\/\/.*$|#.*$)/gm, className: 'code-comment' },
    { regex: /("[^"\\]*(?:\\.[^"\\]*)*"|'[^'\\]*(?:\\.[^'\\]*)*')/g, className: 'code-string' },
    { regex: /\b(\d+\.?\d*)\b/g, className: 'code-number' },
    {
      regex: /\b(function|const|let|var|return|if|else|for|while|class|import|export|from|async|await|try|catch|throw|new|this|def|self|True|False|None|true|false|null|undefined)\b/g,
      className: 'code-keyword',
    },
    { regex: /\b([A-Z][a-zA-Z0-9]+)\b/g, className: 'code-type' },
    { regex: /\b([a-z_][a-zA-Z0-9_]*)\s*\(/g, className: 'code-function' },
  ];

  const processSegment = (text: string, depth: number, key: { v: number }): React.ReactNode[] => {
    if (depth >= patterns.length || text.length === 0) {
      return [<span key={`s-${key.v++}`}>{text}</span>];
    }
    const { regex, className } = patterns[depth];
    regex.lastIndex = 0;
    const result: React.ReactNode[] = [];
    let lastIndex = 0;
    let match: RegExpExecArray | null;
    while ((match = regex.exec(text)) !== null) {
      if (match.index > lastIndex) {
        result.push(...processSegment(text.slice(lastIndex, match.index), depth + 1, key));
      }
      result.push(
        <span key={`h-${key.v++}`} className={className}>
          {match[1] || match[0]}
        </span>,
      );
      lastIndex = match.index + match[0].length;
    }
    if (lastIndex < text.length) {
      result.push(...processSegment(text.slice(lastIndex), depth + 1, key));
    }
    return result.length > 0 ? result : [<span key={`s-${key.v++}`}>{text}</span>];
  };

  return (
    <pre className="p-0 m-0">
      <code className="block text-sm leading-relaxed">
        {lines.map((line, i) => (
          <div key={i} className="flex hover:bg-white/[0.03] transition-colors">
            <span className="flex-shrink-0 w-10 text-right pr-3 text-gray-600 select-none text-xs leading-relaxed border-r border-gray-800/50">
              {i + 1}
            </span>
            <span className="pl-3 pr-4 flex-1 whitespace-pre">
              {processSegment(line, 0, { v: 0 })}
            </span>
          </div>
        ))}
      </code>
    </pre>
  );
}

export default function TrackDetailPage() {
  const { lang, toggle, t } = useLang();
  const params = useParams();
  const trackId = params.trackId as string;

  const [track, setTrack] = useState<Track | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [completed, setCompleted] = useState<Set<string>>(new Set());

  useEffect(() => {
    if (!trackId) return;

    fetch(`${API_BASE}/api/tracks/${trackId}`)
      .then((r) => {
        if (!r.ok) throw new Error(`${r.status}`);
        return r.json();
      })
      .then((data) => {
        setTrack(data);
        setCompleted(getCompletedSkills(trackId));
        setLoading(false);
      })
      .catch(() => {
        setError(true);
        setLoading(false);
      });
  }, [trackId]);

  const toggleSkill = useCallback(
    (skillId: string) => {
      setCompleted((prev) => {
        const next = new Set(prev);
        if (next.has(skillId)) {
          next.delete(skillId);
        } else {
          next.add(skillId);
        }
        saveCompletedSkills(trackId, next);
        return next;
      });
    },
    [trackId],
  );

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0a0a0a] flex items-center justify-center">
        <div className="text-gray-400 text-lg">{lang === 'zh' ? '加载中...' : 'Loading...'}</div>
      </div>
    );
  }

  if (error || !track) {
    return (
      <div className="min-h-screen bg-[#0a0a0a] flex items-center justify-center">
        <div className="text-center">
          <div className="text-4xl mb-4">?</div>
          <div className="text-gray-400 mb-4">
            {lang === 'zh' ? '赛道未找到' : 'Track not found'}
          </div>
          <Link href="/tracks" className="text-blue-400 hover:underline text-sm">
            {lang === 'zh' ? '← 返回赛道列表' : '← Back to tracks'}
          </Link>
        </div>
      </div>
    );
  }

  const title = lang === 'zh' && track.title_zh ? track.title_zh : track.title;
  const goal = lang === 'zh' && track.goal_zh ? track.goal_zh : track.goal;
  const totalSkills = track.skills.length;
  const completedCount = track.skills.filter((s) => completed.has(s.id)).length;
  const progressPct = totalSkills > 0 ? Math.round((completedCount / totalSkills) * 100) : 0;

  return (
    <div className="min-h-screen bg-[#0a0a0a]">
      {/* Header */}
      <header className="border-b border-gray-800 bg-[#0a0a0a]/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
          {/* Breadcrumb */}
          <nav className="flex items-center gap-2 text-sm text-gray-400">
            <Link href="/" className="hover:text-white transition-colors">
              {lang === 'zh' ? '首页' : 'Home'}
            </Link>
            <span className="text-gray-600">/</span>
            <Link href="/tracks" className="hover:text-white transition-colors">
              {t('tracks.breadcrumb')}
            </Link>
            <span className="text-gray-600">/</span>
            <span className="text-white truncate max-w-[200px]">{title}</span>
          </nav>
          <button
            onClick={toggle}
            className="px-3 py-1 rounded-full text-xs font-medium bg-gray-800 text-gray-300 hover:bg-gray-700 border border-gray-700 transition-all"
          >
            {lang === 'zh' ? '中/EN' : 'EN/中'}
          </button>
        </div>
      </header>

      <div className="max-w-5xl mx-auto px-4 py-10">
        {/* Track overview */}
        <div className="mb-10">
          <div className="flex items-center gap-4 mb-3">
            <span className="text-4xl">{track.icon}</span>
            <div>
              <h1 className="text-2xl font-bold">{title}</h1>
              {track.level && (
                <span className="inline-block mt-1 text-[10px] uppercase tracking-wider text-gray-400 bg-gray-800 px-2 py-0.5 rounded">
                  {t('tracks.level')}: {track.level}
                </span>
              )}
            </div>
          </div>

          <p className="text-gray-400 text-sm mb-5 max-w-2xl">{goal}</p>

          {/* Summary bar */}
          <div className="flex items-center gap-6 flex-wrap">
            <div className="flex items-center gap-2">
              <span className="text-xs text-gray-500">{t('tracks.skills')}:</span>
              <span className="text-sm font-medium text-white">{totalSkills}</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs text-gray-500">{t('tracks.progress')}:</span>
              <span className="text-sm font-mono text-white">{completedCount}/{totalSkills}</span>
            </div>
            <div className="flex-1 min-w-[120px] max-w-xs">
              <div className="h-2 w-full rounded-full bg-gray-800 overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${
                    progressPct === 100 ? 'bg-green-500' : progressPct > 0 ? 'bg-blue-500' : 'bg-gray-700'
                  }`}
                  style={{ width: `${progressPct}%` }}
                />
              </div>
            </div>
            <span className="text-xs font-mono text-gray-500">{progressPct}%</span>
          </div>
        </div>

        {/* Skills list */}
        <div className="space-y-5">
          {track.skills.map((skill, index) => {
            const skillTitle = lang === 'zh' && skill.title_zh ? skill.title_zh : skill.title;
            const skillWhy = lang === 'zh' && skill.why_zh ? skill.why_zh : skill.why;
            const isDone = completed.has(skill.id);
            const langLabel = skill.language || 'python';

            return (
              <div
                key={skill.id}
                className={`rounded-xl border transition-all ${
                  isDone ? 'border-green-500/30 bg-green-950/10' : 'border-gray-800 bg-gray-900/50'
                }`}
              >
                {/* Skill header */}
                <div className="px-6 py-4 border-b border-gray-800 flex items-center justify-between gap-4">
                  <div className="flex items-center gap-3 min-w-0">
                    {/* Completion toggle */}
                    <button
                      onClick={() => toggleSkill(skill.id)}
                      className={`flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all ${
                        isDone
                          ? 'border-green-500 bg-green-500 text-white'
                          : 'border-gray-600 hover:border-gray-400'
                      }`}
                      title={isDone ? (lang === 'zh' ? '标记未完成' : 'Mark incomplete') : (lang === 'zh' ? '标记完成' : 'Mark complete')}
                    >
                      {isDone && (
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                          <polyline points="20 6 9 17 4 12" />
                        </svg>
                      )}
                    </button>
                    <div className="min-w-0">
                      <h3 className={`font-bold text-lg ${isDone ? 'text-green-300' : 'text-white'}`}>
                        {index + 1}. {skillTitle}
                      </h3>
                    </div>
                  </div>

                  {/* Lab button */}
                  {skill.lab_id && (
                    <Link
                      href={`/labs/${skill.lab_id}`}
                      className="flex-shrink-0 px-4 py-2 rounded-lg bg-blue-600 text-white text-sm font-medium hover:bg-blue-700 transition-colors"
                    >
                      {t('tracks.start_lab')}
                    </Link>
                  )}
                </div>

                {/* Skill body */}
                <div className="p-6 space-y-5">
                  {/* Why section */}
                  {skillWhy && (
                    <div>
                      <h4 className="text-xs uppercase tracking-wider text-gray-500 mb-2">
                        {t('tracks.why')}
                      </h4>
                      <p className="text-sm text-gray-300 leading-relaxed">
                        {skillWhy}
                      </p>
                    </div>
                  )}

                  {/* Code snippet */}
                  {skill.code && (
                    <div>
                      <h4 className="text-xs uppercase tracking-wider text-gray-500 mb-2">
                        {t('section.code')}
                      </h4>
                      <div className="rounded-lg border border-gray-800 overflow-hidden bg-[#1e1e1e]">
                        {/* Language badge */}
                        <div className="flex items-center justify-between px-4 py-2 bg-gray-900 border-b border-gray-800">
                          <div className="flex items-center gap-1.5">
                            <span className="w-2.5 h-2.5 rounded-full bg-red-500/70" />
                            <span className="w-2.5 h-2.5 rounded-full bg-yellow-500/70" />
                            <span className="w-2.5 h-2.5 rounded-full bg-green-500/70" />
                          </div>
                          <span className="text-[10px] uppercase tracking-wider text-gray-500 bg-gray-800 px-2 py-0.5 rounded">
                            {langLabel}
                          </span>
                        </div>
                        <div className="overflow-x-auto">
                          {highlightCode(skill.code, langLabel)}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {/* Bottom summary */}
        {completedCount === totalSkills && totalSkills > 0 && (
          <div className="mt-10 p-6 rounded-xl border border-green-500/30 bg-green-950/20 text-center">
            <div className="text-2xl mb-2">
              {lang === 'zh' ? '恭喜完成本赛道!' : 'Track Complete!'}
            </div>
            <p className="text-gray-400 text-sm">
              {lang === 'zh'
                ? `你已掌握「${title}」的全部 ${totalSkills} 项技能。`
                : `You've mastered all ${totalSkills} skills in "${title}".`}
            </p>
          </div>
        )}

        {/* Footer nav */}
        <div className="mt-12 pt-6 border-t border-gray-800 flex justify-between">
          <Link
            href="/tracks"
            className="px-4 py-2 rounded-lg bg-gray-800 text-gray-300 hover:bg-gray-700 text-sm transition-colors"
          >
            {lang === 'zh' ? '← 返回赛道列表' : '← All Tracks'}
          </Link>
        </div>
      </div>
    </div>
  );
}
