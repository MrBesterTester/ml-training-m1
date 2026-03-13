---
id: REQ-009
title: "Step 3.2: Verify fine-tuned model inference"
status: pending
created_at: 2026-03-09T12:05:00Z
user_request: UR-002
related: [REQ-008]
batch: ml-training-phase-3
source_step: "3.2"
source_doc: docs/TODO.md
blueprint_ref: docs/BLUEPRINT.md
model_hint: "Claude Code"
---

# Step 3.2: Verify Fine-Tuned Model Inference

## What

Run inference with the fine-tuned model to confirm the adapters load and work, and compare against the base model baseline.

## Requirements

- Run inference with adapter loaded
- Compare response to Step 1.3 baseline
- Try 2-3 additional prompts

## Verification

- Fine-tuned responses show more domain-specific detail than base model

## Blueprint Context

Test inference with the LoRA-adapted model.

Steps:
1. Run inference with the adapter:
   `python -m mlx_lm.generate --model ./models/llama-3.2-3b-4bit --adapter-path ./adapters/hw-diagnostics --prompt "What is boundary scan testing and when would you use it?" --max-tokens 200`
2. Compare the output to the base model response saved in Step 1.3
3. Try 2-3 more prompts to spot-check quality

Context: This is the moment of truth — does the fine-tuned model respond differently than the base model? We use the same prompt from Step 1.3 to get an immediate comparison.

Test: The fine-tuned model generates responses. Responses should show more specific, detailed, or structured knowledge about hardware diagnostics compared to the base model.

## Specification Reference

This step is part of the Hardware Diagnostics LLM Fine-Tuning project. See docs/SPECIFICATION.md for full project context, goals, and constraints.

## Builder Guidance

- Certainty level: Firm (this is a planned, documented step)
- The TODO label suggests: Claude Code
- Follow the Blueprint's instructions closely; they contain tested approaches

## Context

See [user-requests/UR-002/input.md](./user-requests/UR-002/input.md) for the full TODO document.

---
*Source: Ingested from docs/TODO.md, step 3.2*
