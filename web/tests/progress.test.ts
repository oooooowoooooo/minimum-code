/**
 * Tests for Learning Progress System
 * ====================================
 * Tests the localStorage-based progress tracking.
 */

import { describe, it, expect, beforeEach } from 'vitest';

// Mock localStorage
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

// Progress functions (inline for testing)
interface ProgressData {
  completed: string[];
  startedAt: string;
  lastUpdated: string;
}

function getProgress(): ProgressData {
  const stored = localStorage.getItem('ai-era-progress');
  if (stored) {
    return JSON.parse(stored);
  }
  return { completed: [], startedAt: new Date().toISOString(), lastUpdated: new Date().toISOString() };
}

function markComplete(moduleId: string): ProgressData {
  const progress = getProgress();
  if (!progress.completed.includes(moduleId)) {
    progress.completed.push(moduleId);
  }
  progress.lastUpdated = new Date().toISOString();
  localStorage.setItem('ai-era-progress', JSON.stringify(progress));
  return progress;
}

function markIncomplete(moduleId: string): ProgressData {
  const progress = getProgress();
  progress.completed = progress.completed.filter((id) => id !== moduleId);
  progress.lastUpdated = new Date().toISOString();
  localStorage.setItem('ai-era-progress', JSON.stringify(progress));
  return progress;
}

function isComplete(moduleId: string): boolean {
  const progress = getProgress();
  return progress.completed.includes(moduleId);
}

function getCompletionPercentage(totalModules: number): number {
  const progress = getProgress();
  return Math.round((progress.completed.length / totalModules) * 100);
}

function resetProgress(): void {
  localStorage.removeItem('ai-era-progress');
}

// Achievement system
interface Achievement {
  id: string;
  name: string;
  description: string;
  condition: (completed: string[]) => boolean;
}

const ACHIEVEMENTS: Achievement[] = [
  { id: 'first-step', name: 'First Step', description: 'Complete your first module', condition: (c) => c.length >= 1 },
  { id: 'five-modules', name: 'Getting Started', description: 'Complete 5 modules', condition: (c) => c.length >= 5 },
  { id: 'half-way', name: 'Half Way', description: 'Complete 50% of modules', condition: (c) => c.length >= 20 },
  { id: 'graduate', name: 'Graduate', description: 'Complete all modules', condition: (c) => c.length >= 41 },
];

function checkAchievements(completed: string[]): Achievement[] {
  return ACHIEVEMENTS.filter((a) => a.condition(completed));
}


// ============================================================================
// TESTS
// ============================================================================

describe('Progress System', () => {
  beforeEach(() => {
    localStorageMock.clear();
  });

  describe('getProgress', () => {
    it('returns empty progress when nothing stored', () => {
      const progress = getProgress();
      expect(progress.completed).toEqual([]);
      expect(progress.startedAt).toBeDefined();
    });

    it('returns stored progress', () => {
      const data = { completed: ['py-variables'], startedAt: '2024-01-01', lastUpdated: '2024-01-01' };
      localStorage.setItem('ai-era-progress', JSON.stringify(data));
      const progress = getProgress();
      expect(progress.completed).toEqual(['py-variables']);
    });
  });

  describe('markComplete', () => {
    it('adds module to completed list', () => {
      markComplete('py-variables');
      expect(isComplete('py-variables')).toBe(true);
    });

    it('does not duplicate modules', () => {
      markComplete('py-variables');
      markComplete('py-variables');
      const progress = getProgress();
      expect(progress.completed.filter((id) => id === 'py-variables')).toHaveLength(1);
    });

    it('updates lastUpdated timestamp', () => {
      const before = new Date().toISOString();
      markComplete('py-variables');
      const progress = getProgress();
      expect(progress.lastUpdated >= before).toBe(true);
    });
  });

  describe('markIncomplete', () => {
    it('removes module from completed list', () => {
      markComplete('py-variables');
      markIncomplete('py-variables');
      expect(isComplete('py-variables')).toBe(false);
    });

    it('handles removing non-existent module', () => {
      markIncomplete('non-existent');
      const progress = getProgress();
      expect(progress.completed).toEqual([]);
    });
  });

  describe('isComplete', () => {
    it('returns false for uncompleted module', () => {
      expect(isComplete('py-variables')).toBe(false);
    });

    it('returns true for completed module', () => {
      markComplete('py-variables');
      expect(isComplete('py-variables')).toBe(true);
    });
  });

  describe('getCompletionPercentage', () => {
    it('returns 0 when no modules completed', () => {
      expect(getCompletionPercentage(41)).toBe(0);
    });

    it('calculates correct percentage', () => {
      markComplete('py-variables');
      markComplete('py-functions');
      expect(getCompletionPercentage(40)).toBe(5);
    });

    it('returns 100 when all modules completed', () => {
      for (let i = 0; i < 41; i++) {
        markComplete(`module-${i}`);
      }
      expect(getCompletionPercentage(41)).toBe(100);
    });
  });

  describe('resetProgress', () => {
    it('clears all progress', () => {
      markComplete('py-variables');
      markComplete('py-functions');
      resetProgress();
      const progress = getProgress();
      expect(progress.completed).toEqual([]);
    });
  });
});

describe('Achievement System', () => {
  beforeEach(() => {
    localStorageMock.clear();
  });

  it('unlocks First Step after completing one module', () => {
    const achievements = checkAchievements(['py-variables']);
    expect(achievements.map((a) => a.id)).toContain('first-step');
  });

  it('does not unlock First Step with zero modules', () => {
    const achievements = checkAchievements([]);
    expect(achievements.map((a) => a.id)).not.toContain('first-step');
  });

  it('unlocks Getting Started after 5 modules', () => {
    const completed = ['a', 'b', 'c', 'd', 'e'];
    const achievements = checkAchievements(completed);
    expect(achievements.map((a) => a.id)).toContain('five-modules');
  });

  it('unlocks multiple achievements', () => {
    const completed = Array.from({ length: 20 }, (_, i) => `module-${i}`);
    const achievements = checkAchievements(completed);
    expect(achievements.length).toBeGreaterThanOrEqual(3);
  });

  it('unlocks Graduate after completing all modules', () => {
    const completed = Array.from({ length: 41 }, (_, i) => `module-${i}`);
    const achievements = checkAchievements(completed);
    expect(achievements.map((a) => a.id)).toContain('graduate');
  });
});
