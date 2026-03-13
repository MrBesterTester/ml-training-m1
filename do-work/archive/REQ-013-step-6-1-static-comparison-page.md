---
id: REQ-013
title: "Step 6.1: Static comparison page"
status: pending
created_at: 2026-03-09T12:05:00Z
user_request: UR-002
related: [REQ-014]
batch: ml-training-phase-6
source_step: "6.1"
source_doc: docs/TODO.md
blueprint_ref: docs/BLUEPRINT.md
model_hint: "Claude Code"
---

# Step 6.1: Static Comparison Page

## What

Build a styled HTML page showing before/after results for portfolio use.

## Requirements

- Generate styled HTML from results/comparison.md
- Save as web/index.html

## Verification

- Page renders correctly in browser

## Blueprint Context

Create a static HTML comparison page from the evaluation results.

Steps:
1. Create a script or template that reads results/comparison.md and generates a styled HTML page
2. The page should show:
   - Project title and brief description
   - Technical details (model, method, hardware)
   - 10-15 side-by-side comparisons with base vs. fine-tuned responses
   - Visual styling consistent with Sam's other project documents
3. Save as web/index.html

Context: This is a self-contained HTML file (like the proposal documents Sam already has) that could be served from samkirk.com. No backend needed.

Test: Open web/index.html in a browser. The page renders correctly and the comparisons are easy to read.

## Specification Reference

This step is part of the Hardware Diagnostics LLM Fine-Tuning project. See docs/SPECIFICATION.md for full project context, goals, and constraints.

## Builder Guidance

- Certainty level: Firm (this is a planned, documented step)
- The TODO label suggests: Claude Code
- This is an optional/stretch step (Phase 6)
- Follow the Blueprint's instructions closely; they contain tested approaches

## Context

See [user-requests/UR-002/input.md](./user-requests/UR-002/input.md) for the full TODO document.

---
*Source: Ingested from docs/TODO.md, step 6.1*
