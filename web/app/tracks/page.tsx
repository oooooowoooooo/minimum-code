'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useLang } from '@/lib/i18n';
import { API_BASE } from '@/lib/api';

interface Skill {
  id: string;
  title: string;
  title_zh?: string;
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

function getTrackProgress(trackId: string, skillIds: string[]): number {
  try {
    const stored = localStorage.getItem(PROGRESS_KEY);
    if (!stored) return 0;
    const map = JSON.parse(stored) as Record<string, string[]>;
    const completed = map[trackId] || [];
    if (skillIds.length === 0) return 0;
    const done = skillIds.filter((id) => completed.includes(id)).length;
    return Math.round((done / skillIds.length) * 100);
  } catch {
    return 0;
  }
}

export default function TracksPage() {
  const { lang, toggle, t } = useLang();
  const [tracks, setTracks] = useState<Track[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    fetch(`${API_BASE}/api/tracks`)
      .then((r) => {
        if (!r.ok) throw new Error(`${r.status}`);
        return r.json();
      })
      .then((data) => {
        setTracks(Array.isArray(data) ? data : []);
        setLoading(false);
      })
      .catch(() => {
        setError(true);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0a0a0a] flex items-center justify-center">
        <div className="text-gray-400 text-lg">{t('tracks.loading')}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0a0a0a]">
      {/* Header */}
      <header className="border-b border-gray-800 bg-[#0a0a0a]/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
          <Link
            href="/"
            className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors text-sm"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="15 18 9 12 15 6" />
            </svg>
            {t('nav.home')}
          </Link>
          <button
            onClick={toggle}
            className="px-3 py-1 rounded-full text-xs font-medium bg-gray-800 text-gray-300 hover:bg-gray-700 border border-gray-700 transition-all"
          >
            {lang === 'zh' ? '中/EN' : 'EN/中'}
          </button>
        </div>
      </header>

      <div className="max-w-5xl mx-auto px-4 py-12">
        {/* Page title */}
        <div className="mb-10">
          <h1 className="text-3xl font-bold mb-2">
            {t('tracks.title')}
          </h1>
          <p className="text-gray-400 text-sm">
            {t('tracks.subtitle')}
          </p>
        </div>

        {/* Error state */}
        {error && (
          <div className="text-center py-20">
            <div className="text-4xl mb-4">!</div>
            <div className="text-red-400 mb-4">{t('tracks.error')}</div>
          </div>
        )}

        {/* Empty state */}
        {!error && tracks.length === 0 && (
          <div className="text-center py-20">
            <div className="text-4xl mb-4">?</div>
            <div className="text-gray-400">{t('tracks.empty')}</div>
          </div>
        )}

        {/* Track grid */}
        {tracks.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {tracks.map((track) => {
              const progress = getTrackProgress(
                track.id,
                track.skills.map((s) => s.id),
              );
              const title = lang === 'zh' && track.title_zh ? track.title_zh : track.title;
              const goal = lang === 'zh' && track.goal_zh ? track.goal_zh : track.goal;

              return (
                <Link
                  key={track.id}
                  href={`/tracks/${track.id}`}
                  className="group block rounded-xl border border-gray-800 bg-gray-900/50 hover:border-blue-500/50 hover:bg-gray-900 transition-all duration-200 card-hover"
                >
                  <div className="p-6">
                    {/* Icon + title */}
                    <div className="flex items-center gap-3 mb-3">
                      <span className="text-3xl">{track.icon}</span>
                      <div className="flex-1 min-w-0">
                        <h2 className="font-bold text-lg truncate group-hover:text-blue-400 transition-colors">
                          {title}
                        </h2>
                        {track.level && (
                          <span className="text-[10px] uppercase tracking-wider text-gray-500 bg-gray-800 px-2 py-0.5 rounded">
                            {track.level}
                          </span>
                        )}
                      </div>
                    </div>

                    {/* Goal */}
                    <p className="text-sm text-gray-400 mb-4 line-clamp-2">
                      {goal}
                    </p>

                    {/* Skill count */}
                    <div className="text-xs text-gray-500 mb-3">
                      {track.skills.length} {t('tracks.skills')}
                    </div>

                    {/* Progress bar */}
                    <div className="w-full">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs text-gray-500">{t('tracks.progress')}</span>
                        <span className="text-xs font-mono text-gray-500">{progress}%</span>
                      </div>
                      <div className="h-1.5 w-full rounded-full bg-gray-800 overflow-hidden">
                        <div
                          className={`h-full rounded-full transition-all duration-500 ${
                            progress === 100
                              ? 'bg-green-500'
                              : progress > 0
                                ? 'bg-blue-500'
                                : 'bg-gray-700'
                          }`}
                          style={{ width: `${progress}%` }}
                        />
                      </div>
                    </div>
                  </div>
                </Link>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
