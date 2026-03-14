---
id: REQ-030
title: "Evaluate and mitigate software-domain regression from hardware-only LoRA fine-tuning"
status: shelved
created_at: 2026-03-14T00:00:00Z
related: [REQ-028, REQ-029]
---

# Evaluate and Mitigate Software-Domain Regression from Hardware-Only LoRA Fine-Tuning

## What

The current LoRA adapter was trained exclusively on ~416 hardware diagnostics Q&A pairs. Analysis of the 12-prompt evaluation report (`web/evaluation-report.html`) reveals that while the fine-tuned model shows clear improvement on hardware topics, it would likely **regress or produce misleading output** on purely software-oriented questions. This REQ captures the problem, predicted failure modes, and recommended mitigations.

## Problem Analysis

### Observed Fine-Tuned Model Behaviors (from evaluation report)

The evaluation reveals three systemic patterns that predict software-domain failure:

1. **Domain vocabulary overfitting.** The model has learned to route toward hardware terms — TAP controllers, BSDL files, ESR values, thermal resistance, boundary scan. On prompts outside this vocabulary, the adapter weights have no useful signal and may actively interfere with the base model's existing knowledge.

2. **Degenerate repetition under uncertainty.** Entries #5 (TDR), #7 (Thermal), #9 (Voltage Margining), and #11 (MLCC vs Polymer) all show the fine-tuned model falling into repetitive loops. This happens most when the model has partial domain knowledge but insufficient signal to complete a coherent analysis. Software prompts would be maximally out-of-distribution, making repetition even more likely.

