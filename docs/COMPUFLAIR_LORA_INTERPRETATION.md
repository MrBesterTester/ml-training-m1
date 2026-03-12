# CompuFlair Interpretation of LoRA Fine-Tuning

**Date:** March 12, 2026
**Context:** Physics-first interpretation of what this project is actually doing, using the CompuFlair (Ardavan Borzou) framework: P = e^(-F) / Z

---

## Table of Contents

1. [The Framework](#the-framework)
2. [The Base Model as Thermodynamic Equilibrium](#the-base-model-as-thermodynamic-equilibrium)
3. [LoRA as Perturbation Theory](#lora-as-perturbation-theory)
4. [Training Dynamics as Annealing](#training-dynamics-as-annealing)
5. [4-Bit Quantization as Literal Quantization](#4-bit-quantization-as-literal-quantization)
6. [The Full Pipeline in CompuFlair Terms](#the-full-pipeline-in-compuflair-terms)
7. [Why This Matters for the Project](#why-this-matters-for-the-project)
8. [Source Materials](#source-materials)

---

## The Framework

CompuFlair's central thesis is that the entire field of ML can be interpreted through the Gibbs-Boltzmann equation:

```
P = e^(-F) / Z
```

Where F is the free energy (or loss/cost function) and Z is the partition function (normalization over all possible configurations). Training an ML model is equivalent to cooling a physical system — finding the low-energy configuration that best fits the data.

This document applies that lens to every component of our fine-tuning pipeline.

---

## The Base Model as Thermodynamic Equilibrium

**Llama 3.2 3B** was pre-trained on trillions of tokens. In the CompuFlair framework, this pre-training was a massive annealing process: the system (3 billion parameters) was heated (high learning rate, large batches, diverse data) and slowly cooled over weeks of training on clusters of GPUs, settling into a low-energy equilibrium across the loss landscape.

The result is a parameter configuration W₀ that sits in a deep, broad basin of the energy surface. The model's "knowledge" — grammar, reasoning patterns, factual recall — is encoded in the geometry of this basin. The curvature of the loss landscape around W₀ determines how the model responds to perturbations (new inputs).

Key insight: **the base model is a solved system.** Meta spent millions of dollars and weeks of GPU-cluster time carefully annealing 3 billion parameters into this equilibrium. It knows grammar, reasoning, conversation, world knowledge — an enormous amount of structure encoded in the curvature of that energy landscape.

Now you want it to also know about hardware diagnostics.

The brute-force approach — full fine-tuning — would unfreeze all 3 billion parameters and let them all move in response to your 252 training examples. In thermodynamic terms, **you'd be melting the entire system down and re-annealing it from scratch.** All that carefully achieved equilibrium — the grammar, the reasoning, the general knowledge — tossed back into the furnace because you wanted to add some expertise about JTAG chains.

That's insane. You don't melt down a cathedral because you want to add a room.

This is what makes LoRA so elegant, and frankly kind of funny once you see it through the physics lens: **don't melt it — perturb it.**

---

## LoRA as Perturbation Theory

This is the central physics insight of the entire project, and it's not just metaphorical — the mathematics are structurally identical.

### The Perturbation Framework

In quantum mechanics and statistical mechanics, perturbation theory handles problems of the form:

```
H = H₀ + λV
```

Where H₀ is the solved (unperturbed) Hamiltonian, V is a small perturbation, and λ controls the perturbation strength. You don't re-solve the full system — you compute corrections to the known solution.

LoRA does exactly this:

```
W = W₀ + ΔW = W₀ + BA
```

Where:
- **W₀** (frozen base weights) = the **ground state** / unperturbed solution H₀
- **ΔW = BA** (low-rank adapter matrices) = the **perturbation correction** λV
- **B ∈ ℝ^(d×r)** and **A ∈ ℝ^(r×k)** with rank **r << min(d, k)**

The rank r is the dimensionality of the perturbation subspace — how many "modes" of the system you allow to respond to the new data. In our configuration:

| Parameter | Value | Physics Analogy |
|---|---|---|
| Rank r | 8 | 8 perturbation modes per layer |
| Base weights W₀ | ~3B parameters, frozen | Ground state (solved, don't touch) |
| LoRA parameters | ~1-2M trainable | Perturbation corrections only |
| Compression ratio | ~1500:1 | Only 1 in 1500 degrees of freedom needs to move |

### Why This Works (The Deep Physics Point)

The success of a rank-8 perturbation tells us something fundamental about the geometry of the fine-tuning loss landscape: **the "distance" in parameter space between the base model's general-purpose solution and our hardware-diagnostics-specialist solution lies in a very low-dimensional subspace.**

In thermodynamic terms, the domain-specific knowledge occupies only a few "modes" of the full system. Most of the base model's energy landscape doesn't need to change — the grammar, the reasoning patterns, the conversational structure are all preserved in W₀. Only the domain-specific response patterns need adjustment, and those live in a subspace of dimension r × (number of adapted layers).

This is exactly what perturbation theory predicts: when the perturbation is small relative to the unperturbed system, first-order corrections capture most of the effect. Higher-order corrections (higher rank, more layers) give diminishing returns — just as in physics.

---

## Training Dynamics as Annealing

The gradient descent process on LoRA parameters maps directly to the thermodynamics of annealing:

### Temperature and Learning Rate

```
Learning rate η ↔ Temperature T
```

Our learning rate of **1e-5** is very low — this is a cold annealing process. We're making small, careful adjustments to the perturbation parameters, not violent rearrangements. In the Gibbs-Boltzmann framework, the probability of accepting a parameter update that increases the loss (energy) scales as:

```
P(accept) ∝ e^(-ΔF / T)
```

At low temperature (low learning rate), the system almost never accepts uphill moves. It follows the gradient downhill monotonically. This is appropriate because we're refining a perturbation to an already-good solution — we don't need to explore widely.

### Batch Size and Thermal Fluctuations

```
Batch size ↔ Inverse thermal noise
```

Our batch size of **2** is small, which means each gradient estimate is noisy — computed from only 2 examples rather than the full dataset. In thermodynamic terms, this injects stochastic noise into the annealing process:

- **Large batch** (many examples) = low noise = low effective temperature → system follows smooth gradient, may get trapped in local minima
- **Small batch** (few examples) = high noise = higher effective temperature → random kicks help escape shallow local minima

Batch size 2 is a deliberate choice: the noise acts as thermal fluctuations that help the perturbation parameters explore the low-dimensional subspace defined by the LoRA rank, without being so violent as to destabilize the solution.

### Iteration Count as Annealing Schedule

**600 iterations** defines our annealing schedule. With batch size 2 and ~200 training examples, each example is seen roughly 6 times (6 epochs). The system:

1. **Early iterations (0-100):** High loss, rapid descent — the perturbation parameters are moving from their random initialization toward the basin of good solutions. Like the early stages of cooling where the system loses energy quickly.

2. **Middle iterations (100-400):** Loss decreases more slowly — the system is settling into the basin, making finer adjustments. The perturbation correction is converging.

3. **Late iterations (400-600):** Loss plateaus — the system has found its equilibrium within the perturbation subspace. Further iterations are thermal fluctuations around the minimum.

---

## 4-Bit Quantization as Literal Quantization

The 4-bit quantization of the base model is perhaps the most satisfying physics analogy because it's not even an analogy — it's the same mathematical operation.

In quantum mechanics, quantization restricts a continuous observable to discrete values. In our case:

```
Continuous weight space ℝ → 16 discrete levels (4 bits = 2⁴ = 16 values)
```

Each parameter in the base model, which could take any real value, is mapped to one of 16 discrete levels. The information loss is bounded by the spacing between levels, exactly like the energy level spacing in a quantum harmonic oscillator determines the minimum resolvable energy.

The physics insight: quantization works because the information content of each individual weight is low. The model's knowledge is distributed across billions of parameters — no single parameter carries more than a few bits of meaningful information. Restricting each to 4 bits loses very little because the base model is already a low-temperature system where parameters cluster near their equilibrium values.

This is why 4-bit quantization preserves model quality while cutting memory by 4x: **you're not losing information about the ground state; you're just discretizing the coordinate system that describes it.**

---

## The Full Pipeline in CompuFlair Terms

Putting it all together, here's what our fine-tuning pipeline does, interpreted through the Gibbs-Boltzmann framework:

1. **Download base model:** Import a pre-solved thermodynamic system (W₀) that has been annealed to equilibrium by Meta's training infrastructure.

2. **Quantize to 4-bit:** Discretize the state space — map continuous parameters to 16 levels per weight. Information loss is minimal because the system is already at equilibrium.

3. **Initialize LoRA adapters:** Create a low-dimensional perturbation subspace (rank 8 per layer). Initialize to zero — the perturbation starts as "no change."

4. **Training (annealing):** Cool the perturbation parameters from their initial state toward a minimum of the domain-specific loss. Learning rate 1e-5 (cold), batch size 2 (moderate noise for exploration), 600 iterations (complete annealing schedule).

5. **Inference with adapters:** The final model computes W = W₀ + BA at each adapted layer. The base model's ground state is perturbed by the learned correction, producing domain-specialized outputs while preserving the base model's general capabilities.

---

## Why This Matters for the Project

This interpretation isn't just intellectual decoration. It explains:

- **Why LoRA is the right choice for M1 16GB hardware:** Perturbation theory requires orders of magnitude less computation than solving the full problem. We train ~1-2M parameters instead of 3B.

- **Why 4-bit quantization doesn't destroy the model:** You're discretizing an equilibrium system — the quantization noise is small compared to the inter-basin energy barriers that encode the model's knowledge.

- **Why the fine-tuned model can be a specialist without forgetting general skills:** The base weights (ground state) are frozen. The perturbation (LoRA adapters) adds domain knowledge without disrupting the solved equilibrium.

- **Why our hyperparameters are what they are:** Low learning rate (cold annealing for refinement), small batch (thermal noise for exploration), moderate iterations (complete but not excessive annealing).

Understanding the physics makes you a better practitioner — not just of hardware diagnostics, but of ML itself. That's the CompuFlair thesis.

---

## Source Materials

This interpretation draws on:
- **CompuFlair (Ardavan Borzou):** P = e^(-F)/Z as the unifying framework for ML. Physics-first pedagogy.
- **Vanchurin:** Learning dynamics as fundamental physics. Hamiltonian = loss function.
- **Brunton:** Physics-informed ML (five-stage framework). Hard vs. soft constraints.

See `Compu-Flair/` directory and `Physics ML - Vanchurin-Comput-flare/` for primary source documents.
