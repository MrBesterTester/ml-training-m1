#!/usr/bin/env python3
"""
review_fdfi_dataset.py — Quality review tool for FD/FI training entries.

Reads JSONL data files and generates a comprehensive review report
(results/fdfi_review_summary.md) to help Sam evaluate entry quality
before approving for fine-tuning.

Usage:
    python scripts/review_fdfi_dataset.py
"""

import json
import os
import random
import re
from collections import Counter, defaultdict

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CATEGORY_FILES = {
    "FD":    os.path.join(PROJECT_ROOT, "data", "fdfi_fd_entries.jsonl"),
    "FI":    os.path.join(PROJECT_ROOT, "data", "fdfi_fi_entries.jsonl"),
    "FD+FI": os.path.join(PROJECT_ROOT, "data", "fdfi_combined_entries.jsonl"),
    "TRIAGE": os.path.join(PROJECT_ROOT, "data", "fdfi_triage_entries.jsonl"),
}

OUTPUT_PATH = os.path.join(PROJECT_ROOT, "results", "fdfi_review_summary.md")

SEED = 42

# Hardware domain keyword patterns (compiled once).
# Order matters: more specific patterns checked first to avoid false positives.
DOMAIN_PATTERNS = {
    "boundary_scan": re.compile(
        r"\b(boundary.scan|JTAG|TAP|IDCODE|TDI|TDO|TCK|TMS|BSDL|chain.integrity)\b",
        re.IGNORECASE,
    ),
    "signal_integrity": re.compile(
        r"\b(signal.integrit|TDR|impedance|eye.diagram|crosstalk|S-parameter|"
        r"return.loss|insertion.loss|rise.time|overshoot|undershoot|ringing|"
        r"reflection|controlled.impedance)\b",
        re.IGNORECASE,
    ),
    "in_circuit_test": re.compile(
        r"\b(in.circuit.test|ICT|bed.of.nails|flying.probe|fixture|"
        r"probe.contact|guard.point|Kelvin)\b",
        re.IGNORECASE,
    ),
    "thermal": re.compile(
        r"\b(temperature|thermal|heat|Icc|junction.temp|theta_J|"
        r"hot.?spot|IR.camera|thermocouple|heat.?sink|TIM|"
        r"power.dissipation|derating)\b",
        re.IGNORECASE,
    ),
    "mixed_signal": re.compile(
        r"\b(ADC|DAC|jitter|phase.noise|SNR|ENOB|SFDR|DNL|INL|"
        r"analog.to.digital|digital.to.analog|mixed.signal|"
        r"sampling|quantization|aperture)\b",
        re.IGNORECASE,
    ),
    "functional_test": re.compile(
        r"\b(functional.test|logic.test|firmware.test|boot.test|"
        r"POST|self.test|BIST|register.read|bus.exercise|"
        r"memory.test|DDR|DRAM|SRAM)\b",
        re.IGNORECASE,
    ),
    "production_test": re.compile(
        r"\b(SPC|yield|Cpk|process.capabilit|Cp\b|production.test|"
        r"test.coverage|defect.level|DPMO|first.pass|"
        r"test.time|throughput|bin\b|binning)\b",
        re.IGNORECASE,
    ),
    "environmental": re.compile(
        r"\b(humidity|corrosion|vibration|altitude|moisture|"
        r"salt.spray|condensation|dew.point|conformal.coat|"
        r"shock|acceleration|HALT|HASS|MIL-STD)\b",
        re.IGNORECASE,
    ),
}

