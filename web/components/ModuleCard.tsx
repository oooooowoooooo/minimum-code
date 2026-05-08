'use client';

import type { Module, ModuleStatus } from '@/lib/modules';
import { CATEGORY_META } from '@/lib/modules';

interface ModuleCardProps {
  module: Module;
  status: ModuleStatus;
  prerequisites?: Module[];
  onClick?: () => void;
}

const statusConfig: Record<ModuleStatus, { icon: string; label: string; ring: string }> = {
  locked:       { icon: '🔒', label: 'Locked',      ring: 'ring-gray-700' },
  available:    { icon: '⬜', label: 'Available',    ring: 'ring-gray-500 hover:ring-primary-400' },
  'in-progress': { icon: '🔄', label: 'In Progress', ring: 'ring-yellow-500' },
  complete:     { icon: '✅', label: 'Complete',     ring: 'ring-accent-500' },
};

export default function ModuleCard({ module, status, prerequisites, onClick }: ModuleCardProps) {
  const cfg = statusConfig[status];
  const catColor = CATEGORY_META[module.category].color;
  const isClickable = status !== 'locked';

  return (
    <button
      onClick={isClickable ? onClick : undefined}
      disabled={!isClickable}
      className={`
        card-hover relative w-full text-left rounded-xl border border-gray-800
        bg-gradient-to-br from-gray-900 to-gray-950 p-5
        ring-1 ${cfg.ring}
        transition-all duration-200
        ${isClickable ? 'cursor-pointer hover:border-gray-600' : 'cursor-not-allowed opacity-60'}
        ${status === 'complete' ? 'border-accent-700/40' : ''}
      `}
      style={{ borderLeftColor: catColor, borderLeftWidth: '3px' }}
    >
      {/* Status badge */}
      <div className="absolute top-3 right-3 flex items-center gap-1.5 text-xs text-gray-400">
        <span>{cfg.icon}</span>
        <span className="hidden sm:inline">{cfg.label}</span>
      </div>

      {/* Content */}
      <div className="flex items-start gap-3 pr-20">
        <span className="text-2xl flex-shrink-0">{module.icon}</span>
        <div className="min-w-0">
          <h3 className="text-base font-semibold text-gray-100 leading-tight">
            {module.title}
          </h3>
          <p className="mt-1 text-sm text-gray-400 line-clamp-2">
            {module.description}
          </p>
        </div>
      </div>

      {/* Prerequisites (shown when locked) */}
      {status === 'locked' && prerequisites && prerequisites.length > 0 && (
        <div className="mt-3 pt-3 border-t border-gray-800">
          <p className="text-xs text-gray-500 mb-1">Prerequisites:</p>
          <div className="flex flex-wrap gap-1.5">
            {prerequisites.map((pre) => (
              <span
                key={pre.id}
                className="inline-flex items-center gap-1 text-xs bg-gray-800 text-gray-400 rounded-full px-2 py-0.5"
              >
                {pre.icon} {pre.title}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Completion indicator */}
      {status === 'complete' && (
        <div className="absolute inset-0 rounded-xl ring-2 ring-accent-500/20 pointer-events-none" />
      )}
    </button>
  );
}
