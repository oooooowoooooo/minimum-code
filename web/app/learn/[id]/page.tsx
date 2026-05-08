'use client';

import { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { useLang } from '@/lib/i18n';

const API = 'http://localhost:8000';

interface Section {
  title: string;
  content: string;
  type: string;
  language?: string;
}

interface ModuleContent {
  id: string;
  title: string;
  category: string;
  icon: string;
  sections: Section[];
}

interface QuizQuestion {
  question: string;
  options: string[];
  correct: number;
  explanation: string;
}

export default function LearnPage() {
  const { lang, toggle, t } = useLang();
  const params = useParams();
  const moduleId = params.id as string;

  const [content, setContent] = useState<ModuleContent | null>(null);
  const [quiz, setQuiz] = useState<QuizQuestion[]>([]);
  const [isComplete, setIsComplete] = useState(false);
  const [loading, setLoading] = useState(true);
  const [activeSection, setActiveSection] = useState(0);
  const [quizAnswers, setQuizAnswers] = useState<Record<number, number>>({});
  const [showQuiz, setShowQuiz] = useState(false);
  const mainRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    Promise.all([
      fetch(`${API}/api/modules/${moduleId}`).then((r) => r.json()),
      fetch(`${API}/api/modules/${moduleId}/quiz`).then((r) => r.json()),
      fetch(`${API}/api/progress`).then((r) => r.json()),
    ])
      .then(([mod, q, prog]) => {
        setContent(mod);
        setQuiz(q);
        setIsComplete((prog.completed || []).includes(moduleId));
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [moduleId]);

  const scrollToSection = (index: number) => {
    setActiveSection(index);
    setShowQuiz(false);
    setTimeout(() => {
      const el = document.getElementById(`section-${index}`);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }, 50);
  };

  const scrollToQuiz = () => {
    setShowQuiz(true);
    setActiveSection(-1);
    setTimeout(() => {
      const el = document.getElementById('quiz-section');
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }, 50);
  };

  const toggleComplete = async () => {
    await fetch(`${API}/api/progress`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ module_id: moduleId, completed: !isComplete }),
    });
    setIsComplete(!isComplete);
  };

  const handleQuizAnswer = (questionIdx: number, answerIdx: number) => {
    setQuizAnswers((prev) => ({ ...prev, [questionIdx]: answerIdx }));
  };

  const retryQuestion = (questionIdx: number) => {
    setQuizAnswers((prev) => {
      const next = { ...prev };
      delete next[questionIdx];
      return next;
    });
  };

  const retryAllWrong = () => {
    setQuizAnswers((prev) => {
      const next: Record<number, number> = {};
      Object.entries(prev).forEach(([qi, answer]) => {
        const q = quiz[parseInt(qi)];
        if (q && answer === q.correct) {
          next[parseInt(qi)] = answer;
        }
      });
      return next;
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0a0a0a] flex items-center justify-center">
        <div className="text-gray-400">{lang === 'zh' ? '加载中...' : 'Loading...'}</div>
      </div>
    );
  }

  if (!content) {
    return (
      <div className="min-h-screen bg-[#0a0a0a] flex items-center justify-center">
        <div className="text-center">
          <div className="text-4xl mb-4">?</div>
          <div className="text-gray-400 mb-4">{lang === 'zh' ? '模块未找到' : 'Module not found'}</div>
          <Link href="/" className="text-blue-400 hover:underline">{t('nav.home')}</Link>
        </div>
      </div>
    );
  }

  const correctCount = quiz.filter((q, i) => quizAnswers[i] === q.correct).length;
  const answeredCount = Object.keys(quizAnswers).length;
  const wrongCount = answeredCount - correctCount;

  return (
    <div className="min-h-screen bg-[#0a0a0a]">
      {/* Header */}
      <header className="border-b border-gray-800 bg-[#0a0a0a]/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors text-sm">
            {t('nav.home')}
          </Link>
          <div className="flex items-center gap-4">
            <button
              onClick={toggle}
              className="px-3 py-1 rounded-full text-xs font-medium bg-gray-800 text-gray-300 hover:bg-gray-700 border border-gray-700 transition-all"
            >
              {lang === 'zh' ? '中/EN' : 'EN/中'}
            </button>
            <button
              onClick={toggleComplete}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                isComplete ? 'bg-green-500 text-white' : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
              }`}
            >
              {isComplete ? t('action.completed') : t('action.mark_complete')}
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-4 py-8 flex gap-8">
        {/* Sidebar */}
        <aside className="w-64 flex-shrink-0 hidden lg:block">
          <div className="sticky top-20">
            <div className="flex items-center gap-3 mb-6">
              <span className="text-3xl">{content.icon}</span>
              <div>
                <h1 className="font-bold text-lg">{content.title}</h1>
                <span className="text-xs text-gray-500 capitalize">{content.category.replace(/-/g, ' ')}</span>
              </div>
            </div>

            {/* Section Navigation */}
            <nav className="space-y-1 mb-8">
              {content.sections.map((section, i) => (
                <button
                  key={i}
                  onClick={() => scrollToSection(i)}
                  className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-all ${
                    !showQuiz && activeSection === i
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-400 hover:text-white hover:bg-gray-800'
                  }`}
                >
                  {section.title}
                </button>
              ))}
              {quiz.length > 0 && (
                <button
                  onClick={scrollToQuiz}
                  className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-all ${
                    showQuiz ? 'bg-purple-600 text-white' : 'text-gray-400 hover:text-white hover:bg-gray-800'
                  }`}
                >
                  {t('quiz.title')} ({quiz.length} {lang === 'zh' ? '题' : 'questions'})
                </button>
              )}
            </nav>

            {/* Progress */}
            <div className="p-4 rounded-lg bg-gray-900 border border-gray-800">
              <div className="text-sm text-gray-400 mb-2">{lang === 'zh' ? '章节进度' : 'Section Progress'}</div>
              <div className="text-2xl font-bold">
                {showQuiz ? `${content.sections.length}/${content.sections.length}` : `${activeSection + 1}/${content.sections.length}`}
              </div>
              <div className="h-2 bg-gray-800 rounded-full mt-2">
                <div
                  className="h-full bg-blue-500 rounded-full transition-all"
                  style={{ width: showQuiz ? '100%' : `${((activeSection + 1) / content.sections.length) * 100}%` }}
                />
              </div>
              {answeredCount > 0 && (
                <div className="mt-3 text-xs text-gray-400">
                  {t('quiz.title')}: {correctCount}/{answeredCount} {lang === 'zh' ? '正确' : 'correct'}
                </div>
              )}
            </div>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 min-w-0" ref={mainRef}>
          {/* Mobile Title */}
          <div className="lg:hidden flex items-center gap-3 mb-6">
            <span className="text-3xl">{content.icon}</span>
            <h1 className="font-bold text-xl">{content.title}</h1>
          </div>

          <div className="space-y-6">
            {/* Content Sections - always visible */}
            {content.sections.map((section, i) => (
              <div
                key={i}
                id={`section-${i}`}
                className={`rounded-xl border transition-all scroll-mt-20 ${
                  !showQuiz && activeSection === i ? 'border-blue-500 bg-gray-900' : 'border-gray-800 bg-gray-900/50'
                }`}
              >
                <div className="px-6 py-4 border-b border-gray-800 flex items-center justify-between">
                  <h2 className="font-bold text-lg">{section.title}</h2>
                  <span className="text-xs px-2 py-1 rounded bg-gray-800 text-gray-400 capitalize">
                    {section.type}
                  </span>
                </div>
                <div className="p-6">
                  {section.type === 'code' ? (
                    <pre className="bg-[#1a1a2e] rounded-lg p-4 overflow-x-auto text-sm">
                      <code className="text-gray-300 font-mono leading-relaxed">
                        {section.content}
                      </code>
                    </pre>
                  ) : (
                    <div className="text-gray-300 leading-relaxed whitespace-pre-line text-sm">
                      {section.content}
                    </div>
                  )}
                </div>
              </div>
            ))}

            {/* Quiz Section - always visible at bottom if quiz exists */}
            {quiz.length > 0 && (
              <div id="quiz-section" className="scroll-mt-20">
                <div className="rounded-xl border border-purple-500 bg-gray-900 p-6">
                  <h2 className="text-xl font-bold mb-2">{t('quiz.title')}</h2>
                  <p className="text-gray-400 text-sm mb-6">{lang === 'zh' ? `测试你对 ${content.title} 的理解` : `Test your understanding of ${content.title}`}</p>

                  {quiz.map((q, qi) => (
                    <div key={qi} className="mb-8 last:mb-0">
                      <h3 className="font-medium mb-3">
                        {qi + 1}. {q.question}
                      </h3>
                      <div className="space-y-2">
                        {q.options.map((opt, oi) => {
                          const answered = quizAnswers[qi] !== undefined;
                          const selected = quizAnswers[qi] === oi;
                          const isCorrect = oi === q.correct;

                          let bg = 'bg-gray-800 hover:bg-gray-700';
                          if (answered) {
                            if (selected && isCorrect) bg = 'bg-green-800 border-green-500';
                            else if (selected && !isCorrect) bg = 'bg-red-800 border-red-500';
                            else if (isCorrect) bg = 'bg-green-800/30 border-green-700';
                          }

                          return (
                            <button
                              key={oi}
                              onClick={() => !answered && handleQuizAnswer(qi, oi)}
                              disabled={answered}
                              className={`w-full text-left px-4 py-3 rounded-lg border border-transparent text-sm transition-all ${bg}`}
                            >
                              <span className="font-mono text-gray-500 mr-2">{String.fromCharCode(65 + oi)}.</span>
                              {opt}
                              {answered && isCorrect && <span className="ml-2 text-green-400">✓</span>}
                              {answered && selected && !isCorrect && <span className="ml-2 text-red-400">✗</span>}
                            </button>
                          );
                        })}
                      </div>
                      {quizAnswers[qi] !== undefined && (
                        <div className="mt-3 p-3 rounded-lg bg-gray-800/50 text-sm text-gray-300">
                          <div className="flex items-start justify-between">
                            <div>
                              <strong>{t('quiz.explanation')}</strong> {q.explanation}
                            </div>
                            {quizAnswers[qi] !== q.correct && (
                              <button
                                onClick={() => retryQuestion(qi)}
                                className="ml-4 px-3 py-1 rounded bg-yellow-600 text-white text-xs hover:bg-yellow-500 flex-shrink-0"
                              >
                                {lang === 'zh' ? '重试' : 'Retry'}
                              </button>
                            )}
                          </div>
                        </div>
                      )}
                    </div>
                  ))}

                  {answeredCount === quiz.length && (
                    <div className="mt-6 p-4 rounded-lg bg-gradient-to-r from-purple-900/50 to-blue-900/50 border border-purple-700/50">
                      <div className="text-lg font-bold mb-1">
                        Score: {correctCount}/{quiz.length}
                      </div>
                      <div className="text-gray-400 text-sm mb-3">
                        {correctCount === quiz.length
                          ? (lang === 'zh' ? '完美！你已掌握本模块。' : 'Perfect! You mastered this module.')
                          : (lang === 'zh' ? `${wrongCount} 题错误。复习解析后重试。` : `${wrongCount} wrong. Review explanations and retry.`)}
                      </div>
                      {wrongCount > 0 && (
                        <button
                          onClick={retryAllWrong}
                          className="px-4 py-2 rounded-lg bg-yellow-600 text-white text-sm hover:bg-yellow-500"
                        >
                          {lang === 'zh' ? `重试错误 (${wrongCount})` : `Retry All Wrong (${wrongCount})`}
                        </button>
                      )}
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Bottom Navigation */}
            <div className="flex justify-between pt-4">
              <button
                onClick={() => scrollToSection(Math.max(0, activeSection - 1))}
                disabled={activeSection <= 0}
                className="px-4 py-2 rounded-lg bg-gray-800 text-gray-300 hover:bg-gray-700 disabled:opacity-30 text-sm"
              >
                {lang === 'zh' ? '上一节' : 'Previous Section'}
              </button>
              {activeSection < content.sections.length - 1 ? (
                <button
                  onClick={() => scrollToSection(activeSection + 1)}
                  className="px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 text-sm"
                >
                  {lang === 'zh' ? '下一节' : 'Next Section'}
                </button>
              ) : quiz.length > 0 && !showQuiz ? (
                <button
                  onClick={scrollToQuiz}
                  className="px-4 py-2 rounded-lg bg-purple-600 text-white hover:bg-purple-700 text-sm"
                >
                  {lang === 'zh' ? '开始测验' : 'Take Quiz'}
                </button>
              ) : null}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
