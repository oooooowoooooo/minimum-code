'use client';

import { useState, useCallback, useMemo } from 'react';

interface CodeOrderProps {
  lines: string[];
  explanation: string;
  onComplete?: (correct: boolean) => void;
}

export default function CodeOrder({
  lines: correctLines,
  explanation,
  onComplete,
}: CodeOrderProps) {
  // Shuffle on mount using a stable seed
  const [shuffledIndices] = useState<number[]>(() => {
    const indices = correctLines.map((_, i) => i);
    // Fisher-Yates shuffle
    for (let i = indices.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [indices[i], indices[j]] = [indices[j], indices[i]];
    }
    // Ensure it is not already in correct order
    if (indices.every((v, i) => v === i)) {
      // Swap first two
      [indices[0], indices[1]] = [indices[1], indices[0]];
    }
    return indices;
  });

  const [order, setOrder] = useState<number[]>(shuffledIndices);
  const [submitted, setSubmitted] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState<number | null>(null);

  const isCorrect = useMemo(
    () => order.every((origIdx, pos) => origIdx === pos),
    [order],
  );

  const lineResults = useMemo(() => {
    if (!submitted) return [];
    return order.map((origIdx, pos) => origIdx === pos);
  }, [submitted, order]);

  const moveUp = useCallback(
    (pos: number) => {
      if (submitted || pos === 0) return;
      setOrder((prev) => {
        const next = [...prev];
        [next[pos - 1], next[pos]] = [next[pos], next[pos - 1]];
        return next;
      });
    },
    [submitted],
  );

  const moveDown = useCallback(
    (pos: number) => {
      if (submitted || pos === order.length - 1) return;
      setOrder((prev) => {
        const next = [...prev];
        [next[pos], next[pos + 1]] = [next[pos + 1], next[pos]];
        return next;
      });
    },
    [submitted, order.length],
  );

  const handleSelect = useCallback(
    (pos: number) => {
      if (submitted) return;
      if (selectedIndex === null) {
        setSelectedIndex(pos);
      } else if (selectedIndex === pos) {
        setSelectedIndex(null);
      } else {
        // Swap
        setOrder((prev) => {
          const next = [...prev];
          [next[selectedIndex], next[pos]] = [next[pos], next[selectedIndex]];
          return next;
        });
        setSelectedIndex(null);
      }
    },
    [submitted, selectedIndex],
  );

  const handleSubmit = useCallback(() => {
    setSubmitted(true);
    onComplete?.(isCorrect);
  }, [isCorrect, onComplete]);

  const handleReset = useCallback(() => {
    setOrder(shuffledIndices);
    setSubmitted(false);
    setSelectedIndex(null);
  }, [shuffledIndices]);

  const handleShowOrder = useCallback(() => {
    setOrder(correctLines.map((_, i) => i));
  }, [correctLines]);

  return (
    <div className="w-full max-w-2xl mx-auto">
      {/* Prompt */}
      <div className="flex items-center gap-2 mb-4">
        <span className="text-2xl">🔢</span>
        <h3 className="text-lg font-semibold text-white">Put the Code in Order</h3>
      </div>
      <p className="text-sm text-gray-400 mb-4">
        {submitted
          ? 'Here is your result.'
          : 'Drag lines or use arrows to reorder. Tap two lines to swap them.'}
      </p>

      {/* Code lines */}
      <div className="rounded-xl border border-gray-800 overflow-hidden bg-[#1e1e1e] mb-6">
        <div className="flex items-center gap-1.5 px-4 py-2.5 bg-gray-900 border-b border-gray-800">
          <span className="w-3 h-3 rounded-full bg-red-500/70" />
          <span className="w-3 h-3 rounded-full bg-yellow-500/70" />
          <span className="w-3 h-3 rounded-full bg-green-500/70" />
        </div>
        <div className="divide-y divide-gray-800/50">
          {order.map((origIdx, pos) => {
            const isCorrectLine = lineResults[pos];
            const isSelected = selectedIndex === pos;

            let lineBg = 'bg-transparent';
            let borderAccent = '';

            if (isSelected) {
              lineBg = 'bg-blue-500/10';
              borderAccent = 'border-l-2 border-blue-500';
            } else if (submitted) {
              if (isCorrectLine) {
                lineBg = 'bg-green-500/5';
                borderAccent = 'border-l-2 border-green-500';
              } else {
                lineBg = 'bg-red-500/5';
                borderAccent = 'border-l-2 border-red-500';
              }
            }

            return (
              <div
                key={pos}
                onClick={() => handleSelect(pos)}
                className={`
                  flex items-center transition-all duration-200 ${lineBg} ${borderAccent}
                  ${!submitted ? 'hover:bg-white/[0.03] cursor-pointer' : 'cursor-default'}
                  ${submitted && isCorrectLine ? 'animate-correct-glow' : ''}
                  ${submitted && !isCorrectLine ? 'animate-wrong-shake' : ''}
                `}
              >
                {/* Position indicator */}
                <span className="flex-shrink-0 w-10 text-center text-xs text-gray-600 select-none">
                  {pos + 1}
                </span>

                {/* Code line */}
                <span className="flex-1 px-3 py-2.5 text-sm text-gray-300 font-mono whitespace-pre overflow-x-auto">
                  {correctLines[origIdx]}
                </span>

                {/* Status / controls */}
                <div className="flex-shrink-0 flex items-center gap-1 pr-2">
                  {submitted ? (
                    isCorrectLine ? (
                      <span className="text-green-400 text-xs animate-fade-in">✓</span>
                    ) : (
                      <span className="text-red-400 text-xs animate-fade-in">✗</span>
                    )
                  ) : (
                    <div className="flex flex-col gap-0.5">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          moveUp(pos);
                        }}
                        disabled={pos === 0}
                        className="w-6 h-5 flex items-center justify-center text-gray-600 hover:text-white hover:bg-gray-700 rounded disabled:opacity-20 disabled:cursor-not-allowed transition-colors text-xs"
                        aria-label="Move up"
                      >
                        ▲
                      </button>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          moveDown(pos);
                        }}
                        disabled={pos === order.length - 1}
                        className="w-6 h-5 flex items-center justify-center text-gray-600 hover:text-white hover:bg-gray-700 rounded disabled:opacity-20 disabled:cursor-not-allowed transition-colors text-xs"
                        aria-label="Move down"
                      >
                        ▼
                      </button>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center gap-3">
        {!submitted ? (
          <>
            <button
              onClick={handleSubmit}
              className="px-5 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-500 rounded-lg transition-all duration-200 active:scale-95"
            >
              Check Order
            </button>
            <button
              onClick={handleShowOrder}
              className="px-4 py-2 text-sm text-gray-500 hover:text-gray-300 transition-colors"
            >
              Show Correct Order
            </button>
          </>
        ) : (
          <button
            onClick={handleReset}
            className="px-4 py-2 text-sm text-gray-400 hover:text-white border border-gray-700 hover:border-gray-500 rounded-lg transition-all duration-200 hover:bg-gray-800/50"
          >
            Shuffle & Retry
          </button>
        )}
      </div>

      {/* Explanation */}
      {submitted && (
        <div
          className={`
            mt-6 p-4 rounded-xl border transition-all duration-500 animate-slide-up
            ${isCorrect
              ? 'border-green-500/30 bg-green-500/5'
              : 'border-yellow-500/30 bg-yellow-500/5'
            }
          `}
        >
          <div className="flex items-center gap-2 mb-2">
            <span className="text-lg">{isCorrect ? '🎉' : '💡'}</span>
            <span className={`font-semibold text-sm ${isCorrect ? 'text-green-400' : 'text-yellow-400'}`}>
              {isCorrect ? 'Perfect order!' : 'Not quite right'}
            </span>
          </div>
          <p className="text-sm text-gray-400 leading-relaxed">{explanation}</p>
        </div>
      )}

      <style jsx>{`
        @keyframes correct-glow {
          0% { box-shadow: inset 0 0 0 0 rgba(34, 197, 94, 0); }
          50% { box-shadow: inset 0 0 12px 0 rgba(34, 197, 94, 0.08); }
          100% { box-shadow: inset 0 0 0 0 rgba(34, 197, 94, 0); }
        }
        @keyframes wrong-shake {
          0%, 100% { transform: translateX(0); }
          20% { transform: translateX(-3px); }
          40% { transform: translateX(3px); }
          60% { transform: translateX(-2px); }
          80% { transform: translateX(2px); }
        }
        @keyframes fade-in {
          0% { opacity: 0; transform: scale(0.5); }
          100% { opacity: 1; transform: scale(1); }
        }
        @keyframes slide-up {
          0% { opacity: 0; transform: translateY(10px); }
          100% { opacity: 1; transform: translateY(0); }
        }
        .animate-correct-glow { animation: correct-glow 0.6s ease-out; }
        .animate-wrong-shake { animation: wrong-shake 0.4s ease-out; }
        .animate-fade-in { animation: fade-in 0.3s ease-out; }
        .animate-slide-up { animation: slide-up 0.4s ease-out; }
      `}</style>
    </div>
  );
}
