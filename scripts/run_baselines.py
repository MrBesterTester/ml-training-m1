#!/usr/bin/env python3
"""Run baseline inference on selected prompts and save results.

Captures base model responses (no adapter) for pre-training comparison.
Outputs both JSON (machine-readable) and Markdown (human-readable).
"""

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import mlx.core as mx
from mlx_lm import load, generate

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "llama-3.2-3b-4bit"
FDFI_DATA = PROJECT_ROOT / "data" / "fdfi_combined_entries.jsonl"
OUTPUT_JSON = PROJECT_ROOT / "results" / "baseline_responses.json"
OUTPUT_MD = PROJECT_ROOT / "results" / "baseline_responses.md"

MAX_TOKENS = 200

# Original Q&A prompts from Phase 1 baseline (March 9)
ORIGINAL_PROMPTS = [
    {
        "category": "Conceptual Q&A",
        "label": "Boundary Scan Testing",
        "prompt": "What is boundary scan testing and when would you use it?",
    },
    {
        "category": "Conceptual Q&A",
        "label": "Black Screen Diagnostic",
        "prompt": "A laptop powers on but the screen stays black. Walk me through a systematic hardware diagnostic process.",
    },
    {
        "category": "Conceptual Q&A",
        "label": "ECC vs Non-ECC Memory",
        "prompt": "Explain the difference between ECC and non-ECC memory, and how memory errors are detected.",
    },
    {
        "category": "Conceptual Q&A",
        "label": "PCIe Bus Errors",
        "prompt": "What are common causes of intermittent PCIe bus errors and how would you diagnose them?",
    },
]

# Selected FD/FI prompts (indices 0, 1, 2, 6, 10 from fdfi_combined_entries.jsonl)
FDFI_INDICES = [0, 1, 2, 6, 10]
FDFI_LABELS = [
    "TDR Impedance Measurements",
    "Boundary Scan Interconnect Results",
    "Thermal Survey",
    "ADC Code Density Histogram",
    "Voltage Margining Sweep",
]


def load_fdfi_prompts():
    """Load selected FD/FI prompts from the dataset."""
    with open(FDFI_DATA) as f:
        entries = [json.loads(line) for line in f]

    prompts = []
    for idx, label in zip(FDFI_INDICES, FDFI_LABELS):
        prompts.append({
            "category": "Numerical Diagnostics (FD/FI)",
            "label": label,
            "prompt": entries[idx]["instruction"],
        })
    return prompts


def run_inference(model, tokenizer, prompt):
    """Run inference and capture metrics."""
    mx.reset_peak_memory()
    start = time.time()
    response = generate(
        model, tokenizer, prompt=prompt, max_tokens=MAX_TOKENS, verbose=False
    )
    elapsed = time.time() - start
    peak_mem = mx.get_peak_memory() / (1024**3)

    # Estimate token counts from response length
    response_tokens = len(tokenizer.encode(response))
    prompt_tokens = len(tokenizer.encode(prompt))
    gen_tps = response_tokens / elapsed if elapsed > 0 else 0

    return {
        "response": response,
        "prompt_tokens": prompt_tokens,
        "generation_tokens": response_tokens,
        "generation_tps": round(gen_tps, 2),
        "peak_memory_gb": round(peak_mem, 3),
    }


