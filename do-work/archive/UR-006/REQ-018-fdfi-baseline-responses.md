---
id: REQ-018
title: Capture FD/FI numerical baseline responses before fine-tuning
status: completed
created_at: 2026-03-12T12:00:00-07:00
claimed_at: 2026-03-12T12:05:00-07:00
completed_at: 2026-03-12T12:40:00-07:00
route: B
user_request: UR-006
---

# Capture FD/FI Numerical Baseline Responses

## What
Run 4-5 FD/FI numerical diagnostic prompts through the base model (no adapter) and save the responses as pre-training baselines. This ensures Phase 4 evaluation can fairly compare base vs fine-tuned performance on the numerical/physics content added in Phase 2.

## Context
- Existing baselines (results/baseline_responses.md) cover 4 generic hardware diagnostics prompts from March 9
- Since then, FD/FI entries with real numerical data (TDR measurements, boundary scan results, thermal surveys) were added to the training set
- Without baselines for these prompt types, Phase 4 comparison won't show improvement on numerical content
- Use prompts from data/fdfi_combined_entries.jsonl
- Run via mlx_lm.generate with --max-tokens 200 against models/llama-3.2-3b-4bit
- Append results to results/baseline_responses.md in the same format as existing entries
- Also update results/baseline_responses.json

## Addendum (2026-03-12)

User added: merge the old Q&A baseline results with the newer numerical results into a unified report.

- After capturing the new FD/FI baselines, merge them with the existing 4 Q&A baselines into a single cohesive baseline report
- results/baseline_responses.md should read as one unified document — not "old section" + "new section" tacked on
- Update the performance summary table to include all prompts (original Q&A + new FD/FI numerical)
- Same for results/baseline_responses.json — one merged structure

---
*Source: Capture baseline responses from the base model (no adapter) for FD/FI numerical diagnostic prompts BEFORE fine-tuning.*

## Verification

**Source**: UR-006/input.md
**Pre-fix coverage**: 100% (9/9 items)

### Coverage Map

| # | Item | REQ Section | Status |
|---|------|-------------|--------|
| 1 | Base model, no adapter | What | Full |
| 2 | Pick 4-5 prompts from fdfi_combined_entries.jsonl | What, Context | Full |
| 3 | Numerical/physics-first content from Phase 2 | What, Context | Full |
| 4 | Run via mlx_lm.generate --max-tokens 200 | Context | Full |
| 5 | Model: models/llama-3.2-3b-4bit | Context | Full |
| 6 | Append to results/baseline_responses.md in same format | Context | Full |
| 7 | Update results/baseline_responses.json | Context | Full |
| 8 | Establishes pre-training baseline for fair Phase 4 comparison | What | Full |
| 9 | Merge old Q&A + new numerical into unified report | Addendum | Full |

*Verified by verify-request action*

---

## Triage

**Route: B** - Medium

**Reasoning:** Clear deliverables (run prompts, capture output, merge report) but need to select representative FD/FI prompts from the dataset and match existing baseline format.

## Implementation Summary

- Created `scripts/run_baselines.py` — reusable baseline runner that loads prompts, runs inference, captures metrics, and writes unified JSON + Markdown reports
- Selected 5 FD/FI prompts: TDR impedance, boundary scan interconnect, thermal survey, ADC code density, voltage margining
- Ran all 5 through base model (~24 tok/s, ~2.1 GB peak memory)
- Rewrote `results/baseline_responses.md` as unified report: performance summary table (9 prompts), two sections (Conceptual Q&A + Numerical Diagnostics)
- Rewrote `results/baseline_responses.json` as single merged structure with all 9 entries
- Fixed MLX deprecation warnings (mx.metal.* → mx.*)

## Testing

- Script ran successfully: 4 cached Q&A + 5 fresh FD/FI = 9 total baselines
- JSON output: 9 entries with prompt, response, category, label, metrics
- Markdown output: unified performance table + all 9 prompt/response pairs organized by category
- Base model FD/FI responses confirm poor numerical analysis (hallucinated data, wrong calculations, repetition) — strong contrast target for fine-tuning

## Plan

1. **Select 5 FD/FI prompts** from `data/fdfi_combined_entries.jsonl` covering diverse domains:
   - #1: TDR impedance measurements (signal integrity)
   - #2: Boundary scan interconnect results (digital test)
   - #3: Thermal survey (thermal/power)
   - #7: ADC code density histogram (mixed-signal)
   - #11: Voltage margining sweep (functional test)

2. **Create `scripts/run_baselines.py`** — script that:
   - Takes prompts and runs them through base model via `mlx_lm.generate` (--max-tokens 200)
   - Captures response text, token speeds, and peak memory
   - Outputs JSON results

3. **Run the 5 FD/FI prompts** through the base model and capture results

4. **Rewrite `results/baseline_responses.md`** as a unified document:
   - Single performance summary table with all 9 prompts (4 original Q&A + 5 new FD/FI)
   - Organized by category: "Conceptual Q&A" section, "Numerical Diagnostics (FD/FI)" section
   - Same formatting style throughout

5. **Rewrite `results/baseline_responses.json`** as one merged structure with all 9 entries

*Generated by Plan agent*

## Plan Verification

**Source**: REQ-018 requirements + addendum
**Coverage**: 100% (9/9 items)

| # | Requirement | Plan Step | Status |
|---|-------------|-----------|--------|
| 1 | Base model, no adapter | Step 2 (mlx_lm.generate, no adapter flag) | Full |
| 2 | 4-5 prompts from fdfi_combined_entries.jsonl | Step 1 (5 selected) | Full |
| 3 | Numerical/physics-first content | Step 1 (TDR, boundary scan, thermal, ADC, margining) | Full |
| 4 | mlx_lm.generate --max-tokens 200 | Step 2 | Full |
| 5 | models/llama-3.2-3b-4bit | Step 2 | Full |
| 6 | Append to baseline_responses.md in same format | Step 4 (unified rewrite) | Full |
| 7 | Update baseline_responses.json | Step 5 | Full |
| 8 | Pre-training baseline for Phase 4 | Steps 3-5 (captured before training) | Full |
| 9 | Merge old Q&A + new numerical into unified report | Steps 4-5 (single cohesive doc) | Full |

*Verified by verify-plan action*
