# Physics Style Audit Report

**Dataset:** full_dataset.jsonl (252 entries)

## Summary

| Classification | Count | % |
|---|---|---|
| PHYSICS-FIRST | 194 | 77% |
| PHYSICS-DECORATED | 0 | 0% |
| MIXED | 58 | 23% |

## PHYSICS-DECORATED (need reframing)

These entries cover topics where physics is not the primary explanatory framework, but physics equations/analogies are inserted as decoration. Recommended fix: reframe to honestly triage between physics and non-physics causes.


## MIXED (review recommended)

These entries blend physics and non-physics content. Review to confirm the physics is genuinely load-bearing.

### Line 5

**Q:** A boundary scan test detects an unexpected device IDCODE in position 3 of a 5-device chain. The board schematic and BOM ...

- Low signal (sw=0, hw=1, eq=0)

### Line 7

**Q:** Describe the procedure for validating a BSDL file against actual silicon behavior before deploying boundary scan tests i...

- Low signal (sw=0, hw=1, eq=0)

### Line 9

**Q:** Walk through the process of debugging a boundary scan chain integrity failure on a board where the TAP controller does n...

- Low signal (sw=0, hw=1, eq=0)

### Line 21

**Q:** Compare boundary scan chain integrity verification versus interconnect testing in terms of what physical defects each me...

- Low signal (sw=0, hw=1, eq=1)

### Line 24

**Q:** A high-speed serial interface loopback test on a PCIe Gen3 link shows a bit error rate of 10^-8, just above the specific...

- Low signal (sw=0, hw=1, eq=1)

### Line 25

**Q:** A peripheral bus enumeration test discovers a USB 3.0 hub on the board but consistently fails to enumerate one of its fo...

- Low signal (sw=0, hw=1, eq=1)

### Line 26

**Q:** A firmware-assisted POST routine running on an ARM processor reports a memory subsystem error during DDR4 initialization...

- Low signal (sw=0, hw=1, eq=1)

### Line 28

**Q:** What is the recommended procedure for validating clock tree integrity using frequency counters as part of a functional t...

- Low signal (sw=0, hw=0, eq=2)

### Line 31

**Q:** Describe how to set up and execute firmware-assisted POST routines as part of a functional test program for boards with ...

- Low signal (sw=0, hw=0, eq=0)

### Line 32

**Q:** What are the industry best practices for power rail margining during functional test to catch voltage-sensitive defects?...

- Low signal (sw=0, hw=1, eq=2)

### Line 33

**Q:** Describe the DFT considerations that improve clock tree verification outcomes in functional test applications....

- Low signal (sw=0, hw=0, eq=2)

### Line 35

**Q:** What best practices ensure reliable firmware-assisted POST results in a production functional test environment?...

- Low signal (sw=0, hw=1, eq=2)

### Line 40

**Q:** Compare power sequencing validation versus rail margining as functional test strategies. When is each most valuable?...

- Low signal (sw=0, hw=0, eq=0)

### Line 41

**Q:** When would you choose high-speed serial interface loopback testing over direct eye diagram measurement for production fu...

- Low signal (sw=0, hw=0, eq=1)

### Line 42

**Q:** Compare firmware-assisted POST versus external boundary scan testing for detecting memory subsystem defects. What are th...

- Low signal (sw=0, hw=1, eq=1)

### Line 45

**Q:** Guided probe diagnostics on a failed board indicate that a logic gate output is stuck high. The gate is an AND function ...

- Low signal (sw=0, hw=1, eq=1)

### Line 46

**Q:** A Pareto analysis of field returns shows that 40% of failures are 'no fault found' (NFF) after retesting in the lab. Wha...

- Low signal (sw=0, hw=1, eq=1)

### Line 51

**Q:** How do you perform statistical Pareto analysis of field failure returns to identify systematic defect patterns?...

- Low signal (sw=0, hw=0, eq=1)

### Line 52

**Q:** Describe how to implement a 5-why causal chain analysis for intermittent defects found during production testing....

- Low signal (sw=0, hw=0, eq=1)

### Line 62

**Q:** Compare guided probe diagnostics versus automated Pareto analysis as fault isolation strategies in a production environm...

- Low signal (sw=0, hw=1, eq=1)

### Line 63

**Q:** When would you choose 5-why causal chain analysis over statistical Pareto analysis for investigating production test fai...

- Low signal (sw=0, hw=0, eq=0)

### Line 72

**Q:** Walk through the process of identifying untestable nets on a PCB and implementing mitigation strategies to reduce test c...

- Low signal (sw=0, hw=0, eq=1)

### Line 76

**Q:** What common pitfalls should engineers avoid when performing test coverage analysis, and how can these be prevented?...

- Low signal (sw=0, hw=0, eq=2)

### Line 83

**Q:** Compare defect-per-million correlation to test escapes versus entropy-based coverage analysis as methods for evaluating ...

- Low signal (sw=0, hw=0, eq=2)

### Line 89

**Q:** An arbitrary waveform generator (AWG) stimulus-response test on a mixed-signal board shows unexpected harmonics at 3x an...

- Low signal (sw=0, hw=0, eq=1)

### Line 93

**Q:** How do you implement mixed-signal stimulus-response testing using an arbitrary waveform generator for production-level v...

- Low signal (sw=0, hw=0, eq=2)

### Line 99

**Q:** From a physics perspective, why does the Nyquist theorem impose a fundamental limit on ADC sampling, and what happens wh...

- Low signal (sw=0, hw=1, eq=2)

### Line 103

**Q:** Compare INL and DNL measurements as metrics for evaluating ADC linearity. When does one reveal defects that the other mi...

- Low signal (sw=0, hw=1, eq=2)

