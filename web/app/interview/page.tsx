'use client';

import { useState, useEffect, useCallback } from 'react';
import Link from 'next/link';
import { useLang } from '@/lib/i18n';
import { API_BASE } from '@/lib/api';
import { modules, CATEGORY_META, type ModuleCategory } from '@/lib/modules';

// ──────────────────────────────────────────────
//  Types
// ──────────────────────────────────────────────

interface CompletedLab {
  id: string;
  title: string;
  category: string;
  completedAt: string;
}

interface Expression {
  labId: string;
  labTitle: string;
  category: string;
  categoryLabel: string;
  summary: string;
  bullets: string[];
  star: {
    situation: string;
    task: string;
    action: string;
    result: string;
  };
}

// ──────────────────────────────────────────────
//  Localized content helpers
// ──────────────────────────────────────────────

const UI = {
  pageTitle: { zh: '面试表达生成器', en: 'Interview Expression Generator' },
  pageSubtitle: {
    zh: '将你的实验成果转化为面试可用的结构化表达',
    en: 'Convert your lab work into structured interview-ready expressions',
  },
  sectionLabs: { zh: '已完成实验', en: 'Completed Labs' },
  sectionLabsDesc: {
    zh: '以下是你标记为已完成的模块，将用于生成面试表达',
    en: 'Modules you have marked as complete, used to generate expressions',
  },
  sectionGenerate: { zh: '生成表达', en: 'Generate Expressions' },
  sectionGenerateDesc: {
    zh: '基于你的实验成果，AI 将生成 STAR 方法面试回答和简历要点',
    en: 'Based on your lab work, AI generates STAR method answers and resume bullets',
  },
  generateBtn: { zh: '生成面试表达', en: 'Generate Interview Expressions' },
  generating: { zh: '正在生成...', en: 'Generating...' },
  sectionExpressions: { zh: '面试表达卡片', en: 'Expression Cards' },
  summaryLabel: { zh: '一句话总结', en: 'One-Line Summary' },
  bulletsLabel: { zh: '技术要点', en: 'Technical Bullet Points' },
  starLabel: { zh: 'STAR 方法回答', en: 'STAR Method Answer' },
  situation: { zh: '情景 (Situation)', en: 'Situation' },
  task: { zh: '任务 (Task)', en: 'Task' },
  action: { zh: '行动 (Action)', en: 'Action' },
  result: { zh: '结果 (Result)', en: 'Result' },
  sectionResume: { zh: '简历要点生成器', en: 'Resume Bullet Generator' },
  sectionResumeDesc: {
    zh: '将面试表达格式化为简历要点',
    en: 'Format expressions into resume-ready bullet points',
  },
  copyAll: { zh: '复制全部', en: 'Copy All' },
  copied: { zh: '已复制!', en: 'Copied!' },
  copySummary: { zh: '复制总结', en: 'Copy Summary' },
  copyBullets: { zh: '复制要点', en: 'Copy Bullets' },
  copySTAR: { zh: '复制 STAR', en: 'Copy STAR' },
  copyFull: { zh: '复制完整表达', en: 'Copy Full Expression' },
  noLabs: {
    zh: '你还没有完成任何实验。完成实验后，可以在此生成面试表达。',
    en: 'You have not completed any labs yet. Complete labs first to generate expressions here.',
  },
  goToLabs: { zh: '去学习 →', en: 'Go to Labs →' },
  backHome: { zh: '← 首页', en: '← Home' },
  track: { zh: '能力轨道', en: 'Capability Track' },
  resumeFormat: {
    zh: '格式：用 [技术] 构建了 [什么]，实现了 [关键工程决策]，达成 [成果]',
    en: 'Format: Built [what] using [tech], implementing [key decisions], resulting in [outcome]',
  },
  errorGenerating: {
    zh: 'API 生成失败，使用本地模板生成',
    en: 'API failed, using local template generation',
  },
};

// ──────────────────────────────────────────────
//  Fallback expression generator
// ──────────────────────────────────────────────

