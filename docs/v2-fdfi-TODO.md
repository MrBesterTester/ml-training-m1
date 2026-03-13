# TODO: FD/FI Dataset Augmentation

**Tracking checklist for implementation. Check off items as completed.**
**Source:** [v2-fdfi-BLUEPRINT.md](./v2-fdfi-BLUEPRINT.md)

---

## Phase 1: FD/FI Taxonomy & Data Templates

- [ ] **[Claude Code]** 1.1 Define FD/FI scenario taxonomy
  - [ ] Create `scripts/generate_fdfi_dataset.py`
  - [ ] Define four entry categories (FD, FI, FD+FI, TRIAGE) with characteristics
  - [ ] Map each hardware domain to 3-5 specific diagnostic scenarios with data types, value ranges, anomaly signatures, root causes, and connecting physics
  - [ ] Define TRIAGE scenarios (software, config, operator, measurement artifact causes)
  - [ ] **TEST:** Script prints 30+ defined scenarios across multiple domains and all four categories

- [ ] **[Claude Code]** 1.2 Define data presentation templates
  - [ ] Create templates for each measurement data type (TDR, Icc, IDCODE, thermal, SPC, eye diagram, etc.)
  - [ ] Specify realistic parameter ranges per data type
  - [ ] Define how anomalies manifest in each data type
  - [ ] Create function to generate plausible synthetic data points
  - [ ] **TEST:** 5 sample data presentations read like real diagnostic data with correct units and values

---

## Phase 2: Entry Generation

- [ ] **[Claude Code]** 2.1 Generate Fault Detection (FD) entries
  - [ ] Write 30-50 FD entries across boundary scan, signal integrity, ICT, thermal, mixed-signal, production, environmental domains
  - [ ] Each instruction contains specific numerical data
  - [ ] Each response leads with detection conclusion, then physics-based reasoning
  - [ ] Write to `data/fdfi_fd_entries.jsonl`
  - [ ] **TEST:** 30-50 valid JSONL entries, each with specific data and anomaly identification

- [ ] **[Claude Code]** 2.2 Generate Fault Isolation (FI) entries
  - [ ] Write 30-50 FI entries covering root cause isolation across domains
  - [ ] Each entry presents anomaly with supporting data
  - [ ] Each response narrows to specific cause(s) with physical mechanism
  - [ ] Include verification steps (what to measure next)
  - [ ] Write to `data/fdfi_fi_entries.jsonl`
  - [ ] **TEST:** 30-50 valid JSONL entries, each with causal chain from symptom to root cause

- [ ] **[Claude Code]** 2.3 Generate Combined FD+FI entries
  - [ ] Write 20-30 entries presenting raw data with no anomaly hint
  - [ ] Model must detect AND isolate in each response
  - [ ] Cover at least 5 hardware domains
  - [ ] Include multi-anomaly and borderline cases
  - [ ] Write to `data/fdfi_combined_entries.jsonl`
  - [ ] **TEST:** 20-30 valid entries demonstrating both detection and isolation reasoning

- [ ] **[Claude Code]** 2.4 Generate Honest Triage entries
  - [ ] Write 20-30 entries where symptoms mimic hardware faults
  - [ ] Cover non-hardware causes: software bugs, config errors, operator errors, measurement artifacts, environmental
  - [ ] Each response correctly identifies non-hardware cause
  - [ ] Physics used to *rule out* hardware, not force-fit
  - [ ] Write to `data/fdfi_triage_entries.jsonl`
  - [ ] **TEST:** 20-30 valid entries, each correctly identifying non-hardware root cause

> **Note:** Steps 2.1-2.4 are independent and can be executed in parallel.

---

## Phase 3: Integration & Splitting

- [ ] **[Claude Code]** 3.1 Merge & validate
  - [ ] Create `scripts/merge_fdfi.py`
  - [ ] Read existing `data/full_dataset.jsonl` (252 entries)
  - [ ] Read all four staging files (fd, fi, combined, triage)
  - [ ] Validate instruction/input/output keys on all entries
  - [ ] Check for exact duplicate instructions
  - [ ] Append new entries to `data/full_dataset.jsonl`
  - [ ] **TEST:** Combined dataset contains 350-450 entries, no duplicates, all valid JSONL

- [ ] **[Claude Code]** 3.2 Re-split train/eval
  - [ ] Back up existing `data/train.jsonl` and `data/valid.jsonl`
  - [ ] Run `scripts/split_dataset.py` on augmented dataset
  - [ ] Verify eval set contains mix of encyclopedic and FD/FI entries
  - [ ] **TEST:** Combined split count matches full dataset, both splits have FD/FI entries

---

## Phase 4: Review Gate

- [ ] **[Sam]** 4.1 Review & approve augmented dataset
  - [ ] Generate review summary (counts by category, by domain, avg response length, samples)
  - [ ] Flag entries needing special attention (complex physics, judgment calls, triage entries)
  - [ ] Sam reviews new FD/FI entries for technical accuracy and realistic data
  - [ ] Revise any flagged entries
  - [ ] **GATE:** Sam approves dataset → unblocks original TODO steps 2.4 → 3.1 → training

---

## After This TODO Completes

With Sam's approval, return to the **original TODO.md** and continue from:
- [x] 2.3 Review dataset & approve *(completed via this v2-fdfi cycle)*
- [ ] 2.4 Split into train/eval *(completed here as step 3.2)*
- [ ] 3.1 Configure & run LoRA training
- [ ] 3.2 Verify fine-tuned model inference
- [ ] ... (remaining original TODO steps)
