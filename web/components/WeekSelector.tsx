'use client';

import { useRef, useEffect, useCallback } from 'react';

interface WeekSelectorProps {
  weeks: number[];
  selectedWeek: number;
  onSelect: (week: number) => void;
  weekStats?: Record<number, number>;
}

export default function WeekSelector({ weeks, selectedWeek, onSelect, weekStats }: WeekSelectorProps) {
  const scrollRef = useRef<HTMLDivElement>(null);
  const selectedRef = useRef<HTMLButtonElement>(null);

  // Scroll selected tab into view on mount and when selection changes
  useEffect(() => {
    if (selectedRef.current && scrollRef.current) {
      const container = scrollRef.current;
      const btn = selectedRef.current;
      const left = btn.offsetLeft - container.offsetLeft - 16;
      container.scrollTo({ left: Math.max(0, left), behavior: 'smooth' });
    }
  }, [selectedWeek]);

  const handleClick = useCallback(
    (week: number) => {
      onSelect(week);
    },
    [onSelect],
  );

  return (
    <div className="w-full">
      <div
        ref={scrollRef}
        className="flex gap-1.5 overflow-x-auto scrollbar-hide pb-1 -mb-1"
        style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
      >
        {weeks.map((week) => {
          const isSelected = week === selectedWeek;
          const count = weekStats?.[week];

          return (
            <button
              key={week}
              ref={isSelected ? selectedRef : undefined}
              onClick={() => handleClick(week)}
              className={`
                flex-shrink-0 flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-sm font-medium
                transition-all duration-150 whitespace-nowrap
                ${isSelected
                  ? 'bg-primary-600 text-white shadow-lg shadow-primary-600/25'
                  : 'bg-gray-800/60 text-gray-400 hover:bg-gray-800 hover:text-gray-200'
                }
              `}
            >
              <span>W{week}</span>
              {count != null && (
                <span
                  className={`
                    text-xs tabular-nums px-1.5 py-0.5 rounded-full
                    ${isSelected
                      ? 'bg-white/20 text-white/90'
                      : 'bg-gray-700/60 text-gray-500'
                    }
                  `}
                >
                  {count}
                </span>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
}
