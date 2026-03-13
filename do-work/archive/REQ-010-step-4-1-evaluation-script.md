---
id: REQ-010
title: "Step 4.1: Create evaluation script & generate comparisons"
status: pending
created_at: 2026-03-09T12:05:00Z
user_request: UR-002
related: [REQ-011]
batch: ml-training-phase-4
source_step: "4.1"
source_doc: docs/TODO.md
blueprint_ref: docs/BLUEPRINT.md
model_hint: "Claude Code"
---

# Step 4.1: Create Evaluation Script & Generate Comparisons

## What

Build a script that runs the same prompts through both base and fine-tuned models and generates a comparison document. This is the portfolio centerpiece.

## Requirements

- Create scripts/evaluate.py
- Select 10-15 diverse prompts from eval set
- Run both base and fine-tuned model on each
- Write results/comparison.md with side-by-side output

## Verification

- results/comparison.md has 10-15 formatted comparison entries

## Blueprint Context

Create scripts/evaluate.py that generates side-by-side comparisons.

Steps:
1. Create scripts/evaluate.py that:
   - Loads 10-15 prompts from data/eval.jsonl (sample diverse topics)
   - For each prompt, runs inference on:
     a. Base model (no adapter)
     b. Fine-tuned model (with adapter)
   - Captures both responses
   - Writes results/comparison.md with formatted sections:
     - Prompt
     - Base model response
     - Fine-tuned response
     - (Optional) Ground truth from the dataset
   - Prints a summary to stdout
2. Run the evaluation script

Context: This is the portfolio centerpiece — the side-by-side comparison that proves the fine-tuning worked. We want 10-15 diverse prompts from the eval set, with both base and fine-tuned responses captured.

Test: results/comparison.md exists and contains 10-15 comparison entries. Visually inspect: the fine-tuned responses should be noticeably more specific and domain-appropriate.

## Specification Reference

This step is part of the Hardware Diagnostics LLM Fine-Tuning project. See docs/SPECIFICATION.md for full project context, goals, and constraints.

## Builder Guidance

- Certainty level: Firm (this is a planned, documented step)
- The TODO label suggests: Claude Code
- Follow the Blueprint's instructions closely; they contain tested approaches

## Context

See [user-requests/UR-002/input.md](./user-requests/UR-002/input.md) for the full TODO document.

---
*Source: Ingested from docs/TODO.md, step 4.1*
