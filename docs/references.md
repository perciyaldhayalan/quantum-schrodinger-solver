# References

## 1. Overview

This project combines standard results from one-dimensional quantum mechanics with numerical linear algebra, finite-difference discretization, sparse eigensolvers, Fourier transforms, and time-dependent propagation.

The references below provide the theoretical and computational background for the implemented methods.

---

## 2. Quantum Mechanics

### MIT OpenCourseWare — Quantum Physics I

Barton Zwiebach, _Quantum Physics I (8.04)_, Massachusetts Institute of Technology OpenCourseWare, Spring 2016.

Relevant topics include:

- wavefunctions and probability,
- normalization,
- wavepackets,
- momentum space,
- expectation values,
- Hermitian operators,
- uncertainty,
- stationary states,
- infinite square wells,
- finite square wells,
- harmonic oscillators,
- reflection and transmission,
- one-dimensional scattering.

Course materials:

https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/

Lecture notes:

https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/pages/lecture-notes/

---

## 3. Infinite and Finite Square Wells

The analytical infinite-well spectrum used for numerical validation is

\[
E_n
=
\frac{n^2\pi^2\hbar^2}{2mL^2}.
\]

The finite-well analysis uses the standard even- and odd-parity matching conditions for a symmetric finite square well.

A useful reference is:

Barton Zwiebach, _Quantum Physics I_, MIT OpenCourseWare, lectures on one-dimensional potentials.

Relevant material includes:

- infinite square-well energy eigenstates,
- symmetry of eigenfunctions,
- finite square-well setup,
- finite square-well bound states.

https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/pages/video-lectures/part-2/

---

## 4. Harmonic Oscillator

The exact harmonic-oscillator spectrum used for validation is

\[
E_n
=
\hbar\omega
\left(
n+\frac12
\right).
\]

The ground-state uncertainty relation provides an additional analytical benchmark,

\[
\Delta x\Delta p
=
\frac{\hbar}{2}.
\]

Reference:

Barton Zwiebach, _Quantum Physics I_, MIT OpenCourseWare.

The course develops the simple harmonic oscillator using both differential-equation and operator methods.

https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/

---

## 5. Wavepackets and Uncertainty

The time-dependent portion of the project uses Gaussian wavepackets and their momentum-space representation.

Relevant concepts include:

\[
\langle p\rangle=\hbar k_0,
\]

\[
\Delta x\Delta p\geq\frac{\hbar}{2},
\]

and free-wavepacket spreading.

Reference:

Barton Zwiebach, _Quantum Physics I_, MIT OpenCourseWare.

Relevant lecture material includes:

- wavepackets,
- uncertainty,
- time evolution,
- Fourier transforms,
- momentum expectation values.

https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/pages/lecture-notes/

---

## 6. Quantum Scattering and Tunnelling

The rectangular-barrier study uses standard one-dimensional scattering theory.

For sub-barrier energy,

\[
E<V_0,
\]

the decay constant is

\[
\kappa
=
\frac{\sqrt{2m(V_0-E)}}{\hbar}.
\]

The project studies reflection, transmission, barrier penetration, and wavepacket scattering.

Reference:

Barton Zwiebach, _Quantum Physics I_, MIT OpenCourseWare.

Relevant material includes:

- scattering states,
- reflection and transmission coefficients,
- wavepackets,
- classically forbidden regions,
- one-dimensional scattering,
- resonant transmission.

https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/pages/video-lectures/part-2/

---

## 7. Crank-Nicolson Method

The time-dependent Schrödinger solver uses the Crank-Nicolson discretization.

For

\[
i\hbar
\frac{\partial\psi}{\partial t}
=
H\psi,
\]

the implemented update is

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

The method originates from:

J. Crank and P. Nicolson,

_A Practical Method for Numerical Evaluation of Solutions of Partial Differential Equations of the Heat-Conduction Type_,

Proceedings of the Cambridge Philosophical Society, 43, 50–67, 1947.

The method was originally developed for diffusion-type partial differential equations. Its centered implicit structure is also widely used for the time-dependent Schrödinger equation.

---

## 8. Finite-Difference Method

The spatial Schrödinger equation is discretized using the second-order central approximation

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

Its leading truncation error is

\[
O(\Delta x^2).
\]

This discretization produces the tridiagonal kinetic-energy matrix used throughout the stationary and time-dependent solvers.

The observed convergence order is tested numerically rather than assumed solely from the formal stencil accuracy.

---

## 9. SciPy Sparse Linear Algebra

SciPy provides the sparse numerical linear-algebra routines used by the solver.

Documentation:

https://docs.scipy.org/doc/scipy/

