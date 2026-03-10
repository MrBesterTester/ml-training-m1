---
id: REQ-003
title: "Step 1.3: Verify base model inference"
status: pending
created_at: 2026-03-09T12:05:00Z
user_request: UR-002
related: [REQ-001, REQ-002]
batch: ml-training-phase-1
source_step: "1.3"
source_doc: docs/TODO.md
blueprint_ref: docs/BLUEPRINT.md
model_hint: "Claude Code"
---

# Step 1.3: Verify Base Model Inference

## What

Run a simple inference to confirm the base model works on the M1 before any fine-tuning. This is the smoke test and provides our first baseline response for later comparison.

## Requirements

- Run inference with a hardware diagnostics prompt
- Save baseline response for later comparison
- Note tokens/second speed

## Verification

- Model generates coherent text

## Blueprint Context

Run inference on the base Llama 3.2 3B model to verify it works.

Steps:
1. Run a basic generation using mlx_lm:
   `python -m mlx_lm.generate --model ./models/llama-3.2-3b-4bit --prompt "What is boundary scan testing and when would you use it?" --max-tokens 200`
2. Save the output — this is our first baseline sample
3. Try 2-3 more hardware diagnostics prompts to get a feel for the base model's knowledge level

Context: This is our "smoke test" — if inference doesn't work here, nothing else will. It also gives us our first baseline response to compare against later.

Test: Model generates coherent text. Note the tokens/second rate — this is the M1 inference speed baseline.

## Specification Reference

This step is part of the Hardware Diagnostics LLM Fine-Tuning project. See docs/SPECIFICATION.md for full project context, goals, and constraints.

## Builder Guidance

- Certainty level: Firm (this is a planned, documented step)
- The TODO label suggests: Claude Code
- Follow the Blueprint's instructions closely; they contain tested approaches

## Context

See [user-requests/UR-002/input.md](./user-requests/UR-002/input.md) for the full TODO document.

---
*Source: Ingested from docs/TODO.md, step 1.3*
