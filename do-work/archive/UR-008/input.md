---
id: UR-008
title: Retry LoRA training after Metal OOM crash
created_at: 2026-03-12T18:00:00Z
requests: [REQ-020]
word_count: 42
---

# Retry LoRA training after Metal OOM crash

## Full Verbatim Input

Re-run LoRA fine-tuning. The previous attempt hit a Metal memory error and crashed the system. All other apps are now closed to maximize available memory. Review the training script and consider reducing memory usage (smaller batch size, shorter sequence length, gradient checkpointing) before running. The hardware is M1 iMac with 16GB unified memory.

---
*Captured: 2026-03-12T18:00:00Z*
