"""FD/FI scenario taxonomy for hardware diagnostics fine-tuning dataset.

Defines ~46 fault-detection / fault-isolation / triage scenarios organized
by hardware domain.  Each scenario is a *recipe* — Phase 2 will expand
these into full Q&A training entries.

Categories
----------
FD      Fault Detection — "the data looks wrong, what does it mean?"
FI      Fault Isolation — "we know something is wrong, where / why?"
FD_FI   Combined detection + isolation in one scenario
TRIAGE  Misleading data — the obvious hardware hypothesis is wrong

Domains (8)
-----------
boundary_scan, signal_integrity, in_circuit_test, thermal,
mixed_signal, functional_test, production_test, environmental
"""

import json
import random
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Categories
# ---------------------------------------------------------------------------

CATEGORIES = {
    "FD": {
        "name": "Fault Detection",
        "question_frame": "What does this anomalous data indicate?",
        "model_task": "Identify the anomaly and explain its significance",
        "target_count": 14,
    },
    "FI": {
        "name": "Fault Isolation",
        "question_frame": "Given this failure, what is the root cause?",
        "model_task": "Isolate the root cause from the presented evidence",
        "target_count": 11,
    },
    "FD_FI": {
        "name": "Fault Detection + Isolation",
        "question_frame": "Analyze this data — detect the fault and isolate its cause.",
        "model_task": "Detect the anomaly and trace it to a root cause in one step",
        "target_count": 8,
    },
    "TRIAGE": {
        "name": "Triage (Misleading Data)",
        "question_frame": "This looks like a hardware fault — but is it?",
        "model_task": "Recognize that the obvious hardware hypothesis is wrong and identify the true cause",
        "target_count": 13,
    },
}

# ---------------------------------------------------------------------------
# Domains
# ---------------------------------------------------------------------------

DOMAINS = [
    {"name": "boundary_scan", "display_name": "Boundary Scan / JTAG"},
    {"name": "signal_integrity", "display_name": "Signal Integrity"},
    {"name": "in_circuit_test", "display_name": "In-Circuit Test (ICT)"},
    {"name": "thermal", "display_name": "Thermal Analysis"},
    {"name": "mixed_signal", "display_name": "Mixed-Signal Test"},
    {"name": "functional_test", "display_name": "Functional Test"},
    {"name": "production_test", "display_name": "Production Test"},
    {"name": "environmental", "display_name": "Environmental / Reliability"},
]

# ---------------------------------------------------------------------------
# Scenarios  (46 total: 14 FD + 11 FI + 8 FD_FI + 13 TRIAGE)
# ---------------------------------------------------------------------------

