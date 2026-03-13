---
id: UR-006
title: Capture FD/FI numerical baseline responses before fine-tuning
created_at: 2026-03-12T12:00:00-07:00
requests: [REQ-018]
word_count: 83
---

# Capture FD/FI Numerical Baseline Responses

## Full Verbatim Input

Capture baseline responses from the base model (no adapter) for FD/FI numerical diagnostic prompts BEFORE fine-tuning. Pick 4-5 prompts from data/fdfi_combined_entries.jsonl that represent the numerical/physics-first content we added in Phase 2. Run each through the base model (models/llama-3.2-3b-4bit) using mlx_lm.generate with --max-tokens 200. Append the results to results/baseline_responses.md in the same format as the existing 4 prompts. Also update results/baseline_responses.json. This establishes the pre-training baseline for FD/FI content so Phase 4 comparison is fair.

---
*Captured: 2026-03-12T12:00:00-07:00*
