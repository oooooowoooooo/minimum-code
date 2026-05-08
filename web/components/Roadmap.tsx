'use client';

import { modules, CATEGORY_META, type Module, type ModuleCategory, type ModuleStatus } from '@/lib/modules';

interface RoadmapProps {
  moduleStatuses: Record<string, ModuleStatus>;
  onModuleClick: (module: Module) => void;
}

const WEEKS: { label: string; categories: ModuleCategory[] }[] = [
  { label: 'Week 1', categories: ['cognitive'] },
  { label: 'Week 2', categories: ['python-fundamentals'] },
  { label: 'Week 3', categories: ['typescript-fundamentals'] },
  { label: 'Week 4', categories: ['patterns'] },
  { label: 'Week 5', categories: ['python-dissect'] },
  { label: 'Week 6', categories: ['typescript-dissect'] },
  { label: 'Week 7', categories: ['ai-mastery'] },
  { label: 'Week 8', categories: ['practice'] },
];

const statusBorder: Record<ModuleStatus, string> = {
  locked: 'border-gray-700 opacity-40',
  available: 'border-gray-500',
  'in-progress': 'border-yellow-500 animate-pulse-slow',
  complete: 'border-accent-500',
};

const statusBg: Record<ModuleStatus, string> = {
  locked: 'bg-gray-900',
  available: 'bg-gray-800',
  'in-progress': 'bg-gray-800',
  complete: 'bg-accent-900/30',
};

export default function Roadmap({ moduleStatuses, onModuleClick }: RoadmapProps) {
  const getModulesForWeek = (cats: ModuleCategory[]): Module[] =>
    modules.filter((m) => cats.includes(m.category));

  return (
    <div className="w-full overflow-x-auto pb-6">
      <div className="flex gap-6 min-w-max px-4">
        {WEEKS.map((week, wi) => {
          const weekModules = getModulesForWeek(week.categories);
          const catColor = CATEGORY_META[week.categories[0]].color;

          return (
            <div key={wi} className="flex flex-col items-center" style={{ minWidth: 200 }}>
              {/* Week header */}
              <div
                className="mb-4 px-4 py-1.5 rounded-full text-sm font-semibold text-white"
                style={{ backgroundColor: catColor }}
              >
                {week.label}
              </div>

              {/* Connector line from previous week */}
              {wi > 0 && (
                <div
                  className="w-0.5 h-6 -mt-4 mb-2"
                  style={{ backgroundColor: catColor + '60' }}
                />
              )}

              {/* Module cards */}
              <div className="flex flex-col gap-3 w-full">
                {weekModules.map((mod) => {
                  const status = moduleStatuses[mod.id] ?? 'locked';
                  const isClickable = status !== 'locked';

                  return (
                    <button
                      key={mod.id}
                      onClick={isClickable ? () => onModuleClick(mod) : undefined}
                      disabled={!isClickable}
                      className={`
                        relative w-full text-left rounded-lg border p-3
                        transition-all duration-200
                        ${statusBorder[status]} ${statusBg[status]}
                        ${isClickable ? 'cursor-pointer hover:scale-[1.02] hover:shadow-lg' : 'cursor-not-allowed'}
                      `}
                    >
                      {/* Left accent bar */}
                      <div
                        className="absolute left-0 top-2 bottom-2 w-1 rounded-full"
                        style={{ backgroundColor: status === 'complete' ? catColor : catColor + '40' }}
                      />

                      <div className="pl-3">
                        <div className="flex items-center gap-2">
                          <span className="text-base">{mod.icon}</span>
                          <span className="text-sm font-medium text-gray-200 leading-tight">
                            {mod.title}
                          </span>
                        </div>

                        {/* Status dot */}
                        <div className="mt-1.5 flex items-center gap-1.5">
                          <span
                            className={`inline-block w-2 h-2 rounded-full ${
                              status === 'complete'
                                ? 'bg-accent-500'
                                : status === 'in-progress'
                                  ? 'bg-yellow-500'
                                  : status === 'available'
                                    ? 'bg-gray-500'
                                    : 'bg-gray-700'
                            }`}
                          />
                          <span className="text-xs text-gray-500 capitalize">
                            {status.replace('-', ' ')}
                          </span>
                        </div>
                      </div>
                    </button>
                  );
                })}
              </div>

              {/* Connector line to next week */}
              {wi < WEEKS.length - 1 && (
                <div
                  className="w-0.5 h-6 mt-2"
                  style={{ backgroundColor: catColor + '60' }}
                />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
