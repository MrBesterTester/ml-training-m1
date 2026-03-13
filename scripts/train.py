#!/usr/bin/env python3
"""LoRA fine-tuning script for hardware diagnostics LLM.

Wraps mlx_lm.lora with project-specific defaults. Can be run directly
or used to print the equivalent CLI command.

Usage:
    python scripts/train.py              # run training
    python scripts/train.py --dry-run    # print config and CLI command only
"""

import argparse
import subprocess
import sys
from pathlib import Path

# Project paths (relative to repo root)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "llama-3.2-3b-4bit"
DATA_PATH = PROJECT_ROOT / "data"
ADAPTER_PATH = PROJECT_ROOT / "adapters" / "hw-diagnostics"
LOG_PATH = PROJECT_ROOT / "results" / "training_log.txt"

# Training hyperparameters
CONFIG = {
    "iters": 600,
    "batch_size": 2,
    "lora_layers": 8,
    "learning_rate": 1e-5,
}


def check_prerequisites():
    """Verify model and data files exist before training."""
    errors = []
    if not MODEL_PATH.exists():
        errors.append(f"Model not found: {MODEL_PATH}")
    if not (DATA_PATH / "train.jsonl").exists():
        errors.append(f"Training data not found: {DATA_PATH / 'train.jsonl'}")
    if not (DATA_PATH / "valid.jsonl").exists():
        errors.append(f"Validation data not found: {DATA_PATH / 'valid.jsonl'}")
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


def build_command():
    """Build the mlx_lm.lora CLI command."""
    return [
        sys.executable, "-m", "mlx_lm.lora",
        "--model", str(MODEL_PATH),
        "--data", str(DATA_PATH),
        "--train",
        "--iters", str(CONFIG["iters"]),
        "--batch-size", str(CONFIG["batch_size"]),
        "--lora-layers", str(CONFIG["lora_layers"]),
        "--learning-rate", str(CONFIG["learning_rate"]),
        "--adapter-path", str(ADAPTER_PATH),
    ]


def print_config():
    """Print training configuration."""
    print("=" * 60)
    print("Hardware Diagnostics LLM — LoRA Fine-Tuning")
    print("=" * 60)
    print(f"  Model:         {MODEL_PATH}")
    print(f"  Data:          {DATA_PATH}")
    print(f"  Adapter out:   {ADAPTER_PATH}")
    print(f"  Log:           {LOG_PATH}")
    print(f"  Iterations:    {CONFIG['iters']}")
    print(f"  Batch size:    {CONFIG['batch_size']}")
    print(f"  LoRA layers:   {CONFIG['lora_layers']}")
    print(f"  Learning rate: {CONFIG['learning_rate']}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Run LoRA fine-tuning")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print config and command without running")
    args = parser.parse_args()

    check_prerequisites()
    print_config()

    cmd = build_command()
    print(f"\nCommand:\n  {' '.join(cmd)}\n")

    if args.dry_run:
        print("(dry run — not executing)")
        return

    # Ensure output directories exist
    ADAPTER_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Run training, tee output to both stdout and log file
    print("Starting training...\n")
    with open(LOG_PATH, "w") as log_file:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        for line in process.stdout:
            sys.stdout.write(line)
            sys.stdout.flush()
            log_file.write(line)
        process.wait()

    if process.returncode != 0:
        print(f"\nTraining failed with exit code {process.returncode}")
        sys.exit(process.returncode)

    print(f"\nTraining complete. Adapter saved to: {ADAPTER_PATH}")
    print(f"Training log saved to: {LOG_PATH}")


if __name__ == "__main__":
    main()
