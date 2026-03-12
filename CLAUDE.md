# ml_training_m1

Hardware Diagnostics LLM Fine-Tuning — fine-tuning Llama 3.2 3B with LoRA on Apple MLX (M1 iMac, 16GB).

## Project Structure

```
ml_training_m1/
├── docs/
│   ├── SPECIFICATION.md    ← what we're building
│   ├── BLUEPRINT.md        ← how to build it (step-by-step)
│   └── TODO.md             ← implementation checklist
├── scripts/                ← Python scripts (dataset, training, eval)
├── data/                   ← training/eval datasets (JSONL)
├── adapters/               ← trained LoRA adapter weights
├── models/                 ← (gitignored) downloaded base models
├── results/                ← evaluation outputs
├── do-work/                ← task queue (REQ files, user-requests, archive)
└── .claude/skills/         ← Claude Code skills
```

## Three-Document Methodology (Dylan Davis)

All planned work follows the spec → blueprint → todo pipeline:

1. **SPECIFICATION.md** — defines *what* to build (goals, constraints, deliverables)
2. **BLUEPRINT.md** — defines *how* to build it (step-by-step implementation guidance)
3. **TODO.md** — the executable checklist (each step has sub-items and TEST criteria)

Future work cycles can use prefixed doc sets (e.g., `v2-upgrade-SPECIFICATION.md`).

## Workflows

### Autonomous (do-work queue)

For batch processing multiple steps without manual intervention:

```
/ingest-todo                    # parse TODO.md → REQ files in do-work/
do work run                     # process the queue autonomously
/sync-todo                      # (optional) check off completed TODO items
```

Each TODO step becomes one REQ file. The do-work system triages, plans, explores, implements, tests, and commits per REQ. Sub-agents get fresh context for each request.

### Manual (interactive)

For steps requiring human judgment, debugging, or visual verification:

```
/start-step 2.1                 # load full context and begin step 2.1
/continue-step 2.1              # resume a partially completed step
```

Use manual mode for:
- Steps labeled `[Sam]` (require human review/approval)
- Debugging failures from the autonomous loop
- Steps needing visual verification
- Exploratory or experimental work

### Ad-hoc (one-off tasks)

For bugs, ideas, or small tasks outside the TODO:

```
do work fix the dataset validation error
do work add a progress bar to training
```

These go directly into the do-work queue without needing a spec/blueprint/todo cycle.

## Git Workflow

- The do-work queue commits locally per REQ (granular history)
- Squash into clean commits when pushing to remote
- `do-work/working/` is gitignored (transient)
- `do-work/` root (pending REQs) and `do-work/archive/` are committed

## Post-Loop Sync

After `do work run` completes a batch, check off completed TODO items. Archived REQs have `source_step` frontmatter linking back to the TODO step number. This can be done:
- Manually by reviewing archived REQs
- Via `/sync-todo` skill (if created)

## Pushover Notifications (Apple Watch)

**ALWAYS** send a Pushover notification at the end of every task or meaningful work unit — completing a REQ, finishing a do-work run, running a sync, or any work that produces a result Sam should know about. This is a standing instruction; Sam should never need to request it.

```bash
curl -s -X POST https://api.pushover.net/1/messages.json \
  -d "token=aera3invzshp31bkife884fn6i3hbp" \
  -d "user=u7gd46dg9exsyxirtwa5tcwn93yo4e" \
  -d "title=Claude Code" \
  -d "message=YOUR MESSAGE HERE" \
  -d "sound=pushover"
```

Use a concise, specific message describing what's done (e.g., "REQ-015 complete — physics mappings added to generate_dataset.py").

## Key Constraints

- **Hardware:** M1 iMac, 16GB unified memory — all training must fit
- **Framework:** Apple MLX + mlx-lm (native Apple Silicon)
- **Base model:** Llama 3.2 3B Instruct, 4-bit quantized (~2GB)
- **Fine-tuning:** LoRA (Low-Rank Adaptation) — ~1-2M trainable parameters