function categoryToLabel(cat: string): string {
  const key = `cat.${cat}`;
  const map: Record<string, string> = {
    'cognitive': 'Cognitive Foundation',
    'python-fundamentals': 'Python Fundamentals',
    'typescript-fundamentals': 'TypeScript Fundamentals',
    'patterns': 'Industrial Patterns',
    'python-dissect': 'Python Project Dissection',
    'typescript-dissect': 'TS Project Dissection',
    'ai-mastery': 'AI Mastery',
    'practice': 'Practice Projects',
  };
  return map[cat] ?? cat;
}

function generateFallbackExpression(lab: CompletedLab, lang: 'zh' | 'en'): Expression {
  const mod = modules.find((m) => m.id === lab.id);
  const catLabel = categoryToLabel(lab.category);
  const title = mod?.title ?? lab.title;
  const desc = mod?.description ?? '';

  const isPattern = lab.category === 'patterns';
  const isDissect = lab.category === 'python-dissect' || lab.category === 'typescript-dissect';
  const isAI = lab.category === 'ai-mastery';
  const isCognitive = lab.category === 'cognitive';
  const isPractice = lab.category === 'practice';
  const isPy = lab.category === 'python-fundamentals';
  const isTs = lab.category === 'typescript-fundamentals';

  let summary: string;
  let bullets: string[];
  let star: Expression['star'];

  if (lang === 'zh') {
    summary = `完成了「${title}」模块的学习与实战练习，掌握了核心概念与工程实践。`;
    bullets = [
      `深入学习了 ${title} 的核心原理与实现方式`,
      `通过代码示例和交互练习强化理解`,
      `将概念应用到实际工程场景中`,
      `对比 Python 和 TypeScript 的实现差异`,
    ];
    star = {
      situation: `在学习 ${catLabel} 方向时，需要深入理解 ${title} 的核心概念。`,
      task: `系统性地学习 ${title}，理解其原理、最佳实践和常见陷阱。`,
      action: `通过阅读源码分析、编写代码示例、完成交互练习，逐步掌握核心要点。同时对比了不同语言的实现方式。`,
      result: `成功掌握了 ${title} 的核心知识，能够在面试中清晰地解释其原理和应用场景。`,
    };
  } else {
    summary = `Completed the "${title}" module with hands-on exercises, mastering core concepts and engineering practices.`;
    bullets = [
      `Studied the core principles and implementation of ${title}`,
      `Reinforced understanding through code examples and interactive exercises`,
      `Applied concepts to real-world engineering scenarios`,
      `Compared implementation differences across Python and TypeScript`,
    ];
    star = {
      situation: `While studying ${catLabel}, I needed to deeply understand the core concepts of ${title}.`,
      task: `Systematically learn ${title}, understanding its principles, best practices, and common pitfalls.`,
      action: `Studied source code analysis, wrote code examples, and completed interactive exercises to master the key points. Compared implementations across different languages.`,
      result: `Successfully mastered the core knowledge of ${title}, able to clearly explain its principles and use cases in interviews.`,
    };
  }

  // Tailor bullets based on category
  if (isPattern) {
    if (lang === 'zh') {
      bullets = [
        `深入研究了 ${title} 设计模式的原理和适用场景`,
        `用 Python 和 TypeScript 分别实现了该模式`,
        `分析了该模式在 AI 应用中的实际应用`,
        `理解了该模式与其他模式的组合使用方式`,
      ];
    } else {
      bullets = [
        `Studied the principles and use cases of the ${title} design pattern`,
        `Implemented the pattern in both Python and TypeScript`,
        `Analyzed practical applications of the pattern in AI systems`,
        `Understood how to compose this pattern with other patterns`,
      ];
    }
  } else if (isDissect) {
    if (lang === 'zh') {
      bullets = [
        `深入拆解了 ${title} 的源码架构和核心设计决策`,
        `提取了可复用的工程模式和最佳实践`,
        `分析了架构选择背后的技术权衡`,
        `总结了适用于自己项目的设计思路`,
      ];
    } else {
      bullets = [
        `Deep-dived into ${title}'s source code architecture and core design decisions`,
        `Extracted reusable engineering patterns and best practices`,
        `Analyzed technical tradeoffs behind architectural choices`,
        `Summarized design insights applicable to my own projects`,
      ];
    }
  } else if (isAI) {
    if (lang === 'zh') {
      bullets = [
        `掌握了 ${title} 的核心方法论和工作流`,
        `实践了 AI 辅助开发的高效技巧`,
        `学习了如何有效地指导 AI 工具完成复杂任务`,
        `理解了人机协作的最佳实践`,
      ];
    } else {
      bullets = [
        `Mastered the core methodology and workflow of ${title}`,
        `Practiced efficient techniques for AI-assisted development`,
        `Learned how to effectively direct AI tools for complex tasks`,
        `Understood best practices for human-AI collaboration`,
      ];
    }
  } else if (isPractice) {
    if (lang === 'zh') {
      bullets = [
        `完成了 ${title} 阶段的系统性实践`,
        `应用了之前学到的所有设计模式和工程原则`,
        `从需求分析到部署的完整工程流程体验`,
        `积累了工业级项目开发的实战经验`,
      ];
    } else {
      bullets = [
        `Completed the ${title} phase through systematic practice`,
        `Applied all previously learned design patterns and engineering principles`,
        `Experienced the full engineering lifecycle from requirements to deployment`,
        `Accumulated hands-on experience in industrial-grade project development`,
      ];
    }
  }

  return { labId: lab.id, labTitle: title, category: lab.category, categoryLabel: catLabel, summary, bullets, star };
}

