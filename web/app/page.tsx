'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useLang } from '@/lib/i18n';

const API = 'http://localhost:8000';

interface KnowledgeStats {
  total_points: number;
  points_per_week: Record<string, number>;
}

export default function HomePage() {
  const { lang, toggle, t } = useLang();
  const [loading, setLoading] = useState(true);
  const [kpStats, setKpStats] = useState<KnowledgeStats | null>(null);
  const [kpCompleted, setKpCompleted] = useState<number>(0);

  useEffect(() => {
    try {
      const stored = localStorage.getItem('kp_completed');
      if (stored) {
        const parsed = JSON.parse(stored);
        setKpCompleted(Array.isArray(parsed) ? parsed.length : 0);
      }
    } catch {}

    fetch(`${API}/api/knowledge-points/stats`)
      .then((r) => r.json())
      .then((stats) => {
        setKpStats(stats);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0a0a0a] flex items-center justify-center">
        <div className="text-gray-400 text-lg">{lang === 'zh' ? '加载中...' : 'Loading...'}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0a0a0a]">
      {/* Header */}
      <header className="border-b border-gray-800 bg-[#0a0a0a]/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-2xl">🚀</span>
            <div>
              <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                {t('header.title')}
              </h1>
              <p className="text-xs text-gray-500">{t('header.subtitle')}</p>
            </div>
          </div>
          <button
            onClick={toggle}
            className="px-3 py-1 rounded-full text-xs font-medium bg-gray-800 text-gray-300 hover:bg-gray-700 border border-gray-700 transition-all"
          >
            {lang === 'zh' ? '中/EN' : 'EN/中'}
          </button>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 py-16">
        {/* Knowledge Entry Card */}
        <Link
          href="/knowledge"
          className="group block p-8 rounded-2xl border border-gray-800 bg-gradient-to-br from-indigo-950/60 to-purple-950/40 hover:border-indigo-500/50 transition-all duration-300 mb-8"
        >
          <div className="flex items-center gap-4 mb-4">
            <span className="text-4xl">📚</span>
            <div>
              <h2 className="text-xl font-bold text-white group-hover:text-indigo-300 transition-colors">
                {t('kp.title')}
              </h2>
              <p className="text-sm text-gray-400">
                {lang === 'zh'
                  ? `${kpStats?.total_points ?? '—'} 个知识点，用通俗语言和小游戏掌握编程概念`
                  : `${kpStats?.total_points ?? '—'} knowledge points — master concepts through games`}
              </p>
            </div>
          </div>
          <span className="inline-block text-sm text-indigo-400 group-hover:text-indigo-300 transition-colors">
            {t('action.start')}
          </span>
        </Link>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-4">
          <div className="p-5 rounded-xl border border-gray-800 bg-gray-900/50 text-center">
            <div className="text-xs text-gray-500 mb-1">{t('stats.total')}</div>
            <div className="text-3xl font-bold text-white">{kpStats?.total_points ?? '—'}</div>
          </div>
          <div className="p-5 rounded-xl border border-gray-800 bg-gray-900/50 text-center">
            <div className="text-xs text-gray-500 mb-1">{t('stats.completed')}</div>
            <div className="text-3xl font-bold text-green-400">{kpCompleted}</div>
          </div>
          <div className="p-5 rounded-xl border border-gray-800 bg-gray-900/50 text-center">
            <div className="text-xs text-gray-500 mb-1">{t('stats.week_points')}</div>
            <div className="text-3xl font-bold text-blue-400">{kpStats?.total_points ?? '—'}</div>
          </div>
        </div>

        <footer className="mt-16 pt-8 border-t border-gray-800 text-center text-gray-500 text-sm">
          <p>{t('footer.quote')}</p>
        </footer>
      </div>
    </div>
  );
}
