# TODO: FD/FI Dataset Augmentation

**Tracking checklist for implementation. Check off items as completed.**
**Source:** [v2-fdfi-BLUEPRINT.md](./v2-fdfi-BLUEPRINT.md)

---

## Phase 1: FD/FI Taxonomy & Data Templates

- [x] **[Claude Code]** 1.1 Define FD/FI scenario taxonomy
  - [x] Create `scripts/generate_fdfi_dataset.py`
  - [x] Define four entry categories (FD, FI, FD+FI, TRIAGE) with characteristics
  - [x] Map each hardware domain to 3-5 specific diagnostic scenarios with data types, value ranges, anomaly signatures, root causes, and connecting physics
  - [x] Define TRIAGE scenarios (software, config, operator, measurement artifact causes)
  - [x] **TEST:** Script prints 30+ defined scenarios across multiple domains and all four categories

- [x] **[Claude Code]** 1.2 Define data presentation templates
  - [x] Create templates for each measurement data type (TDR, Icc, IDCODE, thermal, SPC, eye diagram, etc.)
  - [x] Specify realistic parameter ranges per data type
  - [x] Define how anomalies manifest in each data type
  - [x] Create function to generate plausible synthetic data points
  - [x] **TEST:** 5 sample data presentations read like real diagnostic data with correct units and values

---

## Phase 2: Entry Generation

- [x] **[Claude Code]** 2.1 Generate Fault Detection (FD) entries
  - [x] Write 30-50 FD entries across boundary scan, signal integrity, ICT, thermal, mixed-signal, production, environmental domains
  - [x] Each instruction contains specific numerical data
  - [x] Each response leads with detection conclusion, then physics-based reasoning
  - [x] Write to `data/fdfi_fd_entries.jsonl`
  - [x] **TEST:** 30-50 valid JSONL entries, each with specific data and anomaly identification

- [x] **[Claude Code]** 2.2 Generate Fault Isolation (FI) entries
  - [x] Write 30-50 FI entries covering root cause isolation across domains
  - [x] Each entry presents anomaly with supporting data
  - [x] Each response narrows to specific cause(s) with physical mechanism
  - [x] Include verification steps (what to measure next)
  - [x] Write to `data/fdfi_fi_entries.jsonl`
  - [x] **TEST:** 30-50 valid JSONL entries, each with causal chain from symptom to root cause

- [x] **[Claude Code]** 2.3 Generate Combined FD+FI entries
  - [x] Write 20-30 entries presenting raw data with no anomaly hint
  - [x] Model must detect AND isolate in each response
  - [x] Cover at least 5 hardware domains
  - [x] Include multi-anomaly and borderline cases
  - [x] Write to `data/fdfi_combined_entries.jsonl`
  - [x] **TEST:** 20-30 valid entries demonstrating both detection and isolation reasoning

- [x] **[Claude Code]** 2.4 Generate Honest Triage entries
  - [x] Write 20-30 entries where symptoms mimic hardware faults
  - [x] Cover non-hardware causes: software bugs, config errors, operator errors, measurement artifacts, environmental
  - [x] Each response correctly identifies non-hardware cause
  - [x] Physics used to *rule out* hardware, not force-fit
  - [x] Write to `data/fdfi_triage_entries.jsonl`
  - [x] **TEST:** 20-30 valid entries, each correctly identifying non-hardware root cause

> **Note:** Steps 2.1-2.4 are independent and can be executed in parallel.

**Phase 2 Results (commit `3266d29`):**

| Category | Count | Domains | Notes |
|----------|-------|---------|-------|
| FD | 40 | All 8 | 2-3 variations per scenario |
| FI | 40 | All 8 | Causal chains + verification steps |
| FD+FI | 28 | 8 | Multi-anomaly + borderline cases |
| TRIAGE | 25 | 7 cause types | Physics used to rule OUT hardware |
| **Total** | **133** | | Target: 100-200 |

**Full test output:** [results/fdfi_phase2_test.txt](../results/fdfi_phase2_test.txt)

---

## Phase 3: Integration & Splitting

- [x] **[Claude Code]** 3.1 Merge & validate
  - [x] Create `scripts/merge_fdfi.py`
  - [x] Read existing `data/full_dataset.jsonl` (252 entries)
  - [x] Read all four staging files (fd, fi, combined, triage)
  - [x] Validate instruction/input/output keys on all entries
  - [x] Check for exact duplicate instructions
  - [x] Append new entries to `data/full_dataset.jsonl`
  - [x] **TEST:** Combined dataset contains 350-450 entries, no duplicates, all valid JSONL

- [x] **[Claude Code]** 3.2 Re-split train/eval
  - [x] Back up existing `data/train.jsonl` and `data/valid.jsonl`
  - [x] Run `scripts/split_dataset.py` on augmented dataset
  - [x] Verify eval set contains mix of encyclopedic and FD/FI entries
  - [x] **TEST:** Combined split count matches full dataset, both splits have FD/FI entries

---

## Phase 4: Review Gate

- [x] **[Sam]** 4.1 Review & approve augmented dataset
  - [x] Generate review summary (counts by category, by domain, avg response length, samples)
  - [x] Flag entries needing special attention (complex physics, judgment calls, triage entries)
  - [x] Sam reviews new FD/FI entries for technical accuracy and realistic data
  - [x] Revise any flagged entries *(no revisions needed — Sam approved as-is)*
  - [x] **GATE:** Sam approves dataset → unblocks original TODO steps 2.4 → 3.1 → training

---

## After This TODO Completes

With Sam's approval, return to the **original TODO.md** and continue from:
- [x] 2.3 Review dataset & approve *(completed via this v2-fdfi cycle)*
- [x] 2.4 Split into train/eval *(completed here as step 3.2)*
- [ ] 3.1 Configure & run LoRA training
- [ ] 3.2 Verify fine-tuned model inference
- [ ] ... (remaining original TODO steps)
