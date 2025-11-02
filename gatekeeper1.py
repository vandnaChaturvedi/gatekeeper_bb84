import numpy as np
from qiskit import QuantumCircuit
#from qiskit.providers.aer import QasmSimulator
#from qiskit import execute

from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import numpy as np
from qiskit.primitives import StatevectorSampler
from qiskit_aer import AerSimulator

rng = np.random.default_rng(42)

def random_bits(n):
    return rng.integers(0, 2, size=n, dtype=np.int8)

def build_bb84_circuit(bits, basis_a, basis_b):
    n = len(bits)
    qc = QuantumCircuit(n, n)
    for i in range(n):
        if bits[i] == 1:
            qc.x(i)
        if basis_a[i] == 1:
            qc.h(i)
    for i in range(n):
        if basis_b[i] == 1:
            qc.h(i)
        qc.measure(i, i)
    return qc

def run_bb84_round(n_qubits=256, shots=1, backend=None):
    bits = random_bits(n_qubits)           # Alice’s raw bits
    basis_a = random_bits(n_qubits)        # Alice’s bases (0=Z,1=X)
    basis_b = random_bits(n_qubits)        # Bob’s bases (0=Z,1=X)
    qc = build_bb84_circuit(bits, basis_a, basis_b)
    # backend = backend or QasmSimulator()
    backend = AerSimulator()
    # res = execute(qc.reverse_bits(), backend=backend, shots=shots).result()
    res  = backend.run(qc.reverse_bits()).result()
    bitstring = list(res.get_counts().most_frequent())  # one shot => one string
    bitstring = np.array([int(b) for b in bitstring], dtype=np.int8)
    # Sifting
    mask = basis_a == basis_b
    alice_sift = bits[mask]
    bob_sift = bitstring[mask]
    return {
        "bits": bits, "basis_a": basis_a, "basis_b": basis_b,
        "alice_sift": alice_sift, "bob_sift": bob_sift, "mask": mask
    }

def estimate_qber(alice_sift, bob_sift, sample_frac=0.2):
    m = len(alice_sift)
    if m == 0:
        return np.nan, np.array([], dtype=np.int32)
    k = max(1, int(sample_frac * m))
    idx = rng.choice(m, size=k, replace=False)
    mismatches = np.sum(alice_sift[idx] != bob_sift[idx])
    qber = mismatches / k
    return qber, idx

# Example: one round, then keep undisclosed positions as candidate key
out = run_bb84_round(n_qubits=256, shots=1)
qber, disclosed_idx = estimate_qber(out["alice_sift"], out["bob_sift"], sample_frac=0.25)
keep_mask = np.ones(len(out["alice_sift"]), dtype=bool)
keep_mask[disclosed_idx] = False
alice_key = out["alice_sift"][keep_mask]
bob_key   = out["bob_sift"][keep_mask]
# print("Sifted length:", len(out["alice_sift"]), " QBER (sample):", qber, " Key length:", len(alice_key))
# print(alice_key,bob_key)