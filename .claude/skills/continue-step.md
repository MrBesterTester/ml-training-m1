---
name: continue-step
description: Resume work on a partially completed TODO step
argument-hint: <step-number> [doc-prefix]
---

# Continue Step Skill

Resume work on a TODO step that was previously started but not finished. Reloads the full document context and picks up where you left off.

## Usage

```
/continue-step 2.1              # reads docs/SPECIFICATION.md, docs/BLUEPRINT.md, docs/TODO.md
/continue-step 2.1 v2-upgrade   # reads docs/v2-upgrade-SPECIFICATION.md, etc.
```

## Workflow

### Step 1: Resolve Documents

Same as start-step: resolve the three document paths using the optional prefix, verify they exist, and read them all.

### Step 2: Assess Current State

1. Read the TODO and find the target step
2. Check which sub-items are already checked (`- [x]`) vs unchecked (`- [ ]`)
3. Scan the project for artifacts that indicate partial completion:
   - Files or directories created by earlier sub-items
   - Scripts that exist but may be incomplete
   - Data files that were generated
4. Read the Blueprint section for this step to understand the full scope

### Step 3: Present Progress Summary

```
## Continuing Step [N.M]: [Title]

### Progress
- [x] Sub-item 1 (done)
- [x] Sub-item 2 (done)
- [ ] Sub-item 3 ← resuming here
- [ ] Sub-item 4
- [ ] TEST: [criteria]

### Artifacts Found
- [list any files/outputs from completed sub-items]

### Remaining Work
[Brief description of what's left]
```

### Step 4: Resume Implementation

Pick up from the first unchecked sub-item. Follow the same process as start-step:
- Announce what you're doing
- Do the work
- Report the result
- Move to the next sub-item

### Step 5: Completion

When all sub-items are done and the TEST criteria is met, report completion and suggest the user check off the step in the TODO.

## Notes

- If no sub-items are checked, this behaves the same as `/start-step` — it just does the project scan first to check for any existing work.
- If all sub-items are already checked, report that the step appears complete and ask if the user wants to re-verify.
- Do not modify the TODO file directly — the user checks off items.
