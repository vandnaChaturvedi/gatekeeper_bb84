# BB84 Gatekeeper

BB84 quantum key distribution (QKD) protocol implementation using Qiskit.

## Prerequisites

Install the required Python packages:

```bash
pip install numpy qiskit qiskit-aer
```

Or using a requirements file:

```bash
pip install -r requirements.txt
```

Required packages:
- `numpy`
- `qiskit`
- `qiskit-aer`

## Running gatekeeper1.py

### Basic Execution

Simply run the script:

```bash
python gatekeeper1.py
```

### What the script does

1. Runs a BB84 QKD protocol simulation with 256 qubits
2. Alice prepares qubits in random bases (Z or X)
3. Bob measures in random bases
4. Performs sifting to keep only matching basis measurements
5. Estimates QBER (Quantum Bit Error Rate) using a 25% sample
6. Generates final secret keys for Alice and Bob (excluding disclosed test bits)

**Note:** The script currently has a debugger breakpoint (`pdb.set_trace()`) on line 68. When you run it, execution will pause at this point and drop you into an interactive debugger. To continue:
- Type `c` and press Enter to continue execution
- Type `q` and press Enter to quit the debugger
- Or remove/comment out the `import pdb; pdb.set_trace()` line for normal execution

### Output

The script generates:
- `alice_key`: Alice's final secret key (numpy array)
- `bob_key`: Bob's final secret key (numpy array)
- Both keys should match (same length and values) when there's no eavesdropping

To see the keys, uncomment the print statement on line 70:
```python
print(alice_key, bob_key)
```

### Customizing Parameters

You can modify the parameters in the script:

- `n_qubits`: Number of qubits to use (default: 256) - modify in line 62
- `sample_frac`: Fraction of sifted bits to use for QBER estimation (default: 0.25) - modify in line 63

Example:
```python
out = run_bb84_round(n_qubits=512, shots=1)  # Use 512 qubits instead
qber, disclosed_idx = estimate_qber(out["alice_sift"], out["bob_sift"], sample_frac=0.3)  # Use 30% for testing
```
Below is a README.md-formatted version of your document that you can copy and paste directly into your GitHub repository.[1]

# BB84 Quantum Key Distribution (QKD) with Qiskit[1]

This repository implements and explains a BB84 Quantum Key Distribution prototype using Qiskit, including end-to-end key generation, measurement and sifting, QBER-based eavesdropping detection, and noise-driven performance analysis suitable for educational use and experimentation.[1]

### Overview
- Implement the BB84 protocol with Alice’s random state preparation, Bob’s random-basis measurement, classical sifting, and QBER-based error estimation to detect eavesdropping or channel/device noise.[1]
- Run baseline, noisy, and adversarial (intercept–resend) scenarios, collect key metrics, and visualize how QBER and key yield change with conditions to demonstrate practical feasibility on today’s platforms.[1]
- Prepare an informative presentation that teaches QKD fundamentals and compares BB84 to standardized post-quantum cryptography such as lattice-based KEMs, emphasizing complementary deployment strategies.[1]

### Features
- End-to-end BB84 flow: random bits and bases, quantum state preparation, measurement, sifting, sampling for QBER, and key retention logic.[1]
- Experiment suite: baseline (noisy-free idealization), noise sweeps, and intercept–resend eavesdropper to highlight detectable disturbance and security thresholds.[1]
- Metrics and visualization: QBER, key rate, and sifting ratio collected and plotted to illustrate performance envelopes and trade-offs.[1]

***

### Architecture
BB84 can be organized around modular classical-quantum functions to make experimentation and testing straightforward.[1]

- generate_random_bits: produce Alice’s raw key bits as a binary array.[1]
- generate_random_bases: produce Alice’s and Bob’s basis choices in Z or X for each qubit position.[1]
- prepare_qubits (Alice): encode bits into qubits using Alice’s basis choices with QuantumCircuit primitives (e.g., X and H).[1]
- send_qubits (Channel): simulate transmission and optionally inject noise or an intercept–resend Eve for adversarial runs.[1]
- measure_qubits (Bob): measure each qubit in Bob’s chosen basis using H transforms and computational measurements.[1]
- sifting: keep only positions where bases match to form the sifted key candidate shared by Alice and Bob.[1]
- error_estimation: reveal a random subset of sifted bits to estimate QBER and decide whether to proceed or abort.[1]

***

