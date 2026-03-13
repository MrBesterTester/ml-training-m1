#!/usr/bin/env python3
"""
Revise physics-decorated entries in full_dataset.jsonl.

Replaces entries where physics was forced/decorative with honest-triage
versions that acknowledge when a problem is NOT physics-rooted, which
is itself a valuable diagnostic skill.

Creates a backup before modifying.
"""

import json
import shutil
from pathlib import Path
from datetime import datetime

DATA_FILE = Path(__file__).parent.parent / "data" / "full_dataset.jsonl"
BACKUP_FILE = DATA_FILE.with_suffix(".jsonl.bak")

# Revised outputs keyed by 1-based line number.
# Only the "output" field is replaced; instruction and input stay the same.

REVISIONS = {

    149: (
        "Deadlock in parallel test systems is a software concurrency problem, "
        "not a hardware fault — but it's easy to misdiagnose because the symptom "
        "(system hangs, instruments unresponsive) looks identical to a hardware "
        "lockup. The key diagnostic clue is that the instruments themselves are "
        "fine when accessed individually; the hang only occurs under parallel "
        "operation. That points to resource contention in your software, not "
        "on the bus.\n\n"
        "The classic deadlock pattern: Thread A holds Instrument 1 and requests "
        "the switching matrix path to Instrument 2, while Thread B holds "
        "Instrument 2 and requests the path to Instrument 1. Neither can "
        "proceed — circular wait. This is Dijkstra's mutual exclusion problem, "
        "and the fix is structural.\n\n"
        "Implement strict resource ordering. Assign each instrument a unique "
        "priority number and require all threads to acquire resources in "
        "ascending order. If every thread requests R1 before R2 before R3, no "
        "circular dependency can form. Create a central ResourceBroker class "
        "that receives each thread's complete resource list, sorts by priority, "
        "and grants access atomically.\n\n"
        "The one place hardware physics does matter here: the switching matrix's "
        "relay settling time (typically 5-10 ms for reed relays, governed by "
        "the coil's L/R time constant plus mechanical bounce) sets the minimum "
        "lock-hold duration. Your broker must enforce this settling delay "
        "between path close and measurement start, regardless of which thread "
        "holds the lock. If you skip this, you won't get deadlocks — you'll "
        "get wrong measurements, which is harder to diagnose.\n\n"
        "Use Python's threading.Condition with a 30-second timeout to detect "
        "potential deadlocks early. Add a watchdog that monitors thread states "
        "and forces controlled teardown (power supplies ramped down safely) "
        "if any thread exceeds 2x its expected test time."
    ),

    150: (
        "This is a protocol sequencing problem, not a hardware defect — though "
        "it can masquerade as one when you're staring at a waveform that clearly "
        "doesn't match what's on screen. The key insight is understanding what "
        "*OPC? actually confirms versus what you think it confirms.\n\n"
        "*OPC? (Operation Complete) returns 1 when the oscilloscope has parsed "
        "your command and armed the trigger. It does NOT confirm that a new "
        "acquisition has completed and that fresh waveform data is available "
        "in the output buffer. The oscilloscope's internal pipeline — ADC "
        "sampling, decimation, trigger processing, display memory update — "
        "introduces latency between trigger-armed and data-ready. During that "
        "window, :WAVEFORM:DATA? returns whatever was in the buffer from the "
        "previous acquisition.\n\n"
        "The fix is to wait for the right completion signal. Replace *OPC? with "
        "a polling loop on :TER? (Trigger Event Register) or :ADER? "
        "(Acquisition Done Event Register), which confirms the full acquisition "
        "pipeline has flushed. The correct SCPI sequence is: send :SINGLE, "
        "poll :TER? until it returns 1, then issue :WAVEFORM:DATA?.\n\n"
        "Alternatively, use the VISA Service Request (SRQ) mechanism: configure "
        "*SRE 32 and *ESE 1 to generate an SRQ when acquisition actually "
        "completes. This event-driven approach eliminates polling and "
        "guarantees data freshness. Always include :WAVEFORM:SOURCE CHANx "
        "before fetching to explicitly bind the output buffer to the correct "
        "channel.\n\n"
        "The broader lesson: when instrument data looks wrong, check your "
        "command sequencing before suspecting the measurement hardware. "
        "Protocol race conditions account for a surprising fraction of "
        "'instrument errors' in automated test systems."
    ),

    151: (
        "This is a protocol compliance bug in your test software, not an "
        "instrument malfunction — but it's a common trap because the error "
        "(-400, Query UNTERMINATED) sounds like the instrument is broken.\n\n"
        "The SCPI error queue is a FIFO buffer with finite depth (typically "
        "20-30 entries per IEEE 488.2 Section 21.8). Error -400 means the "
        "instrument's output buffer contains unretrieved response data when "
        "a new command arrives. The IEEE 488.2 protocol requires that every "
        "query (command ending with ?) be followed by a read before the next "
        "command is sent. If your code sends two queries back-to-back without "
        "reading the first response, the output buffer accumulates stale data. "
        "Eventually the buffer fills (typically 64 KB to 1 MB), and the "
        "instrument enters an error state.\n\n"
        "The fix is disciplined query-response pairing. Every SCPI query must "
        "have a corresponding read. Implement a wrapper: "
        "def scpi_query(session, cmd): session.write(cmd); return session.read(). "
        "Never use write() for query commands.\n\n"
        "Add a cleanup routine at the start of each test iteration: send *CLS "
        "to clear status registers, then loop on SYST:ERR? until you get "
        '0,"No error" to drain the queue. Read and discard any pending output '
        "data with a short-timeout read. Use *RST at test initialization to "
        "return instruments to a known state.\n\n"
        "For robustness, implement a Python context manager that wraps each "
        "instrument session and guarantees error queue drainage in __exit__, "
        "even if exceptions occur. This pattern prevents the accumulation "
        "from ever starting."
    ),

    152: (
        "This is a software race condition, not a hardware timing issue — "
        "and making that distinction matters because the debug approach is "
        "completely different. If this were a hardware problem (say, a "
        "metastable flip-flop in a real state machine), you'd reach for an "
        "oscilloscope. Here, you need logging and thread analysis.\n\n"
        "The symptom — transition fires but entry action doesn't execute — "
        "points to a data visibility problem between your MEASURE state's "
        "exit action and your COMPARE state's entry action. The most likely "
        "cause: the MEASURE state posts a 'measurement complete' event and "
        "the transition guard evaluates to True, but the measured data hasn't "
        "been committed to shared memory yet when the COMPARE entry action "
        "tries to read it.\n\n"
        "On modern CPUs with out-of-order execution, a store to a variable "
        "in one thread may not be visible to another thread immediately, even "
        "after the store instruction completes. Without an explicit memory "
        "barrier or synchronization primitive, the COMPARE action can see "
        "stale or uninitialized data, fail silently, and appear to 'skip.'\n\n"
        "To diagnose: log the state machine's internal state (current_state, "
        "pending_events, guard_evaluations) at each transition with "
        "microsecond timestamps. Look for the COMPARE entry action receiving "
        "None or default values instead of actual measurement data.\n\n"
        "To fix: add explicit synchronization — use threading.Event or "
        "asyncio.Event to gate the COMPARE entry action on confirmed data "
        "availability. Better yet, ensure your state machine framework "
        "enforces run-to-completion semantics where each event fully completes "
        "its transition actions before the next event is dequeued. Libraries "
        "like pytransitions provide atomic transition semantics out of the box."
    ),

    153: (
        "This is a software architecture question. The physics of GPIB versus "
        "LAN communication differ enormously — parallel bus with tri-state "
        "drivers at 1 MB/s versus TCP/IP packets at gigabit speeds — but the "
        "whole point of VISA is that you don't need to care. The VISA resource "
        "string convention hides the transport layer, and your abstraction "
        "should follow the same principle.\n\n"
        "Create a base class InstrumentBase that accepts a VISA resource string "
        "and wraps pyvisa operations. The resource string encodes the "
        "transport: GPIB0::22::INSTR for GPIB address 22, "
        "TCPIP0::192.168.1.100::inst0::INSTR for LAN VXI-11, or "
        "TCPIP0::192.168.1.100::5025::SOCKET for raw socket. The pyvisa "
        "ResourceManager.open_resource() returns a session with uniform "
        "write(), read(), query() methods regardless of transport.\n\n"
        "Add a configuration layer for transport-specific details that do "
        "matter: GPIB needs termination character settings (term_char='\\n', "
        "send_end=True) while LAN sockets need explicit message termination "
        "because TCP is stream-oriented with no built-in message boundaries. "
        "These aren't physics differences — they're protocol framing "
        "differences, and your abstraction layer is the right place to "
        "handle them.\n\n"
        "Build instrument-specific subclasses (e.g., Keysight34465A_DMM "
        "extends InstrumentBase) that expose measurement functions: "
        "measure_dcv(range, resolution), measure_resistance(range). Each "
        "subclass translates high-level calls to SCPI command strings.\n\n"
        "Use a factory pattern with a YAML configuration file mapping logical "
        "names ('DMM_STATION_1') to resource strings. This makes test code "
        "completely transport-agnostic — swap a GPIB DMM for a LAN DMM by "
        "changing one line in the YAML. Add connection health monitoring with "
        "periodic *IDN? queries (every 30 seconds) to detect disconnections "
        "before they cause mid-test failures."
    ),

    154: (
        "A test sequencer state machine formalizes the test flow as a directed "
        "graph: states are test steps, transitions carry guard conditions based "
        "on measurement results. This is fundamentally a software design "
        "problem, but the guard conditions themselves encode hardware physics "
        "— and getting those conditions right is where domain knowledge "
        "matters.\n\n"
        "Use Python's `transitions` library to define the machine. Define "
        "states as an enum: INIT, POWER_ON, MEASURE_VCC, MEASURE_ICC, "
        "FUNCTIONAL_TEST, CALIBRATE, PASS, FAIL. Each state has entry/exit "
        "actions. Transitions carry guard conditions: MEASURE_VCC transitions "
        "to MEASURE_ICC only if 3.135V <= Vcc <= 3.465V (3.3V +/- 5%), "
        "otherwise it transitions to FAIL.\n\n"
        "Where physics enters legitimately: after measuring supply current Icc, "
        "if Icc exceeds the thermal budget (P = Icc * Vcc, compared against "
        "the package's theta_JA rating), you should branch to a THERMAL_RETEST "
        "state. The wait time in that state is governed by real thermal physics "
        "— Newton's cooling law T(t) = T_ambient + delta_T * e^(-t/tau) tells "
        "you how long to wait before the DUT is safe to retest. Similarly, a "
        "controlled shutdown must ramp power supplies at a safe rate (typically "
        "100 mV/ms) to avoid inductor kickback V = L * di/dt. These are "
        "physics constraints that your state machine must respect, not "
        "decorations.\n\n"
        "Store the state machine definition in a JSON or YAML file so "
        "non-programmer test engineers can modify states, transitions, guard "
        "conditions, and limits declaratively. The runtime engine loads the "
        "definition and instantiates the Machine. Log every state transition "
        "with timestamp, measurement value, and guard evaluation result for "
        "full traceability."
    ),

    155: (
        "Parallel multi-DUT testing is primarily a software concurrency "
        "problem constrained by hardware realities. Most instruments sit "
        "idle 90%+ of the time during a test sequence — waiting for relay "
        "settling, thermal stabilization, or DUT response. By interleaving "
        "DUT accesses through a switching matrix, you recover that dead time "
        "and approach throughput of N_DUT / t_longest_measurement.\n\n"
        "Architect the system in three layers.\n\n"
        "Layer 1: a SwitchingMatrix class that abstracts your relay matrix "
        "(e.g., Keithley 7001 with 7011-S cards). The matrix maps logical "
        "paths (DUT_3.VCC_SENSE) to physical relay addresses "
        "(SLOT1:CLOSE (@1!3:4!7)). The one hardware constraint you must "
        "respect: relay settling time. Reed relays need 5-10 ms after closure "
        "before the contact resistance stabilizes. Measure this on your "
        "specific matrix — skipping the settling wait is the #1 source of "
        "phantom measurement errors in parallel test systems.\n\n"
        "Layer 2: a DUTWorker class, one per DUT, running in its own thread. "
        "Each worker executes the test sequence independently but requests "
        "instrument access through a central ResourceScheduler. The scheduler "
        "implements a priority queue with aging (priority increases with wait "
        "time to prevent starvation).\n\n"
        "Layer 3: the ResourceScheduler grants exclusive instrument access "
        "with automatic matrix path setup. When DUT_3 needs a voltage "
        "measurement, the scheduler waits for the DMM to be free, closes the "
        "matrix path, enforces the settling delay, then grants access. After "
        "measurement, the scheduler opens the path and releases the DMM.\n\n"
        "Use Python's concurrent.futures.ThreadPoolExecutor with N workers "
        "matching your DUT count. Synchronize with threading.Semaphore(1) per "
        "shared instrument. Log resource wait times — they identify bottleneck "
        "instruments that you may want to duplicate."
    ),

    156: (
        "Test traceability is a data engineering problem: you need to capture "
        "enough metadata that any measurement can be reconstructed and "
        "explained months or years later. When a field return comes back and "
        "you need to know what the Icc reading was at test, which DMM "
        "measured it, when that DMM was last calibrated, and what firmware "
        "version was running — all of that must be queryable.\n\n"
        "Design a normalized relational schema with these core tables.\n\n"
        "TABLE test_run: run_id (UUID primary key), dut_serial, start_time, "
        "end_time, station_id (FK), fixture_id (FK), sw_version (git SHA), "
        "operator_id, overall_result (PASS/FAIL), ambient_temp_C, "
        "ambient_humidity_pct.\n\n"
        "TABLE test_measurement: measurement_id, run_id (FK), step_name, "
        "measured_value (FLOAT), unit, lower_limit, upper_limit, result "
        "(PASS/FAIL/SKIPPED), timestamp, instrument_id (FK), "
        "measurement_range, NPLC_setting.\n\n"
        "TABLE station_config: station_id, station_name, last_calibration_date, "
        "calibration_due_date, visa_resource_map (JSON).\n\n"
        "TABLE fixture_info: fixture_id, fixture_serial, contact_count, "
        "insertion_count, last_maintenance_date.\n\n"
        "TABLE instrument_cal: instrument_id, instrument_model, serial_number, "
        "cal_date, cal_due_date, cal_certificate_url.\n\n"
        "Use PostgreSQL with TimescaleDB for time-series measurement data — "
        "hypertable partitioning keeps queries fast at millions of rows. "
        "Create indexes on (dut_serial, step_name) for yield analysis and "
        "(station_id, timestamp) for station health monitoring.\n\n"
        "One place where hardware knowledge matters in your schema: include a "
        "measurement_uncertainty column. Calculate it from the instrument's "
        "spec: U = k * sqrt(u_range^2 + u_reading^2 + u_temp^2) where k=2 "
        "for 95% confidence. This lets you flag measurements where the "
        "uncertainty band overlaps the pass/fail limit — those are your "
        "statistically marginal results that may become field returns."
    ),

    157: (
        "CI/CD for hardware testing is a DevOps problem with physical "
        "constraints that pure software CI doesn't face. Software tests run "
        "in milliseconds on elastic cloud runners. Hardware tests take minutes "
        "to hours on a single physical station that can't be spun up on "
        "demand. Your pipeline architecture must account for this.\n\n"
        "Set up a dedicated test runner node (Jenkins agent or GitHub Actions "
        "self-hosted runner) physically connected to your test station. The "
        "runner needs VISA/GPIB interfaces to instruments and serial/JTAG "
        "connections to the DUT. Install pytest with pytest-html and "
        "pytest-json-report plugins.\n\n"
        "Structure your test suite with markers: @pytest.mark.smoke "
        "(30-second critical path), @pytest.mark.regression (full suite, "
        "15+ minutes), @pytest.mark.calibration (monthly). Trigger smoke "
        "tests on every commit and full regression on merge to main.\n\n"
        "The critical difference from software CI: only one test can use the "
        "physical station at a time. Implement a hardware locking mechanism "
        "— Jenkins lockable-resource or a file-based lock with flock(). "
        "Queue management matters because firmware developers waiting 45 "
        "minutes for a test station will start skipping tests.\n\n"
        "Pipeline stages: (1) flash firmware via JTAG/SWD using openocd or "
        "pyocd, (2) wait for boot (poll UART for ready string, timeout 30s), "
        "(3) run pytest with --junitxml=results.xml, (4) archive results and "
        "waveform captures. The hardware constraints that slow you down — DUT "
        "boot time, thermal settling, relay switching — are real physics that "
        "you can't optimize away, so focus on test selection: use git diff to "
        "identify changed firmware modules and map them to relevant test "
        "subsets. If only the ADC driver changed, run only ADC-related tests.\n\n"
        "Store results in the traceability database with the git SHA as "
        "sw_version. Set up Grafana dashboards showing test pass rate vs. "
        "commit history."
    ),

    158: (
        "SCPI command library design is a software engineering problem — "
        "specifically, an API design problem. The goal is the same as any "
        "good abstraction: isolate the parts that change (instrument models, "
        "SCPI command syntax) from the parts that don't (test logic, "
        "measurement workflows).\n\n"
        "First, define abstract interfaces per instrument function, not per "
        "instrument model. Create MeasurementDevice, SourceDevice, and "
        "SwitchDevice abstract base classes. A DMM and an oscilloscope both "
        "implement MeasurementDevice because they both measure voltage — the "
        "SCPI commands differ (MEAS:VOLT:DC? vs. :MEASURE:VMAX?) but test "
        "code calls device.measure_voltage(range=10.0). This follows Liskov "
        "substitution and enables instrument swaps without test code changes.\n\n"
        "Second, separate SCPI command strings from logic using a command "
        "registry pattern. Store commands in instrument-specific YAML files: "
        "keysight_34465a.yaml maps 'measure_dcv' to "
        "'MEAS:VOLT:DC? {range},{resolution}'. The driver loads YAML and "
        "formats at runtime. Replacing a Keysight 34465A with a Keithley "
        "DMM6500 means writing a new YAML file, not touching test code.\n\n"
        "Third, implement command validation. Before sending any SCPI "
        "command, validate parameters against the instrument's documented "
        "ranges. Log every command-response pair with timestamps — this is "
        "invaluable for post-mortem debugging when a test produces unexpected "
        "results and you need to distinguish instrument misconfiguration from "
        "a genuine DUT defect.\n\n"
        "Fourth, version instrument drivers alongside test code in the same "
        "repository. Tag releases with calibration dates so you can "
        "reconstruct the exact software state for any historical test result. "
        "This is critical for ISO 17025 compliance."
    ),

    160: (
        "Test data logging is a data engineering problem with one "
        "hardware-specific twist: your data must capture enough context to "
        "distinguish real DUT behavior from measurement system artifacts, "
        "sometimes years after the test ran.\n\n"
        "Use structured formats exclusively. Every test result should be a "
        "self-contained record in JSON or a database row, never a plain text "
        "log. The record must include: DUT serial, timestamp (ISO 8601 with "
        "timezone), test step ID, measured value with units, pass/fail limits, "
        "result, instrument ID, measurement parameters (range, NPLC, "
        "averaging), and environmental conditions (ambient temperature at "
        "minimum; humidity if you're making high-impedance measurements where "
        "surface leakage current I_leak = V / R_surface is humidity-dependent "
        "— that's a real physics factor that belongs in your data).\n\n"
        "Adopt a write-once, append-only data model. Never update historical "
        "test records — append corrections as new records with a reference "
        "to the original. This creates an auditable chain for ISO 9001 and "
        "AS9100 compliance.\n\n"
        "Store raw ADC data alongside processed results when feasible. A DMM "
        "reading of 3.301V is the processed result, but the raw data (number "
        "of samples, integration time, readings before averaging) enables "
        "retrospective analysis. When someone asks 'was that reading noisy?' "
        "six months later, you want to be able to answer.\n\n"
        "Use Parquet or HDF5 for large datasets — columnar formats compress "
        "well (typical 10:1 for repetitive measurement data) and support "
        "efficient analytical queries. Implement data retention policies "
        "early: safety-critical products (automotive, aerospace, medical) "
        "may need 15+ year retention. Use SHA-256 checksums on archived "
        "datasets to detect bit rot. Include a schema_version field so "
        "future tools can handle format evolution."
    ),

    166: (
        "This is a software deployment decision with a few hardware-relevant "
        "performance considerations. The answer depends on what instruments "
        "you have and how you deploy your test software.\n\n"
        "NI-VISA is a compiled binary library that interfaces with bus "
        "controller hardware through kernel-mode drivers. It supports all "
        "transport types (GPIB, USB-TMC, VXI, PXI, serial), handles "
        "low-level bus timing in optimized C code, provides "
        "hardware-accelerated SRQ handling, and achieves full GPIB throughput "
        "(1 MB/s via DMA). PyVISA-py reimplements VISA communication in pure "
        "Python using OS-level APIs.\n\n"
        "The hardware-relevant tradeoff: for GPIB instruments, NI-VISA's "
        "kernel-mode drivers achieve 1 MB/s throughput versus PyVISA-py's "
        "software-polled 100-300 KB/s. This matters when transferring large "
        "waveform datasets from oscilloscopes over GPIB. For USB-TMC, "
        "NI-VISA is currently the only option — PyVISA-py has limited "
        "USB-TMC support.\n\n"
        "For LAN-connected instruments (increasingly the norm), the "
        "performance difference is negligible. Both implementations use the "
        "OS TCP stack, so latency is dominated by network round-trip time "
        "(0.5-2 ms on local LAN) and instrument processing time (1-100 ms "
        "per command). VXI-11 and raw socket connections work identically.\n\n"
        "The software deployment tradeoff: NI-VISA requires a vendor runtime "
        "installation (problematic for Docker containers, CI/CD, and Linux/ARM "
        "platforms). PyVISA-py is pip-installable with zero external "
        "dependencies.\n\n"
        "Recommendation: use NI-VISA for stations with GPIB or USB-TMC "
        "instruments. Use PyVISA-py for all-LAN test stations, CI/CD "
        "environments, and when you need reproducible Python-only deployments."
    ),

    167: (
        "This is a software architecture choice driven by your test system's "
        "operational requirements. Both approaches work; the question is which "
        "failure modes and complexity tradeoffs you prefer.\n\n"
        "Polling architecture: the sequencer runs a main loop that checks "
        "instrument status registers (e.g., *STB? for Status Byte, bit 4 MAV "
        "for Message Available) at a fixed interval. Advantages: simple, "
        "deterministic, easy to debug because execution flow is linear. "
        "The tradeoff is latency — you detect events within t_poll/2 on "
        "average. At 100 ms poll interval, worst-case detection latency is "
        "100 ms. CPU overhead scales as N_instruments * poll_rate: 10 "
        "instruments polled at 10 Hz means 100 VISA transactions/second of "
        "pure overhead.\n\n"
        "Event-driven architecture: instruments generate Service Requests "
        "(SRQ) via the IEEE 488.1 SRQ line (GPIB) or TCP mechanism (LAN). "
        "The VISA driver fires a callback when SRQ arrives. Advantages: "
        "near-zero latency (limited by OS interrupt handling, typically "
        "< 1 ms), zero polling overhead, and natural support for parallel "
        "operations. The cost is significant complexity — callback thread "
        "safety, spurious SRQ handling, and proper state machines to track "
        "which instrument requested service.\n\n"
        "Use polling for sequential test flows with fewer than 5 instruments "
        "where measurement time dominates overhead. Use event-driven for "
        "parallel multi-DUT systems where instruments operate asynchronously "
        "and low-latency response to triggers or alarms is critical.\n\n"
        "A hybrid approach often wins in practice: event-driven for long "
        "measurements (SRQ on acquisition complete — avoids wasting minutes "
        "polling an oscilloscope during a long capture) and polling for fast "
        "status checks (relay settling confirmation where you just need to "
        "wait a few milliseconds)."
    ),

    168: (
        "This is an infrastructure decision driven by your operational "
        "requirements: how many stations write data, how you query it, and "
        "how long you keep it. Pick the simplest option that meets your "
        "constraints.\n\n"
        "SQLite: single-file embedded database, zero administration. Write "
        "throughput reaches ~50,000 inserts/second with WAL mode and batched "
        "transactions. The single-writer limitation means only one test "
        "station can write concurrently. Perfect for single-station "
        "deployments, portable archives, and prototype systems. The entire "
        "database is one file — trivially backed up, trivially moved. "
        "Practical limit ~100 GB before query performance degrades.\n\n"
        "PostgreSQL: full server database with concurrent write support via "
        "MVCC. Write throughput 100,000+ inserts/second with COPY and "
        "connection pooling. Handles complex joins (measurement data JOIN "
        "instrument calibration JOIN station config) that are essential for "
        "traceability queries. Partitioning by date range keeps performance "
        "stable at terabyte scale. The cost is operational overhead — server "
        "administration, backups, monitoring.\n\n"
        "TimescaleDB (PostgreSQL extension): adds automatic time-based "
        "partitioning and compression (typically 10-20x for measurement "
        "data). Continuous aggregates pre-compute hourly/daily yield "
        "statistics. Time-range queries (all measurements from station 5 "
        "last week) run 10-100x faster than vanilla PostgreSQL.\n\n"
        "For retention: automotive and aerospace standards (IATF 16949) "
        "require 7-15 years of test data. Plan for this from day one — "
        "migrating databases under regulatory requirements is painful.\n\n"
        "Recommendation: PostgreSQL + TimescaleDB for any multi-station "
        "production environment. SQLite only for single-station or portable "
        "scenarios. Avoid standalone InfluxDB — it lacks relational JOINs "
        "needed for traceability queries linking measurements to calibration "
        "records and fixture history."
    ),
}


