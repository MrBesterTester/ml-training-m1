# The Mathematical Mechanism of LoRA: Normal Modes and Layer Hierarchies

**Date:** March 13, 2026
**Context:** A deeper physics-math treatment of LoRA's internal mechanism, complementing the thermodynamic interpretation in `docs/COMPUFLAIR_LORA_INTERPRETATION.md`. Where that document asks "what is LoRA doing to the system as a whole?" (answer: perturbation theory), this document asks "what is happening inside each adapted layer, and why these layers?"

---

## Table of Contents

1. [The Two Decompositions](#the-two-decompositions)
2. [Within Each Layer: Normal Mode Analysis](#within-each-layer-normal-mode-analysis)
3. [Across Layers: The Feature Hierarchy](#across-layers-the-feature-hierarchy)
4. [Resolving the Apparent Paradox](#resolving-the-apparent-paradox)
5. [Implications for This Project](#implications-for-this-project)

---

## The Two Decompositions

LoRA involves two independent structural choices, and they answer different questions:

| Choice | Question | Our Config | Physics Analogy |
|--------|----------|------------|-----------------|
| **Rank** (r = 8) | How many independent correction modes per layer? | 8 modes | Normal mode truncation |
| **Which layers** (top 8 of 32) | Where in the network to apply the correction? | Layers 25–32 | Spatially localized perturbation |

These are orthogonal axes of the same system. Confusing them leads to a paradox we'll resolve below.

---

## Within Each Layer: Normal Mode Analysis

### The SVD Connection

Any matrix can be decomposed via the Singular Value Decomposition:

```
M = UΣVᵀ = σ₁u₁v₁ᵀ + σ₂u₂v₂ᵀ + σ₃u₃v₃ᵀ + ...
```

where σ₁ ≥ σ₂ ≥ σ₃ ≥ ... are the singular values (the "energies" of each mode), and uᵢ, vᵢ are the corresponding basis vectors (the "mode shapes"). Each term σᵢuᵢvᵢᵀ is an independent rank-1 component — a single mode of the matrix.

This is structurally identical to a normal mode expansion of a vibrating system. In vibration analysis, any complex motion decomposes into independent modes, each with its own frequency (energy) and shape. The first few modes — the ones with the most energy — capture most of the system's behavior.

### LoRA as Truncated SVD

The correction LoRA learns for each adapted weight matrix is:

```
ΔW = BA
```

where B ∈ ℝ^(d×r) and A ∈ ℝ^(r×d), with r = 8. This product BA is a matrix of rank at most r. Written in SVD form:

```
ΔW = BA ≈ σ₁u₁v₁ᵀ + σ₂u₂v₂ᵀ + ... + σ₈u₈v₈ᵀ
```

LoRA doesn't compute an SVD explicitly — gradient descent finds the B and A that minimize the training loss. But the result is equivalent: the learned correction is constrained to rank 8, which means it can express at most 8 independent modes of adjustment to the original weight matrix.

### What Each Mode Does

Think of matrix A as a **measurement operator** and matrix B as a **reconstruction operator**:

```
Input x (d-dimensional)
    │
    ▼
  A(x) ──→ 8-dimensional "fingerprint" (what matters about this input for our correction)
    │
    ▼
  B(A(x)) ──→ d-dimensional correction (projected back to the layer's output space)
```

The 8-dimensional bottleneck is an information bottleneck. A learns to extract the 8 most relevant features of the input for the task of "make this layer's output more hardware-diagnostics-appropriate." B learns to turn those 8 features into a correction vector in the full output space.

This is the same structure as a rank-8 filter bank: 8 parallel channels, each sensitive to a different pattern in the input, each contributing its own correction to the output.

### Why Rank 8 Is Enough

The claim implicit in choosing r = 8 is: **the correction needed to each weight matrix lives in a low-dimensional subspace.**

In normal mode terms: the singular value spectrum of ΔW decays rapidly. The first 8 singular values capture the vast majority of the correction's "energy" (Frobenius norm). The remaining singular values — the higher modes — contribute corrections so small they're below the noise floor of the training process.

Empirically, our training run confirmed this: val loss dropped 27.5% with just 8 modes per layer (3.47M parameters out of 3.2B). If the needed correction were high-rank — if many independent modes were required — rank 8 wouldn't capture enough of the correction and the loss wouldn't budge.

The physics interpretation: **the "distance" between a general-purpose LLM and a hardware diagnostics specialist, measured within any single weight matrix, is well-approximated by 8 basis vectors.** Most of the correction's energy is concentrated in a handful of modes, just as most of a vibrating structure's energy is concentrated in its fundamental frequencies.

---

## Across Layers: The Feature Hierarchy

### The CNN Precedent

The layer hierarchy in neural networks was first understood through convolutional networks for vision, which more or less recapitulate the structure of biological visual processing discovered by Hubel and Wiesel in the 1960s:

| Depth | CNN Features | Biological Vision |
|-------|-------------|-------------------|
| Layer 1–2 | Edges, oriented gradients | Simple cells (V1) |
| Layer 3–5 | Textures, patterns, corners | Complex cells (V1/V2) |
| Layer 6–10 | Object parts, component shapes | V4, inferotemporal cortex |
| Final layers | Object identity, scene semantics | High-level recognition areas |

The critical observation for transfer learning: **early layers are universal, late layers are task-specific.** A CNN trained on ImageNet to classify dogs will learn edge detectors in layer 1 that are just as useful for classifying tumors in X-rays. But its final layers — the ones that encode "this combination of features means golden retriever" — are useless for radiology.

This is why classical transfer learning in vision freezes the early layers and replaces or fine-tunes the final layers. The early features transfer across tasks because they're general-purpose; the late features need to be relearned because they're task-specific.

### The Same Hierarchy in Transformers

Transformer LLMs exhibit the same depth gradient, despite having a completely different architecture:

| Depth | Transformer Function | Analogue |
|-------|---------------------|----------|
| Layers 1–8 | Token embeddings, basic syntax, local patterns | Edge detection — structural primitives |
| Layers 9–20 | Grammar, coreference, semantic relationships | Texture/part recognition — compositional structure |
| Layers 21–28 | Abstract reasoning, domain knowledge, style | Object recognition — high-level meaning |
| Layers 29–32 | Task-specific output shaping, response formatting | Classification head — final decision |

Research on transformer internals (probing classifiers, activation patching, causal tracing) consistently finds this pattern: syntactic information is concentrated in early-to-middle layers, while semantic and task-specific information is concentrated in late layers.

### Why LoRA Adapts the Top Layers

Our configuration adapts layers 25–32 (the top 8 of 32). The physics reasoning:

**The deep layers encode the equivalent of Fourier fundamentals for language** — the basic structural modes (syntax, grammar, token relationships) that every language task requires. These are like the edge detectors in a CNN: universal, transferable, and already optimally learned during pre-training. Perturbing them risks destabilizing the entire system for negligible gain.

**The top layers encode domain-specific abstractions** — the high-level features that determine *what kind* of response the model produces. This is where "general helpful assistant" becomes "hardware diagnostics specialist." The correction needed to shift domain behavior lives here, not in the syntactic machinery below.

This is a spatially localized perturbation: perturb the surface (where the system interacts with the task), leave the bulk (structural foundation) alone.

---

## Resolving the Apparent Paradox

Here is a question that seems paradoxical at first:

> In harmonic / Fourier analysis, the fundamental modes (lowest frequency, most energy) come first. In neural networks, the fundamental features (most basic, most universal) are also in the first layers. But we're adapting the LAST layers, not the first. And we said the rank-8 modes are like keeping the "fundamental harmonics" of the correction. So which end is fundamental?

The resolution: **"fundamental" means different things on the two axes.**

### Along the layer axis (1 → 32): compositional hierarchy

Layers are ordered by **abstraction level**, not by importance or energy. Layer 1 isn't the "most important" layer — it's the most basic. Each successive layer composes the representations of the previous one into higher-level abstractions. This is a compositional hierarchy, like:

```
atoms → molecules → cells → organs → organisms
```

You don't adapt the atoms when you want the organism to specialize. The atoms are fine. You adapt the high-level organizational principles — the later, more abstract layers.

### Along the rank axis (mode 1 → 8): energy hierarchy

Within each adapted layer, the 8 modes are ordered by **correction energy** (singular value magnitude). Mode 1 carries the most correction energy — it's the dominant direction the weight matrix needs to shift. Mode 8 carries the least. This is the classical harmonic ordering: fundamental first, overtones after.

### The two axes are orthogonal

```
                    Layer axis (compositional: basic → abstract)
                    ─────────────────────────────────────────────►
                    Layer 1    Layer 16    Layer 25    Layer 32
                    (syntax)   (semantics) (domain)    (output)
Rank axis       ▲
(energy:        │  mode 1 ─── not ──────── adapted ── adapted ──
dominant →      │  mode 2     adapted      (largest    (largest
least)          │  mode 3                   singular    singular
                │  ...                      values      values
                │  mode 8                   here)       here)
```

The rank-8 modes are "fundamental" in the energy sense — they capture the most correction — but they operate within the layers that sit at the abstract end of the compositional hierarchy. There's no contradiction: one axis is about which layers need correcting (the abstract ones), the other is about how efficiently you can represent that correction (8 modes suffice).

---

## Implications for This Project

### What the training run told us

Our results (val loss 2.809 → 2.037 with rank 8, top 8 layers) confirm two empirical claims:

1. **The hardware diagnostics correction is low-rank.** Eight modes per layer captured enough of the needed adjustment to reduce val loss by 27.5%. The correction's singular value spectrum decays fast enough that modes 9+ contribute negligibly.

2. **The correction is concentrated in the upper layers.** Adapting 8 of 32 layers (25%) was sufficient. The lower 24 layers — the syntactic and basic semantic machinery — didn't need to change for the model to learn hardware diagnostics.

### What this means for future iterations

If we wanted to push further, the two axes suggest different strategies:

| Strategy | What it does | When to try it |
|----------|-------------|----------------|
| Increase rank (e.g., 16 or 32) | More modes per adapted layer — captures finer correction structure | If the model gets the general domain right but lacks nuance |
| Adapt more layers (e.g., 16 of 32) | Push the perturbation deeper into semantic layers | If the model needs to change how it reasons about the domain, not just what it says |
| Both | More parameters, richer correction | If the dataset grows substantially and can support it |

The 600-iteration loss curve showed clear diminishing returns after iter 200 (85% of improvement already captured). This suggests the current rank and layer count have extracted most of the available signal from 385 training examples. More data — not more parameters — is likely the next leverage point.

---

*This document extends the thermodynamic interpretation in `docs/COMPUFLAIR_LORA_INTERPRETATION.md` with the mathematical mechanism of LoRA and the physics of neural network layer hierarchies. Together they provide two complementary views: the thermodynamic view (what LoRA does to the system as a whole) and the modal/structural view (what LoRA does inside each layer, and why those layers).*
