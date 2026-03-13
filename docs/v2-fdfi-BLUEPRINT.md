# Blueprint: FD/FI Dataset Augmentation

**Date:** March 12, 2026
**Source:** [v2-fdfi-SPECIFICATION.md](./v2-fdfi-SPECIFICATION.md)

---

## Overview

This blueprint adds 100-200 FD/FI-style diagnostic entries to the existing 252-entry dataset. The work is organized into 4 phases: taxonomy definition, generation (split by entry type), integration, and review. Each step has a verification test.

The existing dataset generation infrastructure (`scripts/generate_dataset.py`) produced encyclopedic entries. The FD/FI entries are structurally different — they present specific data and require analytical responses — so they need their own generation approach.

---

## Phase 1: FD/FI Taxonomy & Data Templates

**Goal:** Define the diagnostic scenarios, data formats, and response patterns for each FD/FI category before generating any entries.

### Step 1.1 — Define FD/FI Scenario Taxonomy

Map each hardware domain to specific diagnostic scenarios with realistic data types.

**Context:** The existing `generate_dataset.py` has topic categories and physics mappings. The FD/FI taxonomy is orthogonal — it's organized by *diagnostic situation* (what kind of data is presented, what kind of reasoning is needed), not by *topic*. A single topic like "boundary scan" might appear in FD entries (detect a failing IDCODE), FI entries (isolate which device in the chain is marginal), and honest triage entries (the failure is actually a software sequencing bug, not a hardware fault).

```
Create scripts/generate_fdfi_dataset.py with the FD/FI scenario taxonomy.

Steps:
1. Define the four entry categories with their characteristics:
   - FD (Fault Detection): data + "is this normal?"
   - FI (Fault Isolation): anomaly + "what's causing it?"
   - FD+FI (Combined): raw data → detect + isolate
   - TRIAGE (Honest Triage): looks like hardware, isn't
2. For each hardware domain (boundary scan, signal integrity, ICT, thermal,
   mixed-signal, functional test, production test, environmental), define
   3-5 specific diagnostic scenarios with:
   - The type of data presented (TDR trace, Icc distribution, IDCODE sequence, etc.)
   - Realistic value ranges and units
   - What the anomaly looks like
   - What the root cause is
   - What physics connects the symptom to the cause
3. For the TRIAGE category, define scenarios across domains where the symptom
   mimics a hardware fault but the cause is software, configuration, operator
   error, or measurement artifact.
4. Print a summary: count of scenarios per domain × category

Test: The script runs and prints 30+ defined diagnostic scenarios across multiple
domains and all four categories. Each scenario has specific data types and value
ranges, not vague descriptions.
```

### Step 1.2 — Define Data Presentation Templates

Create templates for how measurement data appears in the instruction field.

**Context:** FD/FI entries must present *specific data* — not "a TDR trace shows an impedance discontinuity" but actual numbers: "TDR sweep: Z0=51Ω for 0-35mm, dip to 38Ω at 47mm over 2mm, recovery to 50Ω." The templates define realistic data formats for each measurement type so generated entries feel like real diagnostic situations.

```
Extend scripts/generate_fdfi_dataset.py with data presentation templates.

Steps:
1. For each data type in the taxonomy (TDR traces, Icc distributions, IDCODE
   sequences, temperature maps, SPC data, eye diagrams, etc.), create a
   template that specifies:
   - How the data is described in the instruction (narrative, tabular, list)
   - Realistic parameter ranges (impedance in ohms, current in mA, temperature
     in °C, frequency in MHz/GHz, etc.)
   - How anomalies manifest in that data type (shifts, outliers, patterns,
     bit flips, trends)
2. Create a function that generates realistic synthetic data points for each
   template — values should be plausible, not random garbage
3. Generate and print 5 sample data presentations across different types

Test: The 5 sample data presentations read like real diagnostic data that a test
engineer would encounter. Values are in the right ballpark, units are correct,
and the format is natural.
```

---

## Phase 2: Entry Generation

**Goal:** Generate the 100-200 FD/FI entries across all four categories, using the taxonomy and templates from Phase 1.

### Step 2.1 — Generate Fault Detection (FD) Entries

Write 30-50 entries where the model must detect an anomaly in presented data.

**Context:** FD entries are the "is something wrong?" category. The instruction presents specific data and asks the model to evaluate it. The response must: (1) identify the anomaly, (2) explain why it's anomalous using physics/engineering principles, and (3) state the severity or urgency. These should cover multiple hardware domains.

