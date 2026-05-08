"""
Merge knowledge points from multiple JSON files.

Reads knowledge_points.json (base) + weekly files (kp_weeks_*.json),
deduplicates by title, sorts by week then module, writes back.
"""

import json
from pathlib import Path
from collections import defaultdict

DATA_DIR = Path(__file__).parent / "data"
FILES = [
    DATA_DIR / "knowledge_points.json",
    DATA_DIR / "kp_weeks_1_3.json",
    DATA_DIR / "kp_weeks_4_6.json",
    DATA_DIR / "kp_weeks_7_9.json",
    DATA_DIR / "kp_weeks_10_12.json",
    DATA_DIR / "kp_week10.json",
    DATA_DIR / "kp_week11.json",
    DATA_DIR / "kp_week12.json",
]


def load_points(filepath: Path) -> list[dict]:
    """Load points list from a JSON file. Returns [] if file missing."""
    if not filepath.exists():
        print(f"  [SKIP] {filepath.name} not found")
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Handle both formats: {"points": [...]} or bare [...]
    if isinstance(data, list):
        points = data
    elif isinstance(data, dict) and "points" in data:
        points = data["points"]
    else:
        print(f"  [WARN] {filepath.name}: no 'points' key found, skipping")
        return []
    print(f"  [LOAD] {filepath.name}: {len(points)} points")
    return points


def merge_all():
    # 1. Load points from all files
    all_points: list[dict] = []
    for fpath in FILES:
        all_points.extend(load_points(fpath))

    print(f"\nTotal raw points loaded: {len(all_points)}")

    # 2. Deduplicate by title (keep first occurrence)
    seen_titles: set[str] = set()
    unique_points: list[dict] = []
    duplicates = 0
    for pt in all_points:
        title = pt.get("title", "")
        if title in seen_titles:
            duplicates += 1
            continue
        seen_titles.add(title)
        unique_points.append(pt)

    if duplicates:
        print(f"Duplicates removed: {duplicates}")
    print(f"Unique points: {len(unique_points)}")

    # 3. Sort by week, then by module
    unique_points.sort(key=lambda p: (p.get("week", 0), p.get("module", "")))

    # 4. Build by_week index
    by_week: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))
    for pt in unique_points:
        week_key = str(pt["week"])
        module_key = pt["module"]
        by_week[week_key][module_key].append(pt)

    # Convert defaultdict to plain dict for JSON serialization
    by_week_out = {
        w: dict(modules) for w, modules in sorted(by_week.items(), key=lambda x: int(x[0]))
    }

    # 5. Determine max week number
    max_week = max((pt.get("week", 0) for pt in unique_points), default=0)

    # 6. Build output
    output = {
        "total_points": len(unique_points),
        "weeks": max_week,
        "points": unique_points,
        "by_week": by_week_out,
    }

    # 7. Write back
    out_path = DATA_DIR / "knowledge_points.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {len(unique_points)} points -> {out_path.name}")

    # 8. Print statistics
    print("\n" + "=" * 50)
    print("STATISTICS")
    print("=" * 50)

    # Points per week
    print(f"\nTotal points: {len(unique_points)}")
    print(f"Total weeks:  {max_week}")
    print(f"\nPoints per week:")
    for week_num in sorted(by_week.keys(), key=int):
        week_total = sum(len(mods) for mods in by_week[week_num].values())
        mod_count = len(by_week[week_num])
        print(f"  Week {week_num:>2}: {week_total:>3} points, {mod_count} modules")

    # Points per module (across all weeks)
    module_counts: dict[str, int] = defaultdict(int)
    for pt in unique_points:
        module_counts[pt["module"]] += 1

    print(f"\nPoints per module ({len(module_counts)} modules):")
    for module, count in sorted(module_counts.items(), key=lambda x: -x[1]):
        print(f"  {module:<30} {count:>3}")


if __name__ == "__main__":
    merge_all()
