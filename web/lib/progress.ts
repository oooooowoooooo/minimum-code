import { modules, CATEGORY_META, type ModuleStatus } from './modules';

const STORAGE_KEY = 'ai-era-progress';

// ──────────────────────────────────────────────
//  Types
// ──────────────────────────────────────────────

export interface ModuleProgress {
  id: string;
  title: string;
  category: string;
  status: ModuleStatus;
  completedAt: string | null;
}

export interface Achievement {
  id: string;
  name: string;
  description: string;
  icon: string;
  unlockedAt: string | null;
}

interface ProgressStore {
  modules: Record<string, ModuleProgress>;
  achievements: Achievement[];
}

// ──────────────────────────────────────────────
//  Achievement definitions
// ──────────────────────────────────────────────

const ACHIEVEMENT_DEFS: Omit<Achievement, 'unlockedAt'>[] = [
  { id: 'first-step',     name: 'First Step',           description: 'Complete your first module.',                    icon: '👣' },
  { id: 'cognitive-done', name: 'Mind Shift',            description: 'Complete all cognitive foundation modules.',     icon: '🧠' },
  { id: 'py-master',      name: 'Pythonista',            description: 'Complete all Python fundamentals.',              icon: '🐍' },
  { id: 'ts-master',      name: 'Type Whisperer',        description: 'Complete all TypeScript fundamentals.',          icon: '🔷' },
  { id: 'pattern-pro',    name: 'Pattern Pro',           description: 'Complete all industrial patterns.',              icon: '🧩' },
  { id: 'py-dissector',   name: 'Python Dissector',      description: 'Complete all Python project dissections.',        icon: '🔬' },
  { id: 'ts-dissector',   name: 'TS Dissector',          description: 'Complete all TypeScript project dissections.',   icon: '🔭' },
  { id: 'ai-pioneer',     name: 'AI Pioneer',            description: 'Complete all AI mastery modules.',               icon: '🤖' },
  { id: 'graduate',       name: 'Graduate',              description: 'Complete all practice projects.',                icon: '🎓' },
  { id: 'halfway',        name: 'Halfway There',         description: 'Reach 50% overall completion.',                  icon: '⛰️' },
  { id: 'completionist',  name: 'Completionist',         description: 'Complete every single module.',                  icon: '👑' },
  { id: 'streak-5',       name: 'On a Roll',             description: 'Complete 5 modules in one session.',             icon: '🔥' },
];

// ──────────────────────────────────────────────
//  Internal helpers
// ──────────────────────────────────────────────

function loadStore(): ProgressStore {
  if (typeof window === 'undefined') {
    return { modules: {}, achievements: [] };
  }
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { modules: {}, achievements: [] };
    return JSON.parse(raw) as ProgressStore;
  } catch {
    return { modules: {}, achievements: [] };
  }
}

function saveStore(store: ProgressStore): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(store));
}

function ensureModuleEntries(store: ProgressStore): void {
  for (const mod of modules) {
    if (!store.modules[mod.id]) {
      store.modules[mod.id] = {
        id: mod.id,
        title: mod.title,
        category: mod.category,
        status: mod.prerequisites.length === 0 ? 'available' : 'locked',
        completedAt: null,
      };
    }
  }
}

function unlockDependents(store: ProgressStore, completedId: string): void {
  for (const mod of modules) {
    if (mod.prerequisites.includes(completedId)) {
      const allPrereqsDone = mod.prerequisites.every(
        (pid) => store.modules[pid]?.status === 'complete',
      );
      if (allPrereqsDone && store.modules[mod.id]?.status === 'locked') {
        store.modules[mod.id].status = 'available';
      }
    }
  }
}

// ──────────────────────────────────────────────
//  Public API
// ──────────────────────────────────────────────

/** Returns progress for every module. */
export function getProgress(): Record<string, ModuleProgress> {
  const store = loadStore();
  ensureModuleEntries(store);
  saveStore(store);
  return store.modules;
}

