'use client';

interface ProgressBarProps {
  percentage: number;
  label?: string;
  size?: 'sm' | 'md' | 'lg';
}

const sizeClasses = {
  sm: 'h-1.5',
  md: 'h-3',
  lg: 'h-5',
};

function getColor(pct: number): string {
  if (pct < 30) return 'bg-red-500';
  if (pct < 70) return 'bg-yellow-500';
  return 'bg-accent-500';
}

function getGlowColor(pct: number): string {
  if (pct < 30) return 'shadow-red-500/30';
  if (pct < 70) return 'shadow-yellow-500/30';
  return 'shadow-accent-500/30';
}

export default function ProgressBar({ percentage, label, size = 'md' }: ProgressBarProps) {
  const clamped = Math.max(0, Math.min(100, percentage));

  return (
    <div className="w-full">
      {(label != null || size !== 'sm') && (
        <div className="flex items-center justify-between mb-1.5">
          {label && <span className="text-sm text-gray-400">{label}</span>}
          <span className="text-sm font-mono text-gray-500">{clamped}%</span>
        </div>
      )}
      <div
        className={`w-full rounded-full bg-gray-800 overflow-hidden ${sizeClasses[size]}`}
      >
        <div
          className={`${sizeClasses[size]} rounded-full progress-fill shadow-lg ${getColor(clamped)} ${getGlowColor(clamped)}`}
          style={{ width: `${clamped}%` }}
        />
      </div>
    </div>
  );
}
