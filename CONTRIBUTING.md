# Contributing to minimum-code

Thanks for your interest in contributing! Here's how to get started.

## Quick Setup

```bash
git clone https://github.com/oooooowoooooo/minimum-code.git
cd minimum-code

# Backend
cd web/backend
pip install -r requirements.txt

# Frontend
cd ../../web
npm install
```

## How to Contribute

### Adding an Engineering Lab

1. Create a new directory under `labs/your-lab-name/`
2. Include:
   - `starter.py` — skeleton code with TODOs
   - `solution.py` — reference implementation
   - `test_solution.py` — pytest tests with acceptance criteria
   - `README.md` — what the lab teaches and why it matters
3. Add the lab definition to `web/backend/data/labs.json`
4. Run tests: `cd labs/your-lab-name && pytest test_solution.py -v`
5. Submit a PR

### Adding a Competency Track Skill

1. Edit `web/backend/data/competency_map.json`
2. Follow the existing format:
```json
{
  "id": "your-skill-id",
  "title": "Skill Title",
  "title_zh": "技能标题",
  "why": "Why this skill matters for AI app engineering",
  "why_zh": "为什么这项技能对 AI 应用工程很重要",
  "minimum_code": "Short code snippet showing the concept",
  "lab_id": "linked-lab-id"
}
```
3. Submit a PR

### Adding Assessment Questions

1. Edit `web/backend/data/rubrics.json`
2. Each question should have 4 options with scores 0-3
3. Questions should test practical engineering knowledge, not syntax trivia
4. Submit a PR

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

# Individual lab
cd labs/config-loader && pytest test_solution.py -v

# Full verification
python verify_all.py
```

All tests must pass before merging.

## Reporting Issues

- Use the issue templates
- Include steps to reproduce
- Include your OS, Python version, Node.js version

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
