# Blueprint: Hardware Diagnostics LLM Fine-Tuning

**Date:** March 9, 2026
**Source:** [docs/SPECIFICATION.md](./SPECIFICATION.md)

---

## Overview

This blueprint breaks the project into 5 phases (plus 1 optional), each composed of small steps. Every step ends with a verification or test to confirm it works before moving on. Steps are ordered so that nothing is orphaned — each builds on the last.

---

## Phase 1: Environment Setup & Base Model Verification

**Goal:** Get MLX installed, download the base model, and confirm inference works on the M1 iMac before writing any project code.

### Step 1.1 — Python Environment & MLX Installation

Set up a clean Python virtual environment and install MLX with its LLM tooling.

**Context:** The M1 iMac has Python and Homebrew installed. MLX is probably not installed. We want an isolated environment to avoid dependency conflicts.

```
Create a Python virtual environment in the project root and install the required packages for LLM fine-tuning with MLX.

Steps:
1. Create a virtual environment: python3 -m venv .venv
2. Activate it and upgrade pip
3. Install: mlx, mlx-lm, huggingface_hub
4. Create a requirements.txt capturing the installed versions
5. Add .venv/ and models/ to .gitignore

Test: Run `python -c "import mlx.core as mx; print(mx.ones(3))"` and confirm it prints a valid array. Run `python -c "import mlx_lm; print('mlx_lm OK')"` and confirm no errors.
```

### Step 1.2 — Download & Quantize the Base Model

Download Llama 3.2 3B Instruct from HuggingFace and convert it to 4-bit quantized MLX format.

**Context:** The model needs to be in MLX format for both training and inference. The quantized model should be ~2GB and fit comfortably in 16GB unified memory. The `models/` directory is gitignored (model files are large).

```
Download and quantize the Llama 3.2 3B Instruct model for MLX.

Steps:
1. Create the models/ directory
2. Use mlx_lm to fetch and convert the model:
   python -m mlx_lm.convert \
     --hf-path meta-llama/Llama-3.2-3B-Instruct \
     --mlx-path ./models/llama-3.2-3b-4bit \
     --quantize --q-bits 4
3. Verify the converted model directory exists and contains the expected files (weights, config, tokenizer)

Note: This requires a HuggingFace account and acceptance of Meta's Llama license. If access is gated, use `huggingface-cli login` first.

Test: Confirm models/llama-3.2-3b-4bit/ exists and contains model files. Check total size is approximately 2GB.
```

### Step 1.3 — Verify Base Model Inference

Run a simple inference to confirm the base model works on the M1 before any fine-tuning.

**Context:** This is our "smoke test" — if inference doesn't work here, nothing else will. It also gives us our first baseline response to compare against later.

```
Run inference on the base Llama 3.2 3B model to verify it works.

Steps:
1. Run a basic generation using mlx_lm:
   python -m mlx_lm.generate \
     --model ./models/llama-3.2-3b-4bit \
     --prompt "What is boundary scan testing and when would you use it?" \
     --max-tokens 200
2. Save the output — this is our first baseline sample
3. Try 2-3 more hardware diagnostics prompts to get a feel for the base model's knowledge level

Test: Model generates coherent text. Note the tokens/second rate — this is the M1 inference speed baseline.
```

---

## Phase 2: Dataset Generation

**Goal:** Create a high-quality training dataset of ~200-500 hardware diagnostics Q&A pairs in Alpaca-style JSONL format, reviewed and approved by Sam.

### Step 2.1 — Define Topic Taxonomy, Physics Mappings & Prompt Templates

Before generating data, define the topics, map each to its underlying physics, and define the style of Q&A pairs we want.

**Context:** The dataset quality determines the fine-tuning quality. We want to cover the topics listed in the spec (JTAG, boundary scan, functional test, fault isolation, etc.) with varied question types (troubleshooting scenarios, how-to, comparison, best practices). Critically, responses must follow the **physics-first explanatory style** (CompuFlair-inspired) — grounding practical answers in the underlying physics and engineering principles.

