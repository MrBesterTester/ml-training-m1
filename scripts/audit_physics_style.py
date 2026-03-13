#!/usr/bin/env python3
"""
Audit full_dataset.jsonl for physics-first style authenticity.

Classifies each entry as:
  - PHYSICS-FIRST: Physics is load-bearing; remove it and the explanation collapses
  - PHYSICS-DECORATED: Core topic is software/protocol/process; physics is sprinkled in
  - MIXED: Legitimate blend of physics and non-physics diagnostic reasoning

Outputs a report with flagged entries and reasons.
"""

import json
import re
import sys
from pathlib import Path
from collections import Counter

DATA_FILE = Path(__file__).parent.parent / "data" / "full_dataset.jsonl"
REPORT_FILE = Path(__file__).parent.parent / "results" / "physics_audit_report.md"

# --- Heuristic signals ---

# Keywords in the INSTRUCTION suggesting software/protocol/process topics
SOFTWARE_TOPIC_KEYWORDS = [
    r"\bSCPI\b", r"\bVISA\b", r"\bPyVISA\b", r"\bpyvisa\b",
    r"\bPython\b", r"\bstate machine\b", r"\bsequencer\b",
    r"\blogging\b", r"\blog format\b", r"\bdata format\b",
    r"\bdatabase\b", r"\bSQL\b", r"\bSQLite\b", r"\bPostgreSQL\b",
    r"\bInfluxDB\b", r"\bTimescaleDB\b",
    r"\berror handling\b", r"\brecovery\b", r"\babstraction layer\b",
    r"\bpolling\b", r"\bevent.driven\b",
    r"\bCI/CD\b", r"\bDocker\b",
    r"\btest result.*(log|stor|format)\b",
    r"\bautomated test seq\b",
]

# Keywords in the INSTRUCTION suggesting hardware/physics topics
HARDWARE_TOPIC_KEYWORDS = [
    r"\bsolder\b", r"\bBGA\b", r"\breflow\b", r"\bimpedance\b",
    r"\btransmission line\b", r"\bsignal integrity\b", r"\bcrosstalk\b",
    r"\bthermal\b", r"\btemperature\b", r"\bvoltage\b", r"\bcurrent\b",
    r"\bEMI\b", r"\bEMC\b", r"\bESD\b",
    r"\bJTAG\b", r"\bboundary scan\b", r"\bTDR\b",
    r"\bcapacit\w+\b", r"\binduct\w+\b", r"\bresist\w+\b",
    r"\bX-ray\b", r"\bAOI\b", r"\bSPI measurement\b",
    r"\bADC\b", r"\bDAC\b", r"\bPLL\b", r"\bSerDes\b",
    r"\bnoise\b", r"\bjitter\b", r"\bphase noise\b",
    r"\bsolder joint\b", r"\bvoid\b", r"\bcrack\b",
    r"\breflection\b", r"\bringing\b",
    r"\bDDR\b", r"\bUSB\b", r"\bPCIe\b",
    r"\bpower supply\b", r"\bregulator\b",
    r"\bcrystal\b", r"\boscillator\b",
    r"\bfault coverage\b", r"\bstuck.at\b",
    r"\bICT\b", r"\bin-circuit\b",
    r"\bcontact resistance\b", r"\bprobe\b",
    r"\bconformal coat\b", r"\bshock test\b", r"\bburn-in\b",
    r"\bthermal cycl\b", r"\breliability\b",
    r"\bwatchdog\b", r"\bBIST\b", r"\bLFSR\b",
]

# Phrases in the OUTPUT suggesting forced/decorative physics analogies
FORCED_ANALOGY_PHRASES = [
    r"analogous to",
    r"similar to how .* in physics",
    r"just as .* in (physics|electromagnet|circuit)",
    r"akin to .* (physics|wave|field)",
    r"governed by the same physics as",
    r"this is (fundamentally|essentially) a .* (physics|signal|impedance|electromagnetic|wave|transmission) problem",
]

# Equations/formulas (look for = with variables)
EQUATION_PATTERN = re.compile(
    r"[A-Za-z_]\w*\s*=\s*[A-Za-z_\d\(\)].*?[\+\-\*/\^]|"  # var = expr with operator
    r"\b[A-Z]_\w+\s*=\s*|"                                    # V_drop = ...
    r"\bsqrt\(|"
    r"\bexp\(|"
    r"\bln\(|log\d*\(|"
    r"\bintegral\(|"
    r"\bpi\s*\*|"
    r"\bepsilon_|"
    r"\bmu_0|"
    r"\bgamma\s*[\*=]|"
    r"\brho\s*[\*/=]|"
    r"\bomega\b"
)


def count_matches(text, patterns):
    """Count how many patterns match in text (case-insensitive)."""
    count = 0
    matched = []
    for pat in patterns:
        if re.search(pat, text, re.IGNORECASE):
            count += 1
            matched.append(pat)
    return count, matched


def count_equations(text):
    """Count approximate number of equations/formulas in text."""
    return len(EQUATION_PATTERN.findall(text))


