"""
Hardware diagnostics topic taxonomy, question templates, and prompt generator.

Defines ~12 hardware diagnostics categories with realistic subtopics
and underlying physics-principle mappings, five question template styles
(troubleshooting, how_to, comparison, best_practice, physics_why), and a
combinatorial generator that produces diverse training prompts for fine-tuning.
"""

import random
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent

TOPICS = [
    {
        "name": "boundary_scan_jtag",
        "display_name": "Boundary Scan / JTAG Testing",
        "subtopics": [
            "IEEE 1149.1 TAP controller state machine",
            "BSDL file validation for BGA components",
            "boundary scan chain integrity verification",
            "JTAG-based flash programming and debug access",
            "interconnect testing for fine-pitch solder joints",
        ],
        "physics_principles": [
            "signal propagation delay",
            "clock domain crossing",
            "transmission line effects",
        ],
    },
    {
        "name": "functional_test",
        "display_name": "Functional Test Strategies",
        "subtopics": [
            "power sequencing and rail margining validation",
            "clock tree verification using frequency counters",
            "high-speed serial interface loopback testing",
            "peripheral bus enumeration and response checks",
            "firmware-assisted POST (Power-On Self Test) routines",
        ],
        "physics_principles": [
            "power delivery physics",
            "clock distribution",
            "signal integrity",
        ],
    },
    {
        "name": "fault_isolation",
        "display_name": "Fault Isolation and Root Cause Analysis",
        "subtopics": [
            "thermal imaging for hotspot localization",
            "time-domain reflectometry (TDR) for open/short detection",
            "guided probe diagnostics using fault dictionaries",
            "statistical Pareto analysis of field failure returns",
            "5-why causal chain analysis for intermittent defects",
        ],
        "physics_principles": [
            "statistical reasoning",
            "thermal physics (IR imaging)",
            "wave propagation (TDR)",
        ],
    },
    {
        "name": "test_coverage",
        "display_name": "Test Coverage Analysis",
        "subtopics": [
            "stuck-at fault coverage metrics and gap analysis",
            "IDDQ quiescent current testing coverage",
            "defect-per-million (DPM) correlation to test escapes",
            "untestable net identification and mitigation",
            "coverage overlap between ICT, functional, and boundary scan",
        ],
        "physics_principles": [
            "information theory",
            "entropy as coverage metric",
        ],
    },
    {
        "name": "mixed_signal",
        "display_name": "Mixed-Signal Board Testing",
        "subtopics": [
            "ADC/DAC linearity and monotonicity verification",
            "analog-to-digital converter INL/DNL measurement",
            "RF front-end gain and noise figure characterization",
            "phase-locked loop (PLL) lock time and jitter analysis",
            "mixed-signal stimulus-response using arbitrary waveform generators",
        ],
        "physics_principles": [
            "sampling theory (Nyquist)",
            "noise physics",
            "phase-locked loop dynamics",
        ],
    },
    {
        "name": "in_circuit_test",
        "display_name": "In-Circuit Test (ICT) Methodologies",
        "subtopics": [
            "bed-of-nails fixture design for high-density PCBs",
            "guarded measurement techniques for in-circuit resistance",
            "capacitor ESR and inductance measurement under fixture",
            "vectorless test methods for unpowered cluster testing",
            "flying probe versus fixed-fixture ICT trade-offs",
        ],
        "physics_principles": [
            "circuit theory (Kirchhoff's laws, Ohm's law)",
            "impedance",
            "guarded measurements",
        ],
    },
    {
        "name": "embedded_diagnostics",
        "display_name": "Embedded Diagnostics",
        "subtopics": [
            "BIST (Built-In Self Test) for memory subsystems",
            "on-chip temperature and voltage sensor readback",
            "watchdog timer and reset circuit validation",
            "UART/SPI/I2C bus health monitoring via embedded agents",
            "FPGA-based logic BIST pattern generation",
        ],
        "physics_principles": [
            "semiconductor physics (voltage/temp sensors)",
            "digital logic timing",
        ],
    },
    {
        "name": "test_automation",
        "display_name": "Test Automation Frameworks",
        "subtopics": [
            "instrument abstraction layers (VISA, SCPI) for test stations",
            "test sequencer state machines and branching logic",
            "parallel test execution across multi-DUT fixtures",
            "test result database schema and traceability",
            "CI/CD integration for regression test suites on hardware",
        ],
        "physics_principles": [
            "measurement physics (VISA/SCPI instrument models)",
        ],
    },
    {
        "name": "production_test_optimization",
        "display_name": "Production Test Optimization",
        "subtopics": [
            "test time reduction through adaptive test sequencing",
            "yield-aware test flow partitioning",
            "golden board calibration and drift compensation",
            "first-pass yield (FPY) improvement via test data analytics",
            "fixture maintenance scheduling based on contact resistance trends",
        ],
        "physics_principles": [
            "statistical process control",
            "measurement uncertainty",
        ],
    },
    {
        "name": "environmental_stress",
        "display_name": "Environmental and Stress Testing",
        "subtopics": [
            "HALT (Highly Accelerated Life Test) profile design",
            "thermal cycling and solder joint fatigue screening",
            "vibration and mechanical shock qualification per MIL-STD-810",
            "humidity and condensation effects on conformal-coated assemblies",
            "burn-in strategies for infant mortality screening",
        ],
        "physics_principles": [
            "thermodynamics",
            "mechanical stress-strain",
            "Arrhenius acceleration models",
        ],
    },
    {
        "name": "signal_power_integrity",
        "display_name": "Signal Integrity and Power Integrity",
        "subtopics": [
            "eye diagram analysis for high-speed differential pairs",
            "power distribution network (PDN) impedance profiling",
            "crosstalk measurement on adjacent trace pairs",
            "jitter decomposition (RJ, DJ, TJ) on SerDes links",
            "decoupling capacitor placement and PDN resonance mitigation",
        ],
        "physics_principles": [
            "electromagnetic wave propagation",
            "transmission line theory",
            "PDN impedance",
        ],
    },
    {
        "name": "aoi_xray",
        "display_name": "Automated Optical Inspection (AOI) and X-Ray Inspection",
        "subtopics": [
            "solder paste volume measurement via 3D SPI",
            "BGA void percentage analysis using 2D/3D X-ray",
            "tombstone and component skew detection algorithms",
            "head-in-pillow defect identification on package-on-package",
            "machine learning classifiers for false-call reduction in AOI",
        ],
        "physics_principles": [
            "optics",
            "X-ray absorption physics",
            "image processing",
        ],
    },
]