```
Create a dataset generation script at scripts/generate_dataset.py that defines the topic taxonomy, physics mappings, and Q&A generation approach.

Steps:
1. Create scripts/ directory
2. Create scripts/generate_dataset.py with:
   - A list of ~10-15 hardware diagnostics topic categories (from the spec)
   - For each category, a physics mapping that identifies the underlying principles:
     * Signal integrity → transmission line theory, EM wave propagation
     * Thermal testing → thermodynamics, heat transfer
     * ICT → circuit theory (Kirchhoff, Ohm, impedance)
     * Boundary scan → propagation delay, clock domains
     * ESD/EMI → Maxwell's equations, field theory
     * Fault isolation → statistical reasoning, energy minimization analogies
     * Test coverage → information theory, entropy
   - For each category, define 3-4 question templates/styles:
     * Troubleshooting: "X is failing in scenario Y. How do you diagnose this?"
     * How-to: "What is the correct approach to X?"
     * Comparison: "When should you use X vs Y?"
     * Best practice: "What are the key considerations for X?"
     * Physics-why: "Why does X happen from a physics perspective?"
   - A function that combines topics × templates to generate prompt variations
   - Output format: list of instruction strings (no responses yet)
3. Run the script to generate and print ~20 sample prompts for review

Test: The script runs and prints 20 diverse, realistic-sounding hardware diagnostics questions covering multiple topics and question styles. At least some prompts should invite physics-grounded explanations.
```

### Step 2.2 — Generate Full Q&A Dataset (Physics-First Style)

Use the topic taxonomy and physics mappings to generate complete instruction/response pairs and save as JSONL.

**Context:** We need the responses to be detailed, specific, and technically sound — the kind of answers a physicist-engineer would give. The responses should be 100-300 words each, practical and actionable, but **grounded in physics**: explanations should tie practical steps back to underlying physical principles (transmission line theory, thermodynamics, circuit theory, EM field theory, information theory, etc.). This CompuFlair-inspired style is what makes the fine-tuned model distinctive.

```
Extend scripts/generate_dataset.py to generate complete Q&A pairs and write them to JSONL.

Steps:
1. Create the data/ directory
2. Add a bank of pre-written Q&A pairs covering each topic category. For each of the ~10-15 categories, write 15-30 Q&A pairs, targeting 200-500 total.
   - Instructions should be specific scenarios, not generic
   - Responses should be detailed (100-300 words), practical, and structured
   - Responses MUST follow the physics-first style: connect practical advice to the underlying physics
     * Include relevant equations, constants, or physical relationships where natural
     * Explain *why* something works/fails in terms of physical mechanisms, not just *what* to do
     * Use the physics mappings from Step 2.1 to ensure each topic area references its core principles
   - Include specifics: signal names, protocols, tool names, measurement values where appropriate
3. Write all pairs to data/full_dataset.jsonl in Alpaca format:
   {"instruction": "...", "input": "", "output": "..."}
4. Print summary: total count, per-category count, avg response length

Test: data/full_dataset.jsonl exists, contains 200-500 valid JSON lines, each with instruction/input/output keys. Spot-check 5 random entries for quality — verify that responses ground explanations in physics, not just procedures.
```

### Step 2.3 — Review Dataset & Split Train/Eval

Sam reviews the dataset. After approval, split into training and evaluation sets.

**Context:** The 80/20 split gives us ~160-400 training examples and ~40-100 evaluation examples. The eval set is used to compare base vs. fine-tuned model performance.

```
Add a split function to the dataset pipeline and create train/eval files.

Steps:
1. Create scripts/split_dataset.py that:
   - Reads data/full_dataset.jsonl
   - Shuffles with a fixed random seed (42) for reproducibility
   - Splits 80/20 into train and eval (stratified by category if categories are tagged)
   - Writes data/train.jsonl and data/eval.jsonl
   - Prints counts for each split
2. Run the split

Sam reviews: Open data/full_dataset.jsonl and scan for quality. Flag any entries that are inaccurate, too generic, or low quality. Remove or revise flagged entries, then re-run the split.

Test: data/train.jsonl and data/eval.jsonl exist. Combined count equals full_dataset.jsonl count. No duplicates across splits.
```

---

## Phase 3: LoRA Fine-Tuning

**Goal:** Fine-tune the base model with LoRA adapters on the training dataset and save the adapter weights.

### Step 3.1 — Configure & Run LoRA Training

Set up the training configuration and run the fine-tuning.

**Context:** LoRA freezes the base model and trains small rank-8 adapter matrices on the attention layers. With ~200-500 examples and batch size 2, training should take 30-90 minutes on the M1. We use mlx_lm's built-in LoRA support.

