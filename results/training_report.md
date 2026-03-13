# LoRA Fine-Tuning Report — Hardware Diagnostics LLM

**Date:** 2026-03-12 (10:11 PM – 10:58 PM PST)
**Status:** Successful
**REQ:** REQ-020 (retry of REQ-019 after Metal OOM crash)

---

## Table of Contents

- [Executive Summary](#executive-summary)
- [Configuration](#configuration)
- [Dataset](#dataset)
- [Training Curve](#training-curve)
- [Convergence Analysis](#convergence-analysis)
- [Resource Utilization](#resource-utilization)
- [Output Artifacts](#output-artifacts)
- [Baseline Comparison (Pre-Training)](#baseline-comparison-pre-training)
- [Next Steps](#next-steps)

---

## Executive Summary

LoRA fine-tuning of Llama 3.2 3B Instruct (4-bit quantized) completed in **~47 minutes** on an M1 iMac with 16 GB unified memory. Validation loss dropped **27.5%** (2.809 to 2.037) over 600 iterations with no signs of overfitting. Peak memory usage was 3.621 GB — well within the 16 GB hardware constraint.

This was a retry of REQ-019, which crashed with a Metal memory error during the first attempt. The fix was simply closing all other applications to free unified memory.

---

## Configuration

| Parameter | Value | Notes |
|---|---|---|
| Base model | Llama 3.2 3B Instruct | 4-bit quantized via MLX (~2 GB) |
| Framework | Apple MLX + mlx-lm | Native Apple Silicon, no CUDA |
| Fine-tune method | LoRA | Low-Rank Adaptation |
| LoRA rank | 8 | 8 modes per adapted layer |
| LoRA scale | 20.0 | Alpha/rank scaling factor |
| LoRA dropout | 0.0 | No dropout |
| Adapted layers | 8 | Top 8 transformer layers |
| Trainable params | 3.473M / 3,212.750M | 0.108% of total model |
| Optimizer | Adam | Default MLX config |
| Learning rate | 1e-5 | Constant (no schedule) |
| Batch size | 1 | Reduced from 2 to avoid OOM |
| Gradient checkpointing | Yes | Trades compute for memory |
| Max sequence length | 2048 | Default; data max ~1264 tokens |
| Iterations | 600 | ~1.95 epochs over training set |
| Eval interval | Every 200 iters | 25 validation batches per eval |
| Checkpoint interval | Every 100 iters | 6 checkpoints + final |

---

## Dataset

| Split | Examples | Source |
|---|---|---|
| Training | 308 | `data/train.jsonl` |
| Validation | 77 | `data/valid.jsonl` |
| **Total** | **385** | 80/20 split |

The dataset contains 385 physics-grounded Q&A pairs across 12 hardware diagnostics categories, formatted in Alpaca chat template. Topics span signal integrity, thermal analysis, boundary scan, power distribution, memory testing, and more — each answer grounded in first-principles physics rather than rote procedures.

---

## Training Curve

### Validation Loss (evaluated every 200 iterations)

```
Val Loss
2.81 |*
     |
2.60 |
     |
2.40 |
     |
2.20 |
2.15 |          *
2.06 |                    *
2.04 |                              *
     +----------+---------+---------+--
     0         200       400       600   Iter
```

| Iter | Val Loss | Delta | % Improvement |
|------|----------|-------|---------------|
| 1 | 2.809 | — | — |
| 200 | 2.153 | -0.656 | -23.3% |
| 400 | 2.063 | -0.090 | -4.2% |
| 600 | 2.037 | -0.026 | -1.3% |

### Training Loss (sampled every 10 iterations)

| Iter | Train Loss | Notes |
|------|-----------|-------|
| 10 | 2.724 | Starting point |
| 100 | 2.138 | Rapid initial descent |
| 200 | 2.359 | Fluctuation (normal for batch=1) |
| 300 | 2.145 | Stabilizing |
| 400 | 2.101 | Entering plateau |
| 500 | 2.019 | Slow continued improvement |
| 600 | 1.925 | Final |

---

## Convergence Analysis

**Loss reduction:** 27.5% val loss improvement (2.809 → 2.037), 29.3% train loss improvement (2.724 → 1.925).

**Overfitting check:** The gap between final train loss (1.925) and final val loss (2.037) is only **0.112** — a healthy sign. The model is generalizing well, not memorizing. This is expected with LoRA since only 0.108% of parameters are trainable, which acts as a strong implicit regularizer.

**Diminishing returns:** The learning curve follows a classic exponential decay pattern:
- **Iter 0–200:** Captured 85% of total improvement (-0.656 of -0.772 total val loss reduction)
- **Iter 200–400:** Captured 12% (-0.090)
- **Iter 400–600:** Captured 3% (-0.026)

The model is approaching its capacity for this dataset and LoRA configuration. Further training at this learning rate would yield minimal improvement. To push further, options include: increasing LoRA rank, adapting more layers, augmenting the dataset, or using a learning rate schedule with warm restarts.

**Batch-1 noise:** With batch_size=1, individual training loss values fluctuate significantly (e.g., iter 120: 2.397, iter 130: 2.235, iter 140: 2.172). This is expected — each gradient update is computed from a single example. The overall trend is clearly downward despite the noise, and the validation loss (computed over 25 batches) shows smooth monotonic improvement.

---

## Resource Utilization

| Metric | Value |
|---|---|
| Wall-clock time | ~47 minutes |
| Training time | ~43.5 min (600 iters at ~0.23 it/sec) |
| Validation time | ~3.5 min (4 evals x ~55 sec each) |
| Peak memory | 3.621 GB (22.6% of 16 GB) |
| Throughput | 132–148 tokens/sec (improving as caches warm) |
| Total tokens processed | 364,420 |
| Avg tokens/iteration | ~607 |

Memory peaked at iteration 150 (3.621 GB) and stayed there — the Metal allocator found its ceiling and held steady. At 22.6% of the 16 GB unified memory, there's substantial headroom. The OOM crash in the first attempt (REQ-019) was likely caused by other applications competing for the same unified memory pool, not by the training itself.

---

## Output Artifacts

| File | Size | Description |
|---|---|---|
| `adapters/hw-diagnostics/adapters.safetensors` | 13.9 MB | Final adapter weights (iter 600) |
| `adapters/hw-diagnostics/0000100_adapters.safetensors` | 13.9 MB | Checkpoint at iter 100 |
| `adapters/hw-diagnostics/0000200_adapters.safetensors` | 13.9 MB | Checkpoint at iter 200 |
| `adapters/hw-diagnostics/0000300_adapters.safetensors` | 13.9 MB | Checkpoint at iter 300 |
| `adapters/hw-diagnostics/0000400_adapters.safetensors` | 13.9 MB | Checkpoint at iter 400 |
| `adapters/hw-diagnostics/0000500_adapters.safetensors` | 13.9 MB | Checkpoint at iter 500 |
| `adapters/hw-diagnostics/0000600_adapters.safetensors` | 13.9 MB | Checkpoint at iter 600 |
| `adapters/hw-diagnostics/adapter_config.json` | 1 KB | Full configuration |
| `results/training_log.txt` | 189 lines | Raw training output |

All checkpoint files are identical in size (13.9 MB) because the LoRA architecture is fixed — only the learned parameter values change between checkpoints.

---

## Baseline Comparison (Pre-Training)

Before training, the base model was evaluated on 9 prompts (4 conceptual Q&A, 5 numerical diagnostics). Full results are in [`results/baseline_responses.md`](baseline_responses.md).

### Conceptual Q&A (4 prompts)

The base model produced **generic but coherent** answers. It could discuss boundary scan testing, ECC memory, PCIe errors, and black-screen diagnostics at a surface level — but with no physics grounding, no mention of underlying principles, and occasional inaccuracies (e.g., defining boundary scan as "scanning the edges and corners of the board").

### Numerical Diagnostics (5 prompts) — Where the Base Model Fails

The base model **failed badly** on all five numerical diagnostic prompts:

| Prompt | Base Model Failure Mode |
|---|---|
| TDR impedance sweep | Hallucinated an entire S11 reflection table that wasn't in the input |
| Boundary scan interconnect | Miscounted: claimed 8/10 passed when failures appeared in 5/10 runs; wrong failure rates |
| Thermal survey | Verbatim paragraph duplication; fabricated "fan speed" data not in input |
| ADC code density | Reformatted data into meaningless percentages; completely missed the stuck-bit pattern at mid-scale |
| Voltage margining | Repeated "ICs functioned normally" for every passing step; no actual analysis of the 5-step fail region |

**This is the key gap the fine-tuning aims to close:** teaching the model to read numerical data, identify anomalies, and ground its analysis in physics — not hallucinate, parrot, or reformat.

---

## Next Steps

The training run is complete, but **loss numbers alone don't validate quality**. The critical remaining steps are:

1. **Verify fine-tuned inference** (TODO step 3.2) — Run the same 9 baseline prompts through the fine-tuned model and compare responses qualitatively
2. **Evaluation script** (TODO step 4.1) — Automated side-by-side comparison of base vs. fine-tuned outputs
3. **Human review** — Especially on the numerical diagnostics prompts where the base model failed; does the fine-tuned model actually identify anomalies and explain the physics?

The 6 checkpoint files also enable **checkpoint comparison** — if the final model shows any degradation, earlier checkpoints (especially iter 200, which captured 85% of the improvement) can be evaluated as alternatives.

---

*Report generated 2026-03-13. Training log: [`results/training_log.txt`](training_log.txt). Baseline: [`results/baseline_responses.md`](baseline_responses.md).*
