---
id: REQ-007
title: "Step 2.4: Split into train/eval"
status: pending
created_at: 2026-03-09T12:05:00Z
user_request: UR-002
related: [REQ-004, REQ-005, REQ-006]
batch: ml-training-phase-2
source_step: "2.4"
source_doc: docs/TODO.md
blueprint_ref: docs/BLUEPRINT.md
model_hint: "Claude Code"
---

# Step 2.4: Split into Train/Eval

## What

Split the approved dataset into training and evaluation sets.

## Requirements

- Create scripts/split_dataset.py
- Split 80/20 with seed 42
- Write data/train.jsonl and data/valid.jsonl

## Verification

- Combined count matches full dataset, no duplicates

## Blueprint Context

Add a split function to the dataset pipeline and create train/eval files.

Steps:
1. Create scripts/split_dataset.py that:
   - Reads data/full_dataset.jsonl
   - Shuffles with a fixed random seed (42) for reproducibility
   - Splits 80/20 into train and eval (stratified by category if categories are tagged)
   - Writes data/train.jsonl and data/eval.jsonl
   - Prints counts for each split
2. Run the split

Context: The 80/20 split gives us ~160-400 training examples and ~40-100 evaluation examples.

Test: data/train.jsonl and data/eval.jsonl exist. Combined count equals full_dataset.jsonl count. No duplicates across splits.

## Specification Reference

This step is part of the Hardware Diagnostics LLM Fine-Tuning project. See docs/SPECIFICATION.md for full project context, goals, and constraints.

## Builder Guidance

- Certainty level: Firm (this is a planned, documented step)
- The TODO label suggests: Claude Code
- Follow the Blueprint's instructions closely; they contain tested approaches

## Context

See [user-requests/UR-002/input.md](./user-requests/UR-002/input.md) for the full TODO document.

---
*Source: Ingested from docs/TODO.md, step 2.4*
