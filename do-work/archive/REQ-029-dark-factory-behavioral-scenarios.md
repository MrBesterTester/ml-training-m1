---
id: REQ-029
title: "Evaluate Dark Factory / Behavioral Scenarios for model improvement"
status: shelved
created_at: 2026-03-13T00:00:00Z
user_request: UR-013
related: [REQ-028]
---

# Evaluate Dark Factory / Behavioral Scenarios for Model Improvement

## What

Evaluate whether StrongDM's "Dark Factory" approach — independent behavioral scenarios as a holdout validation set — could improve the fine-tuned hardware diagnostics model.

## Analysis

Inspired by the Nate B Jones / Dan Shapiro report on the 5 Levels of AI Coding and StrongDM's Software Factory. The core idea: behavioral scenarios stored outside the codebase validate AI-generated software independently, like holdout sets in ML training.

## Finding: Not Applicable in Full Form

The Dark Factory pattern doesn't map cleanly to this project:

1. **Different problem domain.** StrongDM validates deterministic code behavior. This project produces probabilistic LLM output — there's no single "correct" diagnostic response to validate against.

2. **Expert validation is superior.** Sam's 40 years of diagnostic engineering experience is a more reliable validator than any automated scenario runner. No chatbot knows what a correct diagnostic response looks like the way a domain expert does.

3. **Holdout set already exists.** `valid.jsonl` (77 entries) serves as the holdout. The 12-prompt evaluation comparison is essentially behavioral validation.

4. **Scale mismatch.** StrongDM runs thousands of scenarios per hour to validate production security software. A 3B parameter LoRA fine-tune on a portfolio project doesn't warrant that infrastructure investment.

## Where It Does Apply (Limited)

Targeted **adversarial evaluation / red-teaming** for the v3 diagnostic mode classification work (REQ-028):

- Edge cases where FD vs FI vs TRIAGE classification is ambiguous
- "TRIAGE traps" — scenarios that look like hardware but are actually software/firmware
- Subtle signals that test whether the model reasons about diagnostic mode or just pattern-matches

This would be a **dataset improvement task** (generating challenging training examples), not a Dark Factory infrastructure build.

## Reference

- Source report: `~/Desktop/Nate-B-Jones_ai_coding_levels_comprehensive_report.html`
- Framework: Dan Shapiro's 5 Levels of AI Coding
- Exemplar: StrongDM's 3-person AI team (Justin McCarthy, Jay Taylor, Navan Chauhan)
- Key concepts: Behavioral Scenarios, Digital Twin Universe, Scenario Holdouts, Attractor

---
*Source: UR-013/input.md — Preemptively shelved: captures the thought for future reference without execution.*
