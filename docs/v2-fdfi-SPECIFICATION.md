# Specification: FD/FI Dataset Augmentation

**Date:** March 12, 2026
**Author:** Sam Kirk (with Claude Code)
**Parent:** [SPECIFICATION.md](./SPECIFICATION.md) (overall project spec)
**Trigger:** [DATASET_REVIEW_FINDINGS.md](./DATASET_REVIEW_FINDINGS.md) — Option A

---

## 1. Project Summary

Augment the existing 252-entry hardware diagnostics training dataset with **100-200 new entries** in the **FD/FI (Fault Detection / Fault Isolation)** style. The current dataset teaches the model to *explain* hardware diagnostics concepts. The new entries teach it to *perform* diagnostics — to look at specific data, detect anomalies, and isolate root causes.

This is Option A from the dataset review findings: keep the encyclopedic knowledge base and add the diagnostic skill layer on top.

## 2. Goals

### Primary Goal
Transform the fine-tuned model from a **knowledgeable explainer** into a **working diagnostician** by adding training examples that present specific measurement data and require detection/isolation reasoning.

### Success Criteria
- 100-200 new FD/FI-style Q&A entries added to `data/full_dataset.jsonl`
- Entries present **specific data** (measurements, traces, logs, distributions) — not general scenarios
- Entries require **specific analysis** (detect anomaly, isolate cause, recommend action)
- Final combined dataset of ~350-450 entries covers both knowledge and skill
- Updated train/eval splits reflect the augmented dataset
- Sam reviews and approves the new entries before proceeding to training

## 3. The FD/FI Framework

Drawn from IBM's RAS (Reliability, Availability, Serviceability) design philosophy, FD/FI treats detection and isolation as two distinct, measurable capabilities:

| Capability | Question It Answers | What the Model Must Do |
|---|---|---|
| **Fault Detection (FD)** | "Is something wrong?" | Compare presented data against expected behavior; recognize anomalies; explain *why* it's anomalous |
| **Fault Isolation (FI)** | "What specifically is wrong, and where?" | Narrow from symptom to root cause; identify the failing component/location; explain the physical mechanism |

### Entry Categories

The new entries fall into four categories:

1. **FD — Fault Detection** (~30-50 entries)
   - Present specific measurement data (distributions, waveforms, readings)
   - Ask: "Is this normal? Is something wrong?"
   - Model must detect the anomaly and explain why it's anomalous

2. **FI — Fault Isolation** (~30-50 entries)
   - Present an identified anomaly with supporting data
   - Ask: "What's causing this? Where is the fault?"
   - Model must narrow to a specific cause/location with reasoning

3. **FD+FI Combined** (~20-30 entries)
   - Present raw data without hinting that something is wrong
   - Model must both detect the anomaly AND isolate the cause
   - Most realistic — mirrors how real diagnostic data arrives

4. **Honest Triage** (~20-30 entries)
   - Present scenarios that look like hardware problems but aren't
   - Model must correctly identify non-hardware causes (software, configuration, operator error, measurement artifact)
   - Tests that the model doesn't force-fit everything into a hardware diagnosis

## 4. Data Characteristics

### What Makes FD/FI Entries Different from the Existing Dataset

| Aspect | Existing Entries (Encyclopedic) | New FD/FI Entries |
|---|---|---|
| **Input** | General scenario or concept | Specific data: numbers, patterns, sequences, measurements |
| **Question type** | "Explain this" / "How do you approach this?" | "Here is data — what does it tell you?" |
| **Response** | Physics-grounded explanation of principles | Data-driven analysis leading to specific conclusion |
| **Physics role** | Foundational — physics explains the concept | Diagnostic — physics explains *why* this specific data indicates *this specific fault* |
| **Skill trained** | Knowledge retrieval and explanation | Pattern recognition, anomaly detection, causal reasoning |

### Data Domains for FD/FI Entries

Cover the same hardware diagnostics domains as the existing dataset, but with specific data:

