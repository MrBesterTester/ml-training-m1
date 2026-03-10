---
name: start-step
description: Begin working on a specific TODO step with full document context
argument-hint: <step-number> [doc-prefix]
---

# Start Step Skill

Load the full context for a specific TODO step and begin implementation. This is the manual fallback for when you want to work on a step interactively rather than through the do-work queue.

## Usage

```
/start-step 2.1              # reads docs/SPECIFICATION.md, docs/BLUEPRINT.md, docs/TODO.md
/start-step 2.1 v2-upgrade   # reads docs/v2-upgrade-SPECIFICATION.md, etc.
```

## Workflow

### Step 1: Resolve Documents

1. Parse the step number from the first argument (e.g., `2.1`)
2. Parse the optional doc-prefix from the second argument
3. Resolve file paths:
   - No prefix: `docs/SPECIFICATION.md`, `docs/BLUEPRINT.md`, `docs/TODO.md`
   - With prefix: `docs/[prefix]-SPECIFICATION.md`, `docs/[prefix]-BLUEPRINT.md`, `docs/[prefix]-TODO.md`
4. Verify all three files exist. If any are missing, report and stop.

### Step 2: Read All Three Documents

Read the full content of:
1. SPECIFICATION — for project context, goals, constraints
2. BLUEPRINT — for implementation guidance on this specific step
3. TODO — for the step's checklist items and test criteria

### Step 3: Extract the Step

From the TODO, find the step matching the given number (e.g., `2.1`). Extract:
- The step title
- All sub-items (checkbox items)
- The TEST criteria
- The label (e.g., `[Claude Code]`, `[Sam]`)

From the BLUEPRINT, find the matching section (e.g., `### Step 2.1`). Extract the full section content.

### Step 4: Present the Work Context

Display a summary to the user:

```
## Step [N.M]: [Title]
**Phase:** [phase name]
**Label:** [label]

### TODO Checklist
- [ ] Sub-item 1
- [ ] Sub-item 2
- [ ] TEST: [criteria]

### Blueprint Guidance
[Blueprint section content]

### Key Constraints (from Spec)
[Any relevant constraints from the Specification]
```

### Step 5: Begin Implementation

Start working on the step. As you complete each sub-item:
- Announce what you're doing
- Do the work
- Report the result
- Move to the next sub-item

When the step's TEST criteria is met, report completion and suggest the user check off the step in the TODO.

## Notes

- If the step is labeled `[Sam]` or similar (not `[Claude Code]`), note that this step requires human action and offer to assist where possible.
- Do not modify the TODO file directly — the user checks off items.
- If a step depends on a previous uncompleted step, warn the user.