function generateResumeBullet(expr: Expression, lang: 'zh' | 'en'): string {
  if (lang === 'zh') {
    return `Built ${expr.labTitle}（${expr.categoryLabel}），${expr.bullets[0] ?? ''}，${expr.bullets[1] ?? ''}`;
  }
  return `Built ${expr.labTitle} (${expr.categoryLabel}): ${expr.bullets[0] ?? ''}; ${expr.bullets[1] ?? ''}`;
}

// ──────────────────────────────────────────────
//  Copy helper
// ──────────────────────────────────────────────

function useCopyFeedback() {
  const [copiedKey, setCopiedKey] = useState<string | null>(null);

  const copy = useCallback(async (text: string, key: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedKey(key);
      setTimeout(() => setCopiedKey(null), 2000);
    } catch {
      // Fallback for older browsers
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      setCopiedKey(key);
      setTimeout(() => setCopiedKey(null), 2000);
    }
  }, []);

  return { copiedKey, copy };
}

// ──────────────────────────────────────────────
//  Main component
// ──────────────────────────────────────────────

export default function InterviewPage() {
  const { lang, toggle, t } = useLang();
  const [completedLabs, setCompletedLabs] = useState<CompletedLab[]>([]);
  const [expressions, setExpressions] = useState<Expression[]>([]);
  const [generating, setGenerating] = useState(false);
  const [generated, setGenerated] = useState(false);
  const [apiError, setApiError] = useState(false);
  const { copiedKey, copy } = useCopyFeedback();

  // ── Load completed labs from localStorage ──
  useEffect(() => {
    try {
      const raw = localStorage.getItem('ai-era-progress');
      if (!raw) return;
      const store = JSON.parse(raw) as { modules?: Record<string, { status: string; title: string; category: string; completedAt: string | null }> };
      if (!store.modules) return;

      const completed: CompletedLab[] = Object.entries(store.modules)
        .filter(([, m]) => m.status === 'complete' && m.completedAt)
        .map(([id, m]) => ({
          id,
          title: m.title,
          category: m.category,
          completedAt: m.completedAt!,
        }))
        .sort((a, b) => new Date(b.completedAt).getTime() - new Date(a.completedAt).getTime());

      setCompletedLabs(completed);
    } catch {}
  }, []);

  // ── Generate expressions ──
  const handleGenerate = useCallback(async () => {
    if (completedLabs.length === 0) return;
    setGenerating(true);
    setApiError(false);

    const labIds = completedLabs.map((l) => l.id);

    try {
      const res = await fetch(`${API_BASE}/api/interview/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lab_ids: labIds, lang }),
      });
      if (!res.ok) throw new Error(`API error: ${res.status}`);
      const data = await res.json();
      if (Array.isArray(data) && data.length > 0) {
        setExpressions(data as Expression[]);
      } else {
        throw new Error('Empty response');
      }
    } catch {
      setApiError(true);
      // Fallback: generate locally
      const fallback = completedLabs.map((lab) => generateFallbackExpression(lab, lang));
      setExpressions(fallback);
    } finally {
      setGenerating(false);
      setGenerated(true);
    }
  }, [completedLabs, lang]);

  // ── Build resume bullets ──
  const resumeBullets = expressions.map((expr) => generateResumeBullet(expr, lang));
  const resumeText = resumeBullets.map((b, i) => `${i + 1}. ${b}`).join('\n');

  // ── Full expression text for copying ──
  function fullExpressionText(expr: Expression): string {
    const lines: string[] = [];
    lines.push(`## ${expr.labTitle} (${expr.categoryLabel})`);
    lines.push('');
    lines.push(expr.summary);
    lines.push('');
    lines.push(lang === 'zh' ? '技术要点:' : 'Technical Bullets:');
    expr.bullets.forEach((b) => lines.push(`- ${b}`));
    lines.push('');
    lines.push('STAR Method:');
    lines.push(`  S: ${expr.star.situation}`);
    lines.push(`  T: ${expr.star.task}`);
    lines.push(`  A: ${expr.star.action}`);
    lines.push(`  R: ${expr.star.result}`);
    return lines.join('\n');
  }

  // ── Render ──
  return (
    <div className="min-h-screen bg-[#0a0a0a]">
      {/* Header */}
      <header className="border-b border-gray-800 bg-[#0a0a0a]/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
          <Link
            href="/"
            className="text-sm text-gray-400 hover:text-gray-200 transition-colors"
          >
            {UI.backHome[lang]}
          </Link>
          <h1 className="text-lg font-bold bg-gradient-to-r from-amber-400 to-orange-400 bg-clip-text text-transparent">
            {UI.pageTitle[lang]}
          </h1>
          <button
            onClick={toggle}
            className="px-3 py-1 rounded-full text-xs font-medium bg-gray-800 text-gray-300 hover:bg-gray-700 border border-gray-700 transition-all"
          >
            {lang === 'zh' ? '中/EN' : 'EN/中'}
          </button>
        </div>
      </header>

      <div className="max-w-5xl mx-auto px-4 py-8 space-y-12">
        {/* Page subtitle */}
        <div className="text-center">
          <p className="text-gray-400 text-sm">{UI.pageSubtitle[lang]}</p>
        </div>

        {/* ── Section 1: Completed Labs ── */}
        <section>
          <div className="flex items-center gap-3 mb-2">
            <span className="text-xl">✅</span>
            <h2 className="text-xl font-bold text-white">{UI.sectionLabs[lang]}</h2>
            <span className="ml-auto text-sm text-gray-500">
              {completedLabs.length} {lang === 'zh' ? '个模块' : 'modules'}
            </span>
          </div>
          <p className="text-sm text-gray-500 mb-4">{UI.sectionLabsDesc[lang]}</p>

          {completedLabs.length === 0 ? (
            <div className="p-8 rounded-xl border border-gray-800 bg-gray-900/30 text-center">
              <p className="text-gray-500 mb-4">{UI.noLabs[lang]}</p>
              <Link
                href="/"
                className="inline-block px-5 py-2 rounded-lg bg-gray-800 text-gray-300 hover:bg-gray-700 border border-gray-700 text-sm transition-all"
              >
                {UI.goToLabs[lang]}
              </Link>
            </div>
          ) : (
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
              {completedLabs.map((lab) => {
                const catColor = CATEGORY_META[lab.category as ModuleCategory]?.color ?? '#6b7280';
                return (
                  <div
                    key={lab.id}
                    className="relative p-3 rounded-lg border border-gray-800 bg-gray-900/50 group hover:border-gray-700 transition-all"
                  >
                    <div
                      className="absolute top-0 left-0 right-0 h-0.5 rounded-t-lg"
                      style={{ background: catColor }}
                    />
                    <span className="text-xs text-gray-500 block mb-1">{categoryToLabel(lab.category)}</span>
                    <span className="text-sm text-gray-200 font-medium leading-tight block">{lab.title}</span>
                  </div>
                );
              })}
            </div>
          )}
        </section>

        {/* ── Section 2: Generate Expressions ── */}
        {completedLabs.length > 0 && (
          <section>
            <div className="flex items-center gap-3 mb-2">
              <span className="text-xl">🎯</span>
              <h2 className="text-xl font-bold text-white">{UI.sectionGenerate[lang]}</h2>
            </div>
            <p className="text-sm text-gray-500 mb-4">{UI.sectionGenerateDesc[lang]}</p>

            <div className="flex items-center gap-4">
              <button
                onClick={handleGenerate}
                disabled={generating}
                className="relative px-6 py-3 rounded-xl font-medium text-sm transition-all disabled:opacity-50 disabled:cursor-not-allowed group"
                style={{
                  background: 'linear-gradient(135deg, #f59e0b 0%, #ef4444 100%)',
                  color: '#0a0a0a',
                }}
              >
                <span className="relative z-10">
                  {generating ? UI.generating[lang] : UI.generateBtn[lang]}
                </span>
                <div className="absolute inset-0 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity"
                  style={{ background: 'linear-gradient(135deg, #fbbf24 0%, #f87171 100%)' }}
                />
              </button>

              {apiError && (
                <span className="text-xs text-amber-500">{UI.errorGenerating[lang]}</span>
              )}
            </div>
          </section>
        )}

        {/* ── Section 3: Expression Cards ── */}
        {generated && expressions.length > 0 && (
          <section>
            <div className="flex items-center gap-3 mb-2">
              <span className="text-xl">💬</span>
              <h2 className="text-xl font-bold text-white">{UI.sectionExpressions[lang]}</h2>
            </div>

            <div className="space-y-6 mt-4">
              {expressions.map((expr) => {
                const copyKey = (suffix: string) => `${expr.labId}-${suffix}`;
                return (
                  <div
                    key={expr.labId}
                    className="relative rounded-xl overflow-hidden"
                  >
                    {/* Gradient border */}
                    <div className="absolute inset-0 rounded-xl p-[1px]"
                      style={{ background: 'linear-gradient(135deg, rgba(245,158,11,0.3), rgba(239,68,68,0.1), rgba(168,85,247,0.2))' }}
                    >
                      <div className="w-full h-full rounded-xl bg-[#111111]" />
                    </div>

                    <div className="relative p-6">
                      {/* Header */}
                      <div className="flex items-start justify-between mb-4">
                        <div>
                          <span className="text-xs text-gray-500 block mb-1">
                            {UI.track[lang]}: {expr.categoryLabel}
                          </span>
                          <h3 className="text-lg font-bold text-white">{expr.labTitle}</h3>
                        </div>
                        <button
                          onClick={() => copy(fullExpressionText(expr), copyKey('full'))}
                          className="px-3 py-1.5 rounded-lg text-xs font-medium bg-gray-800 text-gray-300 hover:bg-gray-700 border border-gray-700 transition-all flex items-center gap-1.5"
                        >
                          {copiedKey === copyKey('full') ? UI.copied[lang] : UI.copyFull[lang]}
                        </button>
                      </div>

                      {/* Summary */}
                      <div className="mb-5">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-xs font-medium text-gray-400 uppercase tracking-wider">{UI.summaryLabel[lang]}</span>
                          <button
                            onClick={() => copy(expr.summary, copyKey('summary'))}
                            className="text-xs text-gray-500 hover:text-gray-300 transition-colors"
                          >
                            {copiedKey === copyKey('summary') ? UI.copied[lang] : UI.copySummary[lang]}
                          </button>
                        </div>
                        <p className="text-gray-200 text-sm leading-relaxed pl-3 border-l-2 border-amber-500/30">
                          {expr.summary}
                        </p>
                      </div>

                      {/* Technical Bullets */}
                      <div className="mb-5">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-xs font-medium text-gray-400 uppercase tracking-wider">{UI.bulletsLabel[lang]}</span>
                          <button
                            onClick={() => copy(expr.bullets.map((b) => `- ${b}`).join('\n'), copyKey('bullets'))}
                            className="text-xs text-gray-500 hover:text-gray-300 transition-colors"
                          >
                            {copiedKey === copyKey('bullets') ? UI.copied[lang] : UI.copyBullets[lang]}
                          </button>
                        </div>
                        <ul className="space-y-1.5">
                          {expr.bullets.map((bullet, i) => (
                            <li key={i} className="text-gray-300 text-sm flex items-start gap-2">
                              <span className="text-amber-500 mt-1 shrink-0">&#8226;</span>
                              <span>{bullet}</span>
                            </li>
                          ))}
                        </ul>
                      </div>

                      {/* STAR Method */}
                      <div>
                        <div className="flex items-center justify-between mb-3">
                          <span className="text-xs font-medium text-gray-400 uppercase tracking-wider">{UI.starLabel[lang]}</span>
                          <button
                            onClick={() => {
                              const text = `S: ${expr.star.situation}\nT: ${expr.star.task}\nA: ${expr.star.action}\nR: ${expr.star.result}`;
                              copy(text, copyKey('star'));
                            }}
                            className="text-xs text-gray-500 hover:text-gray-300 transition-colors"
                          >
                            {copiedKey === copyKey('star') ? UI.copied[lang] : UI.copySTAR[lang]}
                          </button>
                        </div>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                          {[
                            { label: UI.situation[lang], value: expr.star.situation, letter: 'S', color: '#3b82f6' },
                            { label: UI.task[lang], value: expr.star.task, letter: 'T', color: '#8b5cf6' },
                            { label: UI.action[lang], value: expr.star.action, letter: 'A', color: '#f59e0b' },
                            { label: UI.result[lang], value: expr.star.result, letter: 'R', color: '#22c55e' },
                          ].map((item) => (
                            <div
                              key={item.letter}
                              className="p-3 rounded-lg bg-gray-900/80 border border-gray-800"
                            >
                              <div className="flex items-center gap-2 mb-1.5">
                                <span
                                  className="w-5 h-5 rounded flex items-center justify-center text-[10px] font-bold text-black"
                                  style={{ background: item.color }}
                                >
                                  {item.letter}
                                </span>
                                <span className="text-xs font-medium text-gray-400">{item.label}</span>
                              </div>
                              <p className="text-gray-300 text-sm leading-relaxed">{item.value}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </section>
        )}

        {/* ── Section 4: Resume Bullets ── */}
        {generated && expressions.length > 0 && (
          <section>
            <div className="flex items-center gap-3 mb-2">
              <span className="text-xl">📄</span>
              <h2 className="text-xl font-bold text-white">{UI.sectionResume[lang]}</h2>
            </div>
            <p className="text-sm text-gray-500 mb-4">{UI.sectionResumeDesc[lang]}</p>

            <div className="relative rounded-xl overflow-hidden">
              <div className="absolute inset-0 rounded-xl p-[1px]"
                style={{ background: 'linear-gradient(135deg, rgba(59,130,246,0.3), rgba(139,92,246,0.2))' }}
              >
                <div className="w-full h-full rounded-xl bg-[#111111]" />
              </div>

              <div className="relative p-6">
                <div className="flex items-center justify-between mb-4">
                  <p className="text-xs text-gray-500">{UI.resumeFormat[lang]}</p>
                  <button
                    onClick={() => copy(resumeText, 'resume-all')}
                    className="px-4 py-2 rounded-lg text-xs font-medium bg-gray-800 text-gray-300 hover:bg-gray-700 border border-gray-700 transition-all"
                  >
                    {copiedKey === 'resume-all' ? UI.copied[lang] : UI.copyAll[lang]}
                  </button>
                </div>
                <ol className="space-y-2">
                  {resumeBullets.map((bullet, i) => (
                    <li key={i} className="flex items-start gap-3 group/bullet">
                      <span className="text-gray-600 text-sm font-mono shrink-0 w-5 text-right">{i + 1}.</span>
                      <span className="text-gray-200 text-sm leading-relaxed">{bullet}</span>
                      <button
                        onClick={() => copy(bullet, `resume-${i}`)}
                        className="shrink-0 opacity-0 group-hover/bullet:opacity-100 text-xs text-gray-500 hover:text-gray-300 transition-all"
                      >
                        {copiedKey === `resume-${i}` ? UI.copied[lang] : lang === 'zh' ? '复制' : 'Copy'}
                      </button>
                    </li>
                  ))}
                </ol>
              </div>
            </div>
          </section>
        )}
      </div>

      {/* Footer */}
      <footer className="mt-8 pb-8 text-center text-gray-600 text-xs">
        <p>{t('footer.quote')}</p>
      </footer>
    </div>
  );
}