SCENARIOS = [
    # ===================================================================
    # Boundary Scan  (5 scenarios)
    # ===================================================================
    {
        "scenario_id": "FD-BS-001",
        "category": "FD",
        "domain": "boundary_scan",
        "title": "Intermittent IDCODE bit flips",
        "data_type": "IDCODE register reads",
        "data_description": "5 consecutive IDCODE reads from device 3 in a 5-device chain, hex values",
        "nominal_range": "Consistent 0x0BA00477 across all reads",
        "units": "hex",
        "anomaly_signature": "Bit 28 alternates between 0 and 1 across reads",
        "root_cause": "Marginal signal integrity on TDO — insufficient setup time margin",
        "physics_connection": "TDO setup time vs TCK falling edge, shift register jitter accumulation through chain, signal integrity degradation at high clock rates",
    },
    {
        "scenario_id": "FD-BS-002",
        "category": "FD",
        "domain": "boundary_scan",
        "title": "Chain length mismatch",
        "data_type": "Boundary register length",
        "data_description": "Expected vs observed boundary register length in bits for a 5-device chain",
        "nominal_range": "Expected total: 1,247 bits (sum of BSDL-defined register lengths)",
        "units": "bits",
        "anomaly_signature": "Observed 1,253 bits — 6 extra bits in chain",
        "root_cause": "Stuck-at fault on TDI/TDO path causing extra shift register stages",
        "physics_connection": "Stuck-at on TDI/TDO affecting shift register propagation, boundary register length defined by physical scan cells in silicon",
    },
    {
        "scenario_id": "FI-BS-001",
        "category": "FI",
        "domain": "boundary_scan",
        "title": "Device N and downstream unresponsive",
        "data_type": "IDCODE read results per device position",
        "data_description": "IDCODE read results for 8-device JTAG chain, devices 1-8",
        "nominal_range": "Each device returns its unique 32-bit IDCODE",
        "units": "hex",
        "anomaly_signature": "Devices 4-8 return all-ones (0xFFFFFFFF)",
        "root_cause": "Open solder joint on device 3 TDO pin",
        "physics_connection": "Daisy-chain continuity — TDO of device N feeds TDI of device N+1, BGA rework thermal profile determines solder joint quality, open joint breaks serial data path",
    },
    {
        "scenario_id": "FD_FI-BS-001",
        "category": "FD_FI",
        "domain": "boundary_scan",
        "title": "Interconnect test with intermittent fail on specific nets",
        "data_type": "Interconnect test results table",
        "data_description": "Pass/fail results for 200 nets in boundary scan interconnect test, 10 consecutive runs",
        "nominal_range": "All nets pass consistently across runs",
        "units": "pass/fail per net per run",
        "anomaly_signature": "3 adjacent nets (NET_147, NET_148, NET_149) fail sporadically — 4 of 10 runs",
        "root_cause": "Crosstalk from capacitive coupling at fine-pitch BGA (0.5 mm) between adjacent signal traces",
        "physics_connection": "Mutual capacitance between parallel traces at fine BGA pitch, boundary scan drive strength marginal vs coupling, C_mutual proportional to trace length and inversely proportional to spacing",
    },
    {
        "scenario_id": "TRIAGE-BS-001",
        "category": "TRIAGE",
        "domain": "boundary_scan",
        "title": "JTAG chain fails only on Monday mornings",
        "data_type": "Fail rate log by day of week and time",
        "data_description": "JTAG chain integrity test fail rate (%) logged hourly over 4 weeks",
        "nominal_range": "Baseline fail rate < 0.5%",
        "units": "percent",
        "anomaly_signature": "4x fail rate (2.1%) on Monday mornings 6:00-9:00 AM, normal the rest of the week",
        "root_cause": "Weekend HVAC shutdown causes thermal shock at Monday power-on — boards cold-soak to 15C overnight",
        "physics_connection": "Rules out hardware defect because fail rate is time-correlated not unit-correlated; thermal contraction at low temperature temporarily increases contact resistance at BGA joints",
        "triage_actual_cause": "Weekend HVAC shutdown causes thermal shock at power-on; environmental, not hardware",
    },

    # ===================================================================
    # Signal Integrity  (5 scenarios)
    # ===================================================================
    {
        "scenario_id": "FD-SI-001",
        "category": "FD",
        "domain": "signal_integrity",
        "title": "TDR impedance anomaly",
        "data_type": "TDR impedance sweep",
        "data_description": "Time-domain reflectometry impedance values sampled at 1 mm intervals along a 100 mm trace",
        "nominal_range": "50 ohm +/- 5 ohm across entire trace length",
        "units": "ohm vs distance (mm)",
        "anomaly_signature": "Impedance dips from 50 to 38 ohm at 47 mm, recovers to 50 ohm by 52 mm",
        "root_cause": "Geometry change at layer transition via — increased capacitance from via pad and antipad",
        "physics_connection": "Z0 = sqrt(L/C); via pad adds parallel capacitance, reducing Z0 locally; TDR resolves spatial location from round-trip time",
    },
    {
        "scenario_id": "FD-SI-002",
        "category": "FD",
        "domain": "signal_integrity",
        "title": "Eye diagram violations",
        "data_type": "Eye diagram measurements",
        "data_description": "Eye width (ps), eye height (mV), and jitter components (RJ, DJ) at 10 Gbps receiver",
        "nominal_range": "Eye height > 120 mV, eye width > 45 ps, total jitter < 35 ps at BER 1e-12",
        "units": "mV, ps",
        "anomaly_signature": "Eye height reduced 40% to 72 mV; DJ dominates at 28 ps",
        "root_cause": "Inter-symbol interference (ISI) from impedance discontinuities at connector via field",
        "physics_connection": "ISI from impedance discontinuities creates reflections that close the eye, Nyquist bandwidth limitation causes frequency-dependent loss, DJ is deterministic and traceable to layout geometry",
    },
    {
        "scenario_id": "FI-SI-001",
        "category": "FI",
        "domain": "signal_integrity",
        "title": "Crosstalk source identification",
        "data_type": "S-parameter measurements (NEXT/FEXT)",
        "data_description": "Near-end (NEXT) and far-end (FEXT) crosstalk S-parameters across 100 MHz to 10 GHz for 4 aggressor-victim pairs",
        "nominal_range": "NEXT < -40 dB, FEXT < -50 dB across frequency range",
        "units": "dB vs frequency (GHz)",
        "anomaly_signature": "NEXT peaks to -22 dB at 2.4 GHz on pair 3 only",
        "root_cause": "Trace coupling at connector via field — parallel run length creates resonant coupling path",
        "physics_connection": "Mutual inductance between parallel traces, quarter-wave resonance at f = c/(4*L_coupled*sqrt(epsilon_eff)) creates narrowband coupling peak, NEXT is dominated by inductive coupling at high frequency",
    },
    {
        "scenario_id": "FI-SI-002",
        "category": "FI",
        "domain": "signal_integrity",
        "title": "PDN resonance causing bit errors",
        "data_type": "PDN impedance sweep Z(f)",
        "data_description": "Power distribution network impedance magnitude measured from 1 MHz to 1 GHz at IC pad",
        "nominal_range": "Z_PDN < 0.5 ohm from DC to 500 MHz (target impedance)",
        "units": "ohm vs frequency (MHz)",
        "anomaly_signature": "Anti-resonance peak: impedance spikes to 2.0 ohm at 150 MHz",
        "root_cause": "Missing decoupling capacitors — insufficient capacitor count in 100-200 MHz range",
        "physics_connection": "Parallel LC resonance of PCB plane capacitance + via inductance; anti-resonance occurs at frequency where inductive impedance of one cap network equals capacitive impedance of another, creating high-Z node",
    },
    {
        "scenario_id": "FD_FI-SI-001",
        "category": "FD_FI",
        "domain": "signal_integrity",
        "title": "S-parameter data with unexpected insertion loss",
        "data_type": "S21 magnitude vs frequency",
        "data_description": "Insertion loss (S21) measured from 100 MHz to 20 GHz on a 6-inch differential pair",
        "nominal_range": "Monotonically increasing loss, -8 dB at 10 GHz per channel model",
        "units": "dB vs frequency (GHz)",
        "anomaly_signature": "3 dB excess loss above 4 GHz with sharp notch at 8.5 GHz",
        "root_cause": "Via stub resonance — back-drilled vias have 30 mil residual stub",
        "physics_connection": "Quarter-wave stub creates notch filter at f = c/(4*L_stub*sqrt(epsilon_r)); 30 mil stub in FR4 (epsilon_r=3.8) resonates near 8.5 GHz, energy couples into stub and is reflected",
    },

    # ===================================================================
    # In-Circuit Test  (5 scenarios)
    # ===================================================================
    {
        "scenario_id": "FD-ICT-001",
        "category": "FD",
        "domain": "in_circuit_test",
        "title": "Icc distribution shift",
        "data_type": "Icc histogram data",
        "data_description": "Quiescent supply current (Icc) readings for a specific IC across 500 boards",
        "nominal_range": "Mean 45 mA, sigma 3.2 mA (established from first 2,000 boards)",
        "units": "mA",
        "anomaly_signature": "Mean shifted to 68 mA (+23 mA) with sigma unchanged at 3.1 mA",
        "root_cause": "Systematic offset — likely design revision or component lot change causing higher quiescent current",
        "physics_connection": "Systematic shift (constant offset, stable sigma) indicates deterministic cause vs random variation; P = Icc * Vdd gives power dissipation impact; stable sigma rules out increased defect rate",
    },
    {
        "scenario_id": "FD-ICT-002",
        "category": "FD",
        "domain": "in_circuit_test",
        "title": "Capacitor ESR measurement drift",
        "data_type": "ESR readings for 100 nF capacitors",
        "data_description": "Equivalent series resistance measurements for C47 (100 nF MLCC) across 200 boards",
        "nominal_range": "Unimodal distribution, mean 0.8 ohm, sigma 0.15 ohm",
        "units": "ohm",
        "anomaly_signature": "Bimodal distribution — peaks at 0.7 ohm and 1.4 ohm",
        "root_cause": "Mixed component lots on reel — two suppliers with different dielectric formulations",
        "physics_connection": "Dielectric loss tangent determines ESR: ESR = tan(delta) / (2*pi*f*C); different ceramic formulations (e.g., X7R vs X5R) have different loss tangents, producing distinct ESR populations",
    },
    {
        "scenario_id": "FI-ICT-001",
        "category": "FI",
        "domain": "in_circuit_test",
        "title": "Wrong resistance but correct component",
        "data_type": "Guarded vs unguarded resistance measurements",
        "data_description": "Measured resistance of R23 (47k ohm) using both guarded and unguarded techniques",
        "nominal_range": "47k ohm +/- 5% (44.65k to 49.35k)",
        "units": "ohm",
        "anomaly_signature": "Unguarded reads 22k ohm; guarded reads 46.8k ohm (within spec)",
        "root_cause": "Parallel path through adjacent components — R24 (47k) in parallel via shared power rail creates 23.5k equivalent",
        "physics_connection": "Kirchhoff's current law — unguarded measurement sees parallel resistance paths; 1/R_measured = 1/R23 + 1/R_parallel; guarded technique sinks stray current through guard pin, isolating the DUT",
    },
    {
        "scenario_id": "FI-ICT-002",
        "category": "FI",
        "domain": "in_circuit_test",
        "title": "Opens detection on QFN center pad",
        "data_type": "Capacitive signature test results",
        "data_description": "Capacitive coupling measurement at QFN exposed pad (ground connection)",
        "nominal_range": "1.8 pF (established from known-good boards)",
        "units": "pF",
        "anomaly_signature": "Measured 0.2 pF — 89% below expected coupling capacitance",
        "root_cause": "Insufficient solder paste on center pad — stencil aperture undersize or blocked",
        "physics_connection": "Parallel plate capacitance C = epsilon_0 * epsilon_r * A / d; open joint increases effective gap d dramatically (air gap vs solder), reducing capacitance proportionally; residual 0.2 pF is fringe capacitance",
    },
    {
        "scenario_id": "FD_FI-ICT-001",
        "category": "FD_FI",
        "domain": "in_circuit_test",
        "title": "Flying probe results with position-dependent errors",
        "data_type": "Resistance measurements vs XY position",
        "data_description": "4-wire resistance readings for 50 test points distributed across board, with XY coordinates",
        "nominal_range": "Each reading within +/- 2% of nominal component value",
        "units": "ohm, mm (XY)",
        "anomaly_signature": "Upper-left quadrant (X < 100, Y > 150) reads 5-10% high systematically; other quadrants within spec",
        "root_cause": "Fixture probe planarity issue — upper-left probes have reduced contact force due to vacuum plate warpage",
        "physics_connection": "Contact resistance R_contact increases with reduced probe force: R_c = rho / (pi * a) where a is contact radius; insufficient force reduces effective contact area, adding series resistance to all measurements in affected zone",
    },

    # ===================================================================
    # Thermal  (4 scenarios)
    # ===================================================================
    {
        "scenario_id": "FD-TH-001",
        "category": "FD",
        "domain": "thermal",
        "title": "Temperature distribution anomaly",
        "data_type": "IR camera thermal grid",
        "data_description": "Infrared camera temperature readings on a 10x10 grid (5 mm spacing) over a voltage regulator area",
        "nominal_range": "Uniform 45-55C across regulator area under typical load",
        "units": "degrees C",
        "anomaly_signature": "15C hot spot (70C) centered on regulator output stage, steep gradient to surrounding 55C",
        "root_cause": "Excessive power dissipation in regulator — dropout voltage higher than expected under load",
        "physics_connection": "P = I^2 * R_ds(on) for MOSFET pass element; thermal resistance theta_JA determines junction temperature: T_j = T_a + P * theta_JA; localized hot spot indicates concentrated power dissipation",
    },
    {
        "scenario_id": "FI-TH-001",
        "category": "FI",
        "domain": "thermal",
        "title": "Thermal runaway identification",
        "data_type": "Temperature vs time profile",
        "data_description": "Thermocouple reading on a power MOSFET over 120-second powered test, sampled at 1 Hz",
        "nominal_range": "Stabilizes at 75C within 30 seconds, steady-state thereafter",
        "units": "degrees C vs seconds",
        "anomaly_signature": "Temperature reaches 85C at 30s but continues accelerating — 95C at 60s, 112C at 90s, rising exponentially",
        "root_cause": "Parasitic BJT latch-up in MOSFET — substrate current triggers NPN action",
        "physics_connection": "Positive thermal feedback: leakage current increases exponentially with temperature per Arrhenius (I_leak proportional to exp(-Ea/kT)); increased leakage raises power, which raises temperature, creating runaway loop",
    },
    {
        "scenario_id": "FD_FI-TH-001",
        "category": "FD_FI",
        "domain": "thermal",
        "title": "Board thermal profile with unexpected gradient",
        "data_type": "Thermocouple readings at multiple locations",
        "data_description": "6 thermocouple readings across a board zone designed for uniform airflow, under steady-state operation",
        "nominal_range": "All thermocouples within 3C of each other (uniform convective cooling)",
        "units": "degrees C",
        "anomaly_signature": "TC1-TC3: 52-54C; TC4-TC6: 64-66C — 12C gradient across what should be a uniform zone",
        "root_cause": "Blocked airflow from misaligned heatsink clip — clip shifted 3 mm, creating shadow zone",
        "physics_connection": "Convective heat transfer Q = h * A * deltaT; blocked airflow reduces local h (convective coefficient), causing temperature to rise until conduction paths compensate; gradient direction indicates airflow obstruction location",
    },
    {
        "scenario_id": "TRIAGE-TH-001",
        "category": "TRIAGE",
        "domain": "thermal",
        "title": "Thermal camera shows hot spot correlating with test failure",
        "data_type": "IR image + test fail correlation",
        "data_description": "IR thermal image of board during functional test, with component overlay and fail log",
        "nominal_range": "All components within rated operating temperature",
        "units": "degrees C",
        "anomaly_signature": "FPGA at 92C, correlates with functional test failure in FPGA-driven memory interface",
        "root_cause": "FPGA runs hot by design — rated to 125C junction; test failure is software timing issue in memory controller firmware",
        "physics_connection": "Junction temperature 92C is within absolute max rating (125C) with margin; T_j = T_case + P * theta_JC; hot spot is normal operation, not the failure cause",
        "triage_actual_cause": "FPGA temperature is within spec (rated 125C); test failure is a software timing bug in memory controller firmware, not thermal",
    },

    # ===================================================================
    # Mixed-Signal  (5 scenarios)
    # ===================================================================
    {
        "scenario_id": "FD-MS-001",
        "category": "FD",
        "domain": "mixed_signal",
        "title": "ADC linearity error",
        "data_type": "INL/DNL measurements",
        "data_description": "Integral nonlinearity (INL) and differential nonlinearity (DNL) across all 4,096 codes of a 12-bit SAR ADC",
        "nominal_range": "INL < +/- 1 LSB, DNL < +/- 0.5 LSB",
        "units": "LSB",
        "anomaly_signature": "INL exceeds +/- 2 LSB at mid-scale (codes 1,800-2,200), DNL shows spikes at major carry transitions",
        "root_cause": "Capacitor mismatch in SAR DAC — MSB capacitor 0.3% off nominal",
        "physics_connection": "SAR ADC binary-weighted capacitor array: each capacitor must match to within 0.5 LSB at its bit weight; 0.3% mismatch on MSB (C = 2048 * C_unit) creates 6 LSB INL error at mid-scale transition",
    },
    {
        "scenario_id": "FD-MS-002",
        "category": "FD",
        "domain": "mixed_signal",
        "title": "Clock jitter measurement",
        "data_type": "Period jitter histogram",
        "data_description": "10,000 consecutive period measurements of a 100 MHz reference clock",
        "nominal_range": "Gaussian distribution, mean 10.000 ns, sigma < 5 ps RMS",
        "units": "ns",
        "anomaly_signature": "Bimodal distribution with peaks at 9.993 ns and 10.008 ns (15 ps separation)",
        "root_cause": "Deterministic jitter from power supply coupling into PLL — switching regulator at 1.2 MHz modulates VCO",
        "physics_connection": "Deterministic jitter from supply coupling: VCO gain K_vco converts supply noise to frequency modulation; PLL bandwidth determines rejection — noise above loop bandwidth passes directly to output; bimodal pattern indicates periodic modulation",
    },
    {
        "scenario_id": "FI-MS-001",
        "category": "FI",
        "domain": "mixed_signal",
        "title": "DAC output noise floor elevated",
        "data_type": "FFT of DAC output",
        "data_description": "4,096-point FFT of 16-bit DAC output at mid-scale, 1 MHz bandwidth",
        "nominal_range": "Noise floor at -110 dBFS, no spurs above -90 dBFS",
        "units": "dBFS vs frequency (MHz)",
        "anomaly_signature": "Noise floor at -100 dBFS (10 dB above spec), discrete spur at 1.2 MHz at -72 dBFS",
        "root_cause": "Inadequate decoupling on AVDD — 1.2 MHz spur matches switching regulator frequency",
        "physics_connection": "DAC PSRR rolls off above decoupling network bandwidth; switching regulator ripple couples through supply pin; spur amplitude = ripple_amplitude - PSRR(f); insufficient decoupling raises high-frequency ripple above PSRR rejection capability",
    },
    {
        "scenario_id": "FI-MS-002",
        "category": "FI",
        "domain": "mixed_signal",
        "title": "PLL fails to lock",
        "data_type": "PLL control voltage and VCO frequency waveforms",
        "data_description": "Control voltage (0-3.3V) and VCO output frequency sampled over 500 us during lock acquisition",
        "nominal_range": "Control voltage settles to ~1.65V within 100 us, VCO locks to 2.4 GHz",
        "units": "V, GHz vs microseconds",
        "anomaly_signature": "Control voltage oscillates between 0.8V and 2.5V with 50 us period, never settles; VCO swings between 2.1 and 2.7 GHz",
        "root_cause": "Wrong capacitor in loop filter — 100 pF installed instead of 10 nF (BOM error)",
        "physics_connection": "PLL stability requires > 45 degrees phase margin; loop filter C sets the pole that determines phase margin; 100x reduction in C moves pole frequency 100x higher, reducing phase margin below 0 degrees — loop is unstable",
    },
    {
        "scenario_id": "FD_FI-MS-001",
        "category": "FD_FI",
        "domain": "mixed_signal",
        "title": "ADC missing codes",
        "data_type": "Code density histogram",
        "data_description": "Code occurrence counts from 12-bit ADC ramp test (1M samples, full-scale linear ramp input)",
        "nominal_range": "Each code appears approximately 244 times (1M / 4096), uniform distribution",
        "units": "count per code",
        "anomaly_signature": "Codes 2047-2049 never appear (0 counts); adjacent codes 2046 and 2050 have 2x expected counts",
        "root_cause": "Stuck bit 11 — comparator offset in flash sub-ADC exceeds threshold",
        "physics_connection": "Bit 11 is the MSB transition at mid-scale; comparator offset voltage exceeds metastability window, causing bit to lock to one state; missing codes at 2^11 boundary are diagnostic of MSB comparator failure",
    },

    # ===================================================================
    # Functional Test  (4 scenarios)
    # ===================================================================
    {
        "scenario_id": "FD-FT-001",
        "category": "FD",
        "domain": "functional_test",
        "title": "Voltage margining failure at low margin",
        "data_type": "Pass/fail vs supply voltage sweep",
        "data_description": "Functional test pass/fail results at 50 mV steps from 4.5V to 5.5V (nominal 5.0V)",
        "nominal_range": "Pass across full +/- 10% range (4.50V to 5.50V)",
        "units": "pass/fail vs volts",
        "anomaly_signature": "Fails below 4.75V (5% margin instead of 10%); passes at 4.80V and above",
        "root_cause": "Timing margin erosion — critical path delay increases at low voltage",
        "physics_connection": "CMOS gate delay is proportional to V / (V - Vth)^2; reducing supply voltage increases delay non-linearly; at 4.75V the critical path delay exceeds clock period, causing setup time violation",
    },
    {
        "scenario_id": "FI-FT-001",
        "category": "FI",
        "domain": "functional_test",
        "title": "Intermittent functional test failure",
        "data_type": "Pass/fail log with timestamps and test step IDs",
        "data_description": "1,000 consecutive functional test runs with per-step pass/fail and timestamps",
        "nominal_range": "All steps pass on all runs (< 0.1% fail rate per step)",
        "units": "pass/fail per step per run",
        "anomaly_signature": "Step 47 (memory write/read) fails 2% of runs (20 of 1,000); all other steps pass 100%",
        "root_cause": "Address bus signal integrity marginal on bit 14 — crosstalk from adjacent clock trace",
        "physics_connection": "Setup time violation probability is a function of jitter: P_fail = erfc(margin / (sigma_jitter * sqrt(2))); 2% fail rate implies margin is approximately 2 sigma; jitter source is crosstalk-induced, deterministic",
    },
    {
        "scenario_id": "FD_FI-FT-001",
        "category": "FD_FI",
        "domain": "functional_test",
        "title": "POST results with unexpected error codes",
        "data_type": "POST code sequence and error register",
        "data_description": "Power-on self-test diagnostic codes and ECC error register contents from memory subsystem test",
        "nominal_range": "POST completes with code 0x00 (no errors), ECC register shows zero corrections",
        "units": "hex error codes, bit field",
        "anomaly_signature": "POST code 0x42 (memory error), ECC register shows single-bit errors in bank 2 only — 14 correctable errors in 256 MB test",
        "root_cause": "Weak DRAM cell with marginal retention time — specific row in bank 2 loses charge before refresh",
        "physics_connection": "DRAM charge storage Q = C_cell * V; weak cell has reduced C_cell or elevated leakage, causing retention time shorter than refresh interval; single-bit errors (not multi-bit) indicate isolated cell weakness, not row/column failure",
    },
    {
        "scenario_id": "TRIAGE-FT-001",
        "category": "TRIAGE",
        "domain": "functional_test",
        "title": "Board fails after firmware update",
        "data_type": "Pass/fail history before and after firmware v2.1",
        "data_description": "Functional test results for 500 boards: 250 tested on firmware v2.0, 250 on v2.1",
        "nominal_range": "> 99% pass rate on functional test",
        "units": "pass/fail with firmware version tag",
        "anomaly_signature": "100% pass rate on v2.0; 100% fail rate on v2.1 — sharp transition at firmware changeover point",
        "root_cause": "Firmware bug — PLL initialization registers written in wrong order in v2.1",
        "physics_connection": "Rules out hardware because fail onset is perfectly correlated with software change, not with board lot, component date code, or any physical parameter; 100% fail rate is inconsistent with hardware defect distribution",
        "triage_actual_cause": "Firmware bug in v2.1 — PLL registers initialized in wrong order, causing clock failure; not a hardware defect",
    },

    # ===================================================================
    # Production Test  (5 scenarios)
    # ===================================================================
    {
        "scenario_id": "FD-PT-001",
        "category": "FD",
        "domain": "production_test",
        "title": "Cpk degradation trend",
        "data_type": "Weekly Cpk values",
        "data_description": "Process capability index (Cpk) for a critical voltage measurement tracked weekly over 20 weeks",
        "nominal_range": "Cpk > 1.33 (4-sigma process capability)",
        "units": "dimensionless (Cpk)",
        "anomaly_signature": "Cpk dropped from 1.80 (week 1) to 1.10 (week 20) — steady decline, sigma stable",
        "root_cause": "Process centering shift — mean drifting toward upper spec limit while spread remains constant",
        "physics_connection": "Cpk = min((USL - mean), (mean - LSL)) / (3 * sigma); stable sigma with declining Cpk indicates systematic mean drift; constant sigma rules out increased variation, pointing to a deterministic shift source",
    },
    {
        "scenario_id": "FD-PT-002",
        "category": "FD",
        "domain": "production_test",
        "title": "SPC chart out-of-control pattern",
        "data_type": "X-bar control chart data",
        "data_description": "X-bar (subgroup mean) values for 30 consecutive subgroups (n=5 each) of an impedance measurement",
        "nominal_range": "Random variation within +/- 3 sigma control limits",
        "units": "ohm (subgroup means)",
        "anomaly_signature": "8 consecutive points above the center line (subgroups 12-19) — Western Electric Rule 2 violation",
        "root_cause": "Assignable cause — process shift occurred at subgroup 12, likely tooling or material change",
        "physics_connection": "Probability of 8 sequential same-side points in a stable process is (0.5)^8 = 0.004; this P < 0.005 threshold triggers Western Electric Rule 2, indicating the process is not in statistical control — a non-random force is acting on the mean",
    },
    {
        "scenario_id": "FI-PT-001",
        "category": "FI",
        "domain": "production_test",
        "title": "Yield drop correlates with component date code",
        "data_type": "Yield percentage by week with lot traceability",
        "data_description": "Weekly first-pass yield (%) with component lot/date-code traceability over 12 weeks",
        "nominal_range": "FPY > 98% sustained",
        "units": "percent yield",
        "anomaly_signature": "FPY drops from 98.5% to 83.2% in week 38, recovers to 97.8% in week 40 when lot changes",
        "root_cause": "Supplier process change — component lot 2024-W38 has shifted parameter distribution outside design guard-band",
        "physics_connection": "Component parameter shift outside design guard-band: if component tolerance overlaps with design margin, yield loss occurs at the tail of the parameter distribution; lot-correlated yield is diagnostic of supplier variation",
    },
    {
        "scenario_id": "FI-PT-002",
        "category": "FI",
        "domain": "production_test",
        "title": "Golden board calibration drift",
        "data_type": "Golden board reference measurements over time",
        "data_description": "Daily reference resistance measurement on golden board standard (100.00 ohm) over 30 days",
        "nominal_range": "100.00 ohm +/- 0.05% (99.95 to 100.05 ohm)",
        "units": "ohm",
        "anomaly_signature": "Measurement drifting upward: 100.00 on day 1, 100.03 on day 10, 100.07 on day 20, 100.10 on day 30 — +0.1%/week linear trend",
        "root_cause": "Fixture probe wear — contact area decreasing over time due to mechanical wear",
        "physics_connection": "Contact resistance R_contact = rho / (pi * a) where a is contact spot radius; probe tip wear reduces effective contact area a, increasing R_contact and adding systematic positive offset to all resistance measurements",
    },
    {
        "scenario_id": "TRIAGE-PT-001",
        "category": "TRIAGE",
        "domain": "production_test",
        "title": "Sudden 100% test failure",
        "data_type": "Test log with abrupt pass-to-fail transition",
        "data_description": "Production test results for 200 consecutive boards: pass/fail status, board serial number, lot code, and timestamp",
        "nominal_range": "> 99% pass rate",
        "units": "pass/fail",
        "anomaly_signature": "Boards 1-147 pass normally; boards 148-200 all fail across multiple different lot codes and board revisions",
        "root_cause": "Test system calibration data corrupted after system crash — reference values invalidated",
        "physics_connection": "Rules out DUT hardware: failures span multiple independent lots and revisions; abrupt onset at a specific serial number (not lot boundary) indicates test-system event; 100% fail rate is inconsistent with stochastic hardware defect",
        "triage_actual_cause": "Calibration data corrupted after test system crash; failure is test-system-correlated, not DUT-correlated",
    },

    # ===================================================================
    # Environmental / Reliability  (5 scenarios)
    # ===================================================================
    {
        "scenario_id": "FD-ENV-001",
        "category": "FD",
        "domain": "environmental",
        "title": "Weibull parameter shift",
        "data_type": "Weibull distribution parameters",
        "data_description": "Weibull beta (shape) and eta (scale/characteristic life) from two HALT batches, 20 units each",
        "nominal_range": "beta = 3.2 (wear-out mode), eta = 5,000 hours",
        "units": "dimensionless (beta), hours (eta)",
        "anomaly_signature": "Batch 2: beta dropped from 3.2 to 1.8, eta increased from 5,000 to 7,200 hours",
        "root_cause": "Failure mechanism shifted — new batch has mixed failure modes (wear-out + random) reducing beta toward 1",
        "physics_connection": "Weibull beta > 1 indicates wear-out (increasing hazard rate); beta = 1 is random (constant hazard); drop from 3.2 to 1.8 indicates shift from pure wear-out to mixed failure mechanism population; Arrhenius acceleration factor changes with mechanism",
    },
    {
        "scenario_id": "FD-ENV-002",
        "category": "FD",
        "domain": "environmental",
        "title": "HALT step-stress unexpected failure mode",
        "data_type": "Temperature step-stress results",
        "data_description": "Number of unit failures at each HALT temperature step (+25C to +125C in 10C steps), 20 units per batch",
        "nominal_range": "No failures below +105C operational limit; 1-2 failures at +115C destruct step",
        "units": "count of failures per temperature step",
        "anomaly_signature": "3 failures at +85C step (well below operational limit) — unexpected early failure cluster",
        "root_cause": "Lower-than-expected activation energy — failure mechanism activates at lower temperature than design assumed",
        "physics_connection": "Arrhenius acceleration: AF = exp((Ea/k) * (1/T_use - 1/T_stress)); lower Ea means less acceleration needed to trigger failure, so failures appear at lower stress levels; 3 failures at +85C suggests Ea approximately 0.4 eV vs assumed 0.7 eV",
    },
    {
        "scenario_id": "FI-ENV-001",
        "category": "FI",
        "domain": "environmental",
        "title": "Solder joint fatigue from thermal cycling",
        "data_type": "Cross-section images and cycle count data",
        "data_description": "Cross-section crack length measurements for BGA solder balls after 500, 1000, and 1500 thermal cycles (-40C to +125C)",
        "nominal_range": "No cracks at 500 cycles, < 10% crack length at 1000 cycles for center balls",
        "units": "percent crack length, cycle count",
        "anomaly_signature": "Corner balls show 50% crack length at 500 cycles, 90% at 1000 cycles; center balls show < 5% at 1000 cycles",
        "root_cause": "CTE mismatch strain maximized at maximum distance from neutral point (DNP) — corner balls experience highest shear strain",
        "physics_connection": "Shear strain gamma = alpha_CTE * deltaT * DNP / h_standoff; corner balls have maximum DNP, so they experience maximum cyclic shear strain; fatigue life follows Coffin-Manson: N_f = C * (delta_gamma)^(-n)",
    },
    {
        "scenario_id": "FI-ENV-002",
        "category": "FI",
        "domain": "environmental",
        "title": "Vibration test failure isolation",
        "data_type": "Frequency response and failure location",
        "data_description": "PCB frequency response (accelerometer) from 20 Hz to 2 kHz random vibration, plus failure location from dye-and-pry analysis",
        "nominal_range": "Transmissibility < 3x across frequency range, no component failures in 4-hour test",
        "units": "g/g (transmissibility) vs frequency (Hz)",
        "anomaly_signature": "Transmissibility peak of 12x at 850 Hz; ceramic capacitor C12 fails (cracked) at that board location",
        "root_cause": "PCB natural frequency matches excitation — resonance amplifies displacement at capacitor location",
        "physics_connection": "Resonant frequency f_n = (1/(2*pi)) * sqrt(k/m) for board panel; at resonance, Q-factor amplifies input vibration; MLCC ceramic is brittle and fails when board flexure exceeds fracture strain of ceramic dielectric",
    },
    {
        "scenario_id": "TRIAGE-ENV-001",
        "category": "TRIAGE",
        "domain": "environmental",
        "title": "Burn-in failures cluster on oven shelf position",
        "data_type": "Failure map by oven position",
        "data_description": "Burn-in test results for 200 boards across 5 oven shelves (40 boards per shelf), 168-hour burn-in at +85C",
        "nominal_range": "< 2% failure rate, randomly distributed across shelves",
        "units": "pass/fail by shelf position",
        "anomaly_signature": "Shelf 3 has 12 failures (30% fail rate); shelves 1,2,4,5 have 0-1 failures each (0-2.5%)",
        "root_cause": "Thermocouple on shelf 3 miscalibrated +15C — actual temperature was 100C, exceeding component ratings",
        "physics_connection": "Rules out DUT hardware because failures are position-correlated (shelf 3 only) not unit-correlated (not lot, revision, or serial number dependent); temperature delta follows Arrhenius — 15C overshoot at 85C gives approximately 4x acceleration",
        "triage_actual_cause": "Thermocouple miscalibrated +15C on shelf 3; boards were stressed at 100C instead of 85C; oven calibration issue, not DUT defect",
    },

    # ===================================================================
    # Cross-Domain TRIAGE  (3 scenarios)
    # ===================================================================
    {
        "scenario_id": "TRIAGE-XDOM-001",
        "category": "TRIAGE",
        "domain": "in_circuit_test",
        "title": "ICT measurement drift mimics component tolerance shift",
        "data_type": "Resistance measurement trend",
        "data_description": "R15 (10k ohm) measurement trend over 2,000 boards across 3 weeks, with fixture maintenance log",
        "nominal_range": "10.0k ohm +/- 2% (9.80k to 10.20k)",
        "units": "ohm",
        "anomaly_signature": "Measurements trending upward: week 1 mean 10.02k, week 2 mean 10.08k, week 3 mean 10.15k — approaching upper limit",
        "root_cause": "Probe tip oxidation increasing contact resistance — measurement artifact, not component drift",
        "physics_connection": "Oxide layer on probe tip acts as series resistance; R_measured = R_component + R_contact_oxide; gradual oxide buildup adds monotonically increasing offset; component population is stable (confirmed by sampling with new probes)",
        "triage_actual_cause": "Probe tip oxidation adding series contact resistance; measurement artifact, not actual component tolerance shift",
    },
    {
        "scenario_id": "TRIAGE-XDOM-002",
        "category": "TRIAGE",
        "domain": "signal_integrity",
        "title": "SI test fails intermittently on all boards",
        "data_type": "TDR impedance traces",
        "data_description": "TDR impedance profiles for 50 boards, same net — measured on production SI test fixture",
        "nominal_range": "50 ohm +/- 10% along entire trace length",
        "units": "ohm vs time (ns)",
        "anomaly_signature": "Random impedance spikes (up to 75 ohm) appearing at inconsistent locations across different boards — location varies between measurements even on the same board",
        "root_cause": "Loose coaxial cable connector on test fixture — intermittent contact creates random reflections",
        "physics_connection": "Discontinuity location varies randomly between measurements (not fixed to a board feature), ruling out PCB defect; random variation indicates measurement path instability, not DUT characteristic; a true PCB impedance anomaly would appear at the same electrical distance on every measurement",
        "triage_actual_cause": "Loose coax cable on SI test fixture; intermittent contact creates random impedance artifacts not related to the DUT",
    },
    {
        "scenario_id": "TRIAGE-XDOM-003",
        "category": "TRIAGE",
        "domain": "mixed_signal",
        "title": "Mixed-signal ADC noise looks like degraded SNR",
        "data_type": "ADC output FFT",
        "data_description": "4,096-point FFT of 12-bit ADC sampling a precision DC reference, captured on test fixture",
        "nominal_range": "SNR > 70 dB, no spurs above -80 dBFS",
        "units": "dBFS vs frequency (kHz)",
        "anomaly_signature": "Elevated noise floor at -85 dBFS (vs expected -95 dBFS), with discrete spurs at 60 Hz, 120 Hz, 180 Hz, and 240 Hz at -65 to -72 dBFS",
        "root_cause": "Ground loop between test fixture and DUT — AC mains coupling through ground impedance",
        "physics_connection": "Spurs at exact power-line harmonics (60/120/180/240 Hz) are diagnostic of AC mains coupling, not broadband ADC noise; true SNR degradation would raise the broadband noise floor uniformly, not create discrete tones; ground loop I_loop * Z_ground creates voltage offset at ADC input",
        "triage_actual_cause": "Ground loop injecting 60 Hz harmonics from AC mains; fixture grounding issue, not ADC degradation",
    },
]


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def get_scenarios() -> list[dict]:
    """Return all scenarios."""
    return SCENARIOS