TEMPLATES = {
    "troubleshooting": [
        "A board fails {display_name} with errors related to {subtopic}. "
        "What are the most likely root causes and how would you systematically "
        "isolate the failure?",
        "During production testing, intermittent failures appear in "
        "{display_name} specifically around {subtopic}. Describe your "
        "diagnostic workflow to identify whether this is a design issue, "
        "a process defect, or a test artifact.",
        "A field return unit exhibits symptoms pointing to {subtopic} "
        "degradation. How would you reproduce the failure in the lab and "
        "confirm the root cause using {display_name} techniques?",
    ],
    "how_to": [
        "Explain step by step how to set up and execute {display_name} "
        "focused on {subtopic} for a newly designed PCB assembly.",
        "What is the recommended procedure for validating {subtopic} "
        "as part of a {display_name} program on a multi-layer board?",
        "Walk through the process of implementing {subtopic} within a "
        "{display_name} workflow, including required equipment and "
        "key measurement parameters.",
    ],
    "comparison": [
        "Compare the effectiveness of {subtopic_a} versus {subtopic_b} "
        "in the context of {display_name}. What are the trade-offs in "
        "fault coverage, test time, and implementation cost?",
        "When would you choose {subtopic_a} over {subtopic_b} for "
        "{display_name}? Discuss the technical and practical factors "
        "that influence this decision.",
    ],
    "best_practice": [
        "What are the industry best practices for {subtopic} within "
        "{display_name}? Include guidelines for test development, "
        "debug, and production deployment.",
        "Describe the design-for-testability (DFT) considerations that "
        "improve {subtopic} outcomes in {display_name} applications.",
        "What common pitfalls should engineers avoid when implementing "
        "{subtopic} as part of {display_name}, and how can these be "
        "prevented?",
    ],
    "physics_why": [
        "From a physics perspective, why does {subtopic} behave the way "
        "it does in {display_name}? Explain the underlying physical "
        "principles.",
        "What are the underlying physical principles that explain "
        "{subtopic} in the context of {display_name}?",
        "Describe the fundamental physics behind {subtopic} and how those "
        "principles shape practical outcomes in {display_name}.",
    ],
}


def generate_prompts(seed: int = 42) -> list[dict]:
    """Generate diverse hardware diagnostics prompts via combinatorial expansion.

    Iterates all topics x all styles, picks one random template variation
    per combination, and fills placeholders with the category display name
    and randomly selected subtopic(s).

    Args:
        seed: Random seed for reproducibility.

    Returns:
        List of dicts with keys: instruction, category, style.
    """
    rng = random.Random(seed)
    prompts: list[dict] = []

    for topic in TOPICS:
        display_name = topic["display_name"]
        subtopics = topic["subtopics"]

        for style, templates in TEMPLATES.items():
            template = rng.choice(templates)

            if style == "comparison":
                # Comparison needs two distinct subtopics
                pair = rng.sample(subtopics, 2)
                instruction = template.format(
                    display_name=display_name,
                    subtopic_a=pair[0],
                    subtopic_b=pair[1],
                )
            else:
                subtopic = rng.choice(subtopics)
                instruction = template.format(
                    display_name=display_name,
                    subtopic=subtopic,
                )

            prompts.append({
                "instruction": instruction,
                "category": topic["name"],
                "style": style,
            })

    return prompts


def main() -> None:
    """Print a diverse sample of generated prompts with summary statistics."""
    all_prompts = generate_prompts()

    # Sample 20 prompts, ensuring diversity across styles
    rng = random.Random(42)
    sample = rng.sample(all_prompts, min(20, len(all_prompts)))

    print(f"{'=' * 80}")
    print("HARDWARE DIAGNOSTICS — SAMPLE PROMPTS")
    print(f"{'=' * 80}\n")

    for i, prompt in enumerate(sample, 1):
        print(f"[{i:02d}]  style={prompt['style']}  |  category={prompt['category']}")
        print(f"      {prompt['instruction']}")
        print()

    # Summary stats
    categories = {p["category"] for p in all_prompts}
    styles = {p["style"] for p in all_prompts}

    print(f"{'=' * 80}")
    print("SUMMARY")
    print(f"{'=' * 80}")
    print(f"  Total prompts generated : {len(all_prompts)}")
    print(f"  Topics covered          : {len(categories)}")
    print(f"  Styles used             : {len(styles)} — {', '.join(sorted(styles))}")
    print(f"  Sample shown above      : {len(sample)}")


if __name__ == "__main__":
    main()
