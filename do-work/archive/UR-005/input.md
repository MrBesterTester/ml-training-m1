---
id: UR-005
title: FD/FI dataset review script for v2-fdfi step 4.1
created_at: 2026-03-12T12:00:00Z
requests: [REQ-018]
word_count: 103
---

# FD/FI Dataset Review Script

## Full Verbatim Input

Create a custom Python review script (scripts/review_fdfi_dataset.py) for v2-fdfi TODO step 4.1 "Review & approve augmented dataset". The script should: (1) Generate a review summary — counts by category (FD, FI, FD+FI, TRIAGE), counts by hardware domain, average response length, and print sample entries from each category. (2) Flag entries needing special attention — complex physics reasoning, judgment calls, triage entries where the non-hardware determination is subtle. (3) Output a formatted review report to results/fdfi_review_summary.md with all the stats, flagged entries, and samples. The data files are in data/fdfi_fd_entries.jsonl, data/fdfi_fi_entries.jsonl, data/fdfi_combined_entries.jsonl, data/fdfi_triage_entries.jsonl, and the merged data/full_dataset.jsonl. Use a custom program — not just a simple counter, but something that helps Sam actually evaluate quality.

---
*Captured: 2026-03-12T12:00:00Z*