/** Mark a module as complete. Unlocks dependent modules. */
export function markComplete(moduleId: string): void {
  const store = loadStore();
  ensureModuleEntries(store);

  const entry = store.modules[moduleId];
  if (!entry) throw new Error(`Unknown module: ${moduleId}`);
  if (entry.status === 'complete') return;

  entry.status = 'complete';
  entry.completedAt = new Date().toISOString();
  unlockDependents(store, moduleId);

  // Track session completions for streak achievement
  const sessionCompletions = parseInt(sessionStorage.getItem('ai-era-session-completions') || '0', 10);
  sessionStorage.setItem('ai-era-session-completions', String(sessionCompletions + 1));

  saveStore(store);
}

/** Check if a specific module is complete. */
export function isComplete(moduleId: string): boolean {
  const store = loadStore();
  return store.modules[moduleId]?.status === 'complete';
}

/** Get overall completion percentage (0-100). */
export function getCompletionPercentage(): number {
  const store = loadStore();
  ensureModuleEntries(store);
  saveStore(store);

  const total = modules.length;
  if (total === 0) return 0;

  const completed = Object.values(store.modules).filter((m) => m.status === 'complete').length;
  return Math.round((completed / total) * 100);
}

/** Get progress breakdown for a specific category. */
export function getModuleProgress(category: string): { total: number; completed: number; percentage: number } {
  const store = loadStore();
  ensureModuleEntries(store);
  saveStore(store);

  const catModules = modules.filter((m) => m.category === category);
  const total = catModules.length;
  const completed = catModules.filter((m) => store.modules[m.id]?.status === 'complete').length;

  return {
    total,
    completed,
    percentage: total === 0 ? 0 : Math.round((completed / total) * 100),
  };
}

/** Reset all progress data (module progress + knowledge point progress). */
export function resetProgress(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem(STORAGE_KEY);
  localStorage.removeItem(KP_STORAGE_KEY);
  sessionStorage.removeItem('ai-era-session-completions');
}

/** Check achievements and return newly unlocked ones. */
export function checkAchievements(): Achievement[] {
  const store = loadStore();
  ensureModuleEntries(store);

  const completedIds = new Set(
    Object.values(store.modules)
      .filter((m) => m.status === 'complete')
      .map((m) => m.id),
  );
  const totalCompleted = completedIds.size;
  const sessionCompletions = parseInt(sessionStorage.getItem('ai-era-session-completions') || '0', 10);
  const alreadyUnlocked = new Set(store.achievements.map((a) => a.id));
  const newlyUnlocked: Achievement[] = [];

  const categoryGroups: Record<string, string[]> = {};
  for (const mod of modules) {
    if (!categoryGroups[mod.category]) categoryGroups[mod.category] = [];
    categoryGroups[mod.category].push(mod.id);
  }

  function isCategoryComplete(cat: string): boolean {
    const ids = categoryGroups[cat] || [];
    return ids.length > 0 && ids.every((id) => completedIds.has(id));
  }

  const unlock = (id: string) => {
    if (alreadyUnlocked.has(id)) return;
    const def = ACHIEVEMENT_DEFS.find((a) => a.id === id);
    if (!def) return;
    const achievement: Achievement = { ...def, unlockedAt: new Date().toISOString() };
    store.achievements.push(achievement);
    newlyUnlocked.push(achievement);
  };

  // Evaluate each achievement condition
  if (totalCompleted >= 1) unlock('first-step');
  if (isCategoryComplete('cognitive')) unlock('cognitive-done');
  if (isCategoryComplete('python-fundamentals')) unlock('py-master');
  if (isCategoryComplete('typescript-fundamentals')) unlock('ts-master');
  if (isCategoryComplete('patterns')) unlock('pattern-pro');
  if (isCategoryComplete('python-dissect')) unlock('py-dissector');
  if (isCategoryComplete('typescript-dissect')) unlock('ts-dissector');
  if (isCategoryComplete('ai-mastery')) unlock('ai-pioneer');
  if (isCategoryComplete('practice')) unlock('graduate');
  if (totalCompleted >= Math.ceil(modules.length / 2)) unlock('halfway');
  if (totalCompleted >= modules.length) unlock('completionist');
  if (sessionCompletions >= 5) unlock('streak-5');

  saveStore(store);
  return newlyUnlocked;
}

/** Get all achievements (locked + unlocked). */
export function getAllAchievements(): Achievement[] {
  const store = loadStore();
  const unlockedMap = new Map(store.achievements.map((a) => [a.id, a]));

  return ACHIEVEMENT_DEFS.map((def) => {
    const unlocked = unlockedMap.get(def.id);
    return {
      ...def,
      unlockedAt: unlocked?.unlockedAt ?? null,
    };
  });
}