- **Boundary scan / JTAG** — IDCODE sequences, chain integrity results, bit-level failures
- **Signal integrity** — TDR traces, eye diagram metrics, S-parameter data, impedance measurements
- **ICT (In-Circuit Test)** — resistance/capacitance/inductance measurements, Icc distributions, opens/shorts patterns
- **Thermal** — temperature distributions, thermal resistance calculations, junction temperature readings
- **Mixed-signal** — ADC/DAC linearity data, noise floor measurements, clock jitter values
- **Functional test** — pass/fail patterns, timing margin data, voltage margining results
- **Production test** — yield trends, SPC data, lot-to-lot drift, Cpk values
- **Environmental / reliability** — HALT/HASS data, failure rate trends, Weibull parameters

### Physics in FD/FI Entries

Physics remains central — but as a diagnostic tool, not a lecture topic:

- FD entries: physics explains *why* a measurement is anomalous ("this impedance dip violates transmission line theory for the specified stack-up")
- FI entries: physics narrows the cause ("only a via stub or trace width change produces this TDR signature at this spatial resolution")
- Honest triage entries: physics *rules out* hardware causes ("the failure pattern is time-correlated, not unit-correlated — this is a software state issue, not a physical defect")

## 5. Format

Same Alpaca-style JSONL as existing entries:

```json
{
  "instruction": "Here are five consecutive boundary scan IDCODE reads from device 3 in a 5-device chain: 0x0BA00477, 0x1BA00477, 0x0BA00477, 0x0BA00477, 0x1BA00477. The expected IDCODE is 0x0BA00477. What's happening?",
  "input": "",
  "output": "The alternating bit in position 28 (0->1->0->0->1) indicates a marginal signal integrity condition on TDO. Bit 28 is the MSB of the manufacturer ID field, so this isn't a different device — it's the correct device with a flaky data capture. The TDO line is a serial shift register output clocked on TCK's falling edge. If the setup time margin on TDO relative to TCK is insufficient — typically because of excessive trace length, impedance mismatch, or a degraded driver — the bit captured at the test access port controller may be metastable. The fact that bit 28 is the specific failure point matters: in a shift register, the last bit shifted out has the tightest timing margin because it has accumulated the most jitter through the chain. Check TDO signal integrity at the connector with an oscilloscope — look for rise time degradation, ringing, or a DC offset that moves the crossing point relative to the TCK edge. Likely causes: (1) TDO trace impedance mismatch causing reflections, (2) a weak TDO driver on device 3 (check supply voltage to that device), or (3) TCK running too fast for the chain length."
}
```

### Response Length and Style

- 150-350 words per response (slightly longer than encyclopedic entries — diagnostic reasoning needs space)
- Lead with the conclusion/detection, then explain the reasoning
- Include specific physical mechanisms, not just categories
- Reference actual measurement values from the prompt in the analysis
- End with actionable next steps (what to measure, where to probe, what to change)

## 6. Constraints

- **No real proprietary data.** All measurement data in prompts is realistic but synthetic.
- **Technically accurate.** Values, units, and physical reasoning must be correct. A wrong diagnosis in the training data teaches the model to be wrong.
- **M1/16GB compatible.** The augmented dataset (350-450 entries) is still small enough for LoRA fine-tuning on the M1 iMac. No memory concerns at this scale.
- **Same format.** Must integrate cleanly with the existing `data/full_dataset.jsonl` and the existing `scripts/split_dataset.py` pipeline.

## 7. Deliverables

1. **FD/FI entry generation script** — New or extended script to produce the FD/FI entries
2. **100-200 new FD/FI entries** — Appended to `data/full_dataset.jsonl`
3. **Updated train/eval splits** — Re-run `scripts/split_dataset.py` on the augmented dataset
4. **Sam's review and approval** — GATE: Sam approves the augmented dataset before training proceeds

## 8. What Is NOT in Scope

- Rewriting the existing 252 entries (they're already revised and audited)
- Changes to the training pipeline, model, or LoRA configuration (those specs remain in the parent SPECIFICATION.md)
- The CompuFlair physics interpretation of the ML process itself (that's a separate deliverable)
- Real measurement data from any proprietary source

## 9. Relationship to Parent Spec

This specification replaces step 2.3 in the original TODO.md with a more thorough augmentation cycle, then feeds back into the same pipeline:

```
Original: 2.3 Review & approve dataset → 2.4 Split → 3.1 Train
Revised:  2.3 Review (done, found gap) → v2-fdfi augmentation → 2.4 Split → 3.1 Train
```

All downstream phases (training, evaluation, documentation, repo finalization) remain as specified in the parent SPECIFICATION.md and BLUEPRINT.md.
