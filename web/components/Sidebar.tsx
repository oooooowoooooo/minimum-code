'use client';

import { useState, useMemo } from 'react';
import { modules, CATEGORY_META, getCategories, getModulesByCategory, type Module, type ModuleCategory, type ModuleStatus } from '@/lib/modules';

interface SidebarProps {
  moduleStatuses: Record<string, ModuleStatus>;
  activeModuleId?: string;
  onModuleClick: (module: Module) => void;
}

interface CollapsibleCategoryProps {
  category: ModuleCategory;
  modules: Module[];
  statuses: Record<string, ModuleStatus>;
  activeModuleId?: string;
  onModuleClick: (module: Module) => void;
  defaultOpen?: boolean;
}

function CollapsibleCategory({
  category,
  modules: catModules,
  statuses,
  activeModuleId,
  onModuleClick,
  defaultOpen = false,
}: CollapsibleCategoryProps) {
  const [isOpen, setIsOpen] = useState(defaultOpen);
  const meta = CATEGORY_META[category];

  const completedCount = catModules.filter((m) => statuses[m.id] === 'complete').length;
  const totalCount = catModules.length;
  const pct = totalCount === 0 ? 0 : Math.round((completedCount / totalCount) * 100);

  return (
    <div className="mb-1">
      {/* Category header */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center gap-2.5 px-3 py-2.5 rounded-lg hover:bg-gray-800/50 transition-colors group"
      >
        {/* Chevron */}
        <svg
          className={`w-3.5 h-3.5 text-gray-500 transition-transform duration-200 ${isOpen ? 'rotate-90' : ''}`}
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth={2}
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
        </svg>

        {/* Color dot */}
        <span
          className="w-2.5 h-2.5 rounded-full flex-shrink-0"
          style={{ backgroundColor: meta.color }}
        />

        {/* Label */}
        <span className="flex-1 text-left text-sm font-medium text-gray-300 group-hover:text-white transition-colors">
          {meta.label}
        </span>

        {/* Progress count */}
        <span className="text-xs text-gray-600 tabular-nums">
          {completedCount}/{totalCount}
        </span>
      </button>

      {/* Progress bar under category */}
      <div className="mx-3 mb-1">
        <div className="h-1 bg-gray-800 rounded-full overflow-hidden">
          <div
            className="h-full rounded-full progress-fill"
            style={{ width: `${pct}%`, backgroundColor: meta.color }}
          />
        </div>
      </div>

      {/* Module list */}
      {isOpen && (
        <div className="ml-5 pl-3 border-l border-gray-800 space-y-0.5 pb-2 animate-fade-in">
          {catModules.map((mod) => {
            const status = statuses[mod.id] ?? 'locked';
            const isActive = mod.id === activeModuleId;
            const isClickable = status !== 'locked';

            return (
              <button
                key={mod.id}
                onClick={isClickable ? () => onModuleClick(mod) : undefined}
                disabled={!isClickable}
                className={`
                  w-full flex items-center gap-2 px-2.5 py-1.5 rounded-md text-left
                  transition-all duration-150
                  ${isActive
                    ? 'bg-primary-600/20 text-primary-300 border border-primary-500/30'
                    : isClickable
                      ? 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/40'
                      : 'text-gray-600 cursor-not-allowed'
                  }
                `}
              >
                {/* Status icon */}
                <span className="text-xs w-4 text-center">
                  {status === 'complete' ? '✅' : status === 'in-progress' ? '🔄' : status === 'locked' ? '🔒' : '⬜'}
                </span>

                {/* Module title */}
                <span className="text-xs truncate">{mod.title}</span>
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default function Sidebar({ moduleStatuses, activeModuleId, onModuleClick }: SidebarProps) {
  const categories = getCategories();

  // Determine which category to open by default (the one containing the active module)
  const activeCategory = useMemo(() => {
    if (!activeModuleId) return categories[0];
    const mod = modules.find((m) => m.id === activeModuleId);
    return mod?.category ?? categories[0];
  }, [activeModuleId, categories]);

  return (
    <aside className="w-72 h-screen sticky top-0 flex flex-col bg-gray-950 border-r border-gray-800 overflow-hidden">
      {/* Logo / Title */}
      <div className="px-4 py-5 border-b border-gray-800">
        <h1 className="text-lg font-bold text-white">
          AI Era <span className="text-primary-400">Learning</span>
        </h1>
        <p className="text-xs text-gray-500 mt-0.5">Master Python + TypeScript</p>
      </div>

      {/* Scrollable category tree */}
      <nav className="flex-1 overflow-y-auto px-2 py-3 space-y-0.5">
        {categories.map((cat) => {
          const catModules = getModulesByCategory(cat);
          return (
            <CollapsibleCategory
              key={cat}
              category={cat}
              modules={catModules}
              statuses={moduleStatuses}
              activeModuleId={activeModuleId}
              onModuleClick={onModuleClick}
              defaultOpen={cat === activeCategory}
            />
          );
        })}
      </nav>

      {/* Footer */}
      <div className="px-4 py-3 border-t border-gray-800">
        <div className="flex items-center gap-2 text-xs text-gray-600">
          <span className="w-2 h-2 rounded-full bg-accent-500" />
          <span>
            {Object.values(moduleStatuses).filter((s) => s === 'complete').length} / {modules.length} complete
          </span>
        </div>
      </div>
    </aside>
  );
}
