# Angle encoding, explained

The code is in [`angle_encoding.py`](angle_encoding.py). It targets Qiskit 2.5 and qiskit-aer 0.17.
To run it: `pip install qiskit qiskit-aer && python angle_encoding.py`.

## 1. What it is

A quantum machine-learning model can only work on data that has been loaded into qubits.
**Angle encoding** is the simplest way to load it. Each number (a *feature*) becomes the
rotation angle of its own qubit. With *n* features you need *n* qubits, and the circuit is
one gate deep.

## 2. Intuition

Picture each qubit as a needle that starts pointing straight up, which is the state |0>.
The feature value says how far to tip the needle towards straight down, which is |1>:
0 means don't tip it, π means tip it all the way over. Measuring the qubit gives 1 more often
the further the needle has been tipped.

**Where the picture breaks:** a qubit is described by complex *amplitudes*, not a physical
needle. The measurement probability is the amplitude squared, and amplitudes can cancel
each other when later gates act on them. The needle picture says nothing about that.

## 3. The maths, small

The gate used is RY(θ), a rotation about the Y axis. In the basis (|0>, |1>):

```
RY(θ) = [ cos(θ/2)  -sin(θ/2) ]
        [ sin(θ/2)   cos(θ/2) ]
```

Applied to |0> = (1, 0), it gives

```
|ψ(θ)> = cos(θ/2)|0> + sin(θ/2)|1>
```

so P(0) = cos²(θ/2) and P(1) = sin²(θ/2). θ is divided by 2 here because of how qubit
rotations are defined: θ = π moves |0> all the way to |1>.

**Step 1: scale the data** (`scale_to_angles`). Raw features are mapped linearly onto
[0, π]. The code uses features 2 and 3 on a 0 to 6 scale:

```
θ0 = 2/6 · π = π/3        θ1 = 3/6 · π = π/2
```

The range stops at π because a larger angle starts to tip the needle back up again, so
two different inputs could produce the same state and the model could not tell them apart.

**Step 2: encode each qubit** (`angle_encode`):

| Qubit | θ | amplitude of \|0> = cos(θ/2) | amplitude of \|1> = sin(θ/2) | P(1) |
|---|---|---|---|---|
| q0 | π/3 | cos(π/6) = 0.8660 | sin(π/6) = 0.5000 | 0.25 |
| q1 | π/2 | cos(π/4) = 0.7071 | sin(π/4) = 0.7071 | 0.50 |

**Step 3: combine the qubits.** For two qubits that were prepared separately, the joint
state is the *tensor product*: multiply every amplitude of q1 by every amplitude of q0.
In Qiskit's bit order (q1 written on the left, q0 on the right):

| Outcome q1 q0 | Amplitude | Probability |
|---|---|---|
| 00 | 0.7071 × 0.8660 = 0.6124 | 0.375 |
| 01 | 0.7071 × 0.5000 = 0.3536 | 0.125 |
| 10 | 0.7071 × 0.8660 = 0.6124 | 0.375 |
| 11 | 0.7071 × 0.5000 = 0.3536 | 0.125 |

The probabilities add up to 1. The state is a *product state*: angle encoding by itself creates
no entanglement. Entanglement only appears when later gates, such as CNOTs in a model layer,
act on the encoded qubits.

**Expectation values.** For a single qubit, <Z> = P(0) − P(1) = cos²(θ/2) − sin²(θ/2) = cos θ.
So <Z0> = cos(π/3) = 0.5 and <Z1> = cos(π/2) = 0.

## 4. The circuit

```
     ┌─────────┐
q_0: ┤ Ry(π/3) ├
     ├─────────┤
q_1: ┤ Ry(π/2) ├
     └─────────┘
```

## 5. Check against Qiskit

Real output from `python angle_encoding.py`:

```
angles (rad): [1.0472 1.5708]
amplitudes: [0.6124 0.3536 0.6124 0.3536]
probabilities: {'00': 0.375, '01': 0.125, '10': 0.375, '11': 0.125}
counts (1000 shots): {'00': 379, '01': 123, '10': 377, '11': 121}
<Z0>, <Z1>: [0.5 0. ]  cos(angles): [0.5 0. ]
```

- `Statevector` gives the exact amplitudes, in the order 00, 01, 10, 11. They match the table
  in step 3.
- `StatevectorSampler` imitates a real device: 1000 measurements, seeded so you get the same
  counts every run. The counts land close to 375 / 125 / 375 / 125, with the small gap you
  expect from random sampling.
- `StatevectorEstimator` returns <Z> for each qubit, and it equals cos θ, as derived above.
  Note that Pauli strings are little-endian too: `"IZ"` measures qubit 0 and `"ZI"` measures qubit 1.

## Points to watch

- **Bit order.** Qiskit prints q0 as the rightmost bit. Textbooks such as Nielsen and Chuang
  put the first qubit on the left, so their table would list 01 and 10 swapped.
- **Cost.** One qubit per feature. 100 features would need 100 qubits, which is why
  *amplitude encoding* (2ⁿ features in n qubits, but with a much deeper circuit) is sometimes
  used instead.
- **Variants.** RX instead of RY gives the same probabilities but complex amplitudes. In
  *dense angle encoding*, RY and then RZ put two features on each qubit.

## What comes next

Angle encoding is the input stage of variational quantum classifiers and quantum neural
networks: the encoded qubits are passed into a trainable layer (parameterised rotations plus
CNOTs), and the measured <Z> values become the model's prediction.
