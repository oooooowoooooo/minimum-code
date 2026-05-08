'use client';

import { useState, useCallback } from 'react';

interface FindBugProps {
  code: string;
  language?: string;
  bugLineIndex: number;
  explanation: string;
  onComplete?: (correct: boolean) => void;
}

export default function FindBug({
  code,
  language = 'javascript',
  bugLineIndex,
  explanation,
  onComplete,
}: FindBugProps) {
  const [selectedLine, setSelectedLine] = useState<number | null>(null);
  const [revealed, setRevealed] = useState(false);

  const lines = code.split('\n');
  const isCorrect = selectedLine === bugLineIndex;

  const handleLineClick = useCallback(
    (lineIndex: number) => {
      if (revealed) return;
      setSelectedLine(lineIndex);
      setRevealed(true);
      onComplete?.(lineIndex === bugLineIndex);
    },
    [revealed, bugLineIndex, onComplete],
  );

  const handleReset = useCallback(() => {
    setSelectedLine(null);
    setRevealed(false);
  }, []);

  return (
    <div className="w-full max-w-2xl mx-auto">
      {/* Prompt */}
      <div className="flex items-center gap-2 mb-4">
        <span className="text-2xl">🐛</span>
        <h3 className="text-lg font-semibold text-white">Find the Bug</h3>
      </div>
      <p className="text-sm text-gray-400 mb-4">
        Click on the line that contains the bug.
      </p>

      {/* Code block */}
      <div className="rounded-xl border border-gray-800 overflow-hidden bg-[#1e1e1e] mb-6">
        <div className="flex items-center gap-1.5 px-4 py-2.5 bg-gray-900 border-b border-gray-800">
          <span className="w-3 h-3 rounded-full bg-red-500/70" />
          <span className="w-3 h-3 rounded-full bg-yellow-500/70" />
          <span className="w-3 h-3 rounded-full bg-green-500/70" />
          <span className="ml-3 text-[10px] uppercase tracking-wider text-gray-500 bg-gray-800 px-2 py-0.5 rounded">
            {language}
          </span>
        </div>
        <div className="overflow-x-auto">
          <pre className="p-0 m-0">
            <code className="block text-sm leading-relaxed">
              {lines.map((line, i) => {
                const isSelected = selectedLine === i;
                const isBugLine = i === bugLineIndex;

                let lineBg = 'hover:bg-white/[0.05]';
                let lineBorder = '';
                let cursorClass = 'cursor-pointer';

                if (revealed) {
                  if (isBugLine) {
                    lineBg = 'bg-red-500/10';
                    lineBorder = 'border-l-2 border-red-500';
                  } else if (isSelected && !isBugLine) {
                    lineBg = 'bg-yellow-500/5';
                    lineBorder = 'border-l-2 border-yellow-500';
                  } else {
                    lineBg = 'opacity-50';
                  }
                  cursorClass = 'cursor-default';
                }

                return (
                  <div
                    key={i}
                    onClick={() => handleLineClick(i)}
                    className={`
                      flex transition-all duration-300 ${lineBg} ${lineBorder} ${cursorClass}
                      ${isSelected && isBugLine ? 'animate-correct-pulse' : ''}
                      ${isSelected && !isBugLine ? 'animate-wrong-shake' : ''}
                    `}
                  >
                    {/* Line number */}
                    <span className="flex-shrink-0 w-12 text-right pr-4 text-gray-600 select-none text-xs leading-relaxed border-r border-gray-800/50">
                      {i + 1}
                    </span>
                    {/* Code */}
                    <span className="pl-4 pr-4 flex-1 whitespace-pre text-gray-300 font-mono">
                      {line}
                    </span>
                    {/* Indicator */}
                    {revealed && isBugLine && (
                      <span className="pr-4 flex items-center text-red-400 text-xs animate-bounce-in">
                        ← bug here
                      </span>
                    )}
                    {revealed && isSelected && !isBugLine && (
                      <span className="pr-4 flex items-center text-yellow-400 text-xs animate-bounce-in">
                        ← not the bug
                      </span>
                    )}
                  </div>
                );
              })}
            </code>
          </pre>
        </div>
      </div>

      {/* Explanation */}
      {revealed && (
        <div
          className={`
            p-4 rounded-xl border transition-all duration-500 animate-slide-up
            ${isCorrect
              ? 'border-green-500/30 bg-green-500/5'
              : 'border-red-500/30 bg-red-500/5'
            }
          `}
        >
          <div className="flex items-center gap-2 mb-2">
            <span className="text-lg">{isCorrect ? '🎉' : '💡'}</span>
            <span className={`font-semibold text-sm ${isCorrect ? 'text-green-400' : 'text-red-400'}`}>
              {isCorrect ? 'You found it!' : 'Not that line!'}
            </span>
          </div>
          <p className="text-sm text-gray-400 leading-relaxed">{explanation}</p>
        </div>
      )}

      {/* Reset button */}
      {revealed && (
        <div className="mt-4 flex justify-center animate-slide-up">
          <button
            onClick={handleReset}
            className="px-4 py-2 text-sm text-gray-400 hover:text-white border border-gray-700 hover:border-gray-500 rounded-lg transition-all duration-200 hover:bg-gray-800/50"
          >
            Try Again
          </button>
        </div>
      )}

      <style jsx>{`
        @keyframes correct-pulse {
          0% { box-shadow: inset 0 0 0 0 rgba(34, 197, 94, 0); }
          50% { box-shadow: inset 0 0 20px 0 rgba(34, 197, 94, 0.1); }
          100% { box-shadow: inset 0 0 0 0 rgba(34, 197, 94, 0); }
        }
        @keyframes wrong-shake {
          0%, 100% { transform: translateX(0); }
          20% { transform: translateX(-4px); }
          40% { transform: translateX(4px); }
          60% { transform: translateX(-2px); }
          80% { transform: translateX(2px); }
        }
        @keyframes bounce-in {
          0% { transform: scale(0); opacity: 0; }
          60% { transform: scale(1.1); }
          100% { transform: scale(1); opacity: 1; }
        }
        @keyframes slide-up {
          0% { opacity: 0; transform: translateY(10px); }
          100% { opacity: 1; transform: translateY(0); }
        }
        .animate-correct-pulse { animation: correct-pulse 0.6s ease-out; }
        .animate-wrong-shake { animation: wrong-shake 0.4s ease-out; }
        .animate-bounce-in { animation: bounce-in 0.3s ease-out; }
        .animate-slide-up { animation: slide-up 0.4s ease-out; }
      `}</style>
    </div>
  );
}
