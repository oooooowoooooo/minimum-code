'use client';

import { useState, useEffect, useCallback, useMemo, lazy, Suspense } from 'react';

const PredictOutput = lazy(() => import('./games/PredictOutput'));
const FindBug = lazy(() => import('./games/FindBug'));
const FillBlank = lazy(() => import('./games/FillBlank'));
const CodeOrder = lazy(() => import('./games/CodeOrder'));

// ──────────────────────────────────────────────
//  Types
// ──────────────────────────────────────────────

interface QuizQuestion {
  question: string;
  options: [string, string, string, string];
  correctIndex: number;
  explanation: string;
}

interface ParsedGame {
  type: 'predict_output' | 'find_bug' | 'fill_blank' | 'code_order';
  instructions?: string;
  content?: Record<string, unknown>;
  [key: string]: unknown;
}

interface KnowledgeCardProps {
  title: string;
  explanation: string;
  code: string;
  game?: string | ParsedGame;
  quiz?: QuizQuestion;
  onComplete?: () => void;
  onGameComplete?: () => void;
  isCompleted?: boolean;
  isGameCompleted?: boolean;
}

// ──────────────────────────────────────────────
//  Helpers
// ──────────────────────────────────────────────

function parseGame(raw: string | ParsedGame | undefined): ParsedGame | null {
  if (!raw) return null;
  if (typeof raw === 'object' && raw.type) return raw;
  if (typeof raw === 'string') {
    try {
      const parsed = JSON.parse(raw);
      if (parsed && typeof parsed === 'object' && parsed.type) return parsed as ParsedGame;
    } catch {
      // Not valid JSON — treat as plain text
      return null;
    }
  }
  return null;
}

const GAME_LABELS: Record<string, string> = {
  predict_output: 'Predict the Output',
  find_bug: 'Find the Bug',
  fill_blank: 'Fill in the Blanks',
  code_order: 'Put the Code in Order',
};

const GAME_ICONS: Record<string, string> = {
  predict_output: '🧩',
  find_bug: '🐛',
  fill_blank: '✏️',
  code_order: '🔢',
};

// ──────────────────────────────────────────────
//  Component
// ──────────────────────────────────────────────

