---
name: sync-todo
description: Check off completed TODO items based on archived do-work REQs
argument-hint: [path-to-TODO.md]
---

# Sync TODO Skill

After `do work run` completes, this skill reads archived REQ files and checks off the corresponding steps in the TODO.md. Keeps the Dylan Davis checklist view in sync with do-work's execution history.

## Usage

```
/sync-todo                      # defaults to docs/TODO.md
/sync-todo docs/v2-upgrade-TODO.md
```

## Workflow

### Step 1: Resolve the TODO File

Accept the path from the user's argument, or default to `docs/TODO.md`. Verify it exists.

### Step 2: Scan Archived REQs

Search for completed REQ files in:
- `do-work/archive/` (top-level archived REQs)
- `do-work/archive/UR-*/` (REQs inside archived UR folders)

For each archived REQ, check for `source_step` and `source_doc` in the frontmatter. Collect all that match the target TODO file.

### Step 3: Read the TODO

Read the current TODO.md. For each step, note whether it's checked (`- [x]`) or unchecked (`- [ ]`).

### Step 4: Determine What to Check Off

A step is eligible for check-off when:
- An archived REQ exists with a matching `source_step` value
- The REQ's status indicates successful completion (not failed/abandoned)
- The step is currently unchecked in the TODO

### Step 5: Present Changes for Approval

Do NOT modify the TODO automatically. Present the proposed changes:

```
Archived REQs found for [TODO filename]: N

Proposed check-offs:
  Step 1.1: Python environment & MLX installation
    └─ REQ-001 (archived, completed)
  Step 1.2: Download & quantize base model
    └─ REQ-002 (archived, completed)
  Step 2.1: Define topic taxonomy & prompt templates
    └─ REQ-004 (archived, completed)

Already checked (no change needed):
  (none)

No matching archive found (still pending):
  Step 1.3: Verify base model inference
  Step 2.2: Generate full Q&A dataset
  ...

Apply these check-offs? (y/n)
```

### Step 6: Apply Changes

After user approval, update the TODO.md:
- Change `- [ ]` to `- [x]` for each approved step
- Also check off sub-items within that step if the REQ's implementation summary indicates they were completed
- Do NOT check off the TEST sub-item unless the REQ shows the test passed

### Step 7: Report

```
Updated [TODO filename]:
  [x] Step 1.1: Python environment & MLX installation
  [x] Step 1.2: Download & quantize base model
  [x] Step 2.1: Define topic taxonomy & prompt templates

3 steps checked off. 11 steps remaining.
```

## Notes

- **Never auto-modify without approval.** Always present proposed changes first.
- **Steps labeled `[Sam]`** are only checked off if Sam has explicitly approved the work.
- **Partial completion:** If a REQ was archived but marked as failed or incomplete, do not check off the step — report it as needing attention.
- **Missing REQs:** Steps without a matching archived REQ are simply listed as still pending. This is expected if those steps haven't been ingested or processed yet.
