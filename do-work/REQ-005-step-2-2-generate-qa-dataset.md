---
id: REQ-005
title: "Step 2.2: Generate full Q&A dataset"
status: pending
created_at: 2026-03-09T12:05:00Z
user_request: UR-002
related: [REQ-004, REQ-006, REQ-007]
batch: ml-training-phase-2
source_step: "2.2"
source_doc: docs/TODO.md
blueprint_ref: docs/BLUEPRINT.md
model_hint: "Claude Code"
---

# Step 2.2: Generate Full Q&A Dataset

## What

Use the topic taxonomy to generate complete instruction/response pairs (200-500) and save as JSONL.

## Requirements

- Create data/ directory
- Generate 200-500 Q&A pairs across all topic categories
- Write to data/full_dataset.jsonl in Alpaca format: `{"instruction": "...", "input": "", "output": "..."}`
- Instructions should be specific scenarios, not generic
- Responses should be detailed (100-300 words), practical, and structured
- Include specifics: signal names, protocols, tool names, measurement values where appropriate

## Verification

- File contains 200-500 valid JSONL entries, spot-check 5

## Blueprint Context

Extend scripts/generate_dataset.py to generate complete Q&A pairs and write them to JSONL.

Steps:
1. Create the data/ directory
2. Add a bank of pre-written Q&A pairs covering each topic category. For each of the ~10-15 categories, write 15-30 Q&A pairs, targeting 200-500 total.
3. Write all pairs to data/full_dataset.jsonl in Alpaca format
4. Print summary: total count, per-category count, avg response length

Context: We need the responses to be detailed, specific, and technically sound — the kind of answers a senior hardware test engineer would give. The responses should be 100-300 words each, practical and actionable.

Test: data/full_dataset.jsonl exists, contains 200-500 valid JSON lines, each with instruction/input/output keys. Spot-check 5 random entries for quality.

## Specification Reference

This step is part of the Hardware Diagnostics LLM Fine-Tuning project. See docs/SPECIFICATION.md for full project context, goals, and constraints.

## Builder Guidance

- Certainty level: Firm (this is a planned, documented step)
- The TODO label suggests: Claude Code
- Follow the Blueprint's instructions closely; they contain tested approaches

## Context

See [user-requests/UR-002/input.md](./user-requests/UR-002/input.md) for the full TODO document.

---
*Source: Ingested from docs/TODO.md, step 2.2*
