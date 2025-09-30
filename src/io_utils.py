import json
from pathlib import Path

def write_jsonl(path, items):
    path = Path(path)
    with path.open("w", encoding="utf8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

def append_jsonl(path, item):
    path = Path(path)
    with path.open("a", encoding="utf8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

def read_jsonl(path):
    path = Path(path)
    for line in path.open("r", encoding="utf8"):
        yield json.loads(line)
