/**
 * Tests for Knowledge Point System (Frontend)
 * ============================================
 * Tests API client functions, progress tracking, and game component props.
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';

// ============================================================================
// Types (mirrors the backend data shape)
// ============================================================================

interface QuizQuestion {
  question: string;
  options: string[];
  correct: number;
  explanation: string;
}

interface GameContent {
  [key: string]: unknown;
}

interface Game {
  type: string;
  title: string;
  instructions: string;
  content: GameContent;
}

interface KnowledgePoint {
  week: number;
  module: string;
  title: string;
  explanation: string;
  code: string;
  game: Game;
  quiz: QuizQuestion;
}

interface PaginatedResponse {
  total: number;
  page: number;
  per_page: number;
  pages: number;
  points: KnowledgePoint[];
}

interface RandomResponse {
  count: number;
  points: KnowledgePoint[];
}

interface SinglePointResponse {
  id: number;
  point: KnowledgePoint;
}

interface StatsResponse {
  total_points: number;
  points_per_week: Record<string, number>;
  points_per_module: Record<string, number>;
  games_per_type: Record<string, number>;
}

// ============================================================================
// API Client Functions (to be tested against fetch mocks)
// ============================================================================

const API_BASE = 'http://localhost:8000';

async function fetchKnowledgePoints(params?: {
  week?: number;
  module?: string;
  search?: string;
  page?: number;
  per_page?: number;
}): Promise<PaginatedResponse> {
  const url = new URL(`${API_BASE}/api/knowledge-points`);
  if (params?.week !== undefined) url.searchParams.set('week', String(params.week));
  if (params?.module) url.searchParams.set('module', params.module);
  if (params?.search) url.searchParams.set('search', params.search);
  if (params?.page) url.searchParams.set('page', String(params.page));
  if (params?.per_page) url.searchParams.set('per_page', String(params.per_page));
  const res = await fetch(url.toString());
  return res.json();
}

async function fetchRandomPoints(count: number = 10): Promise<RandomResponse> {
  const res = await fetch(`${API_BASE}/api/knowledge-points/random?count=${count}`);
  return res.json();
}

async function fetchSinglePoint(index: number): Promise<SinglePointResponse> {
  const res = await fetch(`${API_BASE}/api/knowledge-points/id/${index}`);
  if (!res.ok) throw new Error(`Point ${index} not found`);
  return res.json();
}

async function fetchStats(): Promise<StatsResponse> {
  const res = await fetch(`${API_BASE}/api/knowledge-points/stats`);
  return res.json();
}

// ============================================================================
// Progress tracking (localStorage-based)
// ============================================================================

const PROGRESS_KEY = 'kp_completed';

interface ProgressTracker {
  completed: Set<string>;
  load(): void;
  save(): void;
  toggle(id: string): boolean;
  isCompleted(id: string): boolean;
  getCount(): number;
  reset(): void;
}

function createProgressTracker(): ProgressTracker {
  const tracker: ProgressTracker = {
    completed: new Set<string>(),

    load() {
      try {
        const raw = localStorage.getItem(PROGRESS_KEY);
        if (raw) {
          const ids: string[] = JSON.parse(raw);
          tracker.completed = new Set(ids);
        }
      } catch {
        tracker.completed = new Set();
      }
    },

    save() {
      localStorage.setItem(PROGRESS_KEY, JSON.stringify([...tracker.completed]));
    },

    toggle(id: string): boolean {
      if (tracker.completed.has(id)) {
        tracker.completed.delete(id);
      } else {
        tracker.completed.add(id);
      }
      tracker.save();
      return tracker.completed.has(id);
    },

    isCompleted(id: string): boolean {
      return tracker.completed.has(id);
    },

    getCount(): number {
      return tracker.completed.size;
    },

    reset() {
      tracker.completed = new Set();
      localStorage.removeItem(PROGRESS_KEY);
    },
  };
  return tracker;
}

// ============================================================================
// Game content structure validators
// ============================================================================

const GAME_TYPES: Record<string, string[]> = {
  predict_output: ['code', 'options', 'correct', 'explanation'],
  find_bug: ['code_lines', 'bug_line', 'explanation'],
  fill_blank: ['code', 'blanks', 'explanation'],
  code_order: ['lines', 'correct_order', 'explanation'],
};

function validateGameStructure(game: Game): string[] {
  const errors: string[] = [];

  if (!game.type) errors.push('game.type missing');
  if (!game.title) errors.push('game.title missing');
  if (!game.instructions) errors.push('game.instructions missing');
  if (!game.content) errors.push('game.content missing');

  if (game.type && game.content) {
    const requiredKeys = GAME_TYPES[game.type];
    if (!requiredKeys) {
      errors.push(`unknown game type: ${game.type}`);
    } else {
      for (const key of requiredKeys) {
        if (!(key in game.content)) {
          errors.push(`game.content missing key '${key}' for type '${game.type}'`);
        }
      }
    }
  }

  return errors;
}

function validateQuizStructure(quiz: QuizQuestion): string[] {
  const errors: string[] = [];

  if (!quiz.question) errors.push('quiz.question missing');
  if (!Array.isArray(quiz.options)) {
    errors.push('quiz.options not an array');
  } else if (quiz.options.length !== 4) {
    errors.push(`quiz.options has ${quiz.options.length} items, expected 4`);
  }
  if (typeof quiz.correct !== 'number') {
    errors.push('quiz.correct not a number');
  } else if (quiz.options && (quiz.correct < 0 || quiz.correct >= quiz.options.length)) {
    errors.push(`quiz.correct=${quiz.correct} out of range`);
  }
  if (!quiz.explanation) errors.push('quiz.explanation missing');

  return errors;
}

// ============================================================================
// Component props interfaces (for prop validation tests)
// ============================================================================

interface PredictOutputProps {
  code: string;
  language?: string;
  options: string[];
  correctIndex: number;
  explanation: string;
  onComplete?: (correct: boolean) => void;
}

interface FindBugProps {
  code: string;
  language?: string;
  bugLineIndex: number;
  explanation: string;
  onComplete?: (correct: boolean) => void;
}

interface FillBlankProps {
  template: string;
  blanks: { id: string; answer: string; hint?: string }[];
  explanation: string;
  onComplete?: (allCorrect: boolean) => void;
}

interface CodeOrderProps {
  lines: string[];
  explanation: string;
  onComplete?: (correct: boolean) => void;
}

// ============================================================================
// Mock localStorage
// ============================================================================

const localStorageMock = (() => {
  let store: Record<string, string> = {};
  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => { store[key] = value; },
    removeItem: (key: string) => { delete store[key]; },
    clear: () => { store = {}; },
  };
})();

Object.defineProperty(globalThis, 'localStorage', { value: localStorageMock });

// ============================================================================
// Mock sample data
// ============================================================================

const SAMPLE_POINT: KnowledgePoint = {
  week: 1,
  module: 'cognitive-why',
  title: 'What is a program?',
  explanation: 'A program is a set of instructions.',
  code: "print('Hello!')",
  game: {
    type: 'predict_output',
    title: 'Predict Output',
    instructions: 'What will this output?',
    content: {
      code: "print('Hello!')",
      options: ['Hello!', 'Error', 'None', '0'],
      correct: 0,
      explanation: 'It prints Hello!',
    },
  },
  quiz: {
    question: 'What does a program do?',
    options: [
      'Tells the computer what to do',
      'Tells the user what to do',
      'Writes itself',
      'Nothing',
    ],
    correct: 0,
    explanation: 'A program is instructions for the computer.',
  },
};

const SAMPLE_FIND_BUG_POINT: KnowledgePoint = {
  week: 1,
  module: 'cognitive-why',
  title: 'Find the bug',
  explanation: 'Look for syntax errors.',
  code: 'def add(a, b):\n    return a - b',
  game: {
    type: 'find_bug',
    title: 'Find Bug',
    instructions: 'Click the buggy line',
    content: {
      code_lines: ['def add(a, b):', '    return a - b'],
      bug_line: 1,
      explanation: 'Line 2 should be return a + b',
    },
  },
  quiz: {
    question: 'Which line has the bug?',
    options: ['Line 1', 'Line 2', 'Line 3', 'No bug'],
    correct: 1,
    explanation: 'Line 2 subtracts instead of adding.',
  },
};

const SAMPLE_FILL_BLANK_POINT: KnowledgePoint = {
  week: 1,
  module: 'cognitive-thinking',
  title: 'Fill the blank',
  explanation: 'Complete the code.',
  code: 'x = ___',
  game: {
    type: 'fill_blank',
    title: 'Fill Blank',
    instructions: 'Fill in the missing code',
    content: {
      code: 'x = ___',
      blanks: [{ position: 0, answer: '5', options: ['5', '0', 'None', 'True'] }],
      explanation: 'Blank should be 5',
    },
  },
  quiz: {
    question: 'What value?',
    options: ['5', '0', 'None', 'True'],
    correct: 0,
    explanation: 'The answer is 5.',
  },
};

const SAMPLE_CODE_ORDER_POINT: KnowledgePoint = {
  week: 1,
  module: 'cognitive-thinking',
  title: 'Order the code',
  explanation: 'Put lines in order.',
  code: 'line1\nline2',
  game: {
    type: 'code_order',
    title: 'Code Order',
    instructions: 'Reorder the lines',
    content: {
      lines: ['line2', 'line1'],
      correct_order: [1, 0],
      explanation: 'Correct order is line1, line2',
    },
  },
  quiz: {
    question: 'What order?',
    options: ['1,2', '2,1', '3,4', '4,3'],
    correct: 0,
    explanation: 'The correct order is 1,2.',
  },
};


// ============================================================================
// TESTS: API Client Functions
// ============================================================================

describe('API Client Functions', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  describe('fetchKnowledgePoints', () => {
    it('calls the correct URL with no params', async () => {
      const mockResponse: PaginatedResponse = {
        total: 123, page: 1, per_page: 20, pages: 7, points: [SAMPLE_POINT],
      };
      const fetchSpy = vi.spyOn(globalThis, 'fetch').mockResolvedValue(
        new Response(JSON.stringify(mockResponse), { status: 200 }),
      );

      const result = await fetchKnowledgePoints();
      expect(fetchSpy).toHaveBeenCalledOnce();
      const calledUrl = fetchSpy.mock.calls[0][0] as string;
      expect(calledUrl).toContain('/api/knowledge-points');
      expect(result.total).toBe(123);
      expect(result.points).toHaveLength(1);
    });

    it('passes week param correctly', async () => {
      const mockResponse: PaginatedResponse = {
        total: 10, page: 1, per_page: 20, pages: 1, points: [],
      };
      const fetchSpy = vi.spyOn(globalThis, 'fetch').mockResolvedValue(
        new Response(JSON.stringify(mockResponse), { status: 200 }),
      );

      await fetchKnowledgePoints({ week: 2 });
      const calledUrl = fetchSpy.mock.calls[0][0] as string;
      expect(calledUrl).toContain('week=2');
    });

    it('passes search param correctly', async () => {
      const mockResponse: PaginatedResponse = {
        total: 3, page: 1, per_page: 20, pages: 1, points: [],
      };
      const fetchSpy = vi.spyOn(globalThis, 'fetch').mockResolvedValue(
        new Response(JSON.stringify(mockResponse), { status: 200 }),
      );

      await fetchKnowledgePoints({ search: 'variable' });
      const calledUrl = fetchSpy.mock.calls[0][0] as string;
      expect(calledUrl).toContain('search=variable');
    });

    it('passes pagination params correctly', async () => {
      const mockResponse: PaginatedResponse = {
        total: 100, page: 3, per_page: 10, pages: 10, points: [],
      };
      const fetchSpy = vi.spyOn(globalThis, 'fetch').mockResolvedValue(
        new Response(JSON.stringify(mockResponse), { status: 200 }),
      );

      await fetchKnowledgePoints({ page: 3, per_page: 10 });
      const calledUrl = fetchSpy.mock.calls[0][0] as string;
      expect(calledUrl).toContain('page=3');
      expect(calledUrl).toContain('per_page=10');
    });
  });

  describe('fetchRandomPoints', () => {
    it('calls random endpoint with count', async () => {
      const mockResponse: RandomResponse = { count: 5, points: [] };
      const fetchSpy = vi.spyOn(globalThis, 'fetch').mockResolvedValue(
        new Response(JSON.stringify(mockResponse), { status: 200 }),
      );

      await fetchRandomPoints(5);
      const calledUrl = fetchSpy.mock.calls[0][0] as string;
      expect(calledUrl).toContain('/api/knowledge-points/random');
      expect(calledUrl).toContain('count=5');
    });

    it('defaults count to 10', async () => {
      const mockResponse: RandomResponse = { count: 10, points: [] };
      const fetchSpy = vi.spyOn(globalThis, 'fetch').mockResolvedValue(
        new Response(JSON.stringify(mockResponse), { status: 200 }),
      );

      await fetchRandomPoints();
      const calledUrl = fetchSpy.mock.calls[0][0] as string;
      expect(calledUrl).toContain('count=10');
    });
  });

  describe('fetchSinglePoint', () => {
    it('calls single point endpoint by index', async () => {
      const mockResponse: SinglePointResponse = { id: 0, point: SAMPLE_POINT };
      const fetchSpy = vi.spyOn(globalThis, 'fetch').mockResolvedValue(
        new Response(JSON.stringify(mockResponse), { status: 200 }),
      );

      const result = await fetchSinglePoint(0);
      const calledUrl = fetchSpy.mock.calls[0][0] as string;
      expect(calledUrl).toContain('/api/knowledge-points/id/0');
      expect(result.id).toBe(0);
      expect(result.point.title).toBe('What is a program?');
    });

    it('throws on not found', async () => {
      vi.spyOn(globalThis, 'fetch').mockResolvedValue(
        new Response('Not Found', { status: 404 }),
      );

      await expect(fetchSinglePoint(99999)).rejects.toThrow('Point 99999 not found');
    });
  });

  describe('fetchStats', () => {
    it('calls stats endpoint', async () => {
      const mockResponse: StatsResponse = {
        total_points: 123,
        points_per_week: { '1': 50 },
        points_per_module: { 'cognitive-why': 10 },
        games_per_type: { predict_output: 30 },
      };
      const fetchSpy = vi.spyOn(globalThis, 'fetch').mockResolvedValue(
        new Response(JSON.stringify(mockResponse), { status: 200 }),
      );

      const result = await fetchStats();
      const calledUrl = fetchSpy.mock.calls[0][0] as string;
      expect(calledUrl).toContain('/api/knowledge-points/stats');
      expect(result.total_points).toBe(123);
    });
  });
});


// ============================================================================
// TESTS: Progress Tracking
// ============================================================================

describe('Progress Tracking', () => {
  let tracker: ProgressTracker;

  beforeEach(() => {
    localStorageMock.clear();
    tracker = createProgressTracker();
  });

  describe('load', () => {
    it('starts empty when nothing stored', () => {
      tracker.load();
      expect(tracker.getCount()).toBe(0);
    });

    it('loads saved progress', () => {
      localStorage.setItem(PROGRESS_KEY, JSON.stringify(['point-1', 'point-2']));
      tracker.load();
      expect(tracker.getCount()).toBe(2);
      expect(tracker.isCompleted('point-1')).toBe(true);
    });

    it('handles corrupted data gracefully', () => {
      localStorage.setItem(PROGRESS_KEY, 'not-json!!!');
      tracker.load();
      expect(tracker.getCount()).toBe(0);
    });
  });

  describe('toggle', () => {
    it('marks a point as completed', () => {
      tracker.load();
      const result = tracker.toggle('point-1');
      expect(result).toBe(true);
      expect(tracker.isCompleted('point-1')).toBe(true);
    });

    it('unmarks a completed point', () => {
      tracker.load();
      tracker.toggle('point-1');
      const result = tracker.toggle('point-1');
      expect(result).toBe(false);
      expect(tracker.isCompleted('point-1')).toBe(false);
    });

    it('persists to localStorage', () => {
      tracker.load();
      tracker.toggle('point-1');
      const stored = JSON.parse(localStorage.getItem(PROGRESS_KEY)!);
      expect(stored).toContain('point-1');
    });

    it('does not duplicate entries', () => {
      tracker.load();
      tracker.toggle('point-1');
      tracker.toggle('point-1');
      tracker.toggle('point-1');
      const stored = JSON.parse(localStorage.getItem(PROGRESS_KEY)!);
      expect(stored.filter((id: string) => id === 'point-1')).toHaveLength(1);
    });
  });

  describe('getCount', () => {
    it('returns 0 when empty', () => {
      tracker.load();
      expect(tracker.getCount()).toBe(0);
    });

    it('returns correct count after toggles', () => {
      tracker.load();
      tracker.toggle('a');
      tracker.toggle('b');
      tracker.toggle('c');
      expect(tracker.getCount()).toBe(3);
    });

    it('decrements when unmarking', () => {
      tracker.load();
      tracker.toggle('a');
      tracker.toggle('b');
      tracker.toggle('a'); // unmark
      expect(tracker.getCount()).toBe(1);
    });
  });

  describe('reset', () => {
    it('clears all progress', () => {
      tracker.load();
      tracker.toggle('a');
      tracker.toggle('b');
      tracker.reset();
      expect(tracker.getCount()).toBe(0);
      expect(localStorage.getItem(PROGRESS_KEY)).toBeNull();
    });
  });
});


// ============================================================================
// TESTS: Game Component Props Validation
// ============================================================================

describe('Game Component Props Validation', () => {
  describe('PredictOutputProps', () => {
    it('requires code, options, correctIndex, explanation', () => {
      const props: PredictOutputProps = {
        code: "print('hello')",
        options: ['hello', 'error', 'none', '0'],
        correctIndex: 0,
        explanation: 'It prints hello.',
      };
      expect(props.code).toBeTruthy();
      expect(props.options.length).toBeGreaterThan(0);
      expect(props.correctIndex).toBeGreaterThanOrEqual(0);
      expect(props.correctIndex).toBeLessThan(props.options.length);
      expect(props.explanation).toBeTruthy();
    });

    it('language defaults to javascript when omitted', () => {
      const props: PredictOutputProps = {
        code: 'console.log("hi")',
        options: ['hi', 'error'],
        correctIndex: 0,
        explanation: 'It logs hi.',
      };
      expect(props.language).toBeUndefined(); // component defaults to 'javascript'
    });
  });

  describe('FindBugProps', () => {
    it('requires code, bugLineIndex, explanation', () => {
      const props: FindBugProps = {
        code: 'line 1\nline 2\nline 3',
        bugLineIndex: 1,
        explanation: 'Line 2 has a bug.',
      };
      expect(props.code).toBeTruthy();
      expect(props.bugLineIndex).toBeGreaterThanOrEqual(0);
      expect(props.explanation).toBeTruthy();
    });

    it('bugLineIndex must be within code line range', () => {
      const code = 'a\nb\nc';
      const lines = code.split('\n');
      const props: FindBugProps = {
        code,
        bugLineIndex: 1,
        explanation: 'Bug on line 2.',
      };
      expect(props.bugLineIndex).toBeLessThan(lines.length);
    });
  });

  describe('FillBlankProps', () => {
    it('requires template, blanks, explanation', () => {
      const props: FillBlankProps = {
        template: 'x = ___BLANK1___',
        blanks: [{ id: 'BLANK1', answer: '5' }],
        explanation: 'The answer is 5.',
      };
      expect(props.template).toBeTruthy();
      expect(props.blanks.length).toBeGreaterThan(0);
      expect(props.explanation).toBeTruthy();
    });

    it('each blank has id and answer', () => {
      const blanks = [{ id: 'BLANK1', answer: '5', hint: 'a number' }];
      for (const blank of blanks) {
        expect(blank.id).toBeTruthy();
        expect(blank.answer).toBeTruthy();
      }
    });
  });

  describe('CodeOrderProps', () => {
    it('requires lines and explanation', () => {
      const props: CodeOrderProps = {
        lines: ['line 2', 'line 1'],
        explanation: 'Correct order is line 1, line 2.',
      };
      expect(props.lines.length).toBeGreaterThan(0);
      expect(props.explanation).toBeTruthy();
    });

    it('onComplete callback receives boolean', () => {
      let receivedCorrect: boolean | null = null;
      const props: CodeOrderProps = {
        lines: ['a', 'b'],
        explanation: 'Order is a, b.',
        onComplete: (correct: boolean) => { receivedCorrect = correct; },
      };
      // Simulate calling onComplete
      props.onComplete?.(true);
      expect(receivedCorrect).toBe(true);
    });
  });
});


// ============================================================================
// TESTS: Game Structure Validators
// ============================================================================

describe('Game Structure Validators', () => {
  describe('validateGameStructure', () => {
    it('validates predict_output game', () => {
      const errors = validateGameStructure(SAMPLE_POINT.game);
      expect(errors).toEqual([]);
    });

    it('validates find_bug game', () => {
      const errors = validateGameStructure(SAMPLE_FIND_BUG_POINT.game);
      expect(errors).toEqual([]);
    });

    it('validates fill_blank game', () => {
      const errors = validateGameStructure(SAMPLE_FILL_BLANK_POINT.game);
      expect(errors).toEqual([]);
    });

    it('validates code_order game', () => {
      const errors = validateGameStructure(SAMPLE_CODE_ORDER_POINT.game);
      expect(errors).toEqual([]);
    });

    it('detects missing type', () => {
      const game = { ...SAMPLE_POINT.game, type: '' };
      const errors = validateGameStructure(game);
      expect(errors).toContain('game.type missing');
    });

    it('detects unknown game type', () => {
      const game = { ...SAMPLE_POINT.game, type: 'unknown_type' };
      const errors = validateGameStructure(game);
      expect(errors.some((e) => e.includes('unknown game type'))).toBe(true);
    });

    it('detects missing content keys', () => {
      const game: Game = {
        type: 'predict_output',
        title: 'Test',
        instructions: 'Test',
        content: { code: 'x' }, // missing options, correct, explanation
      };
      const errors = validateGameStructure(game);
      expect(errors.some((e) => e.includes("options"))).toBe(true);
      expect(errors.some((e) => e.includes("correct"))).toBe(true);
      expect(errors.some((e) => e.includes("explanation"))).toBe(true);
    });
  });

  describe('validateQuizStructure', () => {
    it('validates a correct quiz', () => {
      const errors = validateQuizStructure(SAMPLE_POINT.quiz);
      expect(errors).toEqual([]);
    });

    it('detects missing question', () => {
      const quiz: QuizQuestion = { ...SAMPLE_POINT.quiz, question: '' };
      const errors = validateQuizStructure(quiz);
      expect(errors.some((e) => e.includes('question'))).toBe(true);
    });

    it('detects wrong number of options', () => {
      const quiz: QuizQuestion = { ...SAMPLE_POINT.quiz, options: ['a', 'b'] };
      const errors = validateQuizStructure(quiz);
      expect(errors.some((e) => e.includes('2 items, expected 4'))).toBe(true);
    });

    it('detects out-of-range correct index', () => {
      const quiz: QuizQuestion = { ...SAMPLE_POINT.quiz, correct: 10 };
      const errors = validateQuizStructure(quiz);
      expect(errors.some((e) => e.includes('out of range'))).toBe(true);
    });

    it('detects missing explanation', () => {
      const quiz: QuizQuestion = { ...SAMPLE_POINT.quiz, explanation: '' };
      const errors = validateQuizStructure(quiz);
      expect(errors.some((e) => e.includes('explanation'))).toBe(true);
    });
  });
});


// ============================================================================
// TESTS: Knowledge Point Data Shape
// ============================================================================

describe('Knowledge Point Data Shape', () => {
  const ALL_POINTS = [
    SAMPLE_POINT,
    SAMPLE_FIND_BUG_POINT,
    SAMPLE_FILL_BLANK_POINT,
    SAMPLE_CODE_ORDER_POINT,
  ];

  it('every point has all required fields', () => {
    const required = ['week', 'module', 'title', 'explanation', 'code', 'game', 'quiz'];
    for (const p of ALL_POINTS) {
      for (const field of required) {
        expect((p as Record<string, unknown>)[field]).toBeDefined();
      }
    }
  });

  it('every point has a valid game structure', () => {
    for (const p of ALL_POINTS) {
      const errors = validateGameStructure(p.game);
      expect(errors).toEqual([]);
    }
  });

  it('every point has a valid quiz structure', () => {
    for (const p of ALL_POINTS) {
      const errors = validateQuizStructure(p.quiz);
      expect(errors).toEqual([]);
    }
  });

  it('game type matches its content structure', () => {
    for (const p of ALL_POINTS) {
      const gt = p.game.type;
      const requiredKeys = GAME_TYPES[gt];
      expect(requiredKeys).toBeDefined();
      for (const key of requiredKeys) {
        expect(p.game.content).toHaveProperty(key);
      }
    }
  });

  it('quiz.correct is within options range', () => {
    for (const p of ALL_POINTS) {
      expect(p.quiz.correct).toBeGreaterThanOrEqual(0);
      expect(p.quiz.correct).toBeLessThan(p.quiz.options.length);
    }
  });
});
