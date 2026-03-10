---
id: UR-002
title: "Ingested from docs/TODO.md"
created_at: 2026-03-09T12:05:00Z
requests: [REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009, REQ-010, REQ-011, REQ-012, REQ-013, REQ-014]
word_count: 550
source: ingest-todo
---

# Ingested from docs/TODO.md

## Summary

Auto-generated from docs/TODO.md by the ingest-todo skill.
13 steps parsed across 6 phases (step 1.1 skipped — already captured as REQ-001 via UR-001).

Companion docs:
- Specification: docs/SPECIFICATION.md
- Blueprint: docs/BLUEPRINT.md

## Extracted Requests

| ID | Step | Title |
|----|------|-------|
| REQ-001 | 1.1 | Python environment & MLX installation (existing, UR-001) |
| REQ-002 | 1.2 | Download & quantize base model |
| REQ-003 | 1.3 | Verify base model inference |
| REQ-004 | 2.1 | Define topic taxonomy & prompt templates |
| REQ-005 | 2.2 | Generate full Q&A dataset |
| REQ-006 | 2.3 | Review dataset & approve [Sam] |
| REQ-007 | 2.4 | Split into train/eval |
| REQ-008 | 3.1 | Configure & run LoRA training |
| REQ-009 | 3.2 | Verify fine-tuned model inference |
| REQ-010 | 4.1 | Create evaluation script & generate comparisons |
| REQ-011 | 4.2 | Write README |
| REQ-012 | 5.1 | End-to-end verification & cleanup |
| REQ-013 | 6.1 | Static comparison page |
| REQ-014 | 6.2 | HuggingFace model card & upload |

## Full Verbatim Input

# TODO: Hardware Diagnostics LLM Fine-Tuning

**Tracking checklist for implementation. Check off items as completed.**

---

## Phase 1: Environment Setup & Base Model Verification

- [ ] **[Claude Code]** 1.1 Python environment & MLX installation
  - [ ] Create virtual environment (`.venv`)
  - [ ] Install mlx, mlx-lm, huggingface_hub
  - [ ] Create requirements.txt
  - [ ] Update .gitignore (add .venv/, models/, __pycache__/)
  - [ ] **TEST:** Verify `import mlx.core` and `import mlx_lm` work

- [ ] **[Claude Code]** 1.2 Download & quantize base model
  - [ ] Create models/ directory
  - [ ] Login to HuggingFace if needed (`huggingface-cli login`)
  - [ ] Convert Llama 3.2 3B Instruct to 4-bit MLX format
  - [ ] **TEST:** Verify models/llama-3.2-3b-4bit/ exists (~2GB)

- [ ] **[Claude Code]** 1.3 Verify base model inference
  - [ ] Run inference with a hardware diagnostics prompt
  - [ ] Save baseline response for later comparison
  - [ ] Note tokens/second speed
  - [ ] **TEST:** Model generates coherent text

---

## Phase 2: Dataset Generation

- [ ] **[Claude Code]** 2.1 Define topic taxonomy & prompt templates
  - [ ] Create scripts/ directory
  - [ ] Create scripts/generate_dataset.py with topic categories and question templates
  - [ ] **TEST:** Script prints ~20 diverse sample prompts

- [ ] **[Claude Code]** 2.2 Generate full Q&A dataset
  - [ ] Create data/ directory
  - [ ] Generate 200-500 Q&A pairs across all topic categories
  - [ ] Write to data/full_dataset.jsonl (Alpaca format)
  - [ ] **TEST:** File contains 200-500 valid JSONL entries, spot-check 5

- [ ] **[Sam]** 2.3 Review dataset & approve
  - [ ] Sam reviews data/full_dataset.jsonl for quality and accuracy
  - [ ] Flag and revise any low-quality entries
  - [ ] **GATE:** Sam approves dataset before proceeding

- [ ] **[Claude Code]** 2.4 Split into train/eval
  - [ ] Create scripts/split_dataset.py
  - [ ] Split 80/20 with seed 42
  - [ ] Write data/train.jsonl and data/valid.jsonl
  - [ ] **TEST:** Combined count matches full dataset, no duplicates

---

## Phase 3: LoRA Fine-Tuning

- [ ] **[Claude Code]** 3.1 Configure & run LoRA training
  - [ ] Create scripts/train.py (or document CLI command)
  - [ ] Set training config: 600 iters, batch 2, 8 LoRA layers, lr 1e-5
  - [ ] Run training
  - [ ] Save training log to results/training_log.txt
  - [ ] **TEST:** Training completes, loss decreases, adapters/hw-diagnostics/ exists

- [ ] **[Claude Code]** 3.2 Verify fine-tuned model inference
  - [ ] Run inference with adapter loaded
  - [ ] Compare response to Step 1.3 baseline
  - [ ] Try 2-3 additional prompts
  - [ ] **TEST:** Fine-tuned responses show more domain-specific detail

---

## Phase 4: Evaluation & Documentation

- [ ] **[Claude Code]** 4.1 Create evaluation script & generate comparisons
  - [ ] Create scripts/evaluate.py
  - [ ] Select 10-15 diverse prompts from eval set
  - [ ] Run both base and fine-tuned model on each
  - [ ] Write results/comparison.md with side-by-side output
  - [ ] **TEST:** results/comparison.md has 10-15 formatted comparison entries

- [ ] **[Claude Code]** 4.2 Write README
  - [ ] Project description and motivation
  - [ ] Hardware and technical approach
  - [ ] Key results (2-3 highlighted comparisons)
  - [ ] Reproduction steps
  - [ ] Project structure
  - [ ] Acknowledgments
  - [ ] **TEST:** README is complete and references only files that exist

---

## Phase 5: Repo Finalization

- [ ] **[Claude Code]** 5.1 End-to-end verification & cleanup
  - [ ] Remove scratch files, temp outputs, unused code
  - [ ] Verify pipeline sequence runs (scripts exist and work)
  - [ ] Confirm no secrets/tokens committed
  - [ ] Confirm models/ and .venv/ are gitignored
  - [ ] Final commit
  - [ ] **TEST:** Clean git status, no large binaries tracked

---

## Phase 6 (Optional): Web UI & Publishing

- [ ] **[Claude Code]** 6.1 Static comparison page
  - [ ] Generate styled HTML from results/comparison.md
  - [ ] Save as web/index.html
  - [ ] **TEST:** Page renders correctly in browser

- [ ] **[Claude Code + Sam]** 6.2 HuggingFace model card & upload
  - [ ] Write model card
  - [ ] Upload adapter weights to HuggingFace Hub
  - [ ] **TEST:** Model page accessible on huggingface.co

---
*Captured: 2026-03-09T12:05:00Z*
