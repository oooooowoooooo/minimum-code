# -*- coding: utf-8 -*-
"""Load supplementary knowledge points from JSON and merge into knowledge_points.json"""
import json
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "knowledge_points.json"
SUPPLEMENT_PATH = Path(__file__).parent / "data" / "kp_supplement.json"


def main():
    data = json.loads(DATA_PATH.read_text(encoding='utf-8'))
    supplement = json.loads(SUPPLEMENT_PATH.read_text(encoding='utf-8'))
    existing_titles = {p['title'] for p in data['points']}
    added = 0
    for point in supplement:
        if point['title'] not in existing_titles:
            data['points'].append(point)
            existing_titles.add(point['title'])
            added += 1
    DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Added {added} supplementary points. Total: {len(data['points'])}")


if __name__ == '__main__':
    main()
