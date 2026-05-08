# Contributing to minimum-code

Thanks for your interest in contributing! Here's how to get started.

## Quick Setup

```bash
git clone https://github.com/your-username/minimum-code.git
cd minimum-code

# Backend
cd web/backend
pip install fastapi uvicorn pytest httpx

# Frontend
cd ../../web
npm install
```

## How to Contribute

### Adding a Knowledge Point

1. Edit `web/backend/data/knowledge_points.json`
2. Follow the existing format:
```json
{
  "week": 1,
  "module": "py-variables",
  "title": "Your Point Title",
  "explanation": "Clear explanation in plain language.",
  "code": "# Example code",
  "game": {
    "type": "predict_output",
    "title": "Game Title",
    "instructions": "What to do",
    "content": {
      "code": "print('hello')",
      "options": ["hello", "world", "error", "None"],
      "correct": 0,
      "explanation": "print outputs the string"
    }
  },
  "quiz": {
    "question": "What does this print?",
    "options": ["A", "B", "C", "D"],
    "correct": 0,
    "explanation": "Because..."
  }
}
```
3. Run `python verify_all.py` to validate
4. Submit a PR

### Game Types

| Type | Content Fields |
|------|---------------|
| `predict_output` | `code`, `options`, `correct`, `explanation` |
| `find_bug` | `code_lines`, `bug_line`, `explanation` |
| `fill_blank` | `code` (with `___` markers), `blanks`, `explanation` |
| `code_order` | `lines`, `correct_order`, `explanation` |

### Fixing a Bug

1. Open an issue first (optional but appreciated)
2. Fork the repo
3. Create a branch: `git checkout -b fix/your-fix`
4. Make your changes
5. Run tests: `cd web && npm test && cd backend && python -m pytest`
6. Submit a PR

### Adding a New Feature

1. Open an issue to discuss the feature
2. Fork the repo
3. Create a branch: `git checkout -b feature/your-feature`
4. Implement + test
5. Submit a PR

## Code Style

- **TypeScript**: Strict mode, no `any` unless unavoidable
- **Python**: Type hints, f-strings, pathlib over os.path
- **Commits**: Conventional commits (`feat:`, `fix:`, `docs:`, `test:`)

## Testing

```bash
# Frontend
cd web && npm test

# Backend
cd web/backend && python -m pytest -v

# Data integrity
cd web/backend && python verify_all.py
```

All tests must pass before merging.

## Reporting Issues

- Use the issue templates
- Include steps to reproduce
- Include your OS, Python version, Node.js version

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
