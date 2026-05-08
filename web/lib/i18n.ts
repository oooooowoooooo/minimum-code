'use client';

import { useState, useEffect, useCallback } from 'react';

export type Lang = 'zh' | 'en';

const STORAGE_KEY = 'app_lang';

const translations: Record<string, Record<Lang, string>> = {
  // Header
  'header.title': { zh: 'AI 时代 — 编程学习平台', en: 'AI Era — Learn Programming' },
  'header.subtitle': { zh: '用工业级项目拆解掌握 Python + TypeScript', en: 'Master Python + TypeScript through industrial projects' },
  'header.knowledge': { zh: '知识点学习 →', en: 'Knowledge Points →' },
  'header.modules': { zh: '模块', en: 'modules' },

  // Stats
  'stats.total': { zh: '知识点总数', en: 'Total Points' },
  'stats.completed': { zh: '已完成', en: 'Completed' },
  'stats.week_points': { zh: '本周知识点', en: 'Week Points' },

  // Categories
  'cat.all': { zh: '全部', en: 'All' },
  'cat.cognitive': { zh: '认知升级', en: 'Cognitive Upgrade' },
  'cat.python-fundamentals': { zh: 'Python 基础', en: 'Python Fundamentals' },
  'cat.typescript-fundamentals': { zh: 'TypeScript 基础', en: 'TypeScript Fundamentals' },
  'cat.patterns': { zh: '设计模式', en: 'Design Patterns' },
  'cat.python-dissect': { zh: 'Python 项目拆解', en: 'Python Projects' },
  'cat.typescript-dissect': { zh: 'TypeScript 项目拆解', en: 'TypeScript Projects' },
  'cat.ai-mastery': { zh: 'AI 工具精通', en: 'AI Tool Mastery' },
  'cat.practice': { zh: '综合实战', en: 'Comprehensive Practice' },

  // Week descriptions
  'week.1.desc': { zh: '— 认知升级 + 语言速通', en: '— Language Speedrun + Cognitive Upgrade' },
  'week.2.desc': { zh: '— Python 变量与类型', en: '— Python Variables & Types' },
  'week.3.desc': { zh: '— Python 数据结构与文件', en: '— Python Data Structures & Files' },
  'week.4.desc': { zh: '— Python 控制流与循环', en: '— Python Control Flow & Loops' },
  'week.5.desc': { zh: '— Python 函数与闭包', en: '— Python Functions & Closures' },
  'week.6.desc': { zh: '— Python 类与继承', en: '— Python Classes & Inheritance' },
  'week.7.desc': { zh: '— Python 异步与模块', en: '— Python Async & Modules' },
  'week.8.desc': { zh: '— TypeScript 类型与函数', en: '— TypeScript Types & Functions' },
  'week.9.desc': { zh: '— TypeScript 接口与异步', en: '— TypeScript Interfaces & Async' },
  'week.10.desc': { zh: '— 装饰器与设计模式', en: '— Decorators & Design Patterns' },
  'week.11.desc': { zh: '— 模式深入与框架实战', en: '— Patterns Deep Dive & Frameworks' },
  'week.12.desc': { zh: '— AI 架构与工具链', en: '— AI Architecture & Toolchain' },

  // Actions
  'action.start': { zh: '开始学习 →', en: 'Start →' },
  'action.mark_complete': { zh: '标记完成', en: 'Mark Complete' },
  'action.completed': { zh: '✓ 已完成', en: '✓ Completed' },

  // Knowledge page
  'kp.title': { zh: '知识点学习', en: 'Knowledge Points' },
  'kp.search': { zh: '搜索知识点...', en: 'Search knowledge points...' },
  'kp.loading': { zh: '加载知识点...', en: 'Loading knowledge points...' },
  'kp.no_points': { zh: '暂无知识点', en: 'No knowledge points to display.' },
  'kp.week_progress': { zh: '本周进度', en: 'Week Progress' },
  'kp.total': { zh: '总计', en: 'Total' },
  'kp.random': { zh: '随机复习 (10)', en: 'Random Review (10)' },
  'kp.exit_random': { zh: '退出随机', en: 'Exit Random' },
  'kp.week_complete': { zh: '本周完成！', en: 'Week Complete!' },
  'kp.week_complete_msg': { zh: '所有知识点已掌握，做得好！', en: 'All knowledge points mastered. Great work!' },

  // Game
  'game.predict': { zh: '预测输出', en: 'Predict Output' },
  'game.find_bug': { zh: '找 Bug', en: 'Find Bug' },
  'game.fill_blank': { zh: '填空', en: 'Fill Blank' },
  'game.code_order': { zh: '代码排序', en: 'Code Order' },
  'game.challenge': { zh: '迷你挑战', en: 'Mini Challenge' },

  // Quiz
  'quiz.title': { zh: '小测验', en: 'Quiz' },
  'quiz.correct': { zh: '回答正确！', en: 'Correct!' },
  'quiz.wrong': { zh: '再想想', en: 'Not quite!' },
  'quiz.explanation': { zh: '解析：', en: 'Explanation: ' },

  // Navigation
  'nav.prev': { zh: '← 上一个', en: '← Previous' },
  'nav.next': { zh: '下一个 →', en: 'Next →' },
  'nav.home': { zh: '← 首页', en: '← Home' },

  // Footer
  'footer.quote': { zh: 'AI 时代，代码廉价，品味昂贵。', en: 'In the AI era, code is cheap. Taste is expensive.' },

  // Keyboard
  'kb.title': { zh: '快捷键', en: 'Keyboard' },
  'kb.next': { zh: '下一个', en: 'Next' },
  'kb.prev': { zh: '上一个', en: 'Prev' },
  'kb.toggle': { zh: '展开/收起', en: 'Toggle' },

  // Points map
  'map.title': { zh: '知识点地图', en: 'Points Map' },

  // Explanation & Code
  'section.explanation': { zh: '讲解', en: 'Explanation' },
  'section.code': { zh: '代码示例', en: 'Code Example' },
};

export function getLang(): Lang {
  if (typeof window === 'undefined') return 'zh';
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored === 'en' || stored === 'zh') return stored;
  } catch {}
  return 'zh';
}

export function setLang(lang: Lang) {
  localStorage.setItem(STORAGE_KEY, lang);
}

export function t(key: string, lang: Lang): string {
  return translations[key]?.[lang] ?? key;
}

export function useLang() {
  const [lang, setLangState] = useState<Lang>('zh');

  useEffect(() => {
    setLangState(getLang());
  }, []);

  const toggle = useCallback(() => {
    const next = lang === 'zh' ? 'en' : 'zh';
    setLang(next);
    setLangState(next);
  }, [lang]);

  const translate = useCallback((key: string) => t(key, lang), [lang]);

  return { lang, toggle, t: translate };
}
