---
id: REQ-021
title: "Step 3.2: Verify fine-tuned model inference"
status: done
created_at: 2026-03-13T00:00:00Z
related: [REQ-020]
batch: ml-training-phase-3
source_step: "3.2"
source_doc: docs/TODO.md
blueprint_ref: docs/BLUEPRINT.md
model_hint: "Claude Code"
---

# Step 3.2: Verify Fine-Tuned Model Inference

## What

Run inference with the fine-tuned model (LoRA adapter loaded) to confirm adapters work, then compare against the base model baseline from Step 1.3.

## Requirements

- Run inference with adapter loaded on the same boundary scan prompt from Step 1.3
- Compare response to baseline_responses.json
- Try 2-3 additional prompts to spot-check quality
- Save fine-tuned responses for later evaluation

## Verification

- Fine-tuned responses show more domain-specific detail than base model
- Responses demonstrate physics-first explanatory style from training data
