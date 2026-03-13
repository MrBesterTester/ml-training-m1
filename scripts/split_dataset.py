"""Split full_dataset.jsonl into train.jsonl and valid.jsonl (80/20, seed 42).

Verifies that both splits contain FD/FI-style entries by checking for
diagnostic keywords in the instructions.
"""

import json
import random
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

MAIN_DATASET = DATA_DIR / "full_dataset.jsonl"
TRAIN_FILE = DATA_DIR / "train.jsonl"
VALID_FILE = DATA_DIR / "valid.jsonl"

SEED = 42
TRAIN_RATIO = 0.80

# Keywords that suggest an entry is FD/FI-style rather than encyclopedic
FDFI_KEYWORDS = [
    "anomal", "fault", "diagnos", "triage", "root cause", "isolat",
    "failure mode", "out-of-spec", "deviation", "drift",
    "measurement data", "test result", "reading",
]


def is_fdfi_style(entry: dict) -> bool:
    text = (entry["instruction"] + " " + entry["output"]).lower()
    return any(kw in text for kw in FDFI_KEYWORDS)


def write_jsonl(path: Path, entries: list[dict]):
    with open(path, "w") as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main():
    # Load
    print(f"Reading {MAIN_DATASET.name}...")
    with open(MAIN_DATASET) as f:
        entries = [json.loads(line) for line in f if line.strip()]
    print(f"  {len(entries)} total entries")

    # Shuffle and split
    random.seed(SEED)
    random.shuffle(entries)
    split_idx = int(len(entries) * TRAIN_RATIO)
    train = entries[:split_idx]
    valid = entries[split_idx:]

    # Write
    write_jsonl(TRAIN_FILE, train)
    write_jsonl(VALID_FILE, valid)

    # Verify FD/FI presence in both splits
    train_fdfi = sum(1 for e in train if is_fdfi_style(e))
    valid_fdfi = sum(1 for e in valid if is_fdfi_style(e))

    # Summary
    print(f"\n=== Split Summary ===")
    print(f"  Train: {len(train)} entries ({train_fdfi} FD/FI-style)")
    print(f"  Valid: {len(valid)} entries ({valid_fdfi} FD/FI-style)")
    print(f"  Total: {len(train) + len(valid)}")
    print(f"  Ratio: {len(train)/len(entries)*100:.1f}% / {len(valid)/len(entries)*100:.1f}%")

    if train_fdfi == 0 or valid_fdfi == 0:
        print("  WARNING: One split has zero FD/FI entries!")
    else:
        print("  Both splits contain FD/FI entries ✓")


if __name__ == "__main__":
    main()