# Hedging language that suggests judgment calls.
HEDGING_PATTERNS = re.compile(
    r"\b(alternatively|could also be|secondary possibility|"
    r"less likely|another possibility|if .*? then|"
    r"one possibility|cannot rule out|worth investigating|"
    r"differential diagnosis|competing hypothesis|"
    r"ambiguous|either .* or)\b",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_jsonl(path):
    """Load a JSONL file and return a list of dicts."""
    entries = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries


def word_count(text):
    """Simple whitespace word count."""
    return len(text.split())


def infer_domain(entry):
    """Return the best-matching hardware domain for an entry, or 'unclassified'."""
    text = entry["instruction"] + " " + entry["output"]
    matches = []
    for domain, pattern in DOMAIN_PATTERNS.items():
        hits = pattern.findall(text)
        if hits:
            matches.append((domain, len(hits)))
    if not matches:
        return "unclassified"
    # Return domain with most keyword hits.
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches[0][0]


def truncate(text, length):
    """Truncate text to `length` characters, adding ellipsis if needed."""
    if len(text) <= length:
        return text
    return text[:length].rstrip() + "..."


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_all_entries():
    """
    Load entries from each category file.
    Returns dict {category: [entries]} where each entry is augmented with
    'category', 'domain', and 'output_words'.
    """
    data = {}
    for category, path in CATEGORY_FILES.items():
        if not os.path.exists(path):
            print(f"  WARNING: {path} not found, skipping {category}")
            continue
        raw = load_jsonl(path)
        for entry in raw:
            entry["category"] = category
            entry["domain"] = infer_domain(entry)
            entry["output_words"] = word_count(entry["output"])
        data[category] = raw
    return data


# ---------------------------------------------------------------------------
# Report sections
# ---------------------------------------------------------------------------

def section_summary(data):
    """Generate the summary statistics section."""
    lines = []
    lines.append("## 1. Summary Statistics\n")

    # --- Counts by category ---
    lines.append("### Counts by Category\n")
    lines.append("| Category | Count |")
    lines.append("|----------|------:|")
    total = 0
    for cat in ["FD", "FI", "FD+FI", "TRIAGE"]:
        count = len(data.get(cat, []))
        total += count
        lines.append(f"| {cat} | {count} |")
    lines.append(f"| **Total** | **{total}** |")
    lines.append("")

    # --- Counts by inferred domain ---
    lines.append("### Counts by Inferred Hardware Domain\n")
    domain_counter = Counter()
    for entries in data.values():
        for e in entries:
            domain_counter[e["domain"]] += 1
    lines.append("| Domain | Count |")
    lines.append("|--------|------:|")
    for domain, count in domain_counter.most_common():
        lines.append(f"| {domain} | {count} |")
    lines.append("")

    # --- Response length stats by category ---
    lines.append("### Response Length (words) by Category\n")
    lines.append("| Category | Avg | Min | Max |")
    lines.append("|----------|----:|----:|----:|")
    for cat in ["FD", "FI", "FD+FI", "TRIAGE"]:
        entries = data.get(cat, [])
        if not entries:
            continue
        lengths = [e["output_words"] for e in entries]
        avg = sum(lengths) / len(lengths)
        lines.append(f"| {cat} | {avg:.0f} | {min(lengths)} | {max(lengths)} |")

    # Overall
    all_lengths = [e["output_words"] for entries in data.values() for e in entries]
    if all_lengths:
        avg_all = sum(all_lengths) / len(all_lengths)
        lines.append(f"| **All** | **{avg_all:.0f}** | **{min(all_lengths)}** | **{max(all_lengths)}** |")
    lines.append("")

    return "\n".join(lines)


def section_flagged(data):
    """Generate the flagged-entries section."""
    lines = []
    lines.append("## 2. Flagged Entries for Review\n")

    all_entries = [e for entries in data.values() for e in entries]

    # --- Complex physics: top 10% by word count ---
    if all_entries:
        sorted_by_len = sorted(all_entries, key=lambda e: e["output_words"], reverse=True)
        cutoff_idx = max(1, len(sorted_by_len) // 10)
        threshold = sorted_by_len[cutoff_idx - 1]["output_words"]
        complex_entries = [e for e in all_entries if e["output_words"] >= threshold]
    else:
        complex_entries = []

    lines.append(f"### Complex Physics (top 10% by response length, >= {threshold} words)\n")
    lines.append(f"**{len(complex_entries)} entries flagged**\n")
    for e in sorted(complex_entries, key=lambda x: x["output_words"], reverse=True):
        lines.append(f"- **[{e['category']}] {e['domain']}** ({e['output_words']} words)")
        lines.append(f"  - Instruction: {truncate(e['instruction'], 120)}")
        lines.append(f"  - Response preview: {truncate(e['output'], 200)}")
        lines.append("")

    # --- Judgment calls: hedging language ---
    judgment_entries = []
    for e in all_entries:
        matches = HEDGING_PATTERNS.findall(e["output"])
        if matches:
            e["_hedge_matches"] = matches
            judgment_entries.append(e)

    lines.append(f"### Judgment Calls (hedging language detected)\n")
    lines.append(f"**{len(judgment_entries)} entries flagged**\n")
    for e in judgment_entries:
        hedge_examples = list(set(m if isinstance(m, str) else m[0] for m in e["_hedge_matches"]))[:3]
        lines.append(f"- **[{e['category']}] {e['domain']}** ({e['output_words']} words)")
        lines.append(f"  - Hedging: {', '.join(repr(h) for h in hedge_examples)}")
        lines.append(f"  - Instruction: {truncate(e['instruction'], 120)}")
        lines.append(f"  - Response preview: {truncate(e['output'], 200)}")
        lines.append("")

    # --- Subtle triage: triage entries that sound like real faults ---
    # Heuristic: triage instructions that contain fault-like language.
    FAULT_LIKE = re.compile(
        r"\b(fail|failure|failing|defect|fault|anomal|degrad|marginal|"
        r"intermittent|dropout|drift|error|errored|unstable|abnormal|"
        r"out.of.spec|excessive|overshoot|undershoot|miss|missing)\b",
        re.IGNORECASE,
    )
    triage_entries = data.get("TRIAGE", [])
    subtle_triage = []
    for e in triage_entries:
        fault_hits = FAULT_LIKE.findall(e["instruction"])
        if len(fault_hits) >= 2:
            e["_fault_hits"] = list(set(fault_hits))[:4]
            subtle_triage.append(e)

    lines.append(f"### Subtle Triage (instructions that sound like real hardware faults)\n")
    lines.append(f"**{len(subtle_triage)} of {len(triage_entries)} triage entries flagged**\n")
    for e in subtle_triage:
        lines.append(f"- **[TRIAGE] {e['domain']}** ({e['output_words']} words)")
        lines.append(f"  - Fault-like terms in instruction: {', '.join(repr(h) for h in e['_fault_hits'])}")
        lines.append(f"  - Instruction: {truncate(e['instruction'], 120)}")
        lines.append(f"  - Response preview: {truncate(e['output'], 200)}")
        lines.append("")

    return "\n".join(lines)


def section_samples(data):
    """Generate the sample entries section (2 per category, fixed seed)."""
    lines = []
    lines.append("## 3. Sample Entries (2 per category, seed=42)\n")

    rng = random.Random(SEED)

    for cat in ["FD", "FI", "FD+FI", "TRIAGE"]:
        entries = data.get(cat, [])
        if not entries:
            continue

        sample_size = min(2, len(entries))
        samples = rng.sample(entries, sample_size)

        lines.append(f"### {cat}\n")
        for i, e in enumerate(samples, 1):
            lines.append(f"#### Sample {i} — {e['domain']} ({e['output_words']} words)\n")
            lines.append(f"**Instruction:**\n")
            lines.append(f"> {e['instruction']}\n")
            lines.append(f"**Response:**\n")
            lines.append(f"{e['output']}\n")
            lines.append("---\n")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Loading FD/FI entries...")
    data = load_all_entries()

    total = sum(len(v) for v in data.values())
    if total == 0:
        print("ERROR: No entries loaded. Check data file paths.")
        return

    for cat, entries in data.items():
        print(f"  {cat}: {len(entries)} entries")
    print(f"  Total: {total}")

    print("\nBuilding review report...")

    # Assemble report.
    report_parts = []
    report_parts.append("# FD/FI Dataset Quality Review\n")
    report_parts.append(
        "Auto-generated by `scripts/review_fdfi_dataset.py`. "
        "Use this report to evaluate entry quality before approving for training.\n"
    )
    report_parts.append(section_summary(data))
    report_parts.append(section_flagged(data))
    report_parts.append(section_samples(data))

    report = "\n".join(report_parts)

    # Write report.
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\nReport written to: {OUTPUT_PATH}")

    # --- Console summary ---
    all_entries = [e for entries in data.values() for e in entries]
    sorted_by_len = sorted(all_entries, key=lambda e: e["output_words"], reverse=True)
    cutoff_idx = max(1, len(sorted_by_len) // 10)
    threshold = sorted_by_len[cutoff_idx - 1]["output_words"]
    n_complex = sum(1 for e in all_entries if e["output_words"] >= threshold)
    n_judgment = sum(1 for e in all_entries if HEDGING_PATTERNS.search(e["output"]))

    triage_entries = data.get("TRIAGE", [])
    FAULT_LIKE = re.compile(
        r"\b(fail|failure|failing|defect|fault|anomal|degrad|marginal|"
        r"intermittent|dropout|drift|error|errored|unstable|abnormal|"
        r"out.of.spec|excessive|overshoot|undershoot|miss|missing)\b",
        re.IGNORECASE,
    )
    n_subtle = sum(1 for e in triage_entries if len(FAULT_LIKE.findall(e["instruction"])) >= 2)

    print(f"\nFlagged for review:")
    print(f"  Complex physics (long responses): {n_complex}")
    print(f"  Judgment calls (hedging language): {n_judgment}")
    print(f"  Subtle triage (sound like real faults): {n_subtle}/{len(triage_entries)}")
    print(f"\nTotal flagged: {n_complex + n_judgment + n_subtle} "
          f"(some entries may appear in multiple categories)")
    print("\nDone.")


if __name__ == "__main__":
    main()
