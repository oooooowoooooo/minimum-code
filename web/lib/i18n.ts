'use client';

import { useState, useEffect, useCallback } from 'react';

export type Lang = 'zh' | 'en';

const STORAGE_KEY = 'app_lang';

const translations: Record<string, Record<Lang, string>> = {
  // Header
  'header.title': { zh: 'AI 应用开发工程师训练系统', en: 'AI App Engineer Training System' },
  'header.subtitle': { zh: '最小工程能力训练闭环', en: 'Minimum Engineering Capability Training Loop' },

  // Stats
  'stats.total': { zh: '知识点总数', en: 'Total Points' },
  'stats.completed': { zh: '已完成', en: 'Completed' },
  'stats.week_points': { zh: '本周知识点', en: 'Week Points' },

  // Categories
  'cat.all': { zh: '全部', en: 'All' },

  // Actions
  'action.start': { zh: '开始学习', en: 'Start Learning' },
  'action.mark_complete': { zh: '标记完成', en: 'Mark Complete' },
  'action.completed': { zh: '已完成', en: 'Completed' },

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
  'nav.home': { zh: '首页', en: 'Home' },
  'nav.tracks': { zh: '能力模块', en: 'Tracks' },
  'nav.labs': { zh: '工程 Lab', en: 'Labs' },
  'nav.assessment': { zh: '能力测评', en: 'Assessment' },
  'nav.interview': { zh: '面试表达', en: 'Interview' },

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

  // Assessment
  'assessment.title': { zh: '能力测评', en: 'Capability Assessment' },
  'assessment.desc': { zh: '评估你的 AI 应用开发工程能力', en: 'Evaluate your AI app engineering capabilities' },
  'assessment.start': { zh: '开始测评', en: 'Start Assessment' },
  'assessment.next': { zh: '下一题', en: 'Next Question' },
  'assessment.prev': { zh: '上一题', en: 'Previous' },
  'assessment.submit': { zh: '提交测评', en: 'Submit Assessment' },
  'assessment.results': { zh: '测评结果', en: 'Assessment Results' },
  'assessment.score': { zh: '总分', en: 'Total Score' },
  'assessment.level.beginner': { zh: '入门', en: 'Beginner' },
  'assessment.level.intermediate': { zh: '进阶', en: 'Intermediate' },
  'assessment.level.advanced': { zh: '高级', en: 'Advanced' },
  'assessment.level.expert': { zh: '专家', en: 'Expert' },
  'assessment.retake': { zh: '重新测评', en: 'Retake Assessment' },
  'assessment.recommend': { zh: '推荐训练', en: 'Recommended Training' },

  // Tracks
  'tracks.title': { zh: '能力模块', en: 'Capability Tracks' },
  'tracks.desc': { zh: '六大核心能力训练模块', en: 'Six core capability training modules' },
  'tracks.skills': { zh: '技能项', en: 'skills' },
  'tracks.progress': { zh: '进度', en: 'Progress' },
  'tracks.start': { zh: '开始训练', en: 'Start Training' },
  'tracks.view_all': { zh: '查看全部', en: 'View All' },

  // Track names
  'track.python-engineering': { zh: 'Python 工程化', en: 'Python Engineering' },
  'track.fastapi-services': { zh: 'FastAPI 服务', en: 'FastAPI Services' },
  'track.llm-api-client': { zh: 'LLM API 客户端', en: 'LLM API Client' },
  'track.rag-system': { zh: 'RAG 系统', en: 'RAG System' },
  'track.agent-engineering': { zh: 'Agent 工程', en: 'Agent Engineering' },
  'track.deploy-quality': { zh: '部署与质量', en: 'Deployment & Quality' },

  // Labs
  'labs.title': { zh: '工程 Lab', en: 'Engineering Labs' },
  'labs.desc': { zh: '通过可运行任务训练工程能力', en: 'Train engineering skills through runnable tasks' },
  'labs.starter': { zh: '起始代码', en: 'Starter Code' },
  'labs.tests': { zh: '测试文件', en: 'Test File' },
  'labs.solution': { zh: '我的方案', en: 'My Solution' },
  'labs.results': { zh: '运行结果', en: 'Results' },
  'labs.run': { zh: '运行测试', en: 'Run Tests' },
  'labs.copy': { zh: '复制代码', en: 'Copy Code' },
  'labs.copied': { zh: '已复制', en: 'Copied!' },
  'labs.mark_complete': { zh: '标记完成', en: 'Mark Complete' },
  'labs.completed': { zh: '已完成', en: 'Completed' },
  'labs.difficulty.beginner': { zh: '入门', en: 'Beginner' },
  'labs.difficulty.intermediate': { zh: '中级', en: 'Intermediate' },
  'labs.difficulty.advanced': { zh: '高级', en: 'Advanced' },
  'labs.estimated': { zh: '预计用时', en: 'Estimated' },
  'labs.minutes': { zh: '分钟', en: 'minutes' },
  'labs.task': { zh: '任务', en: 'Task' },
  'labs.acceptance': { zh: '验收标准', en: 'Acceptance Criteria' },

  // Interview
  'interview.title': { zh: '面试表达', en: 'Interview Expression' },
  'interview.desc': { zh: '将训练成果转化为面试表达', en: 'Convert training results into interview expressions' },
  'interview.generate': { zh: '生成面试表达', en: 'Generate Expressions' },
  'interview.generating': { zh: '生成中...', en: 'Generating...' },
  'interview.copy_all': { zh: '复制全部', en: 'Copy All' },
  'interview.resume_bullets': { zh: '简历要点', en: 'Resume Bullets' },
  'interview.star': { zh: 'STAR 方法', en: 'STAR Method' },
  'interview.situation': { zh: '情境', en: 'Situation' },
  'interview.task': { zh: '任务', en: 'Task' },
  'interview.action': { zh: '行动', en: 'Action' },
  'interview.result': { zh: '结果', en: 'Result' },
  'interview.no_labs': { zh: '完成 Lab 后即可生成面试表达', en: 'Complete Labs to generate interview expressions' },

  // Dashboard
  'dashboard.welcome': { zh: '欢迎回来', en: 'Welcome Back' },
  'dashboard.overall_progress': { zh: '总体进度', en: 'Overall Progress' },
  'dashboard.labs_completed': { zh: '已完成 Lab', en: 'Labs Completed' },
  'dashboard.skills_mastered': { zh: '已掌握技能', en: 'Skills Mastered' },
  'dashboard.continue_training': { zh: '继续训练', en: 'Continue Training' },
  'dashboard.view_labs': { zh: '查看 Lab', en: 'View Labs' },

  // Footer
  'footer.quote': { zh: 'AI 时代，只学最少的代码，学会最强的架构。', en: 'In the AI era, learn the least code, master the strongest architecture.' },
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
