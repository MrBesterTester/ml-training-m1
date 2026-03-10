---
id: REQ-012
title: "Step 5.1: End-to-end verification & cleanup"
status: pending
created_at: 2026-03-09T12:05:00Z
user_request: UR-002
batch: ml-training-phase-5
source_step: "5.1"
source_doc: docs/TODO.md
blueprint_ref: docs/BLUEPRINT.md
model_hint: "Claude Code"
---

# Step 5.1: End-to-End Verification & Cleanup

## What

Run through the entire pipeline to confirm reproducibility, clean up the repo, and prepare for final commit.

## Requirements

- Remove scratch files, temp outputs, unused code
- Verify pipeline sequence runs (scripts exist and work)
- Confirm no secrets/tokens committed
- Confirm models/ and .venv/ are gitignored
- Final commit

## Verification

- Clean git status, no large binaries tracked

## Blueprint Context

Verify the complete pipeline works.

Steps:
1. Review all files in the repo — remove any scratch files, temp outputs, or unused code
2. Verify the pipeline sequence:
   a. pip install -r requirements.txt (works)
   b. Model download/convert (command documented, not re-run)
   c. python scripts/generate_dataset.py (produces data/full_dataset.jsonl)
   d. python scripts/split_dataset.py (produces train/eval splits)
   e. Training command (documented, adapter weights present)
   f. python scripts/evaluate.py (produces results/comparison.md)
3. Ensure no secrets, API keys, or tokens are committed
4. Ensure models/ and .venv/ are gitignored
5. Final git status — stage and commit all project files

Context: Before calling it done, verify that a fresh start (after model download) produces working results.

Test: git status shows a clean working tree after commit. No large binary files (models, venv) are tracked.

## Specification Reference

This step is part of the Hardware Diagnostics LLM Fine-Tuning project. See docs/SPECIFICATION.md for full project context, goals, and constraints.

## Builder Guidance

- Certainty level: Firm (this is a planned, documented step)
- The TODO label suggests: Claude Code
- Follow the Blueprint's instructions closely; they contain tested approaches

## Context

See [user-requests/UR-002/input.md](./user-requests/UR-002/input.md) for the full TODO document.

---
*Source: Ingested from docs/TODO.md, step 5.1*