3. **Numerical reasoning gaps would persist — and transfer to software data.** The model already misses critical diagnostic findings in the hardware evaluation data. In every case, it can echo the vocabulary but cannot perform the analytical step of "this number is wrong and here's why."

   Specific failures from the evaluation report:

   - **TDR impedance anomaly (entry #5):** The data shows impedance dipping to 38.5 ohm at 44-52mm on a 50 ohm target — a 23% deviation in a 4mm region, a textbook discontinuity indicating a physical defect (damaged trace, bad via transition, or contamination). The fine-tuned model said "the impedance is within 0.5 ohm of the target at all distances." It narrated the nominal data and completely missed the anomaly.

   - **ADC stuck bit (entry #8):** Three consecutive missing codes at mid-scale (2047-2049) with adjacent codes absorbing double counts (code 2046: 512, code 2050: 518 vs expected ~256). This is a classic stuck-bit signature in the SAR ADC's MSB region. The fine-tuned model produced statistical vocabulary (confidence intervals, chi-squared) but never identified what the missing codes mean.

   - **Voltage margin spec violation (entry #9):** The board fails at all voltages below 3.14V, but the spec requires pass across +/-10% (down to 2.97V). The actual low-side margin is only (3.30 - 3.14) / 3.30 = 4.8%, less than half the required 10%. The fine-tuned model correctly found the pass/fail boundary at 3.14V but never flagged the spec non-compliance — the single most important conclusion in the data.

   Software-oriented numerical data — latency percentiles, memory allocation profiles, CPU flame graphs, database query plan costs, log frequency analysis — would hit the exact same wall. The model would narrate the data without identifying the anomaly, which is the entire point of presenting data to a diagnostic assistant.

4. **Predicted behavior on software-oriented prompts:**

| Software Prompt Type | Predicted Behavior |
|---|---|
| "Debug this Python traceback" | Base-model-level or slightly degraded — adapter has no relevant training signal, but adapter weights still modify attention patterns away from base model's software knowledge |
| "Review this API latency percentile data" | Would likely attempt hardware-style analysis (thermal gradients, R_th calculations) on latency numbers, producing confidently wrong output |
| "Explain microservices vs monolith" | Likely minimally affected — generic enough that adapter interference is low. But if the prompt touches "fault isolation" or "diagnostics," the adapter could pull the response toward hardware framing |
| "Parse this server log file for errors" | Might apply hardware "fault isolation" framing — could be accidentally useful (isolation is isolation) or confusingly hardware-centric ("check the boundary scan chain") |
| "This Kubernetes pod keeps crashing with OOMKilled" | High risk of TRIAGE-style misframing: the model might try to diagnose memory hardware rather than recognizing a software resource limit |
| "Review this database query plan" | Likely degraded — base model has strong SQL/query-plan knowledge that adapter weights would partially overwrite with irrelevant hardware signal |

### Root Cause

LoRA at this scale (~1-2M trainable parameters, 416 examples, rank 8, 8 layers) is a **narrow domain lens**. It sharpens the model on exactly what it saw in training and slightly blurs everything else. The adapter modifies attention weights in the target layers, and those modifications apply to *all* inputs, not just hardware-related ones. There is no gating mechanism that says "only apply these adapter weights when the input is about hardware."

## Connection to Existing REQs

### REQ-028 (v3 Diagnostic Mode Classification)

REQ-028's TRIAGE category is directly relevant. TRIAGE is defined as: *"Generally indicates a software problem, not hardware. The model should recognize when the issue is outside the hardware diagnostic domain and flag it as such."*

Phase 2 of REQ-028 calls for 20-30 new TRIAGE examples — scenarios that look like hardware but are actually software/firmware. **This is the same problem viewed from the other direction.** REQ-028 teaches the model to say "this is software, not hardware" when presented with ambiguous data. The current REQ asks: what happens when the model is given a *clearly* software question — does it even recognize it's out of domain?

REQ-028's TRIAGE expansion would partially mitigate this problem by teaching the model the concept of domain boundaries.

### REQ-029 (Dark Factory / Behavioral Scenarios)

REQ-029 identified adversarial evaluation as the applicable subset of the Dark Factory pattern. Specifically:

> "TRIAGE traps — scenarios that look like hardware but are actually software/firmware"

This is exactly the kind of holdout validation that would catch software-domain regression. A set of purely software-oriented prompts in the evaluation suite would quantify how much the adapter degrades non-hardware performance.

## Recommendations

### 1. Expand TRIAGE training in REQ-028 (already planned)
REQ-028 Phase 2 adds TRIAGE examples. Extend this to include **clearly software-only prompts** where the expected response is "This is a software issue — here's what I'd check: [software-appropriate steps]." This teaches the model domain awareness, not just domain knowledge.

### 2. Add software-domain regression prompts to the evaluation suite
Add 5-10 purely software-oriented prompts to the evaluation comparison (alongside the existing 12 hardware prompts). Run these against both the base model and fine-tuned model. If the fine-tuned model scores worse, that quantifies the regression cost.

Suggested evaluation prompts:
- A Python traceback with a clear bug (e.g., off-by-one, None reference)
- API latency data with an obvious outlier
- A Kubernetes/Docker resource issue
- A SQL query plan with a missing index
- A race condition in concurrent code

### 3. Evaluate mixed-domain training
Test a training set that includes ~10-15% software diagnostic examples alongside the hardware data. The goal is not to make the model a software expert, but to prevent the adapter from overwriting the base model's software knowledge. Even a small amount of software-domain data in training can act as a "regularizer" that preserves the base model's existing capabilities.

### 4. Consider adapter gating / conditional application
More advanced: investigate whether the adapter can be conditionally applied based on input classification. MLX supports loading adapters at inference time — a lightweight classifier (or even keyword matching) could decide whether to apply the hardware-diagnostics adapter or use the base model alone. This is architecturally cleaner than mixing domains in training data.

### 5. Benchmark before v3 training (REQ-028)
Before starting the v3 training cycle, run the software-domain evaluation prompts against the current fine-tuned model to establish a regression baseline. After v3 training (which adds TRIAGE examples), re-run to see if domain awareness improves.

## Why This Matters

The model is being positioned as a hardware diagnostics assistant. But in real diagnostic work, a significant fraction of "hardware problems" turn out to be software. Sam's 40 years of experience includes knowing when to stop chasing hardware and look at firmware, drivers, or configuration. If the model can't recognize software issues — or worse, confidently misdiagnoses them as hardware — it undermines the value proposition.

The goal isn't to make the model good at software. It's to make it **honest about the boundaries of its expertise.**

---
*Shelved for future work. Captures analysis and recommendations from evaluation report review (2026-03-14). Execute after REQ-028 v3 training cycle.*
