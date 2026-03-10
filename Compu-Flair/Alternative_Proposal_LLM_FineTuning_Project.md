# Alternative Proposal: LLM Fine-Tuning Portfolio Project

**Date:** March 9, 2026
**Goal:** Close Sam's ML/LLM training experience gap with a focused, high-impact portfolio piece on samkirk.com — in 1-2 weeks, not 18.

---

## The Problem This Solves

Sam's first job applications (Anthropic, Anyscale) were a stretch because he couldn't demonstrate hands-on ML or LLM training experience. The original proposal (CompuFlair + Kaggle House Prices) addresses this directionally but lands too low — Ridge regression on house prices is the "Hello World" of ML. It won't convince anyone that Sam can work in the modern AI stack.

What *will* convince them: fine-tuning a real LLM on Sam's M1 iMac using the same tools and techniques that production AI teams use — LoRA adapters, quantized models, MLX, HuggingFace — and deploying it as a live, interactive demo.

## Why This Works for Sam's Target Roles

| Target Role | What This Project Demonstrates |
|---|---|
| AI/GenAI Consultant | "I can customize LLMs for domain-specific tasks — not just prompt them" |
| AI Instructor/Trainer | "I've done it myself, on consumer hardware, and can teach you how" |
| Software Engineer (AI-augmented) | "I understand the full stack: training, inference, deployment" |
| A.Team / Freelance AI Builder | "I ship AI features, not just talk about them" |

## The Project: Domain-Expert LLM Fine-Tuning

### Concept

Fine-tune a small open-source LLM (3B-8B parameters) with LoRA adapters to become a **hardware test & diagnostics advisor** — a domain where Sam has 40+ years of irreplaceable expertise that no foundation model has seen in its training data. This creates a uniquely compelling demo: *a veteran engineer teaching an AI his craft.*

### Why This Domain

- Sam's hardware test knowledge is deep, specialized, and poorly represented in LLM training corpora
- The contrast between "45 years of domain expertise" and "modern AI fine-tuning" is a powerful narrative
- It's authentic — not a tutorial exercise, but a genuine application of Sam's knowledge
- Interview talking point: "I built a model that knows things about hardware diagnostics that GPT-4 doesn't"

---

## Phase 1: Data Preparation (Days 1-3)

### Task: Build a fine-tuning dataset from Sam's domain expertise

Create a dataset of ~200-500 instruction/response pairs covering hardware test and diagnostics topics. Sources:

1. **Sam's own knowledge** — Claude Code interviews Sam and generates Q&A pairs:
   - "How do you diagnose intermittent failures in boundary scan testing?"
   - "What's the right approach to test coverage analysis for a mixed-signal board?"
   - "When should you use JTAG vs. functional test for fault isolation?"

2. **Sam's resume and project history** — extract scenarios from real projects:
   - Talis BioMedical: embedded diagnostics for medical devices
   - Previous roles: test automation frameworks, firmware validation

3. **General test engineering knowledge** — standard practices Sam can validate and refine

### Output Format (JSONL, Alpaca-style)

```json
{
  "instruction": "A boundary scan test is passing on the bench but failing intermittently in production. What diagnostic steps would you take?",
  "input": "",
  "output": "First, I'd look at the environmental differences between bench and production. Boundary scan is sensitive to signal integrity, so check: (1) Are the TCK frequencies the same? Production lines sometimes run faster clocks. (2) Cable lengths and impedance — bench setups often have shorter, better-shielded JTAG cables. (3) Power supply noise — production environments can have more EMI. (4) Temperature — if the production floor is warmer, you might be hitting timing margins. I'd start by capturing the failing scan chain data and comparing it bit-by-bit to the passing bench data to identify which cells are failing, then work backward to the physical cause."
}
```

### Tools
- Claude Code (to interview Sam and format responses)
- Python script to validate JSONL format
- No external data needed — this is Sam's expertise

---

## Phase 2: Fine-Tuning with MLX (Days 4-7)

### Task: LoRA fine-tune a quantized model on Sam's M1 iMac

#### Base Model Selection

| Model | Parameters | Quantized Size | M1 16GB Feasible? | Notes |
|---|---|---|---|---|
| **Llama 3.2 3B** | 3B | ~2GB (4-bit) | Yes, comfortable | Best for M1 16GB |
| Mistral 7B v0.3 | 7B | ~4GB (4-bit) | Yes, tight | Good quality, fits |
| Phi-3 Mini 3.8B | 3.8B | ~2.5GB (4-bit) | Yes, comfortable | Microsoft, strong reasoning |
| Qwen 2.5 3B | 3B | ~2GB (4-bit) | Yes, comfortable | Multilingual bonus |

**Recommendation:** Start with **Llama 3.2 3B** (4-bit quantized). Comfortable on 16GB, fast iterations, well-supported by MLX.

#### Fine-Tuning Script

```bash
# Install MLX and MLX-LM
pip install mlx mlx-lm

# Download the base model (one-time)
python -m mlx_lm.convert \
  --hf-path meta-llama/Llama-3.2-3B-Instruct \
  --mlx-path ./models/llama-3.2-3b-4bit \
  --quantize --q-bits 4

# Fine-tune with LoRA
python -m mlx_lm.lora \
  --model ./models/llama-3.2-3b-4bit \
  --data ./data \
  --train \
  --iters 600 \
  --batch-size 2 \
  --lora-layers 8 \
  --learning-rate 1e-5 \
  --adapter-path ./adapters/hw-diagnostics
```

#### What's Happening Under the Hood (Interview Talking Points)