def get_scenarios_by_category(category: str) -> list[dict]:
    """Return scenarios filtered by category (FD, FI, FD_FI, TRIAGE)."""
    return [s for s in SCENARIOS if s["category"] == category]


def get_scenarios_by_domain(domain: str) -> list[dict]:
    """Return scenarios filtered by domain name."""
    return [s for s in SCENARIOS if s["domain"] == domain]


# ---------------------------------------------------------------------------
# Summary / display
# ---------------------------------------------------------------------------

def print_summary() -> None:
    """Print a cross-tabulation grid: rows = domains, columns = categories."""
    cat_keys = ["FD", "FI", "FD_FI", "TRIAGE"]
    domain_names = [d["name"] for d in DOMAINS]

    # Build count matrix
    counts: dict[str, dict[str, int]] = {d: {c: 0 for c in cat_keys} for d in domain_names}
    for s in SCENARIOS:
        d = s["domain"]
        c = s["category"]
        if d in counts and c in counts[d]:
            counts[d][c] += 1

    # Column widths
    domain_col = 28
    cat_col = 8
    total_col = 8
    line_len = domain_col + len(cat_keys) * cat_col + total_col

    print(f"\n{'=' * line_len}")
    print("FD/FI SCENARIO TAXONOMY — CROSS-TABULATION")
    print(f"{'=' * line_len}")

    # Header
    header = f"{'Domain':<{domain_col}}"
    for c in cat_keys:
        header += f"{c:>{cat_col}}"
    header += f"{'Total':>{total_col}}"
    print(header)
    print("-" * line_len)

    # Rows
    col_totals = {c: 0 for c in cat_keys}
    grand_total = 0
    for d in domain_names:
        display = next(dm["display_name"] for dm in DOMAINS if dm["name"] == d)
        row = f"{display:<{domain_col}}"
        row_total = 0
        for c in cat_keys:
            n = counts[d][c]
            row += f"{n:>{cat_col}}"
            col_totals[c] += n
            row_total += n
        row += f"{row_total:>{total_col}}"
        grand_total += row_total
        print(row)

    # Totals row
    print("-" * line_len)
    totals_row = f"{'TOTAL':<{domain_col}}"
    for c in cat_keys:
        totals_row += f"{col_totals[c]:>{cat_col}}"
    totals_row += f"{grand_total:>{total_col}}"
    print(totals_row)
    print(f"{'=' * line_len}")

    # Category summaries
    print(f"\nCategory breakdown:")
    for c in cat_keys:
        cat_meta = CATEGORIES[c]
        print(f"  {c:8s} ({cat_meta['name']:32s}): {col_totals[c]:3d}  (target: {cat_meta['target_count']})")

    print(f"\n  Grand total: {grand_total} scenarios")


