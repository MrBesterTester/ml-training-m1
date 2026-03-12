# TODO: Hardware Diagnostics LLM Fine-Tuning

**Tracking checklist for implementation. Check off items as completed.**

---

## Phase 1: Environment Setup & Base Model Verification

- [x] **[Claude Code]** 1.1 Python environment & MLX installation
  - [x] Create virtual environment (`.venv`)
  - [x] Install mlx, mlx-lm, huggingface_hub
  - [x] Create requirements.txt
  - [x] Update .gitignore (add .venv/, models/, __pycache__/)
  - [x] **TEST:** Verify `import mlx.core` and `import mlx_lm` work

- [x] **[Claude Code]** 1.2 Download & quantize base model
  - [x] Create models/ directory
  - [x] Login to HuggingFace if needed (`huggingface-cli login`)
  - [x] Convert Llama 3.2 3B Instruct to 4-bit MLX format
  - [x] **TEST:** Verify models/llama-3.2-3b-4bit/ exists (~2GB)

- [x] **[Claude Code]** 1.3 Verify base model inference
  - [x] Run inference with a hardware diagnostics prompt
  - [x] Save baseline response for later comparison
  - [x] Note tokens/second speed
  - [x] **TEST:** Model generates coherent text

---

## Phase 2: Dataset Generation

- [x] **[Claude Code]** 2.1 Define topic taxonomy, physics mappings & prompt templates
  - [x] Create scripts/ directory
  - [x] Create scripts/generate_dataset.py with topic categories, physics mappings, and question templates
  - [x] Map each topic to underlying physics (transmission line theory, thermodynamics, circuit theory, EM fields, etc.)
  - [x] Include "physics-why" question template style
  - [x] **TEST:** Script prints ~20 diverse sample prompts; some invite physics-grounded explanations

- [x] **[Claude Code]** 2.2 Generate full Q&A dataset (physics-first style)
  - [x] Create data/ directory
  - [x] Generate 200-500 Q&A pairs across all topic categories
  - [x] Responses must follow CompuFlair-inspired physics-first explanatory style
  - [x] Write to data/full_dataset.jsonl (Alpaca format)
  - [x] **TEST:** File contains 200-500 valid JSONL entries, spot-check 5 for physics grounding

- [ ] **[Sam]** 2.3 Review dataset & approve
  - [ ] Sam reviews data/full_dataset.jsonl for quality and accuracy
  - [ ] Verify physics-first style: responses ground explanations in underlying physics, not just procedures
  - [ ] Flag and revise any low-quality or insufficiently physics-grounded entries
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
  - [ ] **CompuFlair physics-first interpretation** — front-and-center explanation of why physics-grounded responses matter, how this settles the "I don't understand ML results" complaint, and what makes this model genuinely distinctive
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