**Why Python, not Swift:** `mlx-lm` provides LoRA fine-tuning out of the box via a single CLI command. `mlx-swift` and `mlx-swift-examples` cover inference only — there is no Swift equivalent of `mlx_lm.lora`. Writing a LoRA training loop from scratch in Swift (attention layer hooking, gradient accumulation, adapter serialization) would be substantial effort for zero benefit, since both languages call the same Metal shaders on the M1 GPU — the actual compute is identical. Swift would make sense for a native macOS inference app (Phase 6), but not for training.

```
Create a training script and run LoRA fine-tuning.

Steps:
1. Create scripts/train.py that wraps the mlx_lm LoRA training with project-specific defaults:
   - Model path: ./models/llama-3.2-3b-4bit
   - Data path: ./data (mlx_lm expects train.jsonl and valid.jsonl here)
   - Rename or symlink data/eval.jsonl to data/valid.jsonl (mlx_lm convention)
   - Training config:
     * iters: 600
     * batch-size: 2
     * lora-layers: 8
     * learning-rate: 1e-5
     * adapter-path: ./adapters/hw-diagnostics
   - The script should also print the training config before starting
2. Alternatively, if mlx_lm's CLI is sufficient, document the exact command:
   python -m mlx_lm.lora \
     --model ./models/llama-3.2-3b-4bit \
     --data ./data \
     --train \
     --iters 600 \
     --batch-size 2 \
     --lora-layers 8 \
     --learning-rate 1e-5 \
     --adapter-path ./adapters/hw-diagnostics
3. Run the training
4. Save the training log output to results/training_log.txt

Test: Training completes without OOM errors. adapters/hw-diagnostics/ directory exists and contains adapter weight files. Training loss decreases over iterations.
```

### Step 3.2 — Verify Fine-Tuned Model Inference

Run inference with the fine-tuned model to confirm the adapters load and work.

**Context:** This is the moment of truth — does the fine-tuned model respond differently than the base model? We use the same prompt from Step 1.3 to get an immediate comparison.

```
Test inference with the LoRA-adapted model.

Steps:
1. Run inference with the adapter:
   python -m mlx_lm.generate \
     --model ./models/llama-3.2-3b-4bit \
     --adapter-path ./adapters/hw-diagnostics \
     --prompt "What is boundary scan testing and when would you use it?" \
     --max-tokens 200
2. Compare the output to the base model response saved in Step 1.3
3. Try 2-3 more prompts to spot-check quality

Test: The fine-tuned model generates responses. Responses should show more specific, detailed, or structured knowledge about hardware diagnostics compared to the base model.
```

---

## Phase 4: Evaluation & Documentation

**Goal:** Systematically compare base vs. fine-tuned model performance, and document everything in the repo.

### Step 4.1 — Create Evaluation Script

Build a script that runs the same prompts through both models and generates a comparison document.

**Context:** This is the portfolio centerpiece — the side-by-side comparison that proves the fine-tuning worked. The evaluation **must** reuse the 9 baseline prompts from `results/baseline_responses.json` (4 conceptual Q&A + 5 FD/FI numerical diagnostics) so the before/after comparison is direct and fair. The base model responses are already captured — the evaluate script only needs to run the fine-tuned model on the same prompts and place the results side-by-side. Additional eval-set prompts can be added on top, but the 9 baselines are the core comparison set.

```
Create scripts/evaluate.py that generates side-by-side comparisons.

Steps:
1. Create scripts/evaluate.py that:
   - Loads 10-15 prompts from data/eval.jsonl (sample diverse topics)
   - For each prompt, runs inference on:
     a. Base model (no adapter)
     b. Fine-tuned model (with adapter)
   - Captures both responses
   - Writes results/comparison.md with a formatted table or sections:
     * Prompt
     * Base model response
     * Fine-tuned response
     * (Optional) Ground truth from the dataset
   - Prints a summary to stdout
2. Run the evaluation script

Test: results/comparison.md exists and contains 10-15 comparison entries. Visually inspect: the fine-tuned responses should be noticeably more specific and domain-appropriate.
```

### Step 4.2 — Write README & Final Repo Structure

Document the project with a clear README and clean up the repo structure.

**Context:** The README is the first thing anyone sees. It should tell the story (what, why, how), show key results, and make reproduction easy.

