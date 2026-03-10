---
id: REQ-002
title: "Step 1.2: Download & quantize base model"
status: pending
created_at: 2026-03-09T12:05:00Z
user_request: UR-002
related: [REQ-001, REQ-003]
batch: ml-training-phase-1
source_step: "1.2"
source_doc: docs/TODO.md
blueprint_ref: docs/BLUEPRINT.md
model_hint: "Claude Code"
---

# Step 1.2: Download & Quantize Base Model

## What

Download Llama 3.2 3B Instruct from HuggingFace and convert it to 4-bit quantized MLX format.

## Requirements

- Create models/ directory
- Login to HuggingFace if needed (`huggingface-cli login`)
- Convert Llama 3.2 3B Instruct to 4-bit MLX format

## Verification

- Verify models/llama-3.2-3b-4bit/ exists (~2GB)

## Blueprint Context

Download and quantize the Llama 3.2 3B Instruct model for MLX.

Steps:
1. Create the models/ directory
2. Use mlx_lm to fetch and convert the model:
   `python -m mlx_lm.convert --hf-path meta-llama/Llama-3.2-3B-Instruct --mlx-path ./models/llama-3.2-3b-4bit --quantize --q-bits 4`
3. Verify the converted model directory exists and contains the expected files (weights, config, tokenizer)

Note: This requires a HuggingFace account and acceptance of Meta's Llama license. If access is gated, use `huggingface-cli login` first.

Context: The model needs to be in MLX format for both training and inference. The quantized model should be ~2GB and fit comfortably in 16GB unified memory. The `models/` directory is gitignored (model files are large).

Test: Confirm models/llama-3.2-3b-4bit/ exists and contains model files. Check total size is approximately 2GB.

## Specification Reference

This step is part of the Hardware Diagnostics LLM Fine-Tuning project. See docs/SPECIFICATION.md for full project context, goals, and constraints.

## Builder Guidance

- Certainty level: Firm (this is a planned, documented step)
- The TODO label suggests: Claude Code
- Follow the Blueprint's instructions closely; they contain tested approaches

## Context

See [user-requests/UR-002/input.md](./user-requests/UR-002/input.md) for the full TODO document.

---
*Source: Ingested from docs/TODO.md, step 1.2*
