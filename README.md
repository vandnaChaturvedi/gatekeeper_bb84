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

