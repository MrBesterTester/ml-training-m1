# Specification: Hardware Diagnostics LLM Fine-Tuning

**Date:** March 9, 2026
**Author:** Sam Kirk (with Claude Code)

---

## 1. Project Summary

Fine-tune a small open-source LLM (Llama 3.2 3B, 4-bit quantized) with LoRA adapters to become a **hardware test & diagnostics advisor**, using Apple's MLX framework on an M1 iMac (16GB). The project demonstrates non-trivial LLM fine-tuning on consumer hardware, producing a finished repo with documented before/after comparisons.

## 2. Goals

### Primary Goal
Demonstrate hands-on LLM fine-tuning competence — not just prompting, but actually training a model with domain-specific data using modern techniques (LoRA, quantization, MLX).

### Success Criteria
- A fine-tuned Llama 3.2 3B model running inference locally on the M1 iMac
- A training dataset of ~200-500 hardware diagnostics instruction/response pairs
- Documented side-by-side comparisons showing measurable improvement over the base model on domain-specific questions
- A complete, well-organized GitHub repo showing the full pipeline

## 3. Domain: Hardware Test & Diagnostics

The training dataset covers hardware test engineering topics including but not limited to:

- Boundary scan / JTAG testing
- Functional test strategies
- Fault isolation and root cause analysis
- Test coverage analysis
- Mixed-signal board testing
- In-circuit test (ICT) methodologies
- Embedded diagnostics
- Test automation frameworks
- Production test optimization
- Environmental and stress testing

### Dataset Approach
- AI-generated Q&A pairs based on publicly available domain knowledge and web resources
- Formatted as instruction/response pairs (Alpaca-style JSONL)
- Sam reviews and approves all training data before use
- Target: 200-500 pairs
- 80/20 train/eval split

### Example Format

```json
{
  "instruction": "A boundary scan test is passing on the bench but failing intermittently in production. What diagnostic steps would you take?",
  "input": "",
  "output": "First, check environmental differences between bench and production. Boundary scan is sensitive to signal integrity: (1) Compare TCK frequencies — production lines sometimes run faster clocks. (2) Check cable lengths and impedance — bench setups often have shorter, better-shielded JTAG cables. (3) Examine power supply noise — production environments can have more EMI. (4) Consider temperature differences. Capture the failing scan chain data and compare bit-by-bit to passing bench data to identify which cells are failing, then work backward to the physical cause."
}
```

## 4. Technical Stack

| Component | Choice | Rationale |
|---|---|---|
| **Base model** | Llama 3.2 3B Instruct | Fits comfortably in 16GB at 4-bit (~2GB). Well-supported by MLX. Meta — local to Sam. |
| **Quantization** | 4-bit (via MLX) | 4x memory reduction with minimal quality loss |
| **Fine-tuning method** | LoRA (Low-Rank Adaptation) | Freezes base model, trains ~1-2M adapter parameters. Feasible on M1. |
| **ML framework** | Apple MLX + mlx-lm | Native Apple Silicon support, unified memory, no .to(device) calls |
| **Language** | Python | MLX and mlx-lm are Python-first |
| **Hardware** | M1 iMac, 16GB unified memory, 8-core GPU | Target constraint — the project proves this hardware is sufficient |

### Environment Prerequisites (already available or easily installed)
- macOS on M1 iMac
- Python 3 (installed)
- Homebrew (installed)
- pip (installed)
- MLX and mlx-lm (to be installed via pip)

## 5. Deliverables

### Minimum Deliverable (Required)
1. **Training dataset** — Reviewed and approved JSONL file(s) in `data/`
2. **Fine-tuning pipeline** — Scripts to convert base model, run LoRA training, and run inference
3. **Trained adapter weights** — Saved LoRA adapter in `adapters/`
4. **Evaluation results** — Documented base vs. fine-tuned comparisons (10-15 example prompts with side-by-side outputs)
5. **Complete repo** — Organized with README, setup instructions, and reproducible steps

