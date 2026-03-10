---
id: REQ-014
title: "Step 6.2: HuggingFace model card & upload"
status: pending
created_at: 2026-03-09T12:05:00Z
user_request: UR-002
related: [REQ-013]
batch: ml-training-phase-6
source_step: "6.2"
source_doc: docs/TODO.md
blueprint_ref: docs/BLUEPRINT.md
model_hint: "Claude Code + Sam"
---

# Step 6.2: HuggingFace Model Card & Upload

## What

Publish the LoRA adapter weights and model card to HuggingFace Hub.

## Requirements

- Write model card
- Upload adapter weights to HuggingFace Hub

## Verification

- Model page accessible on huggingface.co

## Blueprint Context

Publish LoRA adapters and model card to HuggingFace Hub.

Steps:
1. Create a model card (README.md for HuggingFace) with:
   - Model description and intended use
   - Training details: hardware, framework, hyperparameters
   - Dataset description (without exposing full dataset)
   - Example usage code
   - License (match Llama's license)
2. Use huggingface_hub to upload:
   - Adapter weights from adapters/hw-diagnostics/
   - Model card
   - Training config
3. Target repo name: samkirk/hw-diagnostics-advisor-llama3.2-3b-lora

Context: This makes the work publicly verifiable and adds a HuggingFace presence to Sam's profile. Only the adapter weights are uploaded (small, ~10-50MB), not the full model.

Test: The model page is accessible on huggingface.co and shows the model card. Adapter files are listed.

## Specification Reference

This step is part of the Hardware Diagnostics LLM Fine-Tuning project. See docs/SPECIFICATION.md for full project context, goals, and constraints.

## Builder Guidance

- Certainty level: Firm (this is a planned, documented step)
- The TODO label suggests: **Claude Code + Sam** — this step requires human involvement
- This is an optional/stretch step (Phase 6)
- Follow the Blueprint's instructions closely; they contain tested approaches

## Context

See [user-requests/UR-002/input.md](./user-requests/UR-002/input.md) for the full TODO document.

---
*Source: Ingested from docs/TODO.md, step 6.2*
