#!/usr/bin/env python3
"""
Evaluate fine-tuned model against base model baselines.

Loads baseline prompts from results/baseline_responses.json, runs the
fine-tuned model (with LoRA adapter) on each prompt, and writes a
side-by-side comparison to results/comparison.md.

Optionally samples additional prompts from data/valid.jsonl.

Usage:
    python scripts/evaluate.py [--extra N] [--max-tokens 300]
"""

import argparse
import json
import random
import sys
import time
from pathlib import Path

# MLX imports
from mlx_lm import load, generate


PROJECT_ROOT = Path(__file__).resolve().parent.parent
BASELINE_PATH = PROJECT_ROOT / "results" / "baseline_responses.json"
VALID_PATH = PROJECT_ROOT / "data" / "valid.jsonl"
OUTPUT_PATH = PROJECT_ROOT / "results" / "comparison.md"
MODEL_PATH = str(PROJECT_ROOT / "models" / "llama-3.2-3b-4bit")
ADAPTER_PATH = str(PROJECT_ROOT / "adapters" / "hw-diagnostics")


def load_baselines():
    """Load baseline prompts and responses from baseline_responses.json."""
    with open(BASELINE_PATH) as f:
        data = json.load(f)
    return data["results"]


def load_extra_prompts(n):
    """Sample n additional prompts from valid.jsonl (chat format)."""
    entries = []
    with open(VALID_PATH) as f:
        for line in f:
            entry = json.loads(line)
            msgs = entry["messages"]
            user_msg = next((m["content"] for m in msgs if m["role"] == "user"), None)
            asst_msg = next((m["content"] for m in msgs if m["role"] == "assistant"), None)
            if user_msg:
                entries.append({
                    "prompt": user_msg,
                    "ground_truth": asst_msg,
                    "category": "Eval Set",
                    "label": user_msg[:50] + "..." if len(user_msg) > 50 else user_msg,
                })
    random.seed(42)
    random.shuffle(entries)
    return entries[:n]


def run_finetuned(model, tokenizer, prompt, max_tokens):
    """Run inference with the fine-tuned model and return response + stats."""
    import mlx.core as mx

    start = time.time()
    response = generate(
        model, tokenizer, prompt=prompt, max_tokens=max_tokens, verbose=False
    )
    elapsed = time.time() - start
    peak_mem = mx.get_peak_memory() / (1024**3)

    return {
        "response": response,
        "elapsed": elapsed,
        "peak_memory_gb": round(peak_mem, 3),
    }


