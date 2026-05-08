'use client';

import { useState, useEffect, useCallback, useMemo } from 'react';
import Link from 'next/link';
import { useLang } from '@/lib/i18n';
import { API_BASE } from '@/lib/api';

/* ------------------------------------------------------------------ */
/*  Types                                                              */
/* ------------------------------------------------------------------ */

interface AssessmentOption {
  id: string;
  text: string;
}

interface AssessmentQuestion {
  id: string;
  text: string;
  track: string;
  options: AssessmentOption[];
}

interface TrackScore {
  track: string;
  label: string;
  score: number;
  total: number;
  percentage: number;
  level: 'beginner' | 'intermediate' | 'advanced' | 'expert';
}

interface AssessmentResults {
  overall_percentage: number;
  overall_score: number;
  overall_total: number;
  tracks: TrackScore[];
  weakest_track: string;
}

/* ------------------------------------------------------------------ */
/*  Constants                                                          */
/* ------------------------------------------------------------------ */

const TRACK_LABELS_ZH: Record<string, string> = {
  'python-fundamentals': 'Python 基础',
  'typescript-fundamentals': 'TypeScript 基础',
  'ai-mastery': 'AI 工具精通',
  'patterns': '设计模式',
  'project-dissection': '项目拆解',
  'system-architecture': '系统架构',
};

const TRACK_LABELS_EN: Record<string, string> = {
  'python-fundamentals': 'Python Fundamentals',
  'typescript-fundamentals': 'TypeScript Fundamentals',
  'ai-mastery': 'AI Tool Mastery',
  'patterns': 'Design Patterns',
  'project-dissection': 'Project Dissection',
  'system-architecture': 'System Architecture',
};

const TRACK_ICONS: Record<string, string> = {
  'python-fundamentals': '🐍',
  'typescript-fundamentals': '🔷',
  'ai-mastery': '🤖',
  'patterns': '🏗️',
  'project-dissection': '🔍',
  'system-architecture': '🏛️',
};

const TRACK_COLORS: Record<string, string> = {
  'python-fundamentals': '#3b82f6',
  'typescript-fundamentals': '#06b6d4',
  'ai-mastery': '#ec4899',
  'patterns': '#f59e0b',
  'project-dissection': '#22c55e',
  'system-architecture': '#8b5cf6',
};

const LEVEL_LABELS: Record<string, { zh: string; en: string }> = {
  beginner: { zh: '入门', en: 'Beginner' },
  intermediate: { zh: '进阶', en: 'Intermediate' },
  advanced: { zh: '高级', en: 'Advanced' },
  expert: { zh: '专家', en: 'Expert' },
};

const LEVEL_COLORS: Record<string, string> = {
  beginner: 'text-red-400',
  intermediate: 'text-yellow-400',
  advanced: 'text-blue-400',
  expert: 'text-green-400',
};

type Step = 'loading' | 'questions' | 'submitting' | 'results';

/* ------------------------------------------------------------------ */
/*  Component                                                          */
/* ------------------------------------------------------------------ */