export default function KnowledgeCard({
  title,
  explanation,
  code,
  game,
  quiz,
  onComplete,
  onGameComplete,
  isCompleted = false,
  isGameCompleted = false,
}: KnowledgeCardProps) {
  const [isExpanded, setIsExpanded] = useState(true);
  const [selectedOption, setSelectedOption] = useState<number | null>(null);
  const [isAnswered, setIsAnswered] = useState(false);
  const [completed, setCompleted] = useState(isCompleted);
  const [gameCompleted, setGameCompleted] = useState(isGameCompleted);

  const parsedGame = useMemo(() => parseGame(game), [game]);
  const plainGameText = useMemo(() => {
    if (!game) return null;
    if (typeof game === 'string') {
      try {
        JSON.parse(game);
        return null; // valid JSON, not plain text
      } catch {
        return game; // plain text
      }
    }
    return null;
  }, [game]);

  // Load completion state from localStorage on mount
  useEffect(() => {
    if (typeof window === 'undefined') return;
    try {
      if (localStorage.getItem(`kc-completed-${title}`) === 'true') {
        setCompleted(true);
      }
      if (localStorage.getItem(`kc-game-completed-${title}`) === 'true') {
        setGameCompleted(true);
      }
    } catch {
      // localStorage unavailable
    }
  }, [title]);

  // Sync prop changes
  useEffect(() => { setCompleted(isCompleted); }, [isCompleted]);
  useEffect(() => { setGameCompleted(isGameCompleted); }, [isGameCompleted]);

  const handleAnswer = useCallback(
    (index: number) => {
      if (isAnswered || !quiz) return;
      setSelectedOption(index);
      setIsAnswered(true);
      if (index === quiz.correctIndex) {
        setCompleted(true);
        try { localStorage.setItem(`kc-completed-${title}`, 'true'); } catch {}
        onComplete?.();
      }
    },
    [isAnswered, quiz, title, onComplete],
  );

  const handleGameComplete = useCallback(
    (correct: boolean) => {
      if (correct) {
        setGameCompleted(true);
        try { localStorage.setItem(`kc-game-completed-${title}`, 'true'); } catch {}
        onGameComplete?.();
      }
    },
    [title, onGameComplete],
  );

  const toggleExpanded = useCallback(() => setIsExpanded((v) => !v), []);

  // Render the parsed game component
  const renderGame = () => {
    if (!parsedGame) {
      if (plainGameText) {
        return (
          <div className="rounded-lg border border-yellow-700/40 bg-yellow-900/20 p-4 sm:p-5">
            <h3 className="text-sm font-semibold text-yellow-400 mb-2">Puzzle / Game</h3>
            <p className="text-sm leading-relaxed text-yellow-200/80 whitespace-pre-line">{plainGameText}</p>
          </div>
        );
      }
      return null;
    }

    const { type, instructions, content, ...rest } = parsedGame;
    // Game props may be at top level (flat) or inside `content` (nested API format)
    const props = (content && typeof content === 'object' ? content : rest) as Record<string, unknown>;

    return (
      <div className="space-y-3">
        {/* Game header */}
        <div className="flex items-center gap-2">
          <span className="text-lg">{GAME_ICONS[type] ?? '🧩'}</span>
          <h3 className="text-sm font-semibold text-amber-300">
            {GAME_LABELS[type] ?? 'Mini Challenge'}
          </h3>
          {gameCompleted && (
            <span className="ml-auto text-xs px-2 py-0.5 rounded-full bg-green-900/40 text-green-400 border border-green-700/40">
              Completed
            </span>
          )}
        </div>

        {/* Instructions */}
        {instructions && (
          <p className="text-sm text-gray-400 leading-relaxed">{instructions}</p>
        )}

        {/* Game component */}
        <Suspense fallback={<div className="text-gray-500 text-sm py-4">Loading game...</div>}>
          {type === 'predict_output' && (
            <PredictOutput
              code={(props.code as string) ?? ''}
              language={(props.language as string) ?? 'javascript'}
              options={(props.options as string[]) ?? []}
              correctIndex={(props.correctIndex as number) ?? 0}
              explanation={(props.explanation as string) ?? ''}
              onComplete={handleGameComplete}
            />
          )}
          {type === 'find_bug' && (
            <FindBug
              code={(props.code as string) ?? ''}
              language={(props.language as string) ?? 'javascript'}
              bugLineIndex={(props.bugLineIndex as number) ?? 0}
              explanation={(props.explanation as string) ?? ''}
              onComplete={handleGameComplete}
            />
          )}
          {type === 'fill_blank' && (
            <FillBlank
              template={(props.template as string) ?? ''}
              blanks={(props.blanks as { id: string; answer: string; hint?: string }[]) ?? []}
              explanation={(props.explanation as string) ?? ''}
              onComplete={handleGameComplete}
            />
          )}
          {type === 'code_order' && (
            <CodeOrder
              lines={(props.lines as string[]) ?? []}
              explanation={(props.explanation as string) ?? ''}
              onComplete={handleGameComplete}
            />
          )}
        </Suspense>
      </div>
    );
  };

  return (
    <article
      className={`
        w-full rounded-xl border p-5 sm:p-6
        bg-gray-900 text-gray-300 transition-all duration-200
        ${completed ? 'border-accent-600/40' : 'border-gray-800'}
      `}
    >
      {/* ── Header: title + completion badge + collapse toggle ── */}
      <div className="flex items-center justify-between gap-3">
        <div className="flex items-center gap-2 min-w-0">
          {completed && (
            <span className="flex-shrink-0 text-accent-400 text-lg" aria-label="Completed">&#10003;</span>
          )}
          <h2 className="text-lg sm:text-xl font-bold text-gray-100 truncate">{title}</h2>
        </div>
        <button
          type="button"
          onClick={toggleExpanded}
          className="flex-shrink-0 text-gray-500 hover:text-gray-300 transition-colors p-1"
          aria-expanded={isExpanded}
          aria-label={isExpanded ? 'Collapse section' : 'Expand section'}
        >
          <svg
            className={`w-5 h-5 transition-transform duration-200 ${isExpanded ? 'rotate-180' : ''}`}
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={2}
          >
            <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
      </div>

      {/* ── Collapsible body ── */}
      {isExpanded && (
        <div className="mt-4 space-y-5">
          {/* Explanation */}
          <section>
            <p className="text-sm sm:text-base leading-relaxed text-gray-400 whitespace-pre-line">
              {explanation}
            </p>
          </section>

          {/* Code block */}
          {code && (
            <section>
              <h3 className="sr-only">Code Example</h3>
              <div className="rounded-lg overflow-hidden border border-gray-800">
                <pre className="bg-gray-950 p-4 overflow-x-auto text-sm leading-relaxed">
                  <code className="text-gray-200 font-mono">{code}</code>
                </pre>
              </div>
            </section>
          )}

          {/* Game / puzzle */}
          {(parsedGame || plainGameText) && (
            <section className="rounded-lg border border-amber-700/40 bg-amber-900/10 p-4 sm:p-5">
              {renderGame()}
            </section>
          )}

          {/* Quiz */}
          {quiz && (
            <section>
              <div className="rounded-lg border border-gray-800 bg-gray-900/80 p-4 sm:p-5">
                <h3 className="text-sm font-semibold text-gray-200 mb-3">Quiz</h3>
                <p className="text-sm text-gray-300 mb-4">{quiz.question}</p>

                <ul className="space-y-2">
                  {quiz.options.map((option, i) => {
                    let optionClasses =
                      'w-full text-left rounded-lg border px-4 py-2.5 text-sm transition-colors ';

                    if (isAnswered) {
                      if (i === quiz.correctIndex) {
                        optionClasses += 'border-accent-500 bg-accent-900/30 text-accent-300';
                      } else if (i === selectedOption) {
                        optionClasses += 'border-red-500 bg-red-900/30 text-red-300';
                      } else {
                        optionClasses += 'border-gray-800 bg-gray-900 text-gray-600';
                      }
                    } else {
                      optionClasses +=
                        'border-gray-700 bg-gray-800/50 text-gray-300 hover:border-primary-500 hover:bg-primary-900/20 cursor-pointer';
                    }

                    return (
                      <li key={i}>
                        <button
                          type="button"
                          disabled={isAnswered}
                          onClick={() => handleAnswer(i)}
                          className={optionClasses}
                        >
                          <span className="font-mono mr-2 text-gray-500">
                            {String.fromCharCode(65 + i)}.
                          </span>
                          {option}
                        </button>
                      </li>
                    );
                  })}
                </ul>

                {isAnswered && (
                  <div
                    className={`mt-4 p-3 rounded-lg text-sm leading-relaxed ${
                      selectedOption === quiz.correctIndex
                        ? 'bg-accent-900/20 text-accent-300 border border-accent-800/30'
                        : 'bg-red-900/20 text-red-300 border border-red-800/30'
                    }`}
                  >
                    <span className="font-semibold mr-1">
                      {selectedOption === quiz.correctIndex ? 'Correct!' : 'Incorrect.'}
                    </span>
                    {quiz.explanation}
                  </div>
                )}
              </div>
            </section>
          )}
        </div>
      )}
    </article>
  );
}
