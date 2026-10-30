"""Seed Oscar's persistent-memory store from seed.jsonl (Juno's side).

Run once at deploy time (and re-runnable: the writer reconciles, so a
fact that is already stored gets matched instead of blindly duplicated -
but do not re-seed casually; check memory_list first).

    python seed_memories.py [path-to-seed.jsonl]
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _memenv import make_client  # noqa: E402


def main() -> int:
    seed_path = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else Path(__file__).resolve().parent / "seed.jsonl"
    )
    client, cfg = make_client()
    n = 0
    for line in seed_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        row = json.loads(line)
        client.add(
            row["text"],
            user_id=cfg["user_id"],
            source=row.get("source", "juno"),
        )
        n += 1
        print(f"seeded {n}: {row['text'][:70]}...")
    print(f"SEED DONE: {n} facts -> {cfg['dir']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
