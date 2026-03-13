---
id: REQ-008
title: "Step 3.1: Configure & run LoRA training"
status: pending
created_at: 2026-03-09T12:05:00Z
user_request: UR-002
related: [REQ-009]
batch: ml-training-phase-3
source_step: "3.1"
source_doc: docs/TODO.md
blueprint_ref: docs/BLUEPRINT.md
model_hint: "Claude Code"
---

# Step 3.1: Configure & Run LoRA Training

## What

Set up the training configuration and run LoRA fine-tuning on the hardware diagnostics dataset.

## Requirements

- Create scripts/train.py (or document CLI command)
- Set training config: 600 iters, batch 2, 8 LoRA layers, lr 1e-5
- Run training
- Save training log to results/training_log.txt

## Verification

- Training completes without OOM errors
- Loss decreases over iterations
- adapters/hw-diagnostics/ exists and contains adapter weight files

## Blueprint Context

Create a training script and run LoRA fine-tuning.

Steps:
1. Create scripts/train.py that wraps the mlx_lm LoRA training with project-specific defaults:
   - Model path: ./models/llama-3.2-3b-4bit
   - Data path: ./data (mlx_lm expects train.jsonl and valid.jsonl here)
   - Rename or symlink data/eval.jsonl to data/valid.jsonl (mlx_lm convention)
   - Training config: iters: 600, batch-size: 2, lora-layers: 8, learning-rate: 1e-5, adapter-path: ./adapters/hw-diagnostics
   - The script should also print the training config before starting
2. Alternatively, if mlx_lm's CLI is sufficient, document the exact command:
   `python -m mlx_lm.lora --model ./models/llama-3.2-3b-4bit --data ./data --train --iters 600 --batch-size 2 --lora-layers 8 --learning-rate 1e-5 --adapter-path ./adapters/hw-diagnostics`
3. Run the training
4. Save the training log output to results/training_log.txt

Context: LoRA freezes the base model and trains small rank-8 adapter matrices on the attention layers. With ~200-500 examples and batch size 2, training should take 30-90 minutes on the M1. We use mlx_lm's built-in LoRA support.

Test: Training completes without OOM errors. adapters/hw-diagnostics/ directory exists and contains adapter weight files. Training loss decreases over iterations.

## Specification Reference

This step is part of the Hardware Diagnostics LLM Fine-Tuning project. See docs/SPECIFICATION.md for full project context, goals, and constraints.

## Builder Guidance

- Certainty level: Firm (this is a planned, documented step)
- The TODO label suggests: Claude Code
- Follow the Blueprint's instructions closely; they contain tested approaches

## Context

See [user-requests/UR-002/input.md](./user-requests/UR-002/input.md) for the full TODO document.

---
*Source: Ingested from docs/TODO.md, step 3.1*