### Sparse eigensolver

The stationary solver uses

```python
scipy.sparse.linalg.eigsh
```

to compute selected eigenvalues and eigenvectors of the sparse Hermitian Hamiltonian.

Documentation:

https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.eigsh.html

### Sparse LU factorization

The Crank-Nicolson implementation uses sparse factorization so that the time-independent left-hand propagation matrix can be factorized once and reused.

Relevant SciPy sparse linear-algebra documentation:

https://docs.scipy.org/doc/scipy/reference/sparse.linalg.html

---

## 10. NumPy

NumPy provides the numerical array operations used throughout the project.

Documentation:

https://numpy.org/doc/

Applications in this project include:

- numerical arrays,
- complex wavefunctions,
- vectorized potential evaluation,
- numerical integration support,
- linear fitting,
- Fourier transforms,
- momentum-space calculations.

---

## 11. Discrete Fourier Transform

The momentum-space wavefunction is obtained numerically using the discrete Fourier transform.

NumPy provides the FFT implementation through

```python
numpy.fft.fft
```

and related frequency utilities.

Documentation:

https://numpy.org/doc/stable/reference/generated/numpy.fft.fft.html

The FFT is used to transform the real-space wavepacket into momentum space so that the packet's finite momentum distribution can be included in the stationary transmission prediction.

---

## 12. Fast Fourier Transform Algorithm

The efficient FFT algorithm underlying standard numerical Fourier-transform implementations is historically associated with:

James W. Cooley and John W. Tukey,

_An Algorithm for the Machine Calculation of Complex Fourier Series_,

Mathematics of Computation, 19, 297–301, 1965.

This work describes the computational approach now commonly known as the Cooley-Tukey FFT algorithm.

---

## 13. Matplotlib

Matplotlib is used for scientific visualization.

Documentation:

https://matplotlib.org/stable/

The project uses Matplotlib for:

- stationary-state plots,
- energy-level diagrams,
- probability-density plots,
- tunnelling snapshots,
- scattering-probability plots,
- parameter studies,
- TDSE-versus-stationary comparisons,
- animations.

---

## 14. pandas

pandas is included in the scientific Python environment for structured numerical results and tabular analysis.

Documentation:

https://pandas.pydata.org/docs/

Potential uses include storing:

- eigenvalue comparisons,
- convergence results,
- tunnelling parameter scans,
- validation tables.

---

## 15. pytest

The numerical test suite is implemented with pytest.

Documentation:

https://docs.pytest.org/

Tests cover areas including:

- grid construction,
- potential functions,
- Hamiltonian construction,
- Hermiticity,
- stationary eigenstates,
- analytical validation,
- normalization,
- expectation values,
- convergence,
- finite-well bound states,
- double-well splitting,
- Crank-Nicolson propagation,
- probability conservation,
- scattering,
- tunnelling studies,
- scientific visualization.

---

## 16. Ruff

Ruff is used for Python linting and source-quality checks.

Documentation:

https://docs.astral.sh/ruff/

The repository uses Ruff to detect formatting-independent code-quality problems including import ordering and common Python issues.

---

## 17. mypy

mypy is used for static type checking.

Documentation:

https://mypy.readthedocs.io/

The project uses strict type checking for the main package under

```text
src/
```

to make numerical interfaces and array expectations more explicit.

---

## 18. JupyterLab

JupyterLab provides the notebook environment reserved for interactive validation, analysis, and presentation.

Documentation:

https://jupyterlab.readthedocs.io/

The project architecture keeps the primary numerical implementation under

```text
src/schrodinger/
```

rather than placing core solver logic inside notebooks.

This separation improves testing and reproducibility.

---

## 19. Software Versions

The project is developed against a pinned scientific Python environment.

The principal package versions are recorded in

```text
pyproject.toml
```

and should be treated as the authoritative source for the exact reproducible environment.

The repository currently targets Python 3.13.

---

## 20. Project Documentation

The theoretical and numerical discussion specific to this repository is divided across:

```text
docs/theory.md
docs/potentials.md
docs/numerical_methods.md
docs/time_dependent_solver.md
docs/validation.md
docs/tunnelling.md
```

These documents explain how the referenced physical and numerical methods are applied by the implementation.

---

## 21. Reproducibility

The complete automated test suite can be executed with

```bash
pytest -v
```

Static checks can be run using

```bash
ruff check src tests experiments scripts
```

and

```bash
mypy src
```

The generated scientific figures and animation can be reproduced with

```bash
python scripts/generate_all_figures.py
```

The goal is for the repository's numerical conclusions to remain traceable from theory and numerical method through source code, tests, experiments, and generated results.
