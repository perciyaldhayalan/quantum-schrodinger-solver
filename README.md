# Quantum Schrödinger Equation Solver

[![CI](https://github.com/perciyaldhayalan/quantum-schrodinger-solver/actions/workflows/ci.yml/badge.svg)](https://github.com/NoxiousTorpedo2230/quantum-schrodinger-solver/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.13-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-0.1.0-blue)

A research-oriented computational physics project for solving and validating the **one-dimensional Schrödinger equation** using numerical methods.

The project combines sparse finite-difference eigenvalue calculations, analytical validation, quantum observables, Crank-Nicolson time propagation, Gaussian wavepacket dynamics, and quantitative quantum-tunnelling studies.

Rather than treating the Schrödinger equation as only a visualization problem, the repository emphasizes:

- numerical validation,
- convergence analysis,
- probability conservation,
- analytical and semi-analytical benchmarks,
- reproducible computational experiments,
- stationary versus time-dependent scattering comparisons.

---

## Research Questions

This project investigates several related questions in one-dimensional quantum mechanics:

1. How accurately can finite-difference methods reproduce known quantum energy spectra and eigenstates?
2. Does the numerical error exhibit the expected second-order spatial convergence?
3. How do finite barriers modify bound-state wavefunctions compared with ideal infinite confinement?
4. How does tunnelling couple states in a symmetric double well?
5. Can Crank-Nicolson propagation reproduce analytical free-wavepacket motion and spreading?
6. How do barrier width and barrier height affect quantum transmission?
7. Does direct time-dependent wavepacket scattering agree with stationary scattering theory after accounting for the packet's momentum distribution?

---

## Core Physics

The stationary Schrödinger equation is

\[
-\frac{\hbar^2}{2m}
\frac{d^2\psi(x)}{dx^2}

- # V(x)\psi(x)
  E\psi(x).
  \]

The time-dependent Schrödinger equation is

\[
i\hbar
\frac{\partial\psi(x,t)}{\partial t}
=
\left[
-\frac{\hbar^2}{2m}
\frac{\partial^2}{\partial x^2}

- V(x)
  \right]
  \psi(x,t).
  \]

Most numerical experiments use natural units,

\[
\hbar=1,
\qquad
m=1,
\]

while the implementation retains explicit mass and \(\hbar\) parameters.

---

# Scientific Capabilities

## Stationary Quantum Mechanics

The stationary solver constructs the finite-difference Hamiltonian

\[
H=T+V
\]

and solves

\[
H\psi_n=E_n\psi_n
\]

using sparse Hermitian eigenvalue methods.

Implemented stationary systems include:

- infinite square well,
- finite square well,
- harmonic oscillator,
- symmetric quartic double well,
- rectangular barrier scattering.

The solver supports:

- low-energy eigenvalue calculation,
- normalized eigenstates,
- probability densities,
- expectation values,
- uncertainty calculations,
- parity diagnostics,
- orthogonality checks,
- convergence analysis.

---

## Infinite Square Well

For a well of width \(L\), the analytical spectrum is

\[
E_n
=
\frac{
n^2\pi^2\hbar^2
}{
2mL^2
}.
\]

The infinite well is used as the primary finite-difference convergence benchmark.

The numerical calculation checks:

- analytical energy agreement,
- analytical wavefunction overlap,
- \(E_n\propto n^2\),
- normalization,
- boundary conditions,
- second-order convergence.

---

## Harmonic Oscillator

The potential is

\[
V(x)
=
\frac12m\omega^2x^2.
\]

The exact spectrum is

\[
E_n
=
\hbar\omega
\left(
n+\frac12
\right).
\]

The harmonic oscillator provides independent validation of:

- eigenvalues,
- equal level spacing,
- even/odd parity,
- expectation values,
- position uncertainty,
- momentum uncertainty,
- the Heisenberg relation.

For the ground state,

\[
\Delta x\Delta p
=
\frac{\hbar}{2}.
\]

### Numerical Stationary States

![Harmonic oscillator stationary states](results/figures/stationary/harmonic_oscillator_states.png)

### Energy Spectrum

![Harmonic oscillator energy levels](results/figures/stationary/harmonic_oscillator_energies.png)

### Ground-State Probability Density

![Harmonic oscillator ground-state probability density](results/figures/stationary/harmonic_oscillator_ground_density.png)

---

## Finite Square Well

The symmetric finite well is defined as

\[
V(x)
=
\begin{cases}
-V_0, & |x|\leq a,\\
0, & |x|>a.
\end{cases}
\]

Bound states satisfy

\[
-V_0<E<0.
\]

Unlike the infinite well, the wavefunction penetrates into the classically forbidden exterior region.

The numerical eigenvalues are compared with independent semi-analytical solutions of

\[
k\tan(ka)=\kappa
\]

for even states and

\[
-k\cot(ka)=\kappa
\]

for odd states, where

\[
k
=
\frac{\sqrt{2m(E+V_0)}}{\hbar}
\]

and

\[
\kappa
=
\frac{\sqrt{-2mE}}{\hbar}.
\]

---

## Symmetric Double Well

The double-well model is

\[
V(x)
=
a(x^2-b^2)^2.
\]

Its minima occur at

\[
x=\pm b,
\]

while the central barrier is

\[
V(0)=ab^4.
\]

The two lowest states form an even/odd pair separated by

\[
\Delta E=E_1-E_0.
\]

The project studies how this splitting changes as the barrier is increased within the quartic double-well family.

This provides a stationary-state manifestation of quantum tunnelling.

---

# Time-Dependent Quantum Mechanics

## Gaussian Wavepacket

The incident state used in the dynamics experiments is

\[
\psi(x,0)
=
\frac{1}{
(2\pi\sigma^2)^{1/4}
}
\exp
\left[
-\frac{(x-x_0)^2}{4\sigma^2}

- ik_0x
  \right].
  \]

For this convention,

\[
\langle x\rangle=x_0,
\]

\[
\langle p\rangle=\hbar k_0,
\]

\[
\Delta x=\sigma,
\]

and

\[
\Delta p=\frac{\hbar}{2\sigma}.
\]

The mean kinetic energy is

\[
\langle T\rangle
=
\frac{
(\hbar k_0)^2

- \left(
  \frac{\hbar}{2\sigma}
  \right)^2
  }{
  2m
  }.
  \]

  ***

## Crank-Nicolson Propagation

Time evolution is performed using

\[
\left(
I+
\frac{i\Delta tH}{2\hbar}
\right)
\psi^{n+1}
=
\left(
I-
\frac{i\Delta tH}{2\hbar}
\right)
\psi^n.
\]

For a time-independent Hermitian Hamiltonian, the corresponding Crank-Nicolson evolution operator is unitary in exact arithmetic.

The implementation therefore monitors

\[
\int|\psi(x,t)|^2dx
\]

throughout propagation.

The wavefunction is **not artificially renormalized after each time step**, allowing norm conservation to remain a numerical diagnostic.

---

## Free-Wavepacket Validation

Before studying scattering, the propagator is tested against analytical free-particle dynamics.

The expected packet center is

\[
x_c(t)
=
x_0+
\frac{\hbar k_0}{m}t,
\]

while its width evolves as

\[
\sigma_x(t)
=
\sigma_0
\sqrt{
1+
\left(
\frac{
\hbar t
}{
2m\sigma_0^2
}
\right)^2
}.
\]

This validates both translation and quantum dispersion.

---

# Quantum Tunnelling

The primary scattering experiment uses a rectangular barrier,

\[
V(x)
=
\begin{cases}
V_0, & x_L\leq x\leq x_R,\\
0, & \text{otherwise}.
\end{cases}
\]

For a monochromatic component with

\[
E<V_0,
\]

the decay constant inside the barrier is

\[
\kappa
=
\frac{
\sqrt{2m(V_0-E)}
}{
\hbar
}.
\]

The stationary transmission coefficient is

\[
T(E)
=
\left[
1+
\frac{
V_0^2\sinh^2(\kappa L)
}{
4E(V_0-E)
}
\right]^{-1}.
\]

Quantum mechanics therefore predicts

\[
T>0
\]

even for sub-barrier energies.

---

## Time-Dependent Tunnelling

The Gaussian packet is propagated directly toward the barrier.

During scattering, probability is divided into

\[
P_L,
\qquad
P_B,
\qquad
P_R,
\]

representing probability to the left of, inside, and to the right of the barrier.

Probability conservation requires

\[
P_L+P_B+P_R\approx1.
\]

After the reflected and transmitted components separate from the barrier,

\[
P_B\rightarrow0,
\]

allowing

\[
R\approx P_L
\]

and

\[
T\approx P_R.
\]

### Tunnelling Evolution

![Quantum tunnelling snapshots](results/figures/dynamics/tunnelling_snapshots.png)

### Regional Scattering Probabilities

![Scattering probabilities](results/figures/tunnelling/scattering_probabilities.png)

---

## Quantum Tunnelling Animation

The full time-dependent scattering simulation is exported directly from the numerical solver.

![Quantum tunnelling animation](results/animations/tunnelling/quantum_tunnelling.gif)

The animation provides a visual representation of the incident packet interacting with the barrier and separating into reflected and transmitted components.

The quantitative conclusions are obtained from the numerical probabilities rather than from the animation alone.

---

# Quantitative Tunnelling Study

A Gaussian packet contains a finite momentum distribution.

Therefore, comparing the TDSE result only with

\[
T(\langle E\rangle)
\]

would discard information about the packet's energy spread.

The project instead computes a packet-averaged stationary prediction,

\[
T*{\text{packet}}
=
\frac{
\int*{p>0}
P(p)T[E(p)]\,dp
}{
\int\_{p>0}
P(p)\,dp
}.
\]

This is compared directly with the asymptotic TDSE transmission.

---

## Transmission vs Barrier Width

The width scan investigates

\[
L\uparrow
\quad\Rightarrow\quad
T\downarrow.
\]

![Transmission versus barrier width](results/figures/tunnelling/transmission_vs_width.png)

For sufficiently strong tunnelling suppression,

\[
T\propto e^{-2\kappa L}.
\]

Therefore,

\[
\ln T
\]

should become approximately linear with barrier width in an appropriate regime.

![Log transmission versus barrier width](results/figures/tunnelling/log_transmission_vs_width.png)

Because the incident packet contains a range of energies, the fitted slope is not interpreted as exactly equal to a single monochromatic value of \(-2\kappa\).

---

## Transmission vs Barrier Height

Increasing the barrier height increases the decay constant for sub-barrier components,

\[
\kappa
=
\frac{
\sqrt{2m(V_0-E)}
}{
\hbar
}.
\]

Therefore,

\[
V_0\uparrow
\quad\Rightarrow\quad
T\downarrow.
\]

![Transmission versus barrier height](results/figures/tunnelling/transmission_vs_height.png)

---

## TDSE vs Stationary Scattering Theory

The time-dependent transmission is compared with the packet-averaged stationary prediction.

![TDSE versus stationary transmission](results/figures/validation/tdse_vs_stationary_transmission.png)

The comparison provides an independent validation because the two results are obtained using different numerical procedures:

\[
\text{real-space TDSE propagation}
\]

versus

\[
\text{momentum-space weighted stationary scattering}.
\]

---

# Numerical Method

## Spatial Discretization

The second derivative is approximated using

\[
\frac{d^2\psi}{dx^2}
\bigg|_{x_i}
\approx
\frac{
\psi_{i+1}

- 2\psi_i

* \psi\_{i-1}
  }{
  \Delta x^2
  }.
  \]

The leading truncation error is

\[
O(\Delta x^2).
\]

The resulting kinetic-energy matrix is tridiagonal and sparse.

---

## Sparse Hamiltonian

The Hamiltonian has the form

\[
H=T+V.
\]

The kinetic operator contributes the tridiagonal structure while the potential operator is diagonal.

This means the number of nonzero matrix entries grows approximately as

\[
O(N)
\]

rather than

\[
O(N^2).
\]

Sparse matrix representations are therefore used throughout the project.

---

## Stationary Eigensolver

Low-energy stationary states are computed using SciPy's sparse Hermitian eigensolver.

The solver calculates only the requested part of the spectrum rather than diagonalizing the complete dense Hamiltonian.

Numerical eigenvectors are then normalized using

\[
\sum_i
|\psi_i|^2\Delta x
=

1.  \]

---

# Validation Strategy

The project does not rely on a single validation test.

Numerical correctness is assessed using:

- Hamiltonian Hermiticity,
- wavefunction normalization,
- eigenstate orthogonality,
- infinite-well analytical energies,
- infinite-well analytical eigenfunctions,
- finite-difference convergence,
- harmonic-oscillator analytical energies,
- harmonic-oscillator parity,
- uncertainty relations,
- finite-well semi-analytical energies,
- finite-well exterior penetration,
- double-well parity,
- double-well energy splitting,
- analytical free-wavepacket dynamics,
- Crank-Nicolson probability conservation,
- scattering probability conservation,
- stationary versus TDSE transmission.

See:

```text
docs/validation.md
```

for the detailed validation methodology.

---

# Convergence Analysis

The finite-difference stencil is expected to have leading spatial error

\[
\epsilon
\propto
(\Delta x)^2.
\]

The project evaluates the infinite-well ground state using progressively finer grids:

\[
N=
100,\,
200,\,
400,\,
800,\,
1600,\, 3200.
\]

The observed convergence order is estimated from

\[
\log\epsilon
=
p\log\Delta x+C.
\]

A value near

\[
p\approx2
\]

is consistent with the expected second-order finite-difference method.

---

# Project Structure

```text
quantum-schrodinger-solver/
│
├── README.md
├── LICENSE
├── CITATION.cff
├── pyproject.toml
├── .gitignore
├── .python-version
│
├── docs/
│   ├── theory.md
│   ├── numerical_methods.md
│   ├── potentials.md
│   ├── validation.md
│   ├── time_dependent_solver.md
│   ├── tunnelling.md
│   └── references.md
│
├── src/
│   └── schrodinger/
│       ├── constants.py
│       ├── grid.py
│       ├── potentials.py
│       ├── hamiltonian.py
│       │
│       ├── stationary/
│       │   ├── analytic.py
│       │   ├── bound_states.py
│       │   ├── double_well.py
│       │   ├── finite_well_analytic.py
│       │   ├── observables.py
│       │   ├── solver.py
│       │   └── states.py
│       │
│       ├── time_dependent/
│       │   ├── crank_nicolson.py
│       │   ├── momentum_space.py
│       │   ├── propagation.py
│       │   ├── scattering.py
│       │   ├── tunnelling_validation.py
│       │   └── wavepacket.py
│       │
│       ├── analysis/
│       │   ├── convergence.py
│       │   ├── diagnostics.py
│       │   ├── double_well_splitting.py
│       │   ├── errors.py
│       │   ├── expectation.py
│       │   ├── normalization.py
│       │   ├── tunnelling.py
│       │   └── tunnelling_study.py
│       │
│       └── visualization/
│           ├── animation.py
│           ├── energy_levels.py
│           ├── probability.py
│           ├── stationary.py
│           ├── tunnelling.py
│           └── tunnelling_analysis.py
│
├── experiments/
│   ├── stationary/
│   └── dynamics/
│
├── notebooks/
│
├── tests/
│
├── configs/
│
├── results/
│   ├── figures/
│   ├── animations/
│   └── tables/
│
└── scripts/
    └── generate_all_figures.py
```

---

# Installation

## Requirements

The project currently targets:

```text
Python 3.13
```

Clone the repository:

```bash
git clone https://github.com/perciyaldhayalan/quantum-schrodinger-solver
cd quantum-schrodinger-solver
```

Create a virtual environment.

### Windows

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

Upgrade the packaging tools:

```bash
python -m pip install --upgrade pip setuptools wheel
```

Install the project and development dependencies:

```bash
pip install -e ".[dev]"
```

The exact dependency versions are defined in

```text
pyproject.toml
```

for reproducibility.

---

# Running the Tests

Run the complete test suite:

```bash
pytest -v
```

Run Ruff:

```bash
ruff check src tests experiments scripts
```

Run strict static type checking:

```bash
mypy src
```

A successful development validation should therefore pass:

```bash
ruff check src tests experiments scripts
mypy src
pytest -v
```

---

# Reproducing the Figures

Generate all scientific figures and the tunnelling animation with:

```bash
python scripts/generate_all_figures.py
```

The pipeline regenerates outputs under:

```text
results/figures/
results/animations/
```

This is intended to keep the visual results traceable to the actual numerical implementation.

---

# Running Individual Experiments

Examples include:

```bash
python experiments/stationary/infinite_well.py
```

```bash
python experiments/stationary/harmonic_oscillator.py
```

```bash
python experiments/stationary/finite_well.py
```

```bash
python experiments/stationary/double_well.py
```

```bash
python experiments/stationary/convergence_analysis.py
```

```bash
python experiments/dynamics/quantum_tunnelling_validation.py
```

```bash
python experiments/dynamics/tunnelling_parameter_study.py
```

```bash
python experiments/dynamics/generate_tunnelling_animation.py
```

---

# Configuration

Reproducible experiment parameters are stored under

```text
configs/
```

including configurations for:

- infinite square well,
- finite square well,
- harmonic oscillator,
- double well,
- double-well splitting,
- convergence analysis,
- barrier scattering,
- quantum tunnelling,
- tunnelling parameter studies.

The separation of configuration from solver implementation makes parameter choices explicit and easier to reproduce.

---

# Documentation

Detailed scientific documentation is available under `docs/`.

### Theory

```text
docs/theory.md
```

Introduces the Schrödinger equation, observables, uncertainty, bound states, wavepackets, and tunnelling.

### Potential Models

```text
docs/potentials.md
```

Documents the physical potentials and their numerical interpretation.

### Numerical Methods

```text
docs/numerical_methods.md
```

Describes finite differences, sparse Hamiltonians, eigenvalue calculations, numerical normalization, and convergence.

### Time-Dependent Solver

```text
docs/time_dependent_solver.md
```

Derives the Crank-Nicolson propagation scheme and discusses numerical accuracy and probability conservation.

### Validation

```text
docs/validation.md
```

Documents analytical benchmarks and the validation hierarchy.

### Quantum Tunnelling

```text
docs/tunnelling.md
```

Describes the complete stationary and time-dependent tunnelling study.

### References

```text
docs/references.md
```

Lists the physics and numerical-computing references used by the project.

---

# Numerical Limitations

The current solver intentionally focuses on transparent one-dimensional numerical physics.

Current limitations include:

- one spatial dimension,
- non-relativistic quantum mechanics,
- single-particle systems,
- uniform spatial grids,
- second-order finite differences,
- finite computational domains,
- Dirichlet boundary conditions,
- time-independent external potentials,
- no absorbing boundary conditions,
- no adaptive spatial or temporal grids.

Discontinuous potentials also have a finite-grid representation error of order related to the spatial resolution.

---

# Future Extensions

Potential extensions include:

- higher-order finite differences,
- absorbing boundary conditions,
- complex absorbing potentials,
- split-operator Fourier propagation,
- explicitly time-dependent potentials,
- Gaussian barriers,
- potential steps,
- asymmetric barriers,
- multiple barriers,
- resonant tunnelling,
- periodic potentials,
- two-dimensional Schrödinger dynamics.

The existing architecture keeps a location for a future split-operator implementation so that an alternative propagation method can be compared with Crank-Nicolson.

---

# Scientific Reproducibility

The project follows the workflow

\[
\text{theory}
\rightarrow
\text{numerical method}
\rightarrow
\text{implementation}
\rightarrow
\text{automated tests}
\rightarrow
\text{experiment}
\rightarrow
\text{result}
\rightarrow
\text{validation}.
\]

Core solver logic is kept under

```text
src/schrodinger/
```

rather than being embedded exclusively in notebooks.

Experiments are separated from reusable numerical methods, while generated outputs are stored under `results/`.

This structure is intended to make the computational results inspectable and reproducible.

---

# License

This project is released under the MIT License.

See:

```text
LICENSE
```

for details.

---

# Author

**Perciyal D**

Computational Physics / Scientific Python Portfolio Project

GitHub: [perciyaldhayalan](https://github.com/perciyaldhayalan/)

---

## Citation

Citation metadata for this project is provided in:

```text
CITATION.cff
```

If this repository is used as a reference for computational work, please cite the repository using the metadata provided there.