// ──────────────────────────────────────────────
//  Knowledge Point Progress
// ──────────────────────────────────────────────

const KP_STORAGE_KEY = 'kp_progress';

export interface PointScore {
  correct: number;
  total: number;
}

interface PointProgress {
  completedAt: string | null;
  score: PointScore | null;
  timeSpentMs: number;
}

interface KPProgressStore {
  completed: number[];
  points: Record<number, PointProgress>;
}

function loadKPStore(): KPProgressStore {
  if (typeof window === 'undefined') {
    return { completed: [], points: {} };
  }
  try {
    const raw = localStorage.getItem(KP_STORAGE_KEY);
    if (!raw) return { completed: [], points: {} };
    return JSON.parse(raw) as KPProgressStore;
  } catch {
    return { completed: [], points: {} };
  }
}

function saveKPStore(store: KPProgressStore): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem(KP_STORAGE_KEY, JSON.stringify(store));
}

function ensurePointEntry(store: KPProgressStore, pointIndex: number): void {
  if (!store.points[pointIndex]) {
    store.points[pointIndex] = {
      completedAt: null,
      score: null,
      timeSpentMs: 0,
    };
  }
}

/** Get list of completed knowledge point indices. */
export function getCompletedPoints(): number[] {
  const store = loadKPStore();
  return store.completed;
}

/** Mark a knowledge point as completed. */
export function markPointComplete(pointIndex: number): void {
  const store = loadKPStore();
  if (store.completed.includes(pointIndex)) return;
  store.completed.push(pointIndex);
  ensurePointEntry(store, pointIndex);
  store.points[pointIndex].completedAt = new Date().toISOString();
  saveKPStore(store);
}

/** Check if a knowledge point is completed. */
export function isPointComplete(pointIndex: number): boolean {
  const store = loadKPStore();
  return store.completed.includes(pointIndex);
}

/** Get quiz score for a knowledge point, or null if not attempted. */
export function getPointScore(pointIndex: number): PointScore | null {
  const store = loadKPStore();
  return store.points[pointIndex]?.score ?? null;
}

/** Save quiz score for a knowledge point. */
export function savePointScore(pointIndex: number, correct: number, total: number): void {
  const store = loadKPStore();
  ensurePointEntry(store, pointIndex);
  store.points[pointIndex].score = { correct, total };
  saveKPStore(store);
}

/** Get progress for a specific week (week number -> completed/total). */
export function getWeekProgress(week: number): { completed: number; total: number } {
  const store = loadKPStore();
  const weekCategories = Object.entries(CATEGORY_META)
    .filter(([, meta]) => meta.week === week)
    .map(([cat]) => cat);

  const weekModules = modules.filter((m) =>
    weekCategories.includes(m.category),
  );
  const total = weekModules.length;
  const completed = weekModules.filter(
    (m) => store.completed.includes(modules.findIndex((mod) => mod.id === m.id)),
  ).length;

  return { completed, total };
}

/** Get overall knowledge point progress. */
export function getOverallProgress(): { completed: number; total: number; percentage: number } {
  const store = loadKPStore();
  const total = modules.length;
  const completed = store.completed.length;
  return {
    completed,
    total,
    percentage: total === 0 ? 0 : Math.round((completed / total) * 100),
  };
}

/** Reset all knowledge point progress. */
export function resetKPProgress(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem(KP_STORAGE_KEY);
}

/**
 * Get time spent on a knowledge point in milliseconds.
 * Returns 0 if the point has no tracked time.
 */
export function getPointTimeSpent(pointIndex: number): number {
  const store = loadKPStore();
  return store.points[pointIndex]?.timeSpentMs ?? 0;
}

/**
 * Add time spent on a knowledge point (accumulates).
 * @param pointIndex - The point index
 * @param ms - Milliseconds to add
 */
export function addPointTimeSpent(pointIndex: number, ms: number): void {
  const store = loadKPStore();
  ensurePointEntry(store, pointIndex);
  store.points[pointIndex].timeSpentMs += ms;
  saveKPStore(store);
}
