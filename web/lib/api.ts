// ──────────────────────────────────────────────
//  API Client for minimum-code Training System
// ──────────────────────────────────────────────

export const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

// ──────────────────────────────────────────────
//  Types
// ──────────────────────────────────────────────

export interface KnowledgePoint {
  week: number;
  module: string;
  title: string;
  explanation: string;
  code: string;
  game: string;
  quiz: {
    question: string;
    options: string[];
    correct: number;
    explanation: string;
  };
}

export interface Stats {
  total_points: number;
  points_per_week: Record<string, number>;
  points_per_module: Record<string, number>;
}

export interface WeekModule {
  module: string;
  count: number;
}

export interface Week {
  week: number;
  modules: WeekModule[];
  total_points: number;
}

export interface Module {
  id: string;
  title: string;
  category: string;
  icon: string;
  description: string;
  week: number;
  order: number;
}

export interface Section {
  title: string;
  content: string;
  type: string;
  language?: string | null;
}

export interface ModuleContent {
  id: string;
  title: string;
  category: string;
  icon: string;
  sections: Section[];
}

export interface QuizQuestion {
  question: string;
  options: string[];
  correct: number;
  explanation: string;
}

interface PaginatedKnowledgePoints {
  total: number;
  page: number;
  per_page: number;
  pages: number;
  points: KnowledgePoint[];
}

// ──────────────────────────────────────────────
//  Helpers
// ──────────────────────────────────────────────

async function request<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }
  return res.json() as Promise<T>;
}

// ──────────────────────────────────────────────
//  Public API
// ──────────────────────────────────────────────

/** Fetch knowledge points with optional week/module filtering. */
export async function fetchKnowledgePoints(
  week?: number,
  module?: string,
): Promise<KnowledgePoint[]> {
  const params = new URLSearchParams();
  if (week !== undefined) params.set('week', String(week));
  if (module !== undefined) params.set('module', module);
  const qs = params.toString();
  const data = await request<PaginatedKnowledgePoints>(
    `/api/knowledge-points${qs ? `?${qs}` : ''}`,
  );
  return data.points;
}

/** Fetch aggregate statistics about knowledge points. */
export async function fetchKnowledgePointStats(): Promise<Stats> {
  return request<Stats>('/api/knowledge-points/stats');
}

/** Fetch all weeks with their module breakdowns and point counts. */
export async function fetchWeeks(): Promise<Week[]> {
  return request<Week[]>('/api/weeks');
}

/** Fetch all modules (course outline). */
export async function fetchModules(): Promise<Module[]> {
  return request<Module[]>('/api/modules');
}

/** Fetch the full content of a specific module. */
export async function fetchModuleContent(id: string): Promise<ModuleContent> {
  return request<ModuleContent>(`/api/modules/${encodeURIComponent(id)}`);
}

/** Fetch quiz questions for a specific module. */
export async function fetchQuiz(id: string): Promise<QuizQuestion[]> {
  return request<QuizQuestion[]>(`/api/modules/${encodeURIComponent(id)}/quiz`);
}