### Metrics
- QBER: quantum bit error rate computed as errors over tested (disclosed) positions and used to flag eavesdropping or excessive noise.[1]
- Key rate: final secret key length divided by initial qubit count as an efficiency indicator for the full pipeline.[1]
- Sifting ratio: sifted length divided by initial qubit count, typically near $$ \approx \frac{1}{2} $$ under random independent bases.[1]

***

### Experiments
- Baseline run: execute with a large batch size and no noise or Eve; expect near-zero QBER and sifting ratio around $$ \approx \frac{1}{2} $$.[1]
- Noise run: add depolarizing or bit-flip style channel errors (or device-like T1/T2) and sweep the noise probability while plotting QBER versus noise level.[1]
- Eavesdropping run: simulate a simple intercept–resend Eve; QBER should rise markedly, and if it exceeds typical thresholds (often discussed around $$ \approx 11\% $$ for standard BB84 analyses), abort or increase privacy amplification in principle.[1]

***

### Suggested Workflow
1. Implement core functions for randomization, preparation, measurement, sifting, and QBER sampling to produce a reproducible BB84 round pipeline.[1]
2. Run a baseline batch to validate that sifting and QBER behave as expected before introducing noise or adversaries.[1]
3. Add noise and Eve modules, perform parameter sweeps, and log QBER, key rate, and sifting ratio for each configuration to support comparative plots.[1]
4. Use the collected results to build slides explaining how QKD leverages measurement disturbance for security and how BB84 performs under realistic imperfections.[1]

***

### Analysis Strategy
- Baseline: validate correctness and confirm low QBER, establishing a reference for later comparisons.[1]
- Noise: quantify how error channels degrade security-relevant metrics and identify sensitivity to particular error types or rates.[1]
- Eavesdropping: demonstrate detectability via QBER growth and motivate abort decisions or stronger post-processing to maintain security margins.[1]

***

### Results to Capture
- Plots of QBER vs noise level and retained key length vs noise or batch size for reproducible evidence of feasibility and limits.[1]
- Tables summarizing sifting ratio, QBER, and key rate across baseline, noisy, and Eve conditions for quick comparison in the presentation.[1]

***

### BB84 vs PQC (Kyber/ML‑KEM)

| Aspect | BB84 QKD | Kyber/ML‑KEM (PQC) |
|---|---|---|
| Security model | Information-theoretic security based on quantum measurement disturbance and no-cloning principles[1]. | Computational security based on hardness assumptions (e.g., LWE) formalized in lattice-based KEMs[1]. |
| Hardware | Requires quantum channel and photonic devices; distance and device imperfections are key constraints[1]. | Software-deployable on classical networks and readily integrated into existing protocols like TLS/SSH[1]. |
| Function | Key agreement/distribution for generating symmetric keys with on-line eavesdropper detection via QBER[1]. | Key encapsulation for establishing shared secrets without quantum channels and with standardized parameters[1]. |
| Deployment | Point-to-point high-security links; often niche but growing with fiber and free-space optics progress[1]. | Broad near-term adoption via standardization and software rollouts across general-purpose infrastructure[1]. |
| Complementarity | Can be combined with PQC in hybrid schemes to achieve defense-in-depth and secure classical control channels[1]. | Complements QKD by providing quantum-resistant primitives where quantum links are unavailable or impractical[1]. |

***

### Presentation Outline
- QKD fundamentals: explain random bases, measurement disturbance, and why eavesdropping introduces detectable errors in BB84.[1]
- Protocol walkthrough: Alice’s encoding, Bob’s measurement, sifting, sampling for QBER, and decisions to proceed/abort based on thresholds.[1]
- Experiments and plots: baseline vs noisy vs Eve runs with QBER/key-rate comparisons and interpretation of results for practical feasibility.[1]
- PQC comparison: situate BB84 alongside NIST-standardized lattice KEMs, highlighting different security bases and deployment contexts.[1]
- Takeaways: QKD and PQC are complementary; choose based on threat model, infrastructure, and desired assurances, or combine in hybrid stacks.[1]

***

### Notes and Tips
- Use a plotting library of your choice to visualize QBER vs noise and retained key length to make trends clear in your slide deck.[1]
- Keep functions modular so you can toggle noise models and Eve scenarios quickly during experimentation and demos.[1]
- For larger batches, automate repeated runs and aggregate statistics to produce smooth curves and robust comparisons for your presentation.[1]

***

### Acknowledgments
This README synthesizes the BB84 implementation plan, experiment design, and presentation guidance from the provided document for direct inclusion in a repository README.[1]

[1](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/70649216/04f74766-ad3e-4103-b649-c80190b35982/bb84.docx)
