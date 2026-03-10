---
id: REQ-004
title: "Step 2.1: Define topic taxonomy & prompt templates"
status: pending
created_at: 2026-03-09T12:05:00Z
user_request: UR-002
related: [REQ-005, REQ-006, REQ-007]
batch: ml-training-phase-2
source_step: "2.1"
source_doc: docs/TODO.md
blueprint_ref: docs/BLUEPRINT.md
model_hint: "Claude Code"
---

# Step 2.1: Define Topic Taxonomy & Prompt Templates

## What

Create a dataset generation script that defines the topic taxonomy and Q&A generation approach before generating data.

## Requirements

- Create scripts/ directory
- Create scripts/generate_dataset.py with topic categories and question templates
  - ~10-15 hardware diagnostics topic categories (from the spec)
  - For each category, 3-4 question templates/styles:
    - Troubleshooting: "X is failing in scenario Y. How do you diagnose this?"
    - How-to: "What is the correct approach to X?"
    - Comparison: "When should you use X vs Y?"
    - Best practice: "What are the key considerations for X?"
  - A function that combines topics x templates to generate prompt variations

## Verification

- Script prints ~20 diverse sample prompts

## Blueprint Context

Create a dataset generation script at scripts/generate_dataset.py that defines the topic taxonomy and Q&A generation approach.

Steps:
1. Create scripts/ directory
2. Create scripts/generate_dataset.py with:
   - A list of ~10-15 hardware diagnostics topic categories (from the spec)
   - For each category, define 3-4 question templates/styles
   - A function that combines topics x templates to generate prompt variations
   - Output format: list of instruction strings (no responses yet)
3. Run the script to generate and print ~20 sample prompts for review

Context: The dataset quality determines the fine-tuning quality. We want to cover the topics listed in the spec (JTAG, boundary scan, functional test, fault isolation, etc.) with varied question types.

Test: The script runs and prints 20 diverse, realistic-sounding hardware diagnostics questions covering multiple topics and question styles.

## Specification Reference

This step is part of the Hardware Diagnostics LLM Fine-Tuning project. See docs/SPECIFICATION.md for full project context, goals, and constraints.

## Builder Guidance

- Certainty level: Firm (this is a planned, documented step)
- The TODO label suggests: Claude Code
- Follow the Blueprint's instructions closely; they contain tested approaches

## Context

See [user-requests/UR-002/input.md](./user-requests/UR-002/input.md) for the full TODO document.

---
*Source: Ingested from docs/TODO.md, step 2.1*
