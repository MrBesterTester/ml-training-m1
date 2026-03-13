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

## LoRA Fine-Tuning: A Physics Interpretation

LoRA isn't just a memory optimization trick — it's **perturbation theory** applied to neural networks. The full physics interpretation with proper math notation and diagrams is in [`docs/COMPUFLAIR_LORA_INTERPRETATION.html`](docs/COMPUFLAIR_LORA_INTERPRETATION.html) (open in browser for KaTeX-rendered equations and SVG diagrams). Here's the core idea:

The pre-trained base model is a thermodynamic system that has already been annealed to a low-energy equilibrium — Meta spent millions of dollars and weeks of GPU time carefully cooling 3 billion parameters into this state. Full fine-tuning would unfreeze all of them and let them move in response to your 252 training examples. In physics terms, **you'd be melting the entire system down and re-annealing from scratch** — destroying all that carefully achieved equilibrium because you wanted to add some knowledge about JTAG chains. You don't melt down a cathedral to add a room.

**LoRA's insight: don't melt it — perturb it.** Freeze the solved system and learn a small correction:

```
W = W₀ + ΔW = W₀ + BA
```

- **W₀** (frozen base weights) = the ground state, the solved unperturbed system
- **ΔW = BA** (low-rank adapters, rank 8) = the first-order perturbation correction
- **~1-2M trainable parameters** out of 3B = only 1 in 1500 degrees of freedom moves

The training hyperparameters map directly to thermodynamic quantities:

| Hyperparameter | Value | Physics Interpretation |
|---|---|---|
| Learning rate | 1e-5 | Temperature — very cold annealing (careful refinement) |
| Batch size | 2 | Thermal noise — small batches inject stochastic fluctuations that help escape local minima |
| Iterations | 600 | Annealing schedule — ~6 epochs, enough for the perturbation to converge |
| LoRA rank | 8 | Perturbation dimensionality — 8 modes per layer respond to domain data |
| 4-bit quantization | 16 levels/param | Literal quantization — discretizing the state space of the ground state |

The deepest insight: **LoRA works because the distance between "general-purpose LLM" and "hardware diagnostics specialist" lies in a very low-dimensional subspace of parameter space.** Most of the energy landscape doesn't need to change — the domain knowledge occupies only a few modes of the full system.

## Project Status

**Phase 3 complete** — LoRA training finished (600 iterations, val loss 2.809 → 2.037). See the [training report](results/training_report.md) for full details.

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
│   ├── SPECIFICATION.md                  ← what we're building
│   ├── BLUEPRINT.md                      ← how to build it (step-by-step)
│   ├── TODO.md                           ← implementation checklist
│   ├── COMPUFLAIR_LORA_INTERPRETATION.html ← physics interpretation of LoRA (KaTeX + SVG)
│   └── COMPUFLAIR_LORA_INTERPRETATION.md  ← same content, plain markdown
├── Compu-Flair/
│   ├── Physics_of_LoRA.html              ← unified physics interpretation (thermodynamics + normal modes)
│   ├── Original_Proposal_CompuFlair.html ← original portfolio plan (physics-ML pedagogy)
│   └── Alternative_Proposal_LLM_FineTuning_Project.md ← pivot from CompuFlair curriculum to this project
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

## CompuFlair Source Materials

This project's physics-first approach draws on three bodies of work comparing physics and ML:

| Source | Location | What It Contains |
|---|---|---|
| **CompuFlair (Ardavan Borzou)** | `Compu-Flair/Original_Proposal_CompuFlair.html` | Portfolio plan inspired by Borzou's "P = e^(-F)/Z" framework — the idea that all of ML can be interpreted through the Gibbs-Boltzmann equation. Physics-first pedagogy for ML practitioners. |
| **Alternative Proposal** | `Compu-Flair/Alternative_Proposal_LLM_FineTuning_Project.md` | The pivot document: why LoRA fine-tuning on Sam's hardware diagnostics expertise is a stronger portfolio piece than the original CompuFlair curriculum path. This is the project's origin story. |
| **Vanchurin / CompuFlair / Brunton Comparison** | `../Physics ML - Vanchurin-Comput-flare/` (6 HTML documents) | Deep comparison of three approaches to physics-ML intersection: Vanchurin (learning dynamics *are* physics), Borzou/CompuFlair (physics as interpretive lens for ML), Brunton (embed physics into ML architectures). Includes the "Three Roles of the Hamiltonian" analysis. |

The CompuFlair curriculum itself remains a separate learning track. What this project adopts is the **explanatory style**: grounding every answer in the physical principles that govern the system, and interpreting the ML pipeline itself (LoRA, quantization, training dynamics) through the same physics lens.

## Future Direction: Test Result Interpretation

A natural next step is training the model to **interpret actual test program output** — power-on self-test, embedded diagnostics, manufacturing test, and field test results. In practice, so-called "diagnostic programs" rarely pinpoint failures on their own; they're really hardware test programs. True fault isolation requires running many tests and then doing substantial post-test analysis to correlate results and narrow down root causes.

This is a hard problem because test program output formats vary widely across platforms, vendors, and test environments. A future dataset expansion would need to account for that diversity. But it's where the real diagnostic value lives — bridging the gap between raw test output and actionable fault isolation.

## Author

Sam Kirk (with Claude Code)
