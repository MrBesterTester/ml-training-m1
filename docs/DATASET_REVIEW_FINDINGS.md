# Dataset Review Findings — Step 2.3

**Date:** March 12, 2026
**Reviewers:** Sam Kirk, Claude Code
**Status:** In review — GATE not yet passed

---

## Table of Contents

1. [Summary](#summary)
2. [What We Found](#what-we-found)
3. [The FD/FI Gap](#the-fdfi-gap)
4. [Where the Development Went Awry](#where-the-development-went-awry)
5. [What the Dataset Currently Teaches](#what-the-dataset-currently-teaches)
6. [What the Dataset Should Also Teach](#what-the-dataset-should-also-teach)
7. [The Two Meanings of "Physics-First"](#the-two-meanings-of-physics-first)
8. [Recommended Path Forward](#recommended-path-forward)

---

## Summary

During the step 2.3 dataset review, we discovered a fundamental gap in the training data. The 252 Q&A pairs in `data/full_dataset.jsonl` teach the model to *explain* hardware diagnostics concepts — but they do not teach it to *perform* diagnostics on specific data. The dataset produces a textbook, not a diagnostician.

This gap was revealed by applying the **FD/FI (Fault Detection / Fault Isolation)** framework from IBM's RAS (Reliability, Availability, Serviceability) design philosophy to evaluate what the fine-tuned model would actually be able to do.

---

## What We Found

### The Dataset Is High Quality — For What It Is

The 252 entries cover 10+ hardware diagnostics topic areas (JTAG/boundary scan, signal integrity, ICT, mixed-signal, thermal, reliability, inspection, test automation) with technically detailed, physics-grounded responses. A programmatic audit (`scripts/audit_physics_style.py`) classified:

- **77% PHYSICS-FIRST** — physics is load-bearing in the explanation
- **23% MIXED** — blend of physics and procedural content
- **~5% originally PHYSICS-DECORATED** — software/protocol topics with forced physics analogies (these were revised to use honest diagnostic triage framing)

### But the Entries Are All the Same Type

Every single entry follows the same pattern:

> **Q:** "Here is a general scenario or concept. Explain it."
> **A:** "Here is a detailed explanation of the principles, with equations and diagnostic steps."

This is encyclopedic knowledge — the model learns to give lectures. What's missing is the diagnostic act itself.

---

## The FD/FI Gap

IBM's service philosophy, formalized in the **FD/FI** (Fault Detection / Fault Isolation) framework and embedded in their RAS design principles since the System/360 era, treats detection and isolation as two distinct, measurable capabilities:

| Capability | Question It Answers | What It Requires |
|---|---|---|
| **Fault Detection (FD)** | "Is something wrong?" | Comparing observed data against expected behavior — recognizing anomalies |
| **Fault Isolation (FI)** | "What specifically is wrong, and where?" | Narrowing from symptom to root cause — isolating to a replaceable unit (FRU) |

IBM designed this into their hardware (built-in self-test, error detection codes, MAPs, Symptom-to-FRU indexes) and their service process (Customer Engineers followed structured diagnostic procedures from detection through isolation to FRU replacement).

### How This Applies to Our Model

A fine-tuned diagnostics model should be able to do what a skilled diagnostician does:

1. **Look at specific data** — a TDR trace, an Icc distribution, a set of boundary scan results, a thermal image, an error log
2. **Detect** — "this measurement is abnormal; here's what's out of spec"
3. **Isolate** — "based on this pattern, the fault is likely at this component/location, and here's why"

Our current dataset teaches none of this. It teaches the model to explain *in general* why TDR traces show impedance discontinuities — but not to look at *a specific* TDR trace and say "that dip at 47mm is a via stub, and it's on net DDR_DQ7."

---

## Where the Development Went Awry

The root cause traces back to the specification and how "physics-first" was interpreted during dataset generation.

### The Spec's Physics-First Mandate

The SPECIFICATION.md (Section 3) defined physics-first as a universal style requirement for all training responses:

> "Responses in the training dataset should adopt a physics-based explanatory style..."

It then provided physics mappings for every topic category, including forced analogies like:
- "Test coverage → information theory, entropy as a measure of test completeness"
- "Fault isolation → statistical mechanics analogies, root cause as energy minimization"

This was well-intentioned but conflated two different things.

### The Conflation

There are actually **two separate roles** for "physics-first" in this project:

1. **Understanding the ML process through physics** — the CompuFlair interpretation of LoRA as perturbation theory, learning rate as temperature, quantization as literal quantization. This is captured excellently in `Compu-Flair/Physics_of_LoRA.html` and is the project's distinctive intellectual contribution.

2. **Physics in the training data** — the spec mandated physics in every response, which led to 252 entries that all explain concepts through physics. But physics-grounded *explanations* are not the same as physics-grounded *diagnostics*.

The spec optimized for (2) when the real value was always in (1) plus a dataset that teaches the model to actually *do diagnostic work* — including recognizing when a problem isn't physics at all.

---

## What the Dataset Currently Teaches

The model trained on this dataset would be able to:

- Explain why JTAG chains fail at high TCK frequencies (transmission line theory)
- Describe the physics of solder joint failure mechanisms
- Recommend general diagnostic approaches for categories of problems
- Give detailed, equation-rich explanations of hardware phenomena
- Lecture on best practices for test coverage, ICT, boundary scan, etc.

In short: **a knowledgeable explainer**.

## What the Dataset Should Also Teach

For the model to function as a **diagnostician** (the FD/FI capability), it needs training examples that present specific data and require specific analysis:

### Fault Detection Examples

> **Q:** "Here is a distribution of Icc measurements from the last 500 boards. The mean shifted from 245 mA to 268 mA between lot 47 and lot 48, while sigma remained at 8 mA. Is this a problem?"
>
> **A:** "Yes — the 23 mA shift is a systematic offset (the stable sigma rules out increased randomness). This is not a DUT population change; it's a measurement system shift. [Detection reasoning follows...]"

### Fault Isolation Examples

> **Q:** "A TDR sweep of a 50-ohm DDR4 trace shows Z0 = 52 ohm for the first 35mm, then a sharp dip to 38 ohm over a 2mm region at 47mm, recovering to 51 ohm. The PCB stack-up spec calls for 50 +/- 10%. What's causing the dip?"
>
> **A:** "The 38-ohm dip at 47mm, spanning only 2mm, is characteristic of a via transition or layer change where the trace geometry widens or the reference plane distance decreases. Cross-reference the layout at 47mm — [Isolation reasoning follows, narrows to specific physical cause...]"

### Honest Triage Examples (Not Everything Is Hardware)

> **Q:** "Our automated test sequencer occasionally skips a test step. The instruments are fine when accessed manually. Is this a hardware timing issue?"
>
> **A:** "No — the fact that instruments work fine individually points to a software concurrency problem, not a hardware fault. [Explains why this isn't physics, and provides the correct diagnostic framework...]"

### Data Interpretation Examples

> **Q:** "Here are five consecutive boundary scan IDCODE reads from device 3 in a 5-device chain: 0x0BA00477, 0x1BA00477, 0x0BA00477, 0x0BA00477, 0x1BA00477. The expected IDCODE is 0x0BA00477. What's happening?"
>
> **A:** "The alternating bit in position 28 (0→1→0→0→1) indicates a marginal signal integrity condition on TDO. Bit 28 is the MSB of the manufacturer ID field, so this isn't a different device — it's the correct device with a flaky data capture. [Detection + Isolation reasoning...]"

---

## The Two Meanings of "Physics-First"

To be explicit about the distinction:

| Aspect | What It Means | Where It Lives |
|---|---|---|
| **Physics-first understanding of LoRA** | The ML process itself explained through thermodynamics, perturbation theory, annealing | `Compu-Flair/Physics_of_LoRA.html`, README |
| **Physics in the training data** | Responses grounded in physical principles where physics is the actual explanation | The Q&A dataset — but only where physics is genuinely load-bearing |

The first is the project's thesis. The second is a quality criterion for *some* of the training data — specifically the entries where the topic is inherently physical (signal integrity, thermal behavior, circuit theory). For software/protocol topics, honest triage ("this isn't a physics problem") is more valuable than forced physics analogies.

---

## Recommended Path Forward

### Option A: Augment the Existing Dataset

Keep the current 252 encyclopedic entries (they have value as foundational knowledge) and add a second tranche of **FD/FI-style entries** — perhaps 50-100 entries that present specific diagnostic data and require detection/isolation reasoning. This would give the model both the knowledge base and the diagnostic skill.

Rough split:
- ~250 entries: Conceptual/explanatory (existing, revised)
- ~50-100 entries: FD-style (here's data, is something wrong?)
- ~50-100 entries: FI-style (here's the anomaly, what's the cause and where?)

### Option B: Restructure the Dataset

Replace a portion of the encyclopedic entries with FD/FI-style entries, keeping the total count in the 200-500 range specified in the SPECIFICATION.

### Option C: Proceed As-Is, Note for V2

Accept the current dataset as a first iteration that demonstrates the fine-tuning pipeline (the primary project goal per the spec), and document the FD/FI gap as a known improvement for a future version.

### Recommendation

**Option A** is strongest if we want the model to be genuinely useful as a diagnostician. The current entries aren't wasted — a diagnostician needs background knowledge too. But without the FD/FI entries, the model is a reference book that can't work a case.

The SPECIFICATION.md and BLUEPRINT.md should be updated to reflect this understanding before proceeding.

---

## Files Modified During This Review

| File | Change |
|---|---|
| `data/full_dataset.jsonl` | 14 physics-decorated entries revised for honest triage framing |
| `data/full_dataset.jsonl.bak` | Backup of original dataset before revisions |
| `scripts/audit_physics_style.py` | New — programmatic physics-style auditor |
| `scripts/revise_decorated_entries.py` | New — documents and applies the 14 revisions |
| `results/physics_audit_report.md` | New — full audit report |

---

## References

- IBM RAS (Reliability, Availability, Serviceability) — [z/OS Basic Skills](https://www.ibm.com/docs/en/zos-basic-skills?topic=it-mainframe-strengths-reliability-availability-serviceability)
- FD/FI (Fault Detection / Fault Isolation) testability metrics — [DSI International](https://www.dsiintl.com/products/express/diagnostic-design-and-analysis/fdfi-statistics-by-category-report/)
- IBM Symptom-to-FRU methodology — [PC Server 330 Service Guide](https://www.ibm.com/support/pages/symptom-fru-index-pc-server-330)
- CompuFlair physics interpretation of LoRA — `Compu-Flair/Physics_of_LoRA.html`