### Optional / Stretch Deliverables
6. **Web UI** — Either:
   - A **comparison page** (static HTML) showing pre-generated side-by-side base vs. fine-tuned responses (~10-15 examples). No server needed. Portfolio-ready.
   - A **chat-style interface** where visitors can query the fine-tuned model interactively. Requires a running inference backend.
7. **HuggingFace Hub publication** — LoRA adapter weights + model card published to HuggingFace
8. **Deployment** — Web app on `fine-tuning.samkirk.com` or similar subdomain (backend TBD)

### What Is NOT in Scope
- Training a model from scratch
- Multi-GPU or cloud GPU training
- Production-grade deployment infrastructure
- The CompuFlair physics curriculum (separate learning track)
- Rust or Mojo implementations

## 6. Project Structure

```
ml_training_m1/
├── docs/
│   ├── SPECIFICATION.md      ← this file
│   ├── BLUEPRINT.md          ← Phase 2: how to build it
│   └── TODO.md               ← Phase 3: implementation checklist
├── data/
│   ├── train.jsonl           ← training split
│   └── eval.jsonl            ← evaluation split
├── scripts/
│   ├── generate_dataset.py   ← dataset generation
│   ├── convert_model.py      ← download & quantize base model
│   ├── train.py              ← LoRA fine-tuning
│   ├── evaluate.py           ← base vs. fine-tuned comparison
│   └── inference.py          ← interactive inference
├── adapters/
│   └── hw-diagnostics/       ← trained LoRA adapter weights
├── results/
│   └── comparison.md         ← side-by-side evaluation results
├── models/                   ← (gitignored) downloaded/converted models
├── .gitignore
└── README.md
```

## 7. Timeline

With Claude Code assistance, the project is estimated at **3-5 days** of active work:

| Phase | Estimated Time | Description |
|---|---|---|
| Environment setup | 1-2 hours | Install MLX, download model, verify inference |
| Dataset generation | 3-4 hours | Generate, review, approve ~200-500 Q&A pairs |
| Fine-tuning | 1-2 hours | Run LoRA training (~30-90 min compute + iteration) |
| Evaluation | 1-2 hours | Generate comparisons, document results |
| Repo polish | 2-3 hours | README, structure, cleanup |
| **Total** | **~8-13 hours** | |

Optional stretch work (web UI, HuggingFace, deployment) adds 4-8 hours.

## 8. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| 16GB memory too tight for training | Start with Llama 3.2 3B at 4-bit — only ~2GB. LoRA adds minimal overhead. If tight, reduce batch size to 1. |
| Dataset quality insufficient for visible improvement | Focus on a narrow subdomain (e.g., JTAG/boundary scan only) where specialized answers clearly differ from generic base model responses. |
| MLX or mlx-lm version issues on M1 | Pin versions. MLX is mature on M1 as of early 2026. |
| Base model already knows hardware diagnostics well | Choose highly specific, niche topics where the base model gives vague or generic answers — the delta is the proof. |

## 9. Portfolio & Resume Value

### Interview Talking Points
- "I fine-tuned a Llama 3.2 model on domain-specific data using LoRA and Apple's MLX framework — on a consumer M1 iMac, no cloud GPU needed"
- "I built the training dataset from domain expertise in hardware test & diagnostics"
- "The fine-tuned model gives measurably better responses on specialized questions compared to the base model"

### Resume Line
> **LLM Fine-Tuning — Hardware Diagnostics Advisor:** Fine-tuned Llama 3.2 3B with LoRA adapters using Apple MLX on M1 hardware. Built domain-specific training dataset covering hardware test & diagnostics. Documented measurable improvement over base model with side-by-side evaluation.

### Target Roles This Supports
- AI/GenAI Consultant — "I can customize LLMs for domain-specific tasks"
- AI Instructor/Trainer — "I've done it myself on consumer hardware"
- Software Engineer (AI-augmented) — "I understand training, inference, deployment"
