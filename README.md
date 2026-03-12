# Hardware Diagnostics LLM Fine-Tuning

Fine-tuning [Llama 3.2 3B](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) with LoRA on Apple MLX (M1 iMac, 16GB) to create a **hardware test & diagnostics advisor** that explains things the way a physicist-engineer would.

## The Core Idea: Physics-First Interpretation (CompuFlair-Inspired)

People constantly complain that ML and LLM results are opaque — that they can't understand what a model is doing or why it gives the answers it does. This project takes the position that **if you don't understand the foundational physics, you'll never understand the results.** Full stop.

The training data follows a **physics-first explanatory style** inspired by [CompuFlair's](https://compuflair.com) approach: every answer is grounded in the physical principles that govern the system. Not "check your impedance" but "impedance mismatches cause reflections because energy must be conserved at the boundary — the reflected wave carries the energy that can't propagate forward, governed by the reflection coefficient Gamma = (Z_L - Z_0) / (Z_L + Z_0)."

This isn't about making answers longer or more academic. It's about building **genuine understanding**:

- Signal integrity issues → transmission line theory, EM wave propagation, impedance matching
- Thermal failures → thermodynamics, Arrhenius acceleration models, heat transfer
- ICT measurements → circuit theory (Kirchhoff, Ohm), guarded measurement physics
- Test coverage gaps → information theory, entropy as a coverage metric
- Solder joint reliability → Coffin-Manson fatigue models, stress-strain mechanics
- Mixed-signal behavior → Nyquist sampling theory, noise physics, PLL dynamics

The result is a model that doesn't just know *what* to do — it knows *why*, and can explain the causal chain from physics to practical action. That's the difference between a lookup table and an engineer.

## Project Status

**In progress** — Phase 2 (Dataset Generation)

## Tech Stack

| Component   | Choice                                 | Why                                          |
| ----------- | -------------------------------------- | -------------------------------------------- |
| Base model   | Llama 3.2 3B Instruct, 4-bit quantized | Fits in 16GB unified memory (~2GB)           |
| Fine-tuning  | LoRA (Low-Rank Adaptation)             | ~1-2M trainable parameters, memory-efficient |
| Framework    | Apple MLX + mlx-lm                     | Native Apple Silicon, no CUDA needed         |
| Hardware     | M1 iMac, 16GB unified memory           | Consumer hardware — that's the point         |

## Project Structure

```text
ml_training_m1/
├── docs/
│   ├── SPECIFICATION.md    ← what we're building
│   ├── BLUEPRINT.md        ← how to build it (step-by-step)
│   └── TODO.md             ← implementation checklist
├── scripts/
│   ├── generate_dataset.py ← topic taxonomy, physics mappings, dataset generation
│   ├── qa_bank.py          ← 252 physics-grounded Q&A pairs (training data)
│   └── verify_inference.py ← base model inference verification
├── data/                   ← training/eval datasets (JSONL, Alpaca format)
├── adapters/               ← trained LoRA adapter weights
├── models/                 ← (gitignored) downloaded base models
└── results/                ← evaluation outputs, baseline responses
```

## Pipeline

1. **Environment Setup** — Python venv, MLX, mlx-lm, HuggingFace Hub
2. **Base Model** — Download & quantize Llama 3.2 3B to 4-bit MLX format
3. **Dataset** — 252 Q&A pairs across 12 hardware diagnostics categories, physics-grounded
4. **LoRA Training** — 600 iterations, batch 2, 8 LoRA layers, lr 1e-5
5. **Evaluation** — Side-by-side base vs. fine-tuned comparisons
6. **Publishing** — Static comparison page, HuggingFace upload

## Implementation Approach

This project uses the **parallel multi-agent strategy** for large content generation tasks. Rather than running one agent sequentially through hundreds of items, work is split across multiple parallel agents by category — dramatically reducing wall-clock time for bulk generation.

This pattern applies broadly: any time you need to generate large volumes of structured content (dataset entries, test cases, documentation), split by natural boundaries and run agents in parallel.

## Author

Sam Kirk (with Claude Code)