```
Generate FD entries and write to a staging file.

Steps:
1. Using the taxonomy and data templates, write 30-50 FD entries covering:
   - Boundary scan: abnormal IDCODE reads, chain integrity failures
   - Signal integrity: impedance anomalies, eye diagram violations
   - ICT: measurement distributions with shifts or outliers
   - Thermal: unexpected temperature patterns or gradients
   - Mixed-signal: ADC/DAC linearity errors, noise floor anomalies
   - Production: yield drops, SPC out-of-control conditions, Cpk drift
   - Environmental: unexpected failure patterns in stress testing
2. Each entry must present specific numerical data in the instruction
3. Responses must lead with the detection conclusion, then explain the physics
4. Write to data/fdfi_fd_entries.jsonl (staging — not yet merged)
5. Print count and 3 sample entries for review

Test: data/fdfi_fd_entries.jsonl contains 30-50 valid JSONL entries. Each
instruction contains specific measurement data. Each response identifies a
specific anomaly with physics-based reasoning.
```

### Step 2.2 — Generate Fault Isolation (FI) Entries

Write 30-50 entries where the model must isolate the root cause of a known anomaly.

**Context:** FI entries start with a detected anomaly and ask "what's causing it and where?" The instruction describes the symptom with supporting data. The response must: (1) narrow to a specific cause or short list of causes, (2) explain the physical mechanism connecting symptom to cause, and (3) recommend verification steps. FI entries require deeper reasoning — the model must work backward from symptom to source.

```
Generate FI entries and write to a staging file.

Steps:
1. Using the taxonomy, write 30-50 FI entries covering:
   - Boundary scan: isolate failing device in chain, identify marginal signal
   - Signal integrity: pinpoint discontinuity source (via, connector, trace),
     identify coupling mechanism
   - ICT: distinguish component failure vs. measurement artifact vs. design issue
   - Thermal: identify heat source from thermal distribution data
   - Functional test: isolate failing subsystem from symptom pattern
   - Production: distinguish process shift vs. component lot vs. design margin
2. Each entry presents the anomaly with supporting data (measurements, patterns)
3. Responses must narrow to specific cause(s) with physical reasoning
4. Include verification steps — what to measure next to confirm the diagnosis
5. Write to data/fdfi_fi_entries.jsonl
6. Print count and 3 sample entries

Test: data/fdfi_fi_entries.jsonl contains 30-50 valid JSONL entries. Each
response narrows from symptom to specific root cause with a causal chain
grounded in physics.
```

### Step 2.3 — Generate Combined FD+FI Entries

Write 20-30 entries where the model must both detect and isolate from raw data.

**Context:** These are the most realistic entries — raw data arrives, and the model must find the problem AND identify the cause. No hints are given. These test the full diagnostic reasoning chain.

```
Generate combined FD+FI entries.

Steps:
1. Write 20-30 entries where the instruction presents data without indicating
   that anything is wrong. The model must:
   - Detect what's anomalous
   - Isolate the likely cause
   - Recommend action
2. Cover at least 5 different hardware domains
3. Include cases with multiple anomalies (model should catch all of them)
4. Include cases where data is borderline — judgment calls
5. Write to data/fdfi_combined_entries.jsonl
6. Print count and 2 sample entries

Test: data/fdfi_combined_entries.jsonl contains 20-30 entries. Each response
demonstrates both detection and isolation reasoning on unprompted data.
```

### Step 2.4 — Generate Honest Triage Entries

Write 20-30 entries where the apparent hardware problem has a non-hardware cause.

**Context:** A good diagnostician knows when the problem *isn't* hardware. These entries prevent the model from force-fitting every symptom into a hardware diagnosis. The instruction presents a symptom that looks like a hardware fault, but the response correctly identifies a software, configuration, operator, or measurement-system cause.

```
Generate honest triage entries.

Steps:
1. Write 20-30 entries covering non-hardware causes that mimic hardware faults:
   - Software bugs: race conditions, driver errors, timeout misconfigurations
   - Configuration errors: wrong test limits, incorrect fixture setup, bad cal data
   - Operator errors: wrong part orientation, skipped setup steps
   - Measurement artifacts: probe contact issues, ground loop noise, calibration drift
   - Environmental: intermittent building power, HVAC-induced thermal variation
2. Each instruction should present a symptom that a naive diagnostician would
   attribute to hardware
3. Responses must: (1) correctly identify non-hardware cause, (2) explain what
   evidence rules out hardware, (3) explain the actual mechanism
4. Physics is used to *rule out* hardware, not to explain the (non-hardware) cause
5. Write to data/fdfi_triage_entries.jsonl
6. Print count and 2 sample entries

Test: data/fdfi_triage_entries.jsonl contains 20-30 entries. Each correctly
identifies a non-hardware root cause and explains why hardware is ruled out.
```

---

## Phase 3: Integration & Splitting

