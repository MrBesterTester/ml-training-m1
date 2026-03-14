---
id: REQ-028
title: "v3: Train model to explicitly classify diagnostic mode (FD/FI/TRIAGE)"
status: pending
created_at: 2026-03-13T00:00:00Z
user_request: UR-012
---

# v3: Train Model to Explicitly Classify Diagnostic Mode

## What

Retrain the model so it explicitly classifies each problem into a diagnostic mode (FD, FI, FD+FI, or TRIAGE) as the first step of its response, then proceeds with mode-appropriate analysis.

## Diagnostic Mode Definitions

- **FD (Fault Detection)** — Is there a fault? Analyzing data to determine pass/fail, identify anomalies, confirm defects exist
- **FI (Fault Isolation)** — Where is the fault? Narrowing down root cause to a specific component, net, or subsystem
- **FD+FI** — Both detection and isolation in one analysis (common in practice)
- **TRIAGE** — Generally indicates a software problem, not hardware. The model should recognize when the issue is outside the hardware diagnostic domain and flag it as such

## Realistic Scope

The 385 training entries fall into two very different groups:

- **133 FD/FI entries** (v2-fdfi) — diagnostic scenarios with data. These naturally belong to FD/FI/FD+FI/TRIAGE and should get mode labels prepended.
- **252 original Q&A entries** (v1) — conceptual/educational ("What is boundary scan testing?"). These are knowledge questions, not diagnostic scenarios. They don't have a fault to detect or isolate. Leave these as-is.

Additionally, **25 TRIAGE examples is thin** for teaching the model to reliably distinguish "this is software, not hardware." That's a nuanced judgment call built over years of experience. More TRIAGE examples are needed, especially edge cases where it *looks* like hardware but isn't.

## Requirements

### Phase 1: Augment the 133 FD/FI entries
- Prepend a diagnostic mode line to each of the 133 FD/FI training responses (e.g., "**Diagnostic mode: Fault Isolation.** The data shows...")
- Include a brief justification for the classification ("...because the fault has already been detected, so the task is narrowing down the root cause")
- For TRIAGE entries, make clear this is a software issue, not hardware ("**Diagnostic mode: Triage.** This appears to be a software/firmware issue rather than a hardware fault...")

### Phase 2: Expand TRIAGE coverage
- Add 20-30 new TRIAGE examples, focusing on edge cases: problems that look like hardware but are actually software/firmware/configuration
- Examples: driver bugs that mimic hardware failures, firmware misconfiguration causing test failures, OS-level issues masquerading as device faults

### Phase 3: Add explicit classification prompts
- Add 10-20 "classify this scenario" prompts where the expected output is the mode + reasoning
- Include ambiguous cases where reasonable engineers might disagree on the mode

### Phase 4: Retrain and evaluate
- Leave the 252 conceptual Q&A entries unchanged
- Retrain with the same hyperparameters (600 iters, batch 2, 8 LoRA layers, lr 1e-5, rank 8)
- Evaluate: does the fine-tuned model now surface diagnostic mode in its responses to diagnostic data while still handling conceptual questions normally?

## Why

The training data was organized by FD/FI/FD+FI/TRIAGE categories (Sam's diagnostic engineering expertise), but that taxonomy was never surfaced in the model's output. The model learned response patterns per category but doesn't show the expert's first reasoning step — identifying which diagnostic mode applies. Surfacing this gives the engineer something to validate or push back on, making the model a reasoning partner rather than just an answer generator.

## Context

- Current training data: 385 entries — only 133 are diagnostic scenarios (FD/FI/FD+FI/TRIAGE), the other 252 are conceptual Q&A
- The classification taxonomy is Sam's intellectual contribution from 4 decades of Silicon Valley test engineering
- TRIAGE as "software not hardware" is a critical distinction — experienced diagnostic engineers know when to stop chasing a hardware root cause
- This is a v3 training cycle — the existing v1 (original dataset) and v2 (FD/FI expansion) cycles are complete

---
*Source: UR-012/input.md*

## Verification

**Source**: UR-012/input.md
**Pre-fix coverage**: 100% (4/4 items)

### Coverage Map

| # | Item | REQ Section | Status |
|---|------|-------------|--------|
| 1 | Model should classify diagnostic mode | What | Full |
| 2 | Training data was already organized this way | Why | Full |
| 3 | Categories: FD, FI, FD+FI, TRIAGE | Requirements | Full |
| 4 | Gap: model mimics output but doesn't show reasoning | Why | Full |

*Verified by verify-request action*
