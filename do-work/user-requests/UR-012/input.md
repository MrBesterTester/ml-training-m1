---
id: UR-012
title: "v3: Train model to explicitly classify diagnostic mode (FD/FI/TRIAGE)"
created_at: 2026-03-13T00:00:00Z
requests: [REQ-028]
word_count: 42
---

# v3: Train Model to Explicitly Classify Diagnostic Mode

## Full Verbatim Input

Perhaps we missed the boat by not training it do just that. After all, the training data was setup in just that way as you just confirmed.

Context: The training data was organized by FD, FI, FD+FI, and TRIAGE categories, but the model was never trained to explicitly classify which diagnostic mode a problem falls into. The categories shaped the response style but aren't surfaced in the output. Sam (4 decades of diagnostic engineering) identified this as a gap — the model mimics expert output but doesn't show the expert's first reasoning step: identifying the diagnostic mode.

---
*Captured: 2026-03-13*
