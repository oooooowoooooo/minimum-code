"""
Auto-generate structured game data for ALL knowledge points.
Reads knowledge_points.json, converts plain-text games to structured JSON.
"""

import json
import random
import hashlib
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "knowledge_points.json"


def deterministic_seed(title: str) -> int:
    return int(hashlib.md5(title.encode()).hexdigest()[:8], 16)


def make_predict_output(code: str, title: str) -> dict:
    lines = [l for l in code.strip().split('\n') if l.strip() and not l.strip().startswith('#')]
    last_print = None
    for l in reversed(lines):
        if 'print' in l:
            last_print = l.strip()
            break
    if not last_print:
        last_print = lines[-1].strip() if lines else "pass"

    wrong_opts = [
        f"# {title} 相关错误",
        "TypeError",
        "None",
        "SyntaxError",
    ]
    correct = f"正确执行: {last_print}"

    return {
        "type": "predict_output",
        "title": "预测输出",
        "instructions": "这段代码会输出什么？",
        "content": {
            "code": code,
            "options": [correct, wrong_opts[0], wrong_opts[1], wrong_opts[2]],
            "correct": 0,
            "explanation": f"运行代码会执行 {last_print}"
        }
    }


def make_find_bug(code: str, title: str) -> dict:
    lines = code.strip().split('\n')
    code_lines = [l for l in lines if l.strip()]
    if len(code_lines) < 2:
        code_lines = [f"# {title}", "print('hello')", "print('bug here')"]

    bug_idx = len(code_lines) // 2
    buggy_lines = code_lines.copy()
    original = buggy_lines[bug_idx]
    if '=' in original:
        buggy_lines[bug_idx] = original.replace('=', '==', 1)
    elif '+' in original:
        buggy_lines[bug_idx] = original.replace('+', '-', 1)
    else:
        buggy_lines[bug_idx] = '# ' + original

    return {
        "type": "find_bug",
        "title": "找Bug",
        "instructions": "找出代码中的错误",
        "content": {
            "code_lines": buggy_lines,
            "bug_line": bug_idx,
            "explanation": f"第 {bug_idx + 1} 行有错误，原始代码应该是: {original.strip()}"
        }
    }


def make_fill_blank(code: str, title: str) -> dict:
    lines = code.strip().split('\n')
    if len(lines) < 2:
        lines = [f"# {title}", "x = 1", "print(x)"]

    blank_idx = min(1, len(lines) - 1)
    original_line = lines[blank_idx]

    parts = original_line.split('=', 1)
    if len(parts) == 2:
        answer = parts[1].strip()
        blank_line = parts[0] + '= ___'
    else:
        words = original_line.split()
        answer = words[-1] if words else '???'
        blank_line = ' '.join(words[:-1]) + ' ___'

    lines[blank_idx] = blank_line

    return {
        "type": "fill_blank",
        "title": "填空题",
        "instructions": "填写缺失的代码",
        "content": {
            "code": '\n'.join(lines),
            "blanks": [{"position": 0, "answer": answer, "options": [answer, "0", "None", "True"]}],
            "explanation": f"空白处应该填 {answer}"
        }
    }


def make_code_order(code: str, title: str) -> dict:
    lines = [l for l in code.strip().split('\n') if l.strip()]
    if len(lines) < 3:
        lines = [f"# {title}", "x = 1", "print(x)", "# 完成"]

    import random as _r
    _r.seed(deterministic_seed(title))
    indices = list(range(len(lines)))
    shuffled = indices[:]
    _r.shuffle(shuffled)
    while shuffled == indices:
        _r.shuffle(shuffled)

    shuffled_lines = [lines[i] for i in shuffled]
    correct_order = [shuffled.index(i) for i in range(len(lines))]

    return {
        "type": "code_order",
        "title": "代码排序",
        "instructions": "把代码行排列成正确顺序",
        "content": {
            "lines": shuffled_lines,
            "correct_order": correct_order,
            "explanation": f"正确顺序应该是原始代码的顺序"
        }
    }


GAME_TYPES = [make_predict_output, make_find_bug, make_fill_blank, make_code_order]


def enhance():
    data = json.loads(DATA_PATH.read_text(encoding='utf-8'))
    points = data['points']
    random.seed(42)

    for i, p in enumerate(points):
        title = p.get('title', '')
        code = p.get('code', 'print("hello")')
        game_type = GAME_TYPES[i % 4]

        if isinstance(p.get('game'), dict) and 'type' in p['game']:
            continue

        p['game'] = game_type(code, title)

    DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Enhanced {len(points)} knowledge points with structured games")

    type_counts = {}
    for p in points:
        g = p.get('game', {})
        if isinstance(g, dict) and 'type' in g:
            t = g['type']
            type_counts[t] = type_counts.get(t, 0) + 1
    print(f"Game type distribution: {type_counts}")


if __name__ == '__main__':
    enhance()
