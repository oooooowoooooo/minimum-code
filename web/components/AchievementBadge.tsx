'use client';

import type { Achievement } from '@/lib/progress';

interface AchievementBadgeProps {
  achievement: Achievement;
}

interface AchievementGridProps {
  achievements: Achievement[];
}

export function AchievementBadge({ achievement }: AchievementBadgeProps) {
  const isLocked = achievement.unlockedAt === null;

  return (
    <div
      className={`
        relative flex flex-col items-center gap-2 p-4 rounded-xl border
        transition-all duration-300
        ${isLocked
          ? 'border-gray-800 bg-gray-900/50 opacity-50 grayscale'
          : 'border-yellow-600/30 bg-gradient-to-br from-yellow-900/20 to-gray-900 shadow-lg shadow-yellow-500/5'
        }
      `}
    >
      {/* Glow effect for unlocked */}
      {!isLocked && (
        <div className="absolute inset-0 rounded-xl bg-yellow-500/5 animate-pulse-slow pointer-events-none" />
      )}

      {/* Icon */}
      <div className={`text-4xl ${isLocked ? 'grayscale' : ''}`}>
        {isLocked ? '🔒' : achievement.icon}
      </div>

      {/* Name */}
      <h3 className={`text-sm font-semibold text-center ${isLocked ? 'text-gray-600' : 'text-yellow-300'}`}>
        {achievement.name}
      </h3>

      {/* Description */}
      <p className={`text-xs text-center leading-relaxed ${isLocked ? 'text-gray-700' : 'text-gray-400'}`}>
        {achievement.description}
      </p>

      {/* Unlock date */}
      {!isLocked && achievement.unlockedAt && (
        <span className="text-[10px] text-gray-600 mt-auto">
          {new Date(achievement.unlockedAt).toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric',
          })}
        </span>
      )}
    </div>
  );
}

export function AchievementGrid({ achievements }: AchievementGridProps) {
  const unlocked = achievements.filter((a) => a.unlockedAt !== null);
  const locked = achievements.filter((a) => a.unlockedAt === null);

  return (
    <div className="space-y-6">
      {/* Stats header */}
      <div className="flex items-center gap-4">
        <div className="text-sm text-gray-400">
          <span className="text-yellow-400 font-bold text-lg">{unlocked.length}</span>
          <span className="mx-1">/</span>
          <span>{achievements.length}</span>
          <span className="ml-1">unlocked</span>
        </div>
        <div className="flex-1 h-1.5 bg-gray-800 rounded-full overflow-hidden">
          <div
            className="h-full bg-yellow-500 rounded-full progress-fill"
            style={{
              width: `${achievements.length === 0 ? 0 : Math.round((unlocked.length / achievements.length) * 100)}%`,
            }}
          />
        </div>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
        {unlocked.map((a) => (
          <AchievementBadge key={a.id} achievement={a} />
        ))}
        {locked.map((a) => (
          <AchievementBadge key={a.id} achievement={a} />
        ))}
      </div>
    </div>
  );
}