### Line 116

**Q:** What are the best practices for managing test fixture probe wear and maintaining measurement accuracy over high-volume p...

- Low signal (sw=0, hw=1, eq=1)

### Line 117

**Q:** What are the best practices for optimizing ICT test coverage on a board with limited physical access due to component de...

- Low signal (sw=0, hw=1, eq=1)

### Line 119

**Q:** What are the best practices for setting pass/fail thresholds in ICT to minimize both false failures and escaped defects?...

- Low signal (sw=0, hw=1, eq=2)

### Line 149

**Q:** Our test sequencer hangs in a deadlock state when running parallel DUT tests. Two threads are waiting on each other's in...

- Low signal (sw=1, hw=0, eq=0)

### Line 150

**Q:** SCPI commands sent to our oscilloscope are returning stale data from the previous measurement. The *OPC? query returns 1...

- Mixed topic (sw=1, hw=1)

### Line 151

**Q:** Our automated test logs show that SCPI error queue entries (SYST:ERR?) are accumulating across test iterations, eventual...

- Low signal (sw=1, hw=0, eq=0)

### Line 152

**Q:** Our test sequencer's state machine occasionally skips a test step when transitioning from a MEASURE state to a COMPARE s...

- Software/protocol topic (sw=2, hw=0)
- Software topic with minimal physics — may need reframing

### Line 153

**Q:** How do I design a VISA instrument abstraction layer in Python that supports both GPIB and LAN-connected instruments tran...

- Software/protocol topic (sw=3, hw=0)
- Software topic with minimal physics — may need reframing

### Line 154

**Q:** How do I implement a test sequencer state machine with conditional branching based on measurement results?...

- Software/protocol topic (sw=2, hw=0)
- Software topic with minimal physics — may need reframing

### Line 155

**Q:** How do I set up parallel test execution across a multi-DUT fixture with shared instrumentation?...

- Low signal (sw=0, hw=0, eq=0)

### Line 157

**Q:** How do I integrate hardware regression test suites into a CI/CD pipeline so that firmware changes are automatically vali...

- Low signal (sw=1, hw=0, eq=1)

### Line 158

**Q:** What are the best practices for structuring SCPI command libraries in a test automation framework to ensure maintainabil...

- Low signal (sw=1, hw=0, eq=0)

### Line 160

**Q:** What best practices should I follow when designing test result logging and data formats for long-term analysis of hardwa...

- Low signal (sw=1, hw=0, eq=1)

### Line 161

**Q:** What are the best practices for designing robust error handling and recovery in automated test sequences that control ex...

- Mixed topic (sw=2, hw=2)

### Line 162

**Q:** Why does VISA communication over GPIB require specific termination methods, and what is the physics behind the IEEE 488 ...

- Mixed topic (sw=1, hw=1)

### Line 166

**Q:** What are the tradeoffs between using PyVISA with NI-VISA versus PyVISA-py (pure Python VISA) for test automation instrum...

- Software/protocol topic (sw=4, hw=0)
- Software topic with minimal physics — may need reframing

### Line 167

**Q:** How does a polling-based test sequencer compare to an event-driven test sequencer for hardware test automation, and when...

- Software/protocol topic (sw=3, hw=0)
- Software topic with minimal physics — may need reframing

### Line 168

**Q:** What are the differences between SQLite, PostgreSQL, and time-series databases (InfluxDB/TimescaleDB) for storing produc...

- Software/protocol topic (sw=4, hw=0)
- Software topic with minimal physics — may need reframing

### Line 172

**Q:** After implementing yield-aware test flow partitioning, our total test time increased by 20% instead of decreasing. The p...

- Low signal (sw=0, hw=0, eq=1)

### Line 174

**Q:** How do I implement adaptive test sequencing that reduces test time by skipping tests with low defect probability based o...

- Low signal (sw=0, hw=0, eq=1)

### Line 175

**Q:** How do I implement yield-aware test flow partitioning that routes DUTs through different test paths based on predicted y...

- Low signal (sw=0, hw=0, eq=2)

### Line 193

**Q:** Conformal-coated assemblies in our outdoor enclosures show corrosion on fine-pitch QFN ground pads after 18 months in a ...

- Low signal (sw=0, hw=0, eq=2)

### Line 198

**Q:** How do I perform vibration qualification testing on a rugged tablet per MIL-STD-810H Method 514.8 for a military vehicle...

- Low signal (sw=0, hw=0, eq=2)

### Line 201

**Q:** What best practices should I follow when implementing a production burn-in program to minimize cost while effectively sc...

- Low signal (sw=0, hw=1, eq=2)

### Line 208

**Q:** Compare HALT (Highly Accelerated Life Test) with traditional qualification testing (e.g., Telcordia GR-468) for finding ...

- Low signal (sw=0, hw=0, eq=2)

### Line 219

**Q:** How do I measure crosstalk between adjacent high-speed differential pairs on a PCB using a VNA, and how do I interpret t...

- Low signal (sw=0, hw=1, eq=2)

### Line 229

**Q:** Compare time-domain reflectometry (TDR) versus frequency-domain vector network analyzer (VNA) measurements for character...

- Low signal (sw=0, hw=1, eq=2)

### Line 239

**Q:** How do I train and validate a machine learning classifier to reduce false calls on our AOI line?...

- Low signal (sw=0, hw=1, eq=2)

### Line 244

**Q:** What are the best practices for setting up AOI to minimize false calls while maintaining high defect detection on LED as...

- Low signal (sw=0, hw=1, eq=1)

### Line 252

**Q:** How do traditional rule-based AOI algorithms compare to deep learning-based approaches for defect classification, and wh...

- Low signal (sw=0, hw=1, eq=0)