- **LoRA (Low-Rank Adaptation):** Instead of updating all 3B parameters, we freeze the base model and train small adapter matrices (rank 8-16) that modify the attention layers. This reduces trainable parameters from billions to ~1-2 million.
- **Quantization:** 4-bit quantization reduces the model's memory footprint by 4x with minimal quality loss. The M1's unified memory architecture means the GPU can access the full model without PCIe transfer bottlenecks.
- **MLX:** Apple's framework uses lazy evaluation and unified memory natively — no `.to(device)` calls, no CPU-GPU data copying. The model trains where it lives.

#### Expected Training Time on M1 iMac
- ~200-500 examples, 600 iterations, batch size 2
- Estimated: **30-90 minutes** total
- Sam can iterate multiple times per day

#### Evaluation
- Hold out 20% of the dataset for evaluation
- Compare base model vs. fine-tuned model on the same prompts
- Measure: Does the fine-tuned model give more specific, accurate, and actionable hardware diagnostics advice?
- Generate a comparison table showing before/after responses

---

## Phase 3: Interactive Demo for samkirk.com (Days 8-12)

### Option A: Static Demo Page (Simplest — No Server Needed)

Build an HTML page for samkirk.com that showcases the project:

- **Side-by-side comparisons:** Base model vs. fine-tuned model answering the same hardware diagnostics questions
- **Training metrics:** Loss curves, evaluation scores, training time on M1
- **Architecture diagram:** LoRA adapter visualization, MLX pipeline
- **Code snippets:** Key parts of the training script with explanations
- **The dataset philosophy:** How Sam's 40+ years of expertise became training data

This is the fastest path to a portfolio piece and requires zero infrastructure.

### Option B: Live Inference Demo (More Impressive, Needs Hosting)

Deploy the fine-tuned model behind a simple chat interface:

- **Frontend:** React/TypeScript (Sam's existing skills) — simple chat UI
- **Backend:** Python FastAPI server running MLX inference
- **Hosting options:**
  - Sam's M1 iMac as a local server (simplest, but only works when Mac is on)
  - A cloud VM with an M-series chip (e.g., AWS Graviton or a Mac cloud instance)
  - Export to GGUF format and host on a free HuggingFace Space with llama.cpp

### Option C: Hybrid (Recommended)

- Static demo page on samkirk.com (always available)
- HuggingFace model card + adapter weights published publicly
- Optional: HuggingFace Space with a Gradio interface for live inference (free tier)

---

## Phase 4: Publish & Document (Days 12-14)

### HuggingFace Model Card

Publish the LoRA adapters to HuggingFace Hub with a proper model card:

- Model name: `samkirk/hw-diagnostics-advisor-llama3.2-3b-lora`
- Training details: hardware (M1 iMac), framework (MLX), hyperparameters
- Dataset description (without exposing proprietary knowledge)
- Example outputs
- License

### samkirk.com Portfolio Page

Add a new project page to samkirk.com with:

- Project narrative: "Teaching an AI my 40 years of hardware diagnostics expertise"
- Technical details: LoRA, quantization, MLX, Apple Silicon
- Results: before/after comparisons
- Link to HuggingFace model card
- Link to live demo (if Option B or C)

### Resume Line Item

Add to resume under SAK Consulting (2022-Present):

> **LLM Fine-Tuning — Hardware Diagnostics Advisor:** Fine-tuned Llama 3.2 3B with LoRA adapters using Apple MLX on M1 hardware. Built domain-specific training dataset from 40+ years of test engineering expertise. Deployed interactive demo on samkirk.com. Published model adapters on HuggingFace.

---

## What This Costs

| Item | Cost |
|---|---|
| MLX, Python, Claude Code | $0 (already have) |
| Llama 3.2 3B model | $0 (open source, Meta license) |
| HuggingFace account | $0 (free tier) |
| HuggingFace Space (Gradio) | $0 (free tier, CPU inference) |
| Sam's time | ~1-2 weeks, ~30 hrs total |
| **Total** | **$0** |

## What This Does NOT Require

- No cloud GPU rental
- No NVIDIA hardware
- No CompuFlair subscription
- No 18-week roadmap
- No Kaggle competition entry

---

## How This Compares to the Original Proposal

| Dimension | Original (House Prices + CompuFlair) | Alternative (LLM Fine-Tuning) |
|---|---|---|
| **Time to portfolio piece** | 6-8 weeks minimum (Phase 1-2) | 1-2 weeks |
| **Impressiveness** | Entry-level ML (every bootcamp does this) | Modern AI stack (LoRA, quantization, MLX) |
| **Relevance to target roles** | Low — classical ML isn't the gap | High — LLM fine-tuning is exactly the gap |
| **Uniqueness** | Kaggle tutorial project | Sam's 40-year domain expertise as training data |
| **Interview narrative** | "I did a Kaggle project" | "I taught an LLM my craft" |
| **Resume impact** | Weak — shows ML basics | Strong — shows LLM training, deployment, HuggingFace |
| **Cost** | $0 (+ optional CompuFlair sub) | $0 |
| **M1 feasibility** | Excellent | Excellent |

---

## Suggested Next Steps

1. **Sam reviews and approves this plan** (or modifies scope/domain)
2. **Day 1:** Set up MLX environment, download base model, verify inference works on M1
3. **Days 1-3:** Claude Code interviews Sam to build the training dataset
4. **Days 4-7:** Fine-tune, evaluate, iterate on dataset quality
5. **Days 8-12:** Build demo page, publish to HuggingFace
6. **Days 12-14:** Update samkirk.com, update resume

The CompuFlair physics curriculum remains valuable for deeper ML understanding and can be pursued in parallel as personal enrichment — but this project ships a portfolio piece *now*, when Sam needs it most.

---

*Proposal generated March 9, 2026 — Claude Code (Career Agent System)*
