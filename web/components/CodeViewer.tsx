'use client';

import { useState, useCallback } from 'react';

interface CodeViewerProps {
  code: string;
  language: string;
  filePath?: string;
}

const LANGUAGE_LABELS: Record<string, string> = {
  python: 'Python',
  typescript: 'TypeScript',
  tsx: 'TSX',
  javascript: 'JavaScript',
  jsx: 'JSX',
  json: 'JSON',
  yaml: 'YAML',
  bash: 'Bash',
  md: 'Markdown',
  html: 'HTML',
  css: 'CSS',
  rust: 'Rust',
  go: 'Go',
};

function highlightLine(line: string, language: string): React.ReactNode {
  // Simple CSS-based syntax highlighting using the classes from globals.css
  const patterns: { regex: RegExp; className: string }[] = [
    // Comments
    { regex: /(\/\/.*$|#.*$)/gm, className: 'code-comment' },
    // Strings (double and single quoted)
    { regex: /("[^"\\]*(?:\\.[^"\\]*)*"|'[^'\\]*(?:\\.[^'\\]*)*'|`[^`\\]*(?:\\.[^`\\]*)*`)/g, className: 'code-string' },
    // Numbers
    { regex: /\b(\d+\.?\d*)\b/g, className: 'code-number' },
    // Keywords
    {
      regex: /\b(function|const|let|var|return|if|else|for|while|class|import|export|from|async|await|try|catch|throw|new|this|extends|implements|interface|type|enum|def|self|yield|with|as|in|not|and|or|is|True|False|None|true|false|null|undefined|void|readonly|public|private|protected|static|abstract|override|super|typeof|instanceof|keyof|infer|declare|namespace|module|require)\b/g,
      className: 'code-keyword',
    },
    // Types (capitalized words that aren't at line start)
    { regex: /\b([A-Z][a-zA-Z0-9]+)\b/g, className: 'code-type' },
    // Function calls
    { regex: /\b([a-z_][a-zA-Z0-9_]*)\s*\(/g, className: 'code-function' },
  ];

  // Apply patterns sequentially, wrapping matches
  let segments: React.ReactNode[] = [];
  let remaining = line;
  let key = 0;

  // Simple approach: split by first matching pattern
  const processSegment = (text: string, depth: number): React.ReactNode[] => {
    if (depth >= patterns.length || text.length === 0) {
      return [<span key={`s-${key++}`}>{text}</span>];
    }

    const { regex, className } = patterns[depth];
    regex.lastIndex = 0;
    const result: React.ReactNode[] = [];
    let lastIndex = 0;
    let match: RegExpExecArray | null;

    while ((match = regex.exec(text)) !== null) {
      if (match.index > lastIndex) {
        result.push(...processSegment(text.slice(lastIndex, match.index), depth + 1));
      }
      result.push(
        <span key={`h-${key++}`} className={className}>
          {match[1] || match[0]}
        </span>,
      );
      lastIndex = match.index + match[0].length;
    }

    if (lastIndex < text.length) {
      result.push(...processSegment(text.slice(lastIndex), depth + 1));
    }

    return result.length > 0 ? result : [<span key={`s-${key++}`}>{text}</span>];
  };

  return <>{processSegment(line, 0)}</>;
}

export default function CodeViewer({ code, language, filePath }: CodeViewerProps) {
  const [copied, setCopied] = useState(false);

  const lines = code.split('\n');
  const langLabel = LANGUAGE_LABELS[language] || language.toUpperCase();

  const handleCopy = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback
      const ta = document.createElement('textarea');
      ta.value = code;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  }, [code]);

  return (
    <div className="rounded-xl border border-gray-800 overflow-hidden bg-[#1e1e1e]">
      {/* Header bar */}
      <div className="flex items-center justify-between px-4 py-2.5 bg-gray-900 border-b border-gray-800">
        <div className="flex items-center gap-3">
          {/* Traffic lights */}
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-full bg-red-500/70" />
            <span className="w-3 h-3 rounded-full bg-yellow-500/70" />
            <span className="w-3 h-3 rounded-full bg-green-500/70" />
          </div>

          {/* File path */}
          {filePath && (
            <span className="text-xs text-gray-500 font-mono">{filePath}</span>
          )}
        </div>

        <div className="flex items-center gap-3">
          {/* Language badge */}
          <span className="text-[10px] uppercase tracking-wider text-gray-500 bg-gray-800 px-2 py-0.5 rounded">
            {langLabel}
          </span>

          {/* Copy button */}
          <button
            onClick={handleCopy}
            className="flex items-center gap-1.5 text-xs text-gray-400 hover:text-white transition-colors px-2 py-1 rounded hover:bg-gray-800"
          >
            {copied ? (
              <>
                <CheckIcon />
                Copied
              </>
            ) : (
              <>
                <CopyIcon />
                Copy
              </>
            )}
          </button>
        </div>
      </div>

      {/* Code body */}
      <div className="overflow-x-auto">
        <pre className="p-0 m-0">
          <code className="block text-sm leading-relaxed">
            {lines.map((line, i) => (
              <div
                key={i}
                className="flex hover:bg-white/[0.03] transition-colors"
              >
                {/* Line number */}
                <span className="flex-shrink-0 w-12 text-right pr-4 text-gray-600 select-none text-xs leading-relaxed border-r border-gray-800/50">
                  {i + 1}
                </span>
                {/* Code */}
                <span className="pl-4 pr-4 flex-1 whitespace-pre">
                  {highlightLine(line, language)}
                </span>
              </div>
            ))}
          </code>
        </pre>
      </div>
    </div>
  );
}

// ─── Inline SVG icons (avoid external dependency) ───

function CopyIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
    </svg>
  );
}

function CheckIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="20 6 9 17 4 12" />
    </svg>
  );
}
