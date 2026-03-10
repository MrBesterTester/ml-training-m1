"""
Smoke test: run base model inference on hardware diagnostics prompts.

Loads the quantized Llama 3.2 3B model via mlx_lm, runs several
hardware-diagnostics prompts, prints responses with tokens/second,
and saves all results to results/baseline_responses.json.
"""

import json
import time
from pathlib import Path

import mlx_lm

MODEL_PATH = "models/llama-3.2-3b-4bit"
OUTPUT_PATH = "results/baseline_responses.json"
MAX_TOKENS = 200

PROMPTS = [
    "What is boundary scan testing and when would you use it?",
    "A laptop powers on but the screen stays black. Walk me through a systematic hardware diagnostic process.",
    "Explain the difference between ECC and non-ECC memory, and how memory errors are detected.",
    "What are common causes of intermittent PCIe bus errors and how would you diagnose them?",
]


def run_inference(model, tokenizer, prompt: str) -> dict:
    """Run a single prompt through the model and collect timing stats."""
    # Use stream_generate to get per-token timing metadata
    full_text = ""
    final_response = None
    for response in mlx_lm.stream_generate(
        model, tokenizer, prompt, max_tokens=MAX_TOKENS
    ):
        full_text += response.text
        final_response = response

    return {
        "prompt": prompt,
        "response": full_text.strip(),
        "prompt_tokens": final_response.prompt_tokens,
        "generation_tokens": final_response.generation_tokens,
        "prompt_tps": round(final_response.prompt_tps, 2),
        "generation_tps": round(final_response.generation_tps, 2),
        "peak_memory_gb": round(final_response.peak_memory, 3),
    }


def main():
    project_root = Path(__file__).resolve().parent.parent
    model_path = str(project_root / MODEL_PATH)
    output_path = project_root / OUTPUT_PATH

    print(f"Loading model from {model_path} ...")
    model, tokenizer = mlx_lm.load(model_path)
    print("Model loaded.\n")

    results = []
    for i, prompt in enumerate(PROMPTS, 1):
        print(f"{'='*70}")
        print(f"Prompt {i}/{len(PROMPTS)}: {prompt}")
        print(f"{'='*70}")

        result = run_inference(model, tokenizer, prompt)
        results.append(result)

        print(f"\n{result['response']}\n")
        print(
            f"  Prompt tokens: {result['prompt_tokens']}  |  "
            f"Prompt speed: {result['prompt_tps']} tok/s"
        )
        print(
            f"  Generated tokens: {result['generation_tokens']}  |  "
            f"Generation speed: {result['generation_tps']} tok/s"
        )
        print(f"  Peak memory: {result['peak_memory_gb']} GB")
        print()

    # Save results
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output = {
        "model": MODEL_PATH,
        "max_tokens": MAX_TOKENS,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "results": results,
    }
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Baseline responses saved to {output_path}")


if __name__ == "__main__":
    main()