def classify_entry(idx, entry):
    """Classify a single dataset entry. Returns (classification, reasons)."""
    instruction = entry.get("instruction", "")
    output = entry.get("output", "")

    sw_score, sw_matches = count_matches(instruction + " " + output[:200],
                                          SOFTWARE_TOPIC_KEYWORDS)
    hw_score, hw_matches = count_matches(instruction + " " + output[:200],
                                          HARDWARE_TOPIC_KEYWORDS)
    analogy_score, analogy_matches = count_matches(output, FORCED_ANALOGY_PHRASES)
    eq_count = count_equations(output)

    reasons = []

    # Primary classification: is the topic inherently software/protocol?
    topic_is_software = sw_score >= 2 and sw_score > hw_score
    topic_is_hardware = hw_score >= 2 and hw_score > sw_score
    topic_is_mixed = (sw_score >= 1 and hw_score >= 1 and
                      abs(sw_score - hw_score) <= 1)

    if topic_is_software:
        reasons.append(f"Software/protocol topic (sw={sw_score}, hw={hw_score})")

        if eq_count >= 4:
            reasons.append(f"Heavy equation use ({eq_count}) in software topic → likely decorative")
            return "PHYSICS-DECORATED", reasons

        if analogy_score >= 1:
            reasons.append(f"Forced physics analogies: {analogy_matches}")
            return "PHYSICS-DECORATED", reasons

        # Software topic with some equations — could be legitimately relevant
        if eq_count <= 2:
            reasons.append("Software topic with minimal physics — may need reframing")
            return "MIXED", reasons

        reasons.append(f"Software topic with moderate physics ({eq_count} equations)")
        return "PHYSICS-DECORATED", reasons

    if topic_is_hardware:
        if analogy_score >= 2 and eq_count < 2:
            reasons.append("Hardware topic but relies on analogies instead of actual physics")
            return "MIXED", reasons
        reasons.append(f"Hardware/physics topic (hw={hw_score}, eq={eq_count})")
        return "PHYSICS-FIRST", reasons

    if topic_is_mixed:
        if analogy_score >= 1 and sw_score >= hw_score:
            reasons.append(f"Mixed topic leaning software with analogies")
            return "PHYSICS-DECORATED", reasons
        reasons.append(f"Mixed topic (sw={sw_score}, hw={hw_score})")
        return "MIXED", reasons

    # Default: low keyword scores — look at equation density
    if eq_count >= 3:
        reasons.append(f"Good equation density ({eq_count}), likely physics-first")
        return "PHYSICS-FIRST", reasons

    reasons.append(f"Low signal (sw={sw_score}, hw={hw_score}, eq={eq_count})")
    return "MIXED", reasons


def main():
    entries = []
    with open(DATA_FILE, "r") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            entry["_line"] = i
            entries.append(entry)

    print(f"Loaded {len(entries)} entries from {DATA_FILE.name}\n")

    results = {"PHYSICS-FIRST": [], "PHYSICS-DECORATED": [], "MIXED": []}

    for i, entry in enumerate(entries):
        classification, reasons = classify_entry(i, entry)
        results[classification].append({
            "line": entry["_line"],
            "instruction": entry["instruction"][:120],
            "reasons": reasons,
        })

    # --- Console summary ---
    total = len(entries)
    for cat in ["PHYSICS-FIRST", "PHYSICS-DECORATED", "MIXED"]:
        n = len(results[cat])
        pct = 100 * n / total
        print(f"  {cat:20s}: {n:3d} entries ({pct:.0f}%)")

    print(f"\n{'='*70}")
    print(f"PHYSICS-DECORATED entries (need reframing):")
    print(f"{'='*70}")
    for item in results["PHYSICS-DECORATED"]:
        print(f"\n  Line {item['line']:3d}: {item['instruction']}")
        for r in item["reasons"]:
            print(f"          → {r}")

    print(f"\n{'='*70}")
    print(f"MIXED entries (review recommended):")
    print(f"{'='*70}")
    for item in results["MIXED"]:
        print(f"\n  Line {item['line']:3d}: {item['instruction']}")
        for r in item["reasons"]:
            print(f"          → {r}")

    # --- Write markdown report ---
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_FILE, "w") as f:
        f.write("# Physics Style Audit Report\n\n")
        f.write(f"**Dataset:** {DATA_FILE.name} ({total} entries)\n\n")
        f.write("## Summary\n\n")
        f.write("| Classification | Count | % |\n")
        f.write("|---|---|---|\n")
        for cat in ["PHYSICS-FIRST", "PHYSICS-DECORATED", "MIXED"]:
            n = len(results[cat])
            f.write(f"| {cat} | {n} | {100*n/total:.0f}% |\n")

        f.write("\n## PHYSICS-DECORATED (need reframing)\n\n")
        f.write("These entries cover topics where physics is not the primary explanatory ")
        f.write("framework, but physics equations/analogies are inserted as decoration. ")
        f.write("Recommended fix: reframe to honestly triage between physics and ")
        f.write("non-physics causes.\n\n")
        for item in results["PHYSICS-DECORATED"]:
            f.write(f"### Line {item['line']}\n\n")
            f.write(f"**Q:** {item['instruction']}...\n\n")
            for r in item["reasons"]:
                f.write(f"- {r}\n")
            f.write("\n")

        f.write("\n## MIXED (review recommended)\n\n")
        f.write("These entries blend physics and non-physics content. Review to confirm ")
        f.write("the physics is genuinely load-bearing.\n\n")
        for item in results["MIXED"]:
            f.write(f"### Line {item['line']}\n\n")
            f.write(f"**Q:** {item['instruction']}...\n\n")
            for r in item["reasons"]:
                f.write(f"- {r}\n")
            f.write("\n")

    print(f"\nFull report written to {REPORT_FILE}")


if __name__ == "__main__":
    main()
