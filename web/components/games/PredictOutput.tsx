'use client';

import { useState, useCallback } from 'react';

interface PredictOutputProps {
  code: string;
  language?: string;
  options: string[];
  correctIndex: number;
  explanation: string;
  onComplete?: (correct: boolean) => void;
}

export default function PredictOutput({
  code,
  language = 'javascript',
  options,
  correctIndex,
  explanation,
  onComplete,
}: PredictOutputProps) {
  const [selectedIndex, setSelectedIndex] = useState<number | null>(null);
  const [revealed, setRevealed] = useState(false);

  const isCorrect = selectedIndex === correctIndex;

  const handleSelect = useCallback(
    (index: number) => {
      if (revealed) return;
      setSelectedIndex(index);
      setRevealed(true);
      onComplete?.(index === correctIndex);
    },
    [revealed, correctIndex, onComplete],
  );

  const handleReset = useCallback(() => {
    setSelectedIndex(null);
    setRevealed(false);
  }, []);

  return (
    <div className="w-full max-w-2xl mx-auto">
      {/* Prompt */}
      <div className="flex items-center gap-2 mb-4">
        <span className="text-2xl">🧩</span>
        <h3 className="text-lg font-semibold text-white">Predict the Output</h3>
      </div>

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
        <pre className="p-4 overflow-x-auto">
          <code className="text-sm leading-relaxed text-gray-300 font-mono">{code}</code>
        </pre>
      </div>

      {/* Question */}
      <p className="text-sm text-gray-400 mb-4">What will this code output?</p>

      {/* Options */}
      <div className="grid gap-3">
        {options.map((option, i) => {
          const isSelected = selectedIndex === i;
          const isCorrectOption = i === correctIndex;

          let borderClass = 'border-gray-700 hover:border-gray-500';
          let bgClass = 'bg-gray-900/50 hover:bg-gray-800/50';
          let textClass = 'text-gray-300';

          if (revealed) {
            if (isCorrectOption) {
              borderClass = 'border-green-500';
              bgClass = 'bg-green-500/10';
              textClass = 'text-green-400';
            } else if (isSelected && !isCorrectOption) {
              borderClass = 'border-red-500';
              bgClass = 'bg-red-500/10';
              textClass = 'text-red-400';
            } else {
              borderClass = 'border-gray-800';
              bgClass = 'bg-gray-900/30';
              textClass = 'text-gray-600';
            }
          }

          return (
            <button
              key={i}
              onClick={() => handleSelect(i)}
              disabled={revealed}
              className={`
                w-full text-left px-4 py-3 rounded-lg border transition-all duration-300
                ${borderClass} ${bgClass} ${textClass}
                ${!revealed ? 'cursor-pointer active:scale-[0.98]' : 'cursor-default'}
                ${revealed && isCorrectOption ? 'animate-correct-flash' : ''}
                ${revealed && isSelected && !isCorrectOption ? 'animate-wrong-flash' : ''}
              `}
            >
              <div className="flex items-center gap-3">
                <span
                  className={`
                    flex-shrink-0 w-7 h-7 rounded-full border flex items-center justify-center text-xs font-bold
                    ${revealed && isCorrectOption
                      ? 'border-green-500 text-green-400 bg-green-500/20'
                      : revealed && isSelected && !isCorrectOption
                        ? 'border-red-500 text-red-400 bg-red-500/20'
                        : 'border-gray-600 text-gray-500'
                    }
                  `}
                >
                  {String.fromCharCode(65 + i)}
                </span>
                <code className="font-mono text-sm">{option}</code>
                {revealed && isCorrectOption && (
                  <span className="ml-auto text-green-400 text-sm animate-bounce-in">✓</span>
                )}
                {revealed && isSelected && !isCorrectOption && (
                  <span className="ml-auto text-red-400 text-sm animate-bounce-in">✗</span>
                )}
              </div>
            </button>
          );
        })}
      </div>

      {/* Explanation */}
      {revealed && (
        <div
          className={`
            mt-6 p-4 rounded-xl border transition-all duration-500 animate-slide-up
            ${isCorrect
              ? 'border-green-500/30 bg-green-500/5'
              : 'border-red-500/30 bg-red-500/5'
            }
          `}
        >
          <div className="flex items-center gap-2 mb-2">
            <span className="text-lg">{isCorrect ? '🎉' : '💡'}</span>
            <span className={`font-semibold text-sm ${isCorrect ? 'text-green-400' : 'text-red-400'}`}>
              {isCorrect ? 'Correct!' : 'Not quite!'}
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

      {/* Keyframe animations via style tag */}
      <style jsx>{`
        @keyframes correct-flash {
          0% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.4); }
          50% { box-shadow: 0 0 20px 4px rgba(34, 197, 94, 0.2); }
          100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
        }
        @keyframes wrong-flash {
          0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
          50% { box-shadow: 0 0 20px 4px rgba(239, 68, 68, 0.2); }
          100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
        }
        @keyframes bounce-in {
          0% { transform: scale(0); opacity: 0; }
          50% { transform: scale(1.2); }
          100% { transform: scale(1); opacity: 1; }
        }
        @keyframes slide-up {
          0% { opacity: 0; transform: translateY(10px); }
          100% { opacity: 1; transform: translateY(0); }
        }
        .animate-correct-flash { animation: correct-flash 0.6s ease-out; }
        .animate-wrong-flash { animation: wrong-flash 0.6s ease-out; }
        .animate-bounce-in { animation: bounce-in 0.3s ease-out; }
        .animate-slide-up { animation: slide-up 0.4s ease-out; }
      `}</style>
    </div>
  );
}
