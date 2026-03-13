"""Merge FD/FI staging files into the main dataset.

Reads data/full_dataset.jsonl (existing encyclopedic entries) and the four
FD/FI staging files, validates all entries, checks for duplicate instructions,
and writes the combined dataset back to full_dataset.jsonl.
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

MAIN_DATASET = DATA_DIR / "full_dataset.jsonl"
STAGING_FILES = {
    "FD": DATA_DIR / "fdfi_fd_entries.jsonl",
    "FI": DATA_DIR / "fdfi_fi_entries.jsonl",
    "FD+FI": DATA_DIR / "fdfi_combined_entries.jsonl",
    "TRIAGE": DATA_DIR / "fdfi_triage_entries.jsonl",
}
REQUIRED_KEYS = {"instruction", "input", "output"}


def load_jsonl(path: Path) -> list[dict]:
    entries = []
    with open(path) as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"  ERROR: {path.name} line {i}: invalid JSON — {e}")
                sys.exit(1)
            missing = REQUIRED_KEYS - set(entry.keys())
            if missing:
                print(f"  ERROR: {path.name} line {i}: missing keys {missing}")
                sys.exit(1)
            entries.append(entry)
    return entries


def main():
    # Load existing dataset
    print(f"Reading {MAIN_DATASET.name}...")
    existing = load_jsonl(MAIN_DATASET)
    print(f"  {len(existing)} existing entries")

    # Load staging files
    new_entries = {}
    total_new = 0
    for category, path in STAGING_FILES.items():
        if not path.exists():
            print(f"  WARNING: {path.name} not found — skipping")
            continue
        entries = load_jsonl(path)
        new_entries[category] = entries
        total_new += len(entries)
        print(f"  {category}: {len(entries)} entries from {path.name}")

    # Check for duplicate instructions
    print("\nChecking for duplicates...")
    all_instructions = [e["instruction"] for e in existing]
    for category, entries in new_entries.items():
        for e in entries:
            all_instructions.append(e["instruction"])

    seen = set()
    duplicates = []
    for inst in all_instructions:
        if inst in seen:
            duplicates.append(inst[:80])
        seen.add(inst)

    if duplicates:
        print(f"  WARNING: {len(duplicates)} duplicate instruction(s) found:")
        for d in duplicates[:5]:
            print(f"    - {d}...")
        print("  Continuing anyway (duplicates kept).")
    else:
        print("  No duplicates found.")

    # Merge: append new entries to existing
    combined = list(existing)
    for category, entries in new_entries.items():
        combined.extend(entries)

    # Write combined dataset
    print(f"\nWriting {len(combined)} entries to {MAIN_DATASET.name}...")
    with open(MAIN_DATASET, "w") as f:
        for entry in combined:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # Summary
    print("\n=== Merge Summary ===")
    print(f"  Original entries:  {len(existing)}")
    for category, entries in new_entries.items():
        print(f"  + {category:10s}         {len(entries)}")
    print(f"  {'—' * 30}")
    print(f"  Total:             {len(combined)}")
    target_low, target_high = 350, 450
    in_range = target_low <= len(combined) <= target_high
    print(f"  Target range:      {target_low}–{target_high} {'✓' if in_range else '✗ OUT OF RANGE'}")


if __name__ == "__main__":
    main()