**Goal:** Merge the new FD/FI entries into the main dataset and produce updated train/eval splits.

### Step 3.1 — Merge & Validate

Combine staging files into the main dataset and validate the complete set.

**Context:** The staging files from Phase 2 need to be appended to `data/full_dataset.jsonl`. Validation ensures no format errors, no exact duplicates, and the combined dataset is in the target range (350-450 entries).

```
Merge FD/FI entries into the main dataset.

Steps:
1. Create scripts/merge_fdfi.py that:
   - Reads data/full_dataset.jsonl (existing 252 entries)
   - Reads all four staging files:
     * data/fdfi_fd_entries.jsonl
     * data/fdfi_fi_entries.jsonl
     * data/fdfi_combined_entries.jsonl
     * data/fdfi_triage_entries.jsonl
   - Validates each entry has instruction/input/output keys
   - Checks for exact duplicate instructions
   - Appends new entries to full_dataset.jsonl
   - Prints summary: original count, new count per category, total
2. Optionally add a "category" metadata field to each entry for analysis
   (encyclopedic, fd, fi, fd+fi, triage) — only if it doesn't break
   the mlx_lm training format
3. Run the merge

Test: data/full_dataset.jsonl contains 350-450 entries. No duplicate instructions.
All entries have valid instruction/input/output keys.
```

### Step 3.2 — Re-split Train/Eval

Run the existing split script on the augmented dataset.

**Context:** The split must include FD/FI entries in both train and eval sets so that evaluation can test diagnostic capability, not just encyclopedic knowledge.

```
Re-run the dataset split on the augmented dataset.

Steps:
1. Back up existing train.jsonl and valid.jsonl
2. Run scripts/split_dataset.py (uses seed 42, 80/20 split)
3. Verify the eval set contains a mix of encyclopedic and FD/FI entries
4. Print counts for each split

Test: data/train.jsonl and data/valid.jsonl exist. Combined count equals
full_dataset.jsonl. Spot-check that both splits contain FD/FI-style entries.
```

---

## Phase 4: Review Gate

**Goal:** Sam reviews the augmented dataset and approves it for training.

### Step 4.1 — Dataset Review

**Context:** This is the GATE that was identified in step 2.3 of the original TODO. Sam must review the new FD/FI entries for technical accuracy, realistic data values, and correct diagnostic reasoning.

```
Prepare the augmented dataset for Sam's review.

Steps:
1. Generate a review summary showing:
   - Total entries by category (encyclopedic, FD, FI, FD+FI, triage)
   - Entry count by hardware domain
   - Average response length by category
   - 3 representative samples from each FD/FI category
2. Flag any entries Sam should pay special attention to:
   - Entries with complex physics reasoning
   - Entries with borderline/judgment-call diagnoses
   - Triage entries (verify the non-hardware cause is convincing)
3. Sam reviews and either approves or flags entries for revision
4. If entries are flagged: revise and re-merge

GATE: Sam approves the augmented dataset. This unblocks step 2.4 (split) and
3.1 (training) from the original TODO.

Test: Sam has explicitly approved the dataset. Any flagged entries have been
revised or removed.
```

---

## Step Dependency Map

```
1.1 FD/FI Scenario Taxonomy
 └─→ 1.2 Data Presentation Templates
      ├─→ 2.1 Generate FD Entries ──────────┐
      ├─→ 2.2 Generate FI Entries ──────────┤
      ├─→ 2.3 Generate Combined Entries ────┤  (parallel)
      └─→ 2.4 Generate Triage Entries ──────┤
                                             └─→ 3.1 Merge & Validate
                                                  └─→ 3.2 Re-split Train/Eval
                                                       └─→ 4.1 Sam's Review (GATE)
                                                            └─→ [original TODO 2.4 → 3.1 → ...]
```

Note: Steps 2.1-2.4 can be executed **in parallel** — they are independent of each other, sharing only the taxonomy and templates from Phase 1.

---

## Key Principles

1. **Specific data, specific analysis.** Every FD/FI entry must contain concrete numbers, sequences, or measurements — never "the TDR trace showed an anomaly" but always "the TDR trace showed a dip to 38 ohm at 47mm."
2. **Realistic values.** All synthetic data must be physically plausible. Wrong values teach the model wrong norms.
3. **Conclusion first.** FD/FI responses should lead with the detection/isolation conclusion, then explain the reasoning — the way a senior engineer briefs a team.
4. **Physics as diagnostic tool.** Physics explains *why this data means this fault*, not general theory.
5. **Honest triage is a feature.** Correctly identifying non-hardware causes is a diagnostic skill, not a gap in the model's knowledge.
6. **Parallel generation.** The four entry categories (2.1-2.4) are independent and should be generated concurrently for efficiency.