def write_comparison(results, output_path):
    """Write results/comparison.md with side-by-side comparisons."""
    lines = []
    lines.append("# Base vs Fine-Tuned Model Comparison")
    lines.append("")
    lines.append("**Model:** Llama 3.2 3B Instruct (4-bit quantized, MLX)")
    lines.append("**Adapter:** LoRA — 600 iters, lr=1e-5, 8 layers, rank 8")
    lines.append("**Training data:** ~416 physics-first hardware diagnostics Q&A pairs")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Table of contents
    lines.append("## Table of Contents")
    lines.append("")
    for i, r in enumerate(results, 1):
        label = r.get("label", f"Prompt {i}")
        anchor = label.lower().replace(" ", "-").replace("/", "").replace("(", "").replace(")", "")
        lines.append(f"{i}. [{label}](#{anchor})")
    lines.append("")
    lines.append("---")
    lines.append("")

    for i, r in enumerate(results, 1):
        label = r.get("label", f"Prompt {i}")
        category = r.get("category", "Unknown")
        lines.append(f"## {i}. {label}")
        lines.append("")
        lines.append(f"**Category:** {category}")
        lines.append("")

        # Prompt
        lines.append("### Prompt")
        lines.append("")
        prompt_text = r["prompt"]
        if "\n" in prompt_text:
            lines.append("```")
            lines.append(prompt_text)
            lines.append("```")
        else:
            lines.append(f"> {prompt_text}")
        lines.append("")

        # Base model response
        lines.append("### Base Model Response")
        lines.append("")
        base_resp = r.get("base_response", "(no baseline captured)")
        for para in base_resp.split("\n"):
            lines.append(f"> {para}")
        lines.append("")

        # Fine-tuned response
        lines.append("### Fine-Tuned Response")
        lines.append("")
        ft_resp = r.get("finetuned_response", "(not run)")
        for para in ft_resp.split("\n"):
            lines.append(f"> {para}")
        lines.append("")

        # Ground truth if available
        if r.get("ground_truth"):
            lines.append("### Ground Truth (from training/eval data)")
            lines.append("")
            for para in r["ground_truth"].split("\n"):
                lines.append(f"> {para}")
            lines.append("")

        lines.append("---")
        lines.append("")

    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append(f"**Total comparisons:** {len(results)}")
    lines.append("")
    cats = {}
    for r in results:
        cat = r.get("category", "Unknown")
        cats[cat] = cats.get(cat, 0) + 1
    for cat, count in cats.items():
        lines.append(f"- {cat}: {count}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Generated by `scripts/evaluate.py`*")
    lines.append("")

    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    print(f"Wrote {len(results)} comparisons to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Evaluate fine-tuned model against baselines")
    parser.add_argument("--extra", type=int, default=3,
                        help="Number of extra prompts to sample from valid.jsonl (default: 3)")
    parser.add_argument("--max-tokens", type=int, default=300,
                        help="Max tokens for generation (default: 300)")
    args = parser.parse_args()

    # Load baselines
    print("Loading baselines...")
    baselines = load_baselines()
    print(f"  {len(baselines)} baseline prompts loaded")

    # Load extra prompts
    extras = []
    if args.extra > 0 and VALID_PATH.exists():
        extras = load_extra_prompts(args.extra)
        print(f"  {len(extras)} extra prompts sampled from valid.jsonl")

    # Load fine-tuned model
    print(f"Loading model from {MODEL_PATH}")
    print(f"  with adapter from {ADAPTER_PATH}")
    model, tokenizer = load(MODEL_PATH, adapter_path=ADAPTER_PATH)
    print("  Model loaded.")

    # Run inference on all prompts
    all_results = []

    print(f"\nRunning {len(baselines)} baseline prompts...")
    for i, b in enumerate(baselines):
        prompt = b["prompt"]
        label = b.get("label", f"Baseline {i+1}")
        print(f"  [{i+1}/{len(baselines)}] {label}...")

        ft = run_finetuned(model, tokenizer, prompt, args.max_tokens)

        all_results.append({
            "prompt": prompt,
            "base_response": b["response"],
            "finetuned_response": ft["response"],
            "category": b.get("category", "Baseline"),
            "label": label,
            "peak_memory_gb": ft["peak_memory_gb"],
        })

    if extras:
        print(f"\nRunning {len(extras)} extra prompts from eval set...")
        for i, e in enumerate(extras):
            prompt = e["prompt"]
            label = e.get("label", f"Extra {i+1}")
            print(f"  [{i+1}/{len(extras)}] {label[:60]}...")

            ft = run_finetuned(model, tokenizer, prompt, args.max_tokens)

            all_results.append({
                "prompt": prompt,
                "base_response": "(no baseline — eval set prompt)",
                "finetuned_response": ft["response"],
                "ground_truth": e.get("ground_truth"),
                "category": e.get("category", "Eval Set"),
                "label": label,
                "peak_memory_gb": ft["peak_memory_gb"],
            })

    # Write comparison
    print(f"\nWriting comparison to {OUTPUT_PATH}...")
    write_comparison(all_results, OUTPUT_PATH)

    # Summary
    print(f"\nDone. {len(all_results)} total comparisons written.")


if __name__ == "__main__":
    main()
