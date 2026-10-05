"""Angle encoding: load a classical feature vector into qubit rotation angles.

Each feature x_i is placed on its own qubit with an RY(x_i) rotation, giving
    |psi(x_i)> = cos(x_i / 2)|0> + sin(x_i / 2)|1>.

Targets Qiskit 2.x and qiskit-aer 0.17. Run with:  python angle_encoding.py
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator, StatevectorSampler
from qiskit.quantum_info import SparsePauliOp, Statevector


def scale_to_angles(data, low, high):
    """Map raw feature values from [low, high] onto angles in [0, pi].

    Angles beyond pi would wrap around the Bloch sphere, so two different
    inputs could land on the same state; keeping to [0, pi] avoids that.
    """
    data = np.asarray(data, dtype=float)
    return (data - low) / (high - low) * np.pi


def angle_encode(angles):
    """Return a circuit with one qubit per feature, qubit i rotated by RY(angles[i])."""
    qc = QuantumCircuit(len(angles))
    for i, theta in enumerate(angles):
        qc.ry(theta, i)
    return qc


if __name__ == "__main__":
    # Two raw features on a 0..6 scale, e.g. sensor readings 2 and 3.
    raw = [2.0, 3.0]
    angles = scale_to_angles(raw, low=0.0, high=6.0)   # -> [pi/3, pi/2]
    print("angles (rad):", np.round(angles, 4))

    qc = angle_encode(angles)
    print(qc.draw("text"))

    # Exact amplitudes and probabilities (Qiskit bit order: q1 q0).
    sv = Statevector(qc)
    print("amplitudes:", np.round(sv.data.real, 4))
    print("probabilities:", {str(k): round(float(v), 4) for k, v in sv.probabilities_dict().items()})

    # Sampling, as a real device would report it.
    measured = qc.copy()
    measured.measure_all()
    counts = StatevectorSampler(seed=7).run([measured], shots=1000).result()[0].data.meas.get_counts()
    print("counts (1000 shots):", dict(sorted(counts.items())))

    # <Z> on each qubit should equal cos(angle).
    # SparsePauliOp strings are also little-endian: "IZ" acts on qubit 0.
    observables = [SparsePauliOp("IZ"), SparsePauliOp("ZI")]
    evs = StatevectorEstimator().run([(qc, observables)]).result()[0].data.evs
    print("<Z0>, <Z1>:", np.round(evs, 4), " cos(angles):", np.round(np.cos(angles), 4))