def main():
    # Read all entries
    with open(DATA_FILE, "r") as f:
        lines = f.readlines()

    print(f"Read {len(lines)} entries from {DATA_FILE.name}")
    print(f"Revising {len(REVISIONS)} entries: lines {sorted(REVISIONS.keys())}")

    # Backup
    shutil.copy2(DATA_FILE, BACKUP_FILE)
    print(f"Backup saved to {BACKUP_FILE.name}")

    # Apply revisions
    revised_count = 0
    for line_num, new_output in REVISIONS.items():
        idx = line_num - 1  # 0-based
        if idx >= len(lines):
            print(f"  WARNING: line {line_num} out of range, skipping")
            continue

        entry = json.loads(lines[idx].strip())
        old_len = len(entry["output"])
        entry["output"] = new_output
        new_len = len(entry["output"])
        lines[idx] = json.dumps(entry, ensure_ascii=False) + "\n"
        revised_count += 1
        print(f"  Line {line_num}: revised ({old_len} -> {new_len} chars)")
        print(f"    Q: {entry['instruction'][:80]}...")

    # Write back
    with open(DATA_FILE, "w") as f:
        f.writelines(lines)

    print(f"\nDone. Revised {revised_count} entries in {DATA_FILE.name}")
    print(f"Original backed up to {BACKUP_FILE.name}")


if __name__ == "__main__":
    main()
