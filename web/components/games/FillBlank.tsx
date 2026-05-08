'use client';

import { useState, useCallback, useMemo } from 'react';

interface Blank {
  id: string;
  answer: string;
  hint?: string;
}

interface FillBlankProps {
  template: string;
  blanks: Blank[];
  explanation: string;
  onComplete?: (allCorrect: boolean) => void;
}

export default function FillBlank({
  template,
  blanks,
  explanation,
  onComplete,
}: FillBlankProps) {
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [submitted, setSubmitted] = useState(false);
  const [focusedBlank, setFocusedBlank] = useState<string | null>(null);

  const blankIds = useMemo(() => blanks.map((b) => b.id), [blanks]);

  const blankResults = useMemo(() => {
    if (!submitted) return {};
    const results: Record<string, boolean> = {};
    blanks.forEach((blank) => {
      const userAnswer = (answers[blank.id] || '').trim();
      results[blank.id] = userAnswer.toLowerCase() === blank.answer.toLowerCase();
    });
    return results;
  }, [submitted, blanks, answers]);

  const allCorrect = useMemo(
    () => submitted && Object.values(blankResults).every(Boolean),
    [submitted, blankResults],
  );

  const handleChange = useCallback((id: string, value: string) => {
    if (submitted) return;
    setAnswers((prev) => ({ ...prev, [id]: value }));
  }, [submitted]);

  const handleSubmit = useCallback(() => {
    setSubmitted(true);
    const results: Record<string, boolean> = {};
    blanks.forEach((blank) => {
      const userAnswer = (answers[blank.id] || '').trim();
      results[blank.id] = userAnswer.toLowerCase() === blank.answer.toLowerCase();
    });
    onComplete?.(Object.values(results).every(Boolean));
  }, [blanks, answers, onComplete]);

  const handleReset = useCallback(() => {
    setAnswers({});
    setSubmitted(false);
    setFocusedBlank(null);
  }, []);

  const handleShowAnswer = useCallback(() => {
    const newAnswers: Record<string, string> = {};
    blanks.forEach((blank) => {
      newAnswers[blank.id] = blank.answer;
    });
    setAnswers(newAnswers);
  }, [blanks]);

  // Parse template and render with inline inputs
  const renderTemplate = () => {
    const parts: React.ReactNode[] = [];
    let remaining = template;
    let partIndex = 0;

    while (remaining.length > 0) {
      // Find next ___BLANK_ID___
      const match = remaining.match(/___(\w+)___/);
      if (!match || match.index === undefined) {
        parts.push(
          <span key={`t-${partIndex++}`} className="text-gray-300 font-mono">
            {remaining}
          </span>,
        );
        break;
      }

      // Text before blank
      if (match.index > 0) {
        parts.push(
          <span key={`t-${partIndex++}`} className="text-gray-300 font-mono">
            {remaining.slice(0, match.index)}
          </span>,
        );
      }

      const blankId = match[1];
      const blank = blanks.find((b) => b.id === blankId);
      if (blank) {
        const isCorrectBlank = blankResults[blankId];
        const isFocused = focusedBlank === blankId;

        let borderColor = 'border-gray-600';
        let bgColor = 'bg-gray-800/50';
        if (submitted) {
          borderColor = isCorrectBlank ? 'border-green-500' : 'border-red-500';
          bgColor = isCorrectBlank ? 'bg-green-500/10' : 'bg-red-500/10';
        } else if (isFocused) {
          borderColor = 'border-blue-500';
          bgColor = 'bg-blue-500/5';
        }

        parts.push(
          <span key={`blank-${blankId}`} className="relative inline-block mx-0.5">
            <input
              type="text"
              value={answers[blankId] || ''}
              onChange={(e) => handleChange(blankId, e.target.value)}
              onFocus={() => setFocusedBlank(blankId)}
              onBlur={() => setFocusedBlank(null)}
              disabled={submitted}
              placeholder={blank.hint || '?'}
              style={{ width: `${Math.max(blank.answer.length * 0.65, 2.5)}rem` }}
              className={`
                inline-block px-2 py-0.5 text-sm font-mono rounded border
                text-white placeholder-gray-600 text-center
                transition-all duration-200 outline-none
                ${borderColor} ${bgColor}
                ${!submitted ? 'focus:border-blue-400 focus:bg-blue-500/10' : ''}
                ${submitted && isCorrectBlank ? 'animate-correct-highlight' : ''}
                ${submitted && !isCorrectBlank ? 'animate-wrong-highlight' : ''}
              `}
            />
            {submitted && !isCorrectBlank && (
              <span className="absolute -bottom-5 left-0 text-[10px] text-green-400 whitespace-nowrap animate-fade-in">
                answer: {blank.answer}
              </span>
            )}
          </span>,
        );
      }

      remaining = remaining.slice(match.index + match[0].length);
    }

    return parts;
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      {/* Prompt */}
      <div className="flex items-center gap-2 mb-4">
        <span className="text-2xl">✏️</span>
        <h3 className="text-lg font-semibold text-white">Fill in the Blanks</h3>
      </div>
      <p className="text-sm text-gray-400 mb-4">
        Type the missing code to complete the snippet.
      </p>

      {/* Code block */}
      <div className="rounded-xl border border-gray-800 overflow-hidden bg-[#1e1e1e] mb-6">
        <div className="flex items-center gap-1.5 px-4 py-2.5 bg-gray-900 border-b border-gray-800">
          <span className="w-3 h-3 rounded-full bg-red-500/70" />
          <span className="w-3 h-3 rounded-full bg-yellow-500/70" />
          <span className="w-3 h-3 rounded-full bg-green-500/70" />
        </div>
        <div className="p-4 overflow-x-auto leading-loose text-sm">
          {renderTemplate()}
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center gap-3">
        {!submitted ? (
          <>
            <button
              onClick={handleSubmit}
              disabled={blankIds.every((id) => !(answers[id] || '').trim())}
              className="px-5 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-500 disabled:opacity-30 disabled:cursor-not-allowed rounded-lg transition-all duration-200 active:scale-95"
            >
              Check Answer
            </button>
            <button
              onClick={handleShowAnswer}
              className="px-4 py-2 text-sm text-gray-500 hover:text-gray-300 transition-colors"
            >
              Show Answers
            </button>
          </>
        ) : (
          <button
            onClick={handleReset}
            className="px-4 py-2 text-sm text-gray-400 hover:text-white border border-gray-700 hover:border-gray-500 rounded-lg transition-all duration-200 hover:bg-gray-800/50"
          >
            Try Again
          </button>
        )}
      </div>

      {/* Explanation */}
      {submitted && (
        <div
          className={`
            mt-6 p-4 rounded-xl border transition-all duration-500 animate-slide-up
            ${allCorrect
              ? 'border-green-500/30 bg-green-500/5'
              : 'border-yellow-500/30 bg-yellow-500/5'
            }
          `}
        >
          <div className="flex items-center gap-2 mb-2">
            <span className="text-lg">{allCorrect ? '🎉' : '💡'}</span>
            <span className={`font-semibold text-sm ${allCorrect ? 'text-green-400' : 'text-yellow-400'}`}>
              {allCorrect ? 'All blanks correct!' : 'Some blanks need fixing'}
            </span>
          </div>
          <p className="text-sm text-gray-400 leading-relaxed">{explanation}</p>
        </div>
      )}

      <style jsx>{`
        @keyframes correct-highlight {
          0% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.4); }
          50% { box-shadow: 0 0 12px 2px rgba(34, 197, 94, 0.2); }
          100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
        }
        @keyframes wrong-highlight {
          0%, 100% { transform: translateX(0); }
          20% { transform: translateX(-3px); }
          40% { transform: translateX(3px); }
          60% { transform: translateX(-2px); }
          80% { transform: translateX(2px); }
        }
        @keyframes fade-in {
          0% { opacity: 0; }
          100% { opacity: 1; }
        }
        @keyframes slide-up {
          0% { opacity: 0; transform: translateY(10px); }
          100% { opacity: 1; transform: translateY(0); }
        }
        .animate-correct-highlight { animation: correct-highlight 0.6s ease-out; }
        .animate-wrong-highlight { animation: wrong-highlight 0.4s ease-out; }
        .animate-fade-in { animation: fade-in 0.3s ease-out; }
        .animate-slide-up { animation: slide-up 0.4s ease-out; }
      `}</style>
    </div>
  );
}
