---
id: REQ-004
title: "Step 2.1: Define topic taxonomy & prompt templates"
status: completed
claimed_at: 2026-03-10T12:00:00Z
completed_at: 2026-03-10T12:15:00Z
route: B
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

---

## Triage

**Route: B** - Medium

**Reasoning:** Clear deliverable (create a specific script) but need to pull topic categories from the spec and design template structures that work across all categories. Not just a config change, but not multi-system either.

## Plan

### Overview
Create `scripts/generate_dataset.py` with a hardware diagnostics topic taxonomy (~12 categories from the spec), four question template styles, a combinatorial prompt generator function, and a `__main__` block that prints ~20 diverse sample prompts.

### Steps

**Step 1: Define TOPICS constant**
Module-level list of dicts, each with `name`, `display_name`, and `subtopics` (4-5 per category). 12 categories derived from SPECIFICATION.md Section 3:
1. Boundary Scan / JTAG Testing
2. Functional Test Strategies
3. Fault Isolation and Root Cause Analysis
4. Test Coverage Analysis
5. Mixed-Signal Board Testing
6. In-Circuit Test (ICT) Methodologies
7. Embedded Diagnostics
8. Test Automation Frameworks
9. Production Test Optimization
10. Environmental and Stress Testing
11. Signal Integrity and Power Integrity
12. Automated Optical Inspection (AOI) and X-Ray Inspection

**Step 2: Define TEMPLATES constant**
Dict keyed by style name, each containing 2-3 template format strings using `{display_name}` and `{subtopic}` placeholders:
- `troubleshooting`: scenario-based diagnosis questions
- `how_to`: process/methodology questions
- `comparison`: trade-off questions (needs two subtopics)
- `best_practice`: design/implementation guidance

**Step 3: Implement `generate_prompts()` function**
- Iterates topics x styles, picks random template variation, fills with category + subtopic(s)
- Uses `random.seed(42)` for reproducibility
- Returns list of dicts: `{"instruction": str, "category": str, "style": str}`
- Produces ~48 prompts (12 topics x 4 styles)

**Step 4: Implement `__main__` block**
- Calls `generate_prompts()`, samples 20, prints with style/category labels
- Shows summary stats (total prompts, topics covered, styles used)

**Step 5: Verification**
- Run `python scripts/generate_dataset.py` and confirm ~20 diverse, realistic prompts printed

### Patterns to Follow
- Match conventions from `scripts/verify_inference.py` (docstring, uppercase constants, main(), `if __name__ == "__main__"`)
- Structure for forward compatibility with Step 2.2 (module-level constants, category field in output)

*Generated by Plan agent*

## Plan Verification

**Source**: REQ-004 (6 items enumerated)
**Pre-fix coverage**: 100% (6 full, 0 partial, 0 missing)
**Post-fix coverage**: 100% (6/6 items addressed)

### Coverage Map

| # | Requirement | Plan Step | Status |
|---|------------|-----------|--------|
| 1 | Create scripts/ directory | Already exists (verify_inference.py) | Full |
| 2 | Create scripts/generate_dataset.py | Steps 1-4 create the file | Full |
| 3 | ~10-15 topic categories from spec | Step 1: 12 categories defined | Full |
| 4 | 3-4 question template styles (troubleshooting, how-to, comparison, best practice) | Step 2: all 4 styles | Full |
| 5 | Function combining topics x templates | Step 3: generate_prompts() | Full |
| 6 | Script prints ~20 diverse sample prompts | Steps 4-5: sampling + verification | Full |

### Fixes Applied

None needed — plan covers all requirements.

*Verified by verify-plan action*

## Exploration

- `scripts/` directory exists with `verify_inference.py`
- Conventions: module docstring, ALL_CAPS constants, type hints, `Path(__file__).resolve().parent.parent` for project root, `if __name__ == "__main__": main()`
- Virtual environment at `.venv` with MLX dependencies installed
- No special path setup needed

*Generated by Explore agent*

## Implementation Summary

- Created `scripts/generate_dataset.py` with:
  - 12 hardware diagnostics topic categories (JTAG, functional test, fault isolation, ICT, mixed-signal, etc.)
  - 5 specific subtopics per category using realistic test engineering terminology
  - 4 question template styles (troubleshooting, how-to, comparison, best practice) with 2-3 variations each
  - `generate_prompts(seed=42)` function producing 48 prompts (12 topics x 4 styles)
  - `main()` function sampling and printing 20 diverse prompts with summary stats

*Completed by work action (Route B)*

## Testing

**Tests run:** `.venv/bin/python scripts/generate_dataset.py`
**Result:** Script runs successfully, prints 20 diverse sample prompts covering all 12 topics and 4 styles (48 total generated)

**No testing infrastructure detected** — verification was the script execution itself per the REQ's test criteria.

*Verified by work action*
