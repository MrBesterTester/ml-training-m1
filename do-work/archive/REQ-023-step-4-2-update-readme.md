---
id: REQ-023
title: "Step 4.2: Update README with evaluation results and project status"
status: pending
created_at: 2026-03-13T00:00:00Z
user_request: UR-009
related: [REQ-024, REQ-022]
source_step: "4.2"
source_doc: docs/TODO.md
blueprint_ref: docs/BLUEPRINT.md
---

# Step 4.2: Update README

## What

Update the existing README.md to reflect current project status (Phase 4 complete). The README already has substantial content — physics-first explanation, LoRA interpretation, tech stack, project structure, pipeline. Focus on adding missing elements from the TODO checklist and updating status.

## Requirements

- Update project status section (Phase 3 → Phase 4 complete)
- Add 2-3 highlighted before/after comparison examples from results/comparison.md
- Add reproduction steps (prerequisites, setup, training command, inference command)
- Verify project structure section matches current directory layout
- Update scripts/ listing to include evaluate.py
- Ensure all referenced files actually exist
- Keep existing physics-first and LoRA interpretation sections (already strong)

## Context

- README.md already has ~123 lines with strong content on physics-first approach, LoRA interpretation, tech stack, project structure, and pipeline
- Compu-Flair/ docs have been extensively reworked and are referenced in README
- This is primarily an update/polish pass, not a rewrite

## Builder Guidance

- Certainty level: Firm (TODO step 4.2 checklist is clear)
- The README is already good — this is additive, not a rewrite
- Focus on: key results, reproduction steps, status update

---
*Source: UR-009/input.md*

## Verification

**Source**: UR-009/input.md
**Pre-fix coverage**: 100% (5/5 items)

### Coverage Map

| # | Item | REQ Section | Status |
|---|------|-------------|--------|
| 1 | Step 4.2 from TODO | Requirements | Full |
| 2 | README already has substance | Context | Full |
| 3 | Compu-Flair docs reworked | Context | Full |
| 4 | Docs duplicated elsewhere | REQ-024 | Full |
| 5 | Move duplicates to archive | REQ-024 | Full |

*Verified by verify-request action*
