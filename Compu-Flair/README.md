# Compu-Flair/

CompuFlair-inspired materials for the Hardware Diagnostics LLM fine-tuning project.

---

## Physics of LoRA (start here)

**[Physics_of_LoRA.html](Physics_of_LoRA.html)** -- Unified physics interpretation of LoRA fine-tuning through the CompuFlair framework. Open in a browser for KaTeX-rendered equations and embedded SVG diagrams. Three parts:

- **Part I -- The Outside View (Thermodynamics):** Base model as equilibrium, LoRA as perturbation theory, training as annealing, quantization as literal quantization.
- **Part II -- The Inside View (Normal Modes):** SVD decomposition within each layer, rank-8 as truncated normal mode expansion, CNN/transformer feature hierarchy, why top layers get adapted, and the "two meanings of fundamental" paradox.
- **Part III -- Connecting the Views:** How the macroscopic thermodynamic description *predicts* the microscopic modal structure. One implies the other -- same physics, two scales.

## Project History

- **[Original_Proposal_CompuFlair.html](Original_Proposal_CompuFlair.html)** -- Original portfolio plan (Mar 2). Two CompuFlair-inspired projects: Kaggle regression ported to Rust/Mojo, and a tiny active-inference agent. Predates this fine-tuning project.
- **[Alternative_Proposal_LLM_FineTuning_Project.md](Alternative_Proposal_LLM_FineTuning_Project.md)** -- The pivot document (Mar 9). Why LoRA fine-tuning on Sam's hardware diagnostics expertise is a stronger portfolio piece than the CompuFlair curriculum path. This project's origin story.

## Archive

**[archive/](archive/)** -- The two source documents merged into `Physics_of_LoRA.html`:

- `COMPUFLAIR_LORA_INTERPRETATION.html/.md` -- thermodynamic view only (Mar 12)
- `LoRA_Mathematical_Mechanism.html/.md` -- modal/structural view only (Mar 13)

Kept for git history. The unified document supersedes both.

---

## Source Materials

Full references with links (CompuFlair/Borzou, Vanchurin, Brunton, the LoRA paper) are in Section 13 of [Physics_of_LoRA.html](Physics_of_LoRA.html).
