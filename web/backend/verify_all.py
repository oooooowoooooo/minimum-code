"""
统一验证脚本：检查 888+ 知识点、888+ 游戏、888+ 测试
"""

import json
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "knowledge_points.json"

def verify():
    if not DATA_PATH.exists():
        print("FAIL: knowledge_points.json not found")
        return False

    data = json.loads(DATA_PATH.read_text(encoding='utf-8'))
    points = data.get('points', [])

    print(f"=== 知识点验证报告 ===")
    print(f"总知识点数: {len(points)}")
    print(f"目标: >= 888")
    print()

    # 1. 检查数量
    if len(points) < 888:
        print(f"FAIL: 知识点数量 {len(points)} < 888")
    else:
        print(f"PASS: 知识点数量 {len(points)} >= 888")

    # 2. 检查每个知识点的必要字段
    required_fields = ['week', 'module', 'title', 'explanation', 'code', 'game', 'quiz']
    missing_fields = 0
    for i, p in enumerate(points):
        for f in required_fields:
            if f not in p:
                missing_fields += 1
                if missing_fields <= 5:
                    print(f"  WARN: Point {i} missing field '{f}'")

    if missing_fields == 0:
        print(f"PASS: 所有知识点都有必要字段")
    else:
        print(f"FAIL: {missing_fields} 个字段缺失")

    # 3. 检查游戏
    games_ok = 0
    games_missing = 0
    games_types = {}
    for i, p in enumerate(points):
        game = p.get('game')
        if isinstance(game, dict) and 'type' in game:
            games_ok += 1
            t = game['type']
            games_types[t] = games_types.get(t, 0) + 1
        else:
            games_missing += 1
            if games_missing <= 5:
                print(f"  WARN: Point {i} ('{p.get('title','')}') has no structured game")

    print(f"\n=== 游戏验证 ===")
    print(f"有效游戏数: {games_ok}")
    print(f"缺失游戏数: {games_missing}")
    print(f"游戏类型分布:")
    for t, c in sorted(games_types.items()):
        print(f"  {t}: {c}")

    if games_ok >= 888:
        print(f"PASS: 游戏数量 {games_ok} >= 888")
    else:
        print(f"FAIL: 游戏数量 {games_ok} < 888")

    # 4. 检查测验
    quiz_ok = 0
    quiz_missing = 0
    quiz_bad_options = 0
    for i, p in enumerate(points):
        quiz = p.get('quiz')
        if isinstance(quiz, dict) and 'question' in quiz and 'options' in quiz:
            quiz_ok += 1
            opts = quiz.get('options', [])
            if len(opts) != 4:
                quiz_bad_options += 1
        else:
            quiz_missing += 1

    print(f"\n=== 测验验证 ===")
    print(f"有效测验数: {quiz_ok}")
    print(f"缺失测验数: {quiz_missing}")
    print(f"选项数量错误: {quiz_bad_options}")

    if quiz_ok >= 888:
        print(f"PASS: 测验数量 {quiz_ok} >= 888")
    else:
        print(f"FAIL: 测验数量 {quiz_ok} < 888")

    # 5. 检查重复标题
    titles = [p.get('title', '') for p in points]
    unique_titles = set(titles)
    duplicates = len(titles) - len(unique_titles)
    print(f"\n=== 去重验证 ===")
    print(f"总标题数: {len(titles)}")
    print(f"唯一标题数: {len(unique_titles)}")
    print(f"重复数: {duplicates}")

    if duplicates == 0:
        print(f"PASS: 无重复知识点")
    else:
        print(f"FAIL: 有 {duplicates} 个重复知识点")
        # Show some duplicates
        from collections import Counter
        title_counts = Counter(titles)
        for title, count in title_counts.most_common(5):
            if count > 1:
                print(f"  '{title}' 出现 {count} 次")

    # 6. 按周统计
    print(f"\n=== 按周分布 ===")
    weeks = {}
    for p in points:
        w = p.get('week', 0)
        weeks[w] = weeks.get(w, 0) + 1
    for w in sorted(weeks.keys()):
        print(f"  Week {w}: {weeks[w]} 个知识点")

    # 7. 按模块统计
    print(f"\n=== 按模块分布 ===")
    modules = {}
    for p in points:
        m = p.get('module', 'unknown')
        modules[m] = modules.get(m, 0) + 1
    for m in sorted(modules.keys()):
        print(f"  {m}: {modules[m]} 个知识点")

    # 总结
    print(f"\n=== 总结 ===")
    all_pass = True
    if len(points) < 888:
        print(f"FAIL: 知识点不足 888")
        all_pass = False
    if games_ok < 888:
        print(f"FAIL: 游戏不足 888")
        all_pass = False
    if quiz_ok < 888:
        print(f"FAIL: 测验不足 888")
        all_pass = False
    if duplicates > 0:
        print(f"FAIL: 有重复知识点")
        all_pass = False

    if all_pass:
        print("ALL PASS!")
    else:
        print("SOME CHECKS FAILED")

    return all_pass


if __name__ == '__main__':
    verify()