export default function AssessmentPage() {
  const { lang, toggle, t } = useLang();

  /* ---- state ---- */
  const [questions, setQuestions] = useState<AssessmentQuestion[]>([]);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [results, setResults] = useState<AssessmentResults | null>(null);
  const [step, setStep] = useState<Step>('loading');
  const [currentQ, setCurrentQ] = useState(0);
  const [error, setError] = useState<string | null>(null);

  /* ---- fetch questions on mount ---- */
  useEffect(() => {
    fetch(`${API_BASE}/api/assessment/questions`)
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((data) => {
        const qs: AssessmentQuestion[] = Array.isArray(data) ? data : data.questions ?? [];
        setQuestions(qs);
        setStep('questions');
      })
      .catch((err) => {
        console.error('Failed to load assessment questions:', err);
        setError(
          lang === 'zh'
            ? '加载评估题目失败，请稍后重试。'
            : 'Failed to load assessment questions. Please try again later.',
        );
        setStep('questions');
      });
  }, [lang]);

  /* ---- track labels helper ---- */
  const getTrackLabel = useCallback(
    (track: string) => {
      const map = lang === 'zh' ? TRACK_LABELS_ZH : TRACK_LABELS_EN;
      return map[track] ?? track;
    },
    [lang],
  );

  /* ---- derived ---- */
  const totalQuestions = questions.length;
  const answeredCount = Object.keys(answers).length;
  const progressPct = totalQuestions > 0 ? Math.round((answeredCount / totalQuestions) * 100) : 0;
  const canSubmit = answeredCount === totalQuestions && totalQuestions > 0;
  const currentQuestion = questions[currentQ] ?? null;

  /* ---- grouped by track for results ---- */
  const trackOrder = useMemo(() => {
    if (!results) return [];
    return results.tracks.sort((a, b) => a.percentage - b.percentage);
  }, [results]);

  const weakestTrackLabel = useMemo(() => {
    if (!results) return '';
    return getTrackLabel(results.weakest_track);
  }, [results, getTrackLabel]);

  /* ---- actions ---- */
  const selectAnswer = useCallback(
    (questionId: string, optionId: string) => {
      setAnswers((prev) => ({ ...prev, [questionId]: optionId }));
    },
    [],
  );

  const goNext = useCallback(() => {
    setCurrentQ((i) => Math.min(totalQuestions - 1, i + 1));
  }, [totalQuestions]);

  const goPrev = useCallback(() => {
    setCurrentQ((i) => Math.max(0, i - 1));
  }, []);

  const jumpTo = useCallback((idx: number) => {
    setCurrentQ(idx);
  }, []);

  const submitAssessment = useCallback(async () => {
    if (!canSubmit) return;
    setStep('submitting');
    setError(null);
    try {
      const payload = Object.entries(answers).map(([questionId, optionId]) => ({
        question_id: questionId,
        option_id: optionId,
      }));
      const res = await fetch(`${API_BASE}/api/assessment/submit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answers: payload }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data: AssessmentResults = await res.json();
      setResults(data);
      setStep('results');
    } catch (err) {
      console.error('Failed to submit assessment:', err);
      setError(
        lang === 'zh'
          ? '提交失败，请检查网络后重试。'
          : 'Submission failed. Please check your connection and try again.',
      );
      setStep('questions');
    }
  }, [canSubmit, answers, lang]);

  const retakeAssessment = useCallback(() => {
    setAnswers({});
    setResults(null);
    setCurrentQ(0);
    setError(null);
  }, []);

  /* ---- keyboard nav ---- */
  useEffect(() => {
    if (step !== 'questions') return;
    const handler = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;
      if (e.key === 'ArrowRight' || e.key === 'j') {
        e.preventDefault();
        goNext();
      } else if (e.key === 'ArrowLeft' || e.key === 'k') {
        e.preventDefault();
        goPrev();
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [step, goNext, goPrev]);

  /* ================================================================ */
  /*  Render: Loading                                                  */
  /* ================================================================ */

  if (step === 'loading') {
    return (
      <div className="min-h-screen bg-[#0a0a0a] flex items-center justify-center">
        <div className="text-center space-y-4">
          <div className="w-10 h-10 border-2 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto" />
          <div className="text-gray-400 text-lg">
            {lang === 'zh' ? '加载评估题目...' : 'Loading assessment...'}
          </div>
        </div>
      </div>
    );
  }

  /* ================================================================ */
  /*  Render: Submitting                                               */
  /* ================================================================ */

  if (step === 'submitting') {
    return (
      <div className="min-h-screen bg-[#0a0a0a] flex items-center justify-center">
        <div className="text-center space-y-4">
          <div className="w-10 h-10 border-2 border-purple-500 border-t-transparent rounded-full animate-spin mx-auto" />
          <div className="text-gray-400 text-lg">
            {lang === 'zh' ? '正在评估你的能力...' : 'Evaluating your skills...'}
          </div>
        </div>
      </div>
    );
  }

  /* ================================================================ */
  /*  Render: Results                                                  */
  /* ================================================================ */

  if (step === 'results' && results) {
    const circumference = 2 * Math.PI * 54;
    const offset = circumference - (results.overall_percentage / 100) * circumference;

    return (
      <div className="min-h-screen bg-[#0a0a0a]">
        {/* Header */}
        <header className="border-b border-gray-800 bg-[#0a0a0a]/80 backdrop-blur-sm sticky top-0 z-50">
          <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Link
                href="/"
                className="text-gray-400 hover:text-white transition-colors text-sm"
              >
                {t('nav.home')}
              </Link>
              <span className="text-gray-600">/</span>
              <h1 className="text-lg font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                {lang === 'zh' ? '评估报告' : 'Assessment Report'}
              </h1>
            </div>
            <button
              onClick={toggle}
              className="px-3 py-1 rounded-full text-xs font-medium bg-gray-800 text-gray-300 hover:bg-gray-700 border border-gray-700 transition-all"
            >
              {lang === 'zh' ? '中/EN' : 'EN/中'}
            </button>
          </div>
        </header>

        <div className="max-w-4xl mx-auto px-4 py-10 space-y-10">
          {/* Overall Score */}
          <div className="flex flex-col items-center text-center space-y-4">
            <div className="relative w-36 h-36">
              <svg className="w-full h-full -rotate-90" viewBox="0 0 120 120">
                <circle
                  cx="60"
                  cy="60"
                  r="54"
                  fill="none"
                  stroke="#1f2937"
                  strokeWidth="8"
                />
                <circle
                  cx="60"
                  cy="60"
                  r="54"
                  fill="none"
                  stroke="url(#scoreGradient)"
                  strokeWidth="8"
                  strokeLinecap="round"
                  strokeDasharray={circumference}
                  strokeDashoffset={offset}
                  className="transition-all duration-1000 ease-out"
                />
                <defs>
                  <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stopColor="#3b82f6" />
                    <stop offset="100%" stopColor="#a855f7" />
                  </linearGradient>
                </defs>
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-4xl font-bold text-white">
                  {results.overall_percentage}%
                </span>
                <span className="text-xs text-gray-500">
                  {results.overall_score}/{results.overall_total}
                </span>
              </div>
            </div>
            <div>
              <p className="text-gray-300 text-lg font-medium">
                {lang === 'zh'
                  ? `你的总体水平：${LEVEL_LABELS[getLevel(results.overall_percentage)][lang]}`
                  : `Your overall level: ${LEVEL_LABELS[getLevel(results.overall_percentage)][lang]}`}
              </p>
              <p className="text-gray-500 text-sm mt-1">
                {lang === 'zh'
                  ? '以下是你在各能力维度的详细评估'
                  : 'Here is your detailed assessment across all tracks'}
              </p>
            </div>
          </div>

          {/* Per-Track Scores */}
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-white">
              {lang === 'zh' ? '各维度得分' : 'Track Breakdown'}
            </h2>
            {trackOrder.map((track) => {
              const level = getLevel(track.percentage);
              const color = TRACK_COLORS[track.track] ?? '#6b7280';
              const icon = TRACK_ICONS[track.track] ?? '📊';
              return (
                <div
                  key={track.track}
                  className="rounded-xl border border-gray-800 bg-gray-900/50 p-5"
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <span className="text-lg">{icon}</span>
                      <span className="text-sm font-medium text-gray-200">
                        {getTrackLabel(track.track)}
                      </span>
                    </div>
                    <div className="flex items-center gap-3">
                      <span
                        className={`text-xs font-medium px-2 py-0.5 rounded-full ${LEVEL_COLORS[level]} bg-gray-800`}
                      >
                        {LEVEL_LABELS[level][lang]}
                      </span>
                      <span className="text-sm font-bold text-white tabular-nums">
                        {track.percentage}%
                      </span>
                    </div>
                  </div>
                  <div className="h-2.5 bg-gray-800 rounded-full overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all duration-1000 ease-out"
                      style={{
                        width: `${track.percentage}%`,
                        background: `linear-gradient(90deg, ${color}, ${color}88)`,
                      }}
                    />
                  </div>
                  <div className="mt-2 text-xs text-gray-500">
                    {track.score}/{track.total}{' '}
                    {lang === 'zh' ? '题正确' : 'correct'}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Recommended Next Steps */}
          <div className="rounded-xl border border-blue-800/50 bg-blue-900/10 p-6 space-y-4">
            <h2 className="text-lg font-semibold text-blue-300">
              {lang === 'zh' ? '建议下一步' : 'Recommended Next Steps'}
            </h2>
            <p className="text-gray-300 text-sm leading-relaxed">
              {lang === 'zh'
                ? `你在「${weakestTrackLabel}」维度得分最低，建议优先加强该领域的学习。下方按钮将跳转到对应的学习模块。`
                : `Your weakest track is "${weakestTrackLabel}". We recommend focusing on this area first. The button below will take you to the relevant learning module.`}
            </p>
            <div className="flex flex-wrap gap-3 pt-2">
              <Link
                href={`/learn/${results.weakest_track}`}
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-gradient-to-r from-blue-600 to-purple-600 text-white text-sm font-medium hover:from-blue-500 hover:to-purple-500 transition-all shadow-lg shadow-blue-500/20"
              >
                {lang === 'zh' ? '开始训练' : 'Start Training'}
                <span aria-hidden="true">&rarr;</span>
              </Link>
              <button
                onClick={retakeAssessment}
                className="px-5 py-2.5 rounded-lg bg-gray-800 text-gray-300 text-sm font-medium hover:bg-gray-700 border border-gray-700 transition-all"
              >
                {lang === 'zh' ? '重新评估' : 'Retake Assessment'}
              </button>
            </div>
          </div>

          {/* Footer */}
          <footer className="pt-8 border-t border-gray-800 text-center text-gray-500 text-sm pb-12">
            <p>{t('footer.quote')}</p>
          </footer>
        </div>
      </div>
    );
  }

  /* ================================================================ */
  /*  Render: Questions                                                */
  /* ================================================================ */

  return (
    <div className="min-h-screen bg-[#0a0a0a]">
      {/* Header */}
      <header className="border-b border-gray-800 bg-[#0a0a0a]/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link
              href="/"
              className="text-gray-400 hover:text-white transition-colors text-sm"
            >
              {t('nav.home')}
            </Link>
            <span className="text-gray-600">/</span>
            <h1 className="text-lg font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              {lang === 'zh' ? '能力评估' : 'Skill Assessment'}
            </h1>
          </div>
          <button
            onClick={toggle}
            className="px-3 py-1 rounded-full text-xs font-medium bg-gray-800 text-gray-300 hover:bg-gray-700 border border-gray-700 transition-all"
          >
            {lang === 'zh' ? '中/EN' : 'EN/中'}
          </button>
        </div>
        {/* Progress bar */}
        <div className="h-1 bg-gray-800 relative">
          <div
            className="h-full bg-gradient-to-r from-blue-500 to-purple-500 transition-all duration-500"
            style={{ width: `${progressPct}%` }}
          />
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Error banner */}
        {error && (
          <div className="mb-6 rounded-xl border border-red-800/50 bg-red-900/20 px-5 py-4 text-red-300 text-sm">
            {error}
          </div>
        )}

        {questions.length === 0 && !error ? (
          <div className="text-center text-gray-500 py-20">
            {lang === 'zh' ? '暂无评估题目' : 'No assessment questions available.'}
          </div>
        ) : (
          <>
            {/* Progress info + question counter */}
            <div className="flex items-center justify-between mb-6">
              <div className="text-sm text-gray-400">
                {lang === 'zh'
                  ? `第 ${currentQ + 1} / ${totalQuestions} 题`
                  : `Question ${currentQ + 1} / ${totalQuestions}`}
              </div>
              <div className="text-sm text-gray-500">
                {lang === 'zh'
                  ? `已答 ${answeredCount} 题`
                  : `${answeredCount} answered`}
                {answeredCount < totalQuestions && (
                  <span className="ml-2 text-gray-600">
                    ({lang === 'zh' ? `剩余 ${totalQuestions - answeredCount} 题` : `${totalQuestions - answeredCount} remaining`})
                  </span>
                )}
              </div>
            </div>

            {/* Question card */}
            {currentQuestion && (
              <div className="animate-fade-in" key={currentQuestion.id}>
                <div className="rounded-2xl border border-gray-800 bg-gray-900/50 p-6 md:p-8 mb-6">
                  {/* Track tag */}
                  <div className="mb-4">
                    <span
                      className="inline-flex items-center gap-1.5 text-xs px-2.5 py-1 rounded-full border"
                      style={{
                        borderColor: `${TRACK_COLORS[currentQuestion.track] ?? '#6b7280'}40`,
                        backgroundColor: `${TRACK_COLORS[currentQuestion.track] ?? '#6b7280'}15`,
                        color: TRACK_COLORS[currentQuestion.track] ?? '#9ca3af',
                      }}
                    >
                      <span>{TRACK_ICONS[currentQuestion.track] ?? '📊'}</span>
                      {getTrackLabel(currentQuestion.track)}
                    </span>
                  </div>

                  {/* Question text */}
                  <h2 className="text-lg md:text-xl font-semibold text-white mb-6 leading-relaxed">
                    {currentQuestion.text}
                  </h2>

                  {/* Options */}
                  <div className="space-y-3">
                    {currentQuestion.options.map((opt) => {
                      const isSelected = answers[currentQuestion.id] === opt.id;
                      return (
                        <button
                          key={opt.id}
                          onClick={() => selectAnswer(currentQuestion.id, opt.id)}
                          className={`w-full text-left px-5 py-4 rounded-xl border-2 transition-all duration-200 ${
                            isSelected
                              ? 'border-blue-500 bg-blue-900/30 text-white shadow-lg shadow-blue-500/10'
                              : 'border-gray-700 bg-gray-800/50 text-gray-300 hover:border-gray-600 hover:bg-gray-800'
                          }`}
                        >
                          <div className="flex items-start gap-3">
                            <div
                              className={`mt-0.5 w-5 h-5 rounded-full border-2 flex-shrink-0 flex items-center justify-center transition-all ${
                                isSelected
                                  ? 'border-blue-400 bg-blue-500'
                                  : 'border-gray-600'
                              }`}
                            >
                              {isSelected && (
                                <div className="w-2 h-2 rounded-full bg-white" />
                              )}
                            </div>
                            <span className="text-sm md:text-base leading-relaxed">
                              {opt.text}
                            </span>
                          </div>
                        </button>
                      );
                    })}
                  </div>
                </div>
              </div>
            )}

            {/* Navigation */}
            <div className="flex items-center justify-between mb-8">
              <button
                onClick={goPrev}
                disabled={currentQ === 0}
                className="px-5 py-2.5 rounded-lg bg-gray-800 text-gray-300 hover:bg-gray-700 disabled:opacity-30 text-sm transition-all"
              >
                {lang === 'zh' ? '上一题' : 'Previous'}
              </button>

              {currentQ < totalQuestions - 1 ? (
                <button
                  onClick={goNext}
                  className="px-5 py-2.5 rounded-lg bg-blue-600 text-white hover:bg-blue-700 text-sm transition-all"
                >
                  {lang === 'zh' ? '下一题' : 'Next'}
                </button>
              ) : (
                <button
                  onClick={submitAssessment}
                  disabled={!canSubmit}
                  className={`px-6 py-2.5 rounded-lg text-sm font-medium transition-all ${
                    canSubmit
                      ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-500 hover:to-purple-500 shadow-lg shadow-purple-500/20'
                      : 'bg-gray-800 text-gray-500 cursor-not-allowed'
                  }`}
                >
                  {lang === 'zh' ? '提交评估' : 'Submit Assessment'}
                </button>
              )}
            </div>

            {/* Question dot map */}
            <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-5">
              <div className="text-xs text-gray-500 mb-3 uppercase tracking-wider">
                {lang === 'zh' ? '题目导航' : 'Question Map'}
              </div>
              <div className="flex flex-wrap gap-2">
                {questions.map((q, i) => {
                  const answered = answers[q.id] !== undefined;
                  const active = i === currentQ;
                  return (
                    <button
                      key={q.id}
                      onClick={() => jumpTo(i)}
                      className={`w-8 h-8 rounded-lg text-xs font-medium transition-all flex items-center justify-center ${
                        active
                          ? 'bg-blue-600 text-white ring-2 ring-blue-400/50 scale-110'
                          : answered
                          ? 'bg-green-800/60 text-green-300 border border-green-700/50'
                          : 'bg-gray-800 text-gray-500 hover:bg-gray-700 border border-gray-700'
                      }`}
                    >
                      {i + 1}
                    </button>
                  );
                })}
              </div>
              <div className="flex items-center gap-4 mt-3 text-[11px] text-gray-600">
                <div className="flex items-center gap-1.5">
                  <div className="w-3 h-3 rounded bg-blue-600" />
                  {lang === 'zh' ? '当前' : 'Current'}
                </div>
                <div className="flex items-center gap-1.5">
                  <div className="w-3 h-3 rounded bg-green-800/60 border border-green-700/50" />
                  {lang === 'zh' ? '已答' : 'Answered'}
                </div>
                <div className="flex items-center gap-1.5">
                  <div className="w-3 h-3 rounded bg-gray-800 border border-gray-700" />
                  {lang === 'zh' ? '未答' : 'Unanswered'}
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Helpers                                                            */
/* ------------------------------------------------------------------ */

function getLevel(percentage: number): 'beginner' | 'intermediate' | 'advanced' | 'expert' {
  if (percentage >= 75) return 'expert';
  if (percentage >= 50) return 'advanced';
  if (percentage >= 25) return 'intermediate';
  return 'beginner';
}