def main() -> None:
    """Print summary, sample scenarios, and pass/fail verdict."""
    print_summary()

    # Print 3 sample scenarios (one FD, one FI, one TRIAGE)
    samples = [
        get_scenarios_by_category("FD")[0],
        get_scenarios_by_category("FI")[2],
        get_scenarios_by_category("TRIAGE")[-1],
    ]

    print(f"\n{'=' * 76}")
    print("SAMPLE SCENARIOS (3 of {})".format(len(SCENARIOS)))
    print(f"{'=' * 76}")

    for i, s in enumerate(samples, 1):
        print(f"\n--- [{i}] {s['scenario_id']}: {s['title']} ---")
        print(f"  Category:          {s['category']}")
        print(f"  Domain:            {s['domain']}")
        print(f"  Data type:         {s['data_type']}")
        print(f"  Data description:  {s['data_description'][:90]}...")
        print(f"  Nominal range:     {s['nominal_range'][:80]}")
        print(f"  Anomaly:           {s['anomaly_signature'][:80]}")
        print(f"  Root cause:        {s['root_cause'][:80]}")
        print(f"  Physics:           {s['physics_connection'][:80]}...")
        if "triage_actual_cause" in s:
            print(f"  Triage actual:     {s['triage_actual_cause'][:80]}")

    # Validation
    total = len(SCENARIOS)
    categories_found = set(s["category"] for s in SCENARIOS)
    domains_found = set(s["domain"] for s in SCENARIOS)
    threshold = 30

    # Check TRIAGE scenarios have triage_actual_cause
    triage_missing = [
        s["scenario_id"] for s in SCENARIOS
        if s["category"] == "TRIAGE" and "triage_actual_cause" not in s
    ]

    # Check all required keys present
    required_keys = {
        "scenario_id", "category", "domain", "title", "data_type",
        "data_description", "nominal_range", "units", "anomaly_signature",
        "root_cause", "physics_connection",
    }
    missing_keys = []
    for s in SCENARIOS:
        missing = required_keys - set(s.keys())
        if missing:
            missing_keys.append((s["scenario_id"], missing))

    print(f"\n{'=' * 76}")
    print("VALIDATION")
    print(f"{'=' * 76}")
    print(f"  Total scenarios:       {total}")
    print(f"  Threshold (min 30):    {'PASS' if total >= threshold else 'FAIL'} ({total} >= {threshold})")
    print(f"  Categories found:      {sorted(categories_found)} ({'PASS' if len(categories_found) == 4 else 'FAIL'})")
    print(f"  Domains found:         {len(domains_found)} of {len(DOMAINS)} ({'PASS' if len(domains_found) >= 4 else 'FAIL'})")
    print(f"  TRIAGE actual_cause:   {'PASS' if not triage_missing else 'FAIL — missing: ' + ', '.join(triage_missing)}")
    print(f"  Required keys:         {'PASS' if not missing_keys else 'FAIL — ' + str(missing_keys)}")

    per_cat = Counter(s["category"] for s in SCENARIOS)
    print(f"\n  Per-category counts:   FD={per_cat['FD']}, FI={per_cat['FI']}, FD_FI={per_cat['FD_FI']}, TRIAGE={per_cat['TRIAGE']}")

    all_pass = (
        total >= threshold
        and len(categories_found) == 4
        and len(domains_found) >= 4
        and not triage_missing
        and not missing_keys
    )
    print(f"\n  OVERALL: {'PASS' if all_pass else 'FAIL'}")


if __name__ == "__main__":
    main()
