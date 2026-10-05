# test-repo

An interactive demo of **angle encoding**, the simplest way to load classical data into qubits.
Open `index.html` in a browser. There's nothing to install.

- `index.html`: the visual demo. Move the feature sliders to see the RY angles, each qubit's state on the Bloch circle, the joint probabilities, and simulated 1000-shot measurements.
- `angle_encoding.py`: the same circuit in Qiskit (`pip install qiskit qiskit-aer && python angle_encoding.py`).
- `ANGLE_ENCODING.md`: a step-by-step explanation, with the hand calculation checked against Qiskit.

## Design system

Colors, type, spacing and the light/dark theme switch are defined as tokens.
See [DESIGN.md](DESIGN.md), and open `design-preview.html` for a live preview.
