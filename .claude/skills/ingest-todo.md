---
name: ingest-todo
description: Parse a TODO.md and generate do-work REQ files for each step
argument-hint: [path-to-TODO.md]
---

# Ingest TODO Skill

Parses a Dylan Davis-style TODO.md file and generates do-work REQ files — one per numbered step. This bridges the three-document planning methodology (SPECIFICATION → BLUEPRINT → TODO) with do-work's queue-based execution.

## Inputs

- **TODO file path** (optional, default: `docs/TODO.md`)
- Companion docs are auto-resolved by naming convention:
  - `docs/TODO.md` → `docs/BLUEPRINT.md` + `docs/SPECIFICATION.md`
  - `docs/v2-upgrade-TODO.md` → `docs/v2-upgrade-BLUEPRINT.md` + `docs/v2-upgrade-SPECIFICATION.md`

## Workflow

### Step 1: Resolve the Document Set

1. Accept the TODO path from the user's argument, or default to `docs/TODO.md`
2. Derive the companion doc paths:
   - Replace `TODO.md` with `BLUEPRINT.md` → blueprint path
   - Replace `TODO.md` with `SPECIFICATION.md` → specification path
3. Verify all three files exist. If any are missing, report and stop.
4. Read all three files.

### Step 2: Parse the TODO

Extract every numbered step from the TODO file. A step looks like:

```markdown
- [ ] **[Label]** N.M Step title
  - [ ] Sub-item 1
  - [ ] Sub-item 2
  - [ ] **TEST:** Verification criteria
```

For each step, extract:
- **Step number** (e.g., `1.1`, `2.3`)
- **Phase number** (the integer part: `1`, `2`, etc.)
- **Phase name** (from the `## Phase N:` heading above it)
- **Title** (the step title text after the number)
- **Label** (the text in `**[brackets]**`, e.g., `Claude Code`, `Sam`)
- **Sub-items** (all checkbox items nested under the step)
- **Test criteria** (any sub-item starting with `**TEST:**`)

Skip steps that are already checked (`- [x]`).

### Step 3: Derive Batch Name

Generate a batch name from the TODO filename:
- `docs/TODO.md` → `ml-training-phase-N` (one batch per phase)
- `docs/v2-upgrade-TODO.md` → `v2-upgrade-phase-N`

### Step 4: Find the Corresponding Blueprint Section

For each step, locate the matching section in the BLUEPRINT:
- Step `1.1` matches `### Step 1.1` in the Blueprint
- Extract the full content of that Blueprint section (context, instructions, test criteria)

### Step 5: Create the UR Folder

1. Determine the next UR number (check `do-work/user-requests/` and `do-work/archive/UR-*/`)
2. Create `do-work/user-requests/UR-NNN/input.md` containing:

```markdown
---
id: UR-NNN
title: "Ingested from [TODO filename]"
created_at: [ISO 8601 timestamp]
requests: []  # filled in after creating REQs
word_count: [word count of full TODO file]
source: ingest-todo
---

# Ingested from [TODO filename]

## Summary

Auto-generated from [TODO filename] by the ingest-todo skill.
[N] steps parsed across [M] phases.

Companion docs:
- Specification: [spec path]
- Blueprint: [blueprint path]

## Full Verbatim Input

[Paste the ENTIRE TODO.md content here, unmodified]

---
*Captured: [timestamp]*
```

### Step 6: Create REQ Files

For each unchecked step, create `do-work/REQ-NNN-step-N-M-slug.md`:

```markdown
---
id: REQ-NNN
title: "Step N.M: [step title]"
status: pending
created_at: [ISO 8601 timestamp]
user_request: UR-NNN
related: [other REQ IDs in same phase]
batch: [batch-name-phase-N]
source_step: "N.M"
source_doc: [TODO file path]
blueprint_ref: [BLUEPRINT file path]
model_hint: "[label from TODO, e.g. Claude Code]"
---

# Step N.M: [Step Title]

## What

[Step title and description from TODO]

## Requirements

[List all sub-items from the TODO step as bullet points]

- Sub-item 1
- Sub-item 2
- ...

## Verification

[The TEST: sub-item from the TODO, if present]

- [TEST criteria]

## Blueprint Context

[Paste the matching Blueprint section content here — this gives the builder
the full implementation guidance, context, and detailed instructions]

## Specification Reference

This step is part of the [project name] project. See [spec path] for full
project context, goals, and constraints.

## Builder Guidance

- Certainty level: Firm (this is a planned, documented step)
- The TODO label suggests: [label] — use this as advisory guidance
- Steps marked **[Sam]** require human review — complete the implementation
  but flag that manual verification is needed
- Follow the Blueprint's instructions closely; they contain tested approaches

## Context

See [user-requests/UR-NNN/input.md](./user-requests/UR-NNN/input.md) for the
full TODO document.

---
*Source: Ingested from [TODO path], step N.M*
```

### Step 7: Update the UR

Go back to `do-work/user-requests/UR-NNN/input.md` and fill in the `requests` array with all created REQ IDs.

### Step 8: Report Back

Print a summary:

```
Ingested: [TODO filename]
Companion docs: [spec], [blueprint]
UR: UR-NNN
REQs created: N

Phase 1 — [phase name]:
  REQ-001 → Step 1.1: [title]
  REQ-002 → Step 1.2: [title]
  REQ-003 → Step 1.3: [title]

Phase 2 — [phase name]:
  REQ-004 → Step 2.1: [title]
  ...

Steps skipped (already checked): [list or "none"]
Steps requiring manual review: [list steps labeled [Sam] or similar]
```

**STOP after reporting.** Do not start processing the queue.

## Notes

- **Granularity:** Each numbered step (1.1, 2.3, etc.) = one REQ. Sub-items within a step are requirements *inside* that REQ, not separate REQs.
- **Already-checked steps** (`- [x]`) are skipped — they're already done.
- **Manual review steps** (labeled `[Sam]` or similar non-agent labels) still get REQ files, but include a note that human review is needed.
- **Phase grouping:** The `batch` and `related` fields group steps by phase, so the work action can process them in order.
- **Re-running:** If REQ files already exist for these steps (check `source_step` frontmatter), warn the user and ask before creating duplicates.
