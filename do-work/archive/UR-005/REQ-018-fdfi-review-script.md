---
id: REQ-018
title: FD/FI dataset review script
status: completed
claimed_at: 2026-03-12T12:05:00Z
completed_at: 2026-03-12T12:15:00Z
route: B
created_at: 2026-03-12T12:00:00Z
user_request: UR-005
source_step: "v2-fdfi 4.1"
---

# FD/FI Dataset Review Script

## What

Create `scripts/review_fdfi_dataset.py` — a custom Python review program for v2-fdfi TODO step 4.1 ("Review & approve augmented dataset"). This script helps Sam evaluate the quality of the augmented FD/FI dataset before approving it for training.

## Requirements

- **Review summary stats:** counts by category (FD, FI, FD+FI, TRIAGE), counts by hardware domain, average response length per category, and sample entries from each category
- **Flag entries needing attention:** complex physics reasoning, judgment calls, triage entries where the non-hardware determination is subtle
- **Output:** formatted review report to `results/fdfi_review_summary.md` with all stats, flagged entries, and samples
- **Data sources:** `data/fdfi_fd_entries.jsonl`, `data/fdfi_fi_entries.jsonl`, `data/fdfi_combined_entries.jsonl`, `data/fdfi_triage_entries.jsonl`, and merged `data/full_dataset.jsonl`
- **Quality tool, not just a counter:** must help Sam actually evaluate quality — surface interesting/questionable entries, not just aggregate numbers

## Context

This is the review gate for the v2-fdfi augmentation cycle. Sam needs to review and approve the 133 FD/FI entries before they go into training. The script should make that review efficient and thorough.

---
*Source: Create a custom Python review script for v2-fdfi TODO step 4.1*

## Verification

**Source**: UR-005/input.md
**Pre-fix coverage**: 100% (13/13 items)

### Coverage Map

| # | Item | REQ Section | Status |
|---|------|-------------|--------|
| 1 | Create scripts/review_fdfi_dataset.py | What | Full |
| 2 | For v2-fdfi TODO step 4.1 | What | Full |
| 3 | Counts by category (FD, FI, FD+FI, TRIAGE) | Requirements | Full |
| 4 | Counts by hardware domain | Requirements | Full |
| 5 | Average response length | Requirements | Full |
| 6 | Sample entries from each category | Requirements | Full |
| 7 | Flag complex physics reasoning | Requirements | Full |
| 8 | Flag judgment calls | Requirements | Full |
| 9 | Flag subtle triage non-hardware determinations | Requirements | Full |
| 10 | Output to results/fdfi_review_summary.md | Requirements | Full |
| 11 | Stats, flagged entries, and samples in report | Requirements | Full |
| 12 | Data sources: four JSONL files + full_dataset.jsonl | Requirements | Full |
| 13 | Custom quality tool, not just a counter | Requirements | Full |

*Verified by verify-request action*

## Triage

**Route:** B (Medium) — new script, clear requirements, needs exploration of data format

## Plan

1. Create `scripts/review_fdfi_dataset.py` that reads all 4 staging JSONL files + full_dataset.jsonl
2. Compute stats: entry counts by category (file-based), domain detection via keyword matching against known 8 domains from taxonomy, avg response length per category
3. Flag entries: identify entries with long/complex physics chains, triage entries with subtle determinations, entries with judgment calls — use heuristics like response length, keyword density (physics terms, hedging language)
4. Sample entries: select 2-3 representative entries per category for human review
5. Output formatted `results/fdfi_review_summary.md` with: overview stats table, domain breakdown, flagged entries with excerpts, sample entries
6. Run script and verify output

## Implementation Summary

- Created `scripts/review_fdfi_dataset.py` (standard library only)
- Script reads all 4 FD/FI staging JSONL files, infers domains via keyword matching
- Three flagging dimensions: complex physics (top 10% by length), judgment calls (hedging language), subtle triage
- 2 random sample entries per category (seed=42) for direct reading
- Output: `results/fdfi_review_summary.md` (652 lines)

## Testing

- Script runs successfully: `python scripts/review_fdfi_dataset.py`
- Counts: FD=40, FI=40, FD+FI=28, TRIAGE=25 (133 total) — matches expected
- Domain detection: 130/133 classified, 3 unclassified
- Flagged: 13 complex physics, 47 judgment calls, 12 subtle triage
- Report output verified: stats tables, flagged entries with excerpts, full sample entries
