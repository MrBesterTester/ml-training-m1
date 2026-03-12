---
id: REQ-015
title: "Step 2.1 (rework): Add physics mappings & physics-why template to generate_dataset.py"
status: pending
created_at: 2026-03-12T00:00:00Z
user_request: UR-002
related: [REQ-004, REQ-005, REQ-006]
batch: ml-training-phase-2
source_step: "2.1"
source_doc: docs/TODO.md
blueprint_ref: docs/BLUEPRINT.md
model_hint: "Claude Code"
---

# Step 2.1 (Rework): Add Physics Mappings & Physics-Why Template

## What

Update the existing `scripts/generate_dataset.py` (created by REQ-004) to add physics-principle mappings for each topic category and a 5th "physics-why" question template style. This implements the CompuFlair-inspired physics-first requirements added to the spec, blueprint, and TODO.

## Background

REQ-004 created the script with 12 topic categories, 5 subtopics each, and 4 question template styles. It did NOT include physics mappings because the physics-first style requirement was added after REQ-004 completed. The script is functional and its existing structure is good — it just needs the physics layer added.

## Requirements

- Add a `physics_principles` field to each topic dict in `TOPICS`, mapping the category to its underlying physics:
  * Boundary scan / JTAG → signal propagation delay, clock domain crossing, transmission line effects
  * Functional test → power delivery physics, clock distribution, signal integrity
  * Fault isolation → statistical reasoning, thermal physics (IR imaging), wave propagation (TDR)
  * Test coverage → information theory, entropy as coverage metric
  * Mixed-signal → sampling theory (Nyquist), noise physics, phase-locked loop dynamics
  * ICT → circuit theory (Kirchhoff's laws, Ohm's law, impedance, guarded measurements)
  * Embedded diagnostics → semiconductor physics (voltage/temp sensors), digital logic timing
  * Test automation → (less physics-heavy — focus on measurement physics: VISA/SCPI instrument models)
  * Production test optimization → statistical process control, measurement uncertainty
  * Environmental/stress → thermodynamics, mechanical stress-strain, Arrhenius acceleration models
  * Signal/power integrity → electromagnetic wave propagation, transmission line theory, PDN impedance
  * AOI/X-ray → optics, X-ray absorption physics, image processing
- Add a 5th template style `physics_why` with 2-3 template variations:
  * "From a physics perspective, why does {subtopic} behave the way it does in {display_name}?"
  * "What are the underlying physical principles that explain {subtopic} in the context of {display_name}?"
  * Similar variations that invite physics-grounded explanations
- Update `generate_prompts()` to include the new style (total prompts: 12 topics × 5 styles = 60)
- Update `main()` summary output if needed
- Preserve existing structure, seed, and conventions — this is an additive change

## Verification

- Script runs and prints ~20 diverse sample prompts
- At least some prompts use the new `physics_why` style
- Each topic in `TOPICS` has a `physics_principles` field
- Total generated prompts increased from 48 to 60
- Existing prompt styles still work unchanged

## Builder Guidance

- Certainty level: Firm (requirements are well-defined)
- This is a rework of completed REQ-004 — the script exists and works, just needs the physics layer
- Read the current `scripts/generate_dataset.py` first — preserve its conventions
- The physics_principles field will be consumed by REQ-005 (step 2.2) when generating responses
- Do NOT generate Q&A response content — that's REQ-005's job

## Specification Reference

See docs/SPECIFICATION.md § "Explanatory Style: Physics-First (CompuFlair-Inspired)" for the full physics mapping list and rationale.

---
*Created 2026-03-12 — rework of archived REQ-004 to add physics-first requirements*
