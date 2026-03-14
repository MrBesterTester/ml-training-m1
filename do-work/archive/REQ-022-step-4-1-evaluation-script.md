---
id: REQ-022
title: "Step 4.1: Create evaluation script & generate comparisons"
status: done
created_at: 2026-03-13T00:00:00Z
completed_at: 2026-03-13T00:00:00Z
related: [REQ-021]
batch: ml-training-phase-4
source_step: "4.1"
source_doc: docs/TODO.md
blueprint_ref: docs/BLUEPRINT.md
model_hint: "Claude Code"
---

# Step 4.1: Create Evaluation Script & Generate Comparisons

## What

Create scripts/evaluate.py and generate results/comparison.md with side-by-side base vs fine-tuned model comparisons.

## Requirements

- Create scripts/evaluate.py
- Reuse the 9 baseline prompts from results/baseline_responses.json (4 conceptual Q&A + 5 FD/FI numerical)
- Add extra prompts from eval set to reach 10-15 total
- Run fine-tuned model on each prompt
- Write results/comparison.md with side-by-side output

## Verification

- results/comparison.md has 12 formatted comparison entries (9 baseline + 3 eval set)
- Covers both conceptual and numerical prompts
- Fine-tuned responses show clear domain knowledge improvement

---
*Source: docs/TODO.md, step 4.1*