```
Create a comprehensive README.md for the project.

Steps:
1. Write README.md with:
   - Project title and one-line description
   - Motivation: why fine-tune an LLM for hardware diagnostics?
   - Hardware: M1 iMac, 16GB (this is a feature, not a limitation)
   - Technical approach: base model, LoRA, MLX, dataset
   - Key results: 2-3 highlighted before/after examples (pulled from results/comparison.md)
   - How to reproduce:
     * Prerequisites (Python, HuggingFace account, M1 Mac)
     * Setup steps (venv, pip install, model download)
     * Training command
     * Inference command
   - Project structure (directory tree)
   - Acknowledgments (Meta for Llama, Apple for MLX)
2. Verify all scripts referenced in the README actually exist and work
3. Ensure .gitignore covers: .venv/, models/, __pycache__/, .DS_Store

Test: A developer reading the README can understand the project, reproduce the training, and run inference without asking questions.
```

---

## Phase 5: Repo Finalization

**Goal:** Clean up, verify everything works end-to-end, and prepare for git.

### Step 5.1 — End-to-End Verification

Run through the entire pipeline from scratch to confirm reproducibility.

**Context:** Before calling it done, verify that a fresh start (after model download) produces working results.

```
Verify the complete pipeline works.

Steps:
1. Review all files in the repo — remove any scratch files, temp outputs, or unused code
2. Verify the pipeline sequence:
   a. pip install -r requirements.txt (works)
   b. Model download/convert (command documented, not re-run)
   c. python scripts/generate_dataset.py (produces data/full_dataset.jsonl)
   d. python scripts/split_dataset.py (produces train/eval splits)
   e. Training command (documented, adapter weights present)
   f. python scripts/evaluate.py (produces results/comparison.md)
3. Ensure no secrets, API keys, or tokens are committed
4. Ensure models/ and .venv/ are gitignored
5. Final git status — stage and commit all project files

Test: git status shows a clean working tree after commit. No large binary files (models, venv) are tracked.
```

---

## Phase 6 (Optional): Web UI & Publishing

**Goal:** If time permits, add a static comparison page and/or publish adapters to HuggingFace.

### Step 6.1 — Static Comparison Page

Build an HTML page showing the before/after results for portfolio use.

**Context:** This is a self-contained HTML file (like the proposal documents Sam already has) that could be served from samkirk.com. No backend needed.

```
Create a static HTML comparison page from the evaluation results.

Steps:
1. Create a script or template that reads results/comparison.md and generates a styled HTML page
2. The page should show:
   - Project title and brief description
   - Technical details (model, method, hardware)
   - 10-15 side-by-side comparisons with base vs. fine-tuned responses
   - Visual styling consistent with Sam's other project documents
3. Save as web/index.html

Test: Open web/index.html in a browser. The page renders correctly and the comparisons are easy to read.
```

### Step 6.2 — HuggingFace Model Card & Adapter Upload

Publish the LoRA adapter weights to HuggingFace Hub.

**Context:** This makes the work publicly verifiable and adds a HuggingFace presence to Sam's profile. Only the adapter weights are uploaded (small, ~10-50MB), not the full model.

```
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

Test: The model page is accessible on huggingface.co and shows the model card. Adapter files are listed.
```

---

## Step Dependency Map

```
1.1 Python/MLX Setup
 └─→ 1.2 Download Base Model
      └─→ 1.3 Verify Base Inference
           ├─→ 2.1 Define Topics & Templates
           │    └─→ 2.2 Generate Full Dataset
           │         └─→ 2.3 Review & Split Dataset
           │              └─→ 3.1 LoRA Training
           │                   └─→ 3.2 Verify Fine-Tuned Inference
           │                        └─→ 4.1 Evaluation Script
           │                             └─→ 4.2 README & Repo Structure
           │                                  └─→ 5.1 End-to-End Verification
           │                                       ├─→ 6.1 Static Comparison Page (optional)
           │                                       └─→ 6.2 HuggingFace Upload (optional)
           └─→ (base model responses feed into 4.1 evaluation)
```

---

## Key Principles

1. **Every step has a test.** Don't move on until it passes.
2. **Real data, not mocks** (where applicable). We generate a real dataset and do real training — no placeholder results.
3. **Small steps.** Each step is 15-60 minutes of work (plus compute time for training).
4. **Nothing orphaned.** Every script is used by a later step. Every output feeds into something.
5. **M1 constraints respected.** All steps are designed for 16GB unified memory. If something doesn't fit, we adapt (reduce batch size, fewer layers, smaller dataset).