def write_json(all_results, timestamp):
    """Write unified JSON with all baseline results."""
    output = {
        "model": str(MODEL_PATH.relative_to(PROJECT_ROOT)),
        "max_tokens": MAX_TOKENS,
        "timestamp": timestamp,
        "results": all_results,
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w") as f:
        json.dump(output, f, indent=2)
    print(f"Wrote {OUTPUT_JSON}")


def write_markdown(all_results, timestamp):
    """Write unified Markdown baseline report."""
    lines = [
        "# Baseline Responses — Llama 3.2 3B Instruct (4-bit MLX)",
        "",
        f"**Model:** `models/llama-3.2-3b-4bit`",
        f"**Max tokens:** {MAX_TOKENS}",
        f"**Timestamp:** {timestamp}",
        "**Hardware:** M1 iMac, 16GB unified memory",
        "",
        "---",
        "",
        "## Performance Summary",
        "",
        "| # | Category | Prompt | Generation tok/s | Peak Memory |",
        "|---|----------|--------|-----------------|-------------|",
    ]

    for i, r in enumerate(all_results, 1):
        lines.append(
            f"| {i} | {r['category']} | {r['label']} | {r['generation_tps']} | {r['peak_memory_gb']} GB |"
        )

    # Calculate averages
    avg_tps = sum(r["generation_tps"] for r in all_results) / len(all_results)
    lines.extend([
        "",
        f"**Average generation speed:** ~{avg_tps:.0f} tok/s",
        "",
        "---",
        "",
    ])

    # Group by category
    categories = {}
    for r in all_results:
        categories.setdefault(r["category"], []).append(r)

    prompt_num = 0
    for cat, results in categories.items():
        lines.append(f"## {cat}")
        lines.append("")

        for r in results:
            prompt_num += 1
            lines.append(f"### Prompt {prompt_num}: {r['label']}")
            lines.append("")
            # Quote the prompt — handle multiline
            prompt_lines = r["prompt"].split("\n")
            for pl in prompt_lines:
                lines.append(f"> {pl}")
            lines.append("")
            lines.append(r["response"])
            lines.append("")
            lines.append("---")
            lines.append("")

    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_MD, "w") as f:
        f.write("\n".join(lines))
    print(f"Wrote {OUTPUT_MD}")


def main():
    # Check for --fdfi-only flag (skip re-running original prompts, use cached)
    fdfi_only = "--fdfi-only" in sys.argv

    print("Loading model...")
    model, tokenizer = load(str(MODEL_PATH))

    timestamp = datetime.now(timezone.utc).astimezone().isoformat()
    all_results = []

    if fdfi_only and OUTPUT_JSON.exists():
        # Load cached original results, enriching with category/label if missing
        print("Loading cached original Q&A baselines...")
        with open(OUTPUT_JSON) as f:
            cached = json.load(f)
        for i, r in enumerate(cached["results"]):
            if "category" not in r and i < len(ORIGINAL_PROMPTS):
                r["category"] = ORIGINAL_PROMPTS[i]["category"]
                r["label"] = ORIGINAL_PROMPTS[i]["label"]
            all_results.append(r)
        print(f"  Loaded {len(all_results)} cached results")
    else:
        # Run original prompts
        print(f"\nRunning {len(ORIGINAL_PROMPTS)} original Q&A prompts...")
        for p in ORIGINAL_PROMPTS:
            print(f"  [{p['label']}] ...", end=" ", flush=True)
            result = run_inference(model, tokenizer, p["prompt"])
            result["category"] = p["category"]
            result["label"] = p["label"]
            result["prompt"] = p["prompt"]
            all_results.append(result)
            print(f"{result['generation_tps']} tok/s")

    # Run FD/FI prompts
    fdfi_prompts = load_fdfi_prompts()
    print(f"\nRunning {len(fdfi_prompts)} FD/FI numerical prompts...")
    for p in fdfi_prompts:
        print(f"  [{p['label']}] ...", end=" ", flush=True)
        result = run_inference(model, tokenizer, p["prompt"])
        result["category"] = p["category"]
        result["label"] = p["label"]
        result["prompt"] = p["prompt"]
        all_results.append(result)
        print(f"{result['generation_tps']} tok/s")

    # Write unified outputs
    print(f"\nWriting unified report ({len(all_results)} total prompts)...")
    write_json(all_results, timestamp)
    write_markdown(all_results, timestamp)

    print(f"\nDone. {len(all_results)} baseline responses captured.")


if __name__ == "__main__":
    main()
