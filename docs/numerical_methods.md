# Numerical Methods

## 1. Overview

The one-dimensional Schrödinger equation is converted into a finite-dimensional numerical problem by discretizing position on a uniform grid.

The stationary problem becomes a sparse matrix eigenvalue problem,

\[
H\boldsymbol{\psi}\_n
=
E_n\boldsymbol{\psi}\_n,
\]

while the time-dependent problem becomes a sequence of sparse linear solves.

The principal numerical methods used in this project are:

- second-order central finite differences,
- sparse matrix representations,
- sparse Hermitian eigensolvers,
- Crank-Nicolson time propagation,
- numerical normalization and quadrature,
- convergence analysis against analytical reference solutions.

Unless otherwise specified, calculations use natural units,

\[
\hbar=1,
\qquad
m=1.
\]

The implementation nevertheless retains explicit \(\hbar\) and mass parameters.

---

## 2. Spatial Grid

Consider the finite computational domain

\[
x*{\min}
\leq
x
\leq
x*{\max}.
\]

It is divided into \(N\) uniformly spaced grid points,

\[
x*i
=
x*{\min}

- i\Delta x,
  \]

where

\[
i=0,1,\ldots,N-1
\]

and

\[
\Delta x
=
\frac{
x*{\max}-x*{\min}
}{
N-1
}.
\]

The numerical wavefunction is represented by the vector

\[
\boldsymbol{\psi}
=
\begin{bmatrix}
\psi*0 &
\psi_1 &
\cdots &
\psi*{N-1}
\end{bmatrix}^{T}.
\]

For the real-space solver, Dirichlet boundary conditions are imposed:

\[
\psi*0
=
\psi*{N-1}
= 0.
\]

Therefore, the Hamiltonian is constructed on the \(N-2\) interior points.

---

## 3. Second Derivative

The second spatial derivative is approximated using the second-order central finite-difference formula,

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

The truncation error is

\[
O(\Delta x^2).
\]

This approximation is the basis of the discretized kinetic-energy operator.

---

## 4. Discrete Kinetic-Energy Operator

The continuous kinetic-energy operator is

\[
\hat{T}
=
-\frac{\hbar^2}{2m}
\frac{d^2}{dx^2}.
\]

Applying the central finite difference gives

\[
\hat{T}\psi*i
\approx
-\frac{\hbar^2}{2m\Delta x^2}
\left(
\psi*{i+1}

- 2\psi_i

* \psi\_{i-1}
  \right).
  \]

Rearranging,

\[
\hat{T}\psi_i
\approx
\frac{\hbar^2}{m\Delta x^2}
\psi_i

- \frac{\hbar^2}{2m\Delta x^2}
  \psi\_{i-1}
- \frac{\hbar^2}{2m\Delta x^2}
  \psi\_{i+1}.
  \]

The matrix representation is therefore tridiagonal:

\[
T
=
\frac{\hbar^2}{
2m\Delta x^2
}
\begin{bmatrix}
2 & -1 & 0 & \cdots & 0 \\
-1 & 2 & -1 & \ddots & \vdots \\
0 & -1 & 2 & \ddots & 0 \\
\vdots & \ddots & \ddots & \ddots & -1 \\
0 & \cdots & 0 & -1 & 2
\end{bmatrix}.
\]

The tridiagonal structure is sparse and symmetric.

---

## 5. Discrete Potential Operator

The potential-energy operator acts multiplicatively,

\[
\hat{V}\psi(x)
=
V(x)\psi(x).
\]

On the grid it becomes a diagonal matrix,

\[
V
=
\begin{bmatrix}
V(x*1) & 0 & \cdots & 0 \\
0 & V(x_2) & \cdots & 0 \\
\vdots & \vdots & \ddots & \vdots \\
0 & 0 & \cdots & V(x*{N-2})
\end{bmatrix}.
\]

Only the interior grid values are used in the Hamiltonian.

---

## 6. Discrete Hamiltonian

The numerical Hamiltonian is

\[
H
=
T+V.
\]

Its diagonal entries are

\[
H\_{ii}
=
\frac{\hbar^2}{
m\Delta x^2
}

- V(x_i),
  \]

and its nearest-neighbour entries are

\[
H\_{i,i\pm1}
=
-\frac{\hbar^2}{
2m\Delta x^2
}.
\]

All other entries vanish.

The resulting matrix is sparse and Hermitian for real-valued potentials:

\[
H^{\dagger}
=
H.
\]

The implementation checks this property as a numerical diagnostic.

---

## 7. Sparse Representation

A dense matrix representation would store approximately

\[
(N-2)^2
\]

matrix elements even though almost all of them are zero.

The finite-difference Hamiltonian contains only the main diagonal and two neighbouring diagonals.

Therefore, the number of nonzero elements grows approximately linearly with grid size,

\[
O(N),
\]

rather than quadratically.

Sparse storage is consequently used throughout the solver.

This is particularly important for fine grids and repeated time propagation.

---

## 8. Stationary Eigenvalue Problem

The stationary Schrödinger equation becomes

\[
H\boldsymbol{\psi}\_n
=
E_n\boldsymbol{\psi}\_n.
\]

For many physical applications only the lowest few eigenstates are required.

The project therefore uses a sparse Hermitian eigensolver rather than computing the complete spectrum of the Hamiltonian.

The requested low-energy eigenpairs are computed numerically and then ordered such that

\[
E_0<E_1<E_2<\cdots.
\]

After solving on the interior grid, zero-valued boundary points are restored to the wavefunction.

---

## 9. Eigenvector Sign Ambiguity

If

\[
H\psi
=
E\psi,
\]

then

\[
H(-\psi)
=
E(-\psi).
\]

Therefore, the overall sign of a real eigenvector is physically irrelevant.

Numerical eigensolvers are not required to return a deterministic sign.

For this reason, validation should not generally compare numerical and analytical eigenfunctions point by point with a fixed sign assumption.

Instead, comparisons can use quantities such as

\[
\left|
\langle
\psi*{\text{exact}}
|
\psi*{\text{numerical}}
\rangle
\right|,
\]

probability densities, or parity.

---

## 10. Numerical Normalization

A continuous normalized state satisfies

\[
\int
|\psi(x)|^2\,dx
=

1.  \]

On a uniform grid, the project evaluates the discrete approximation

\[
\sum_i
|\psi_i|^2
\Delta x
\approx

1.  \]

A numerical eigenvector returned by a matrix eigensolver is normally normalized according to the Euclidean vector norm,

\[
\sum_i|\psi_i|^2=1,
\]

which is not identical to continuous spatial normalization.

Therefore, eigenvectors are explicitly normalized using the spatial integration measure \(\Delta x\).

---

## 11. Numerical Expectation Values

Expectation values are evaluated using

\[
\langle A\rangle
=
\int
\psi^\*
\hat{A}\psi\,dx.
\]

On the grid,

\[
\langle A\rangle
\approx
\sum_i
\psi_i^\*
(\hat{A}\psi)\_i
\Delta x.
\]

For the position operator,

\[
(\hat{x}\psi)\_i
=
x_i\psi_i.
\]

For momentum,

\[
\hat{p}
=
-i\hbar
\frac{d}{dx},
\]

the first derivative is approximated in the interior by

\[
\frac{d\psi}{dx}
\bigg|_{x_i}
\approx
\frac{
\psi_{i+1}-\psi\_{i-1}
}{
2\Delta x
}.
\]

Thus,

\[
(\hat{p}\psi)_i
\approx
-i\hbar
\frac{
\psi_{i+1}-\psi\_{i-1}
}{
2\Delta x
}.
\]

The squared momentum operator uses the same second derivative employed in the Hamiltonian:

\[
(\hat{p}^2\psi)_i
\approx
-\hbar^2
\frac{
\psi_{i+1}

- 2\psi_i

* \psi\_{i-1}
  }{
  \Delta x^2
  }.
  \]

For Dirichlet-boundary calculations, momentum-squared expectation values are evaluated consistently on the interior numerical domain.

---

## 12. Numerical Error

Several independent sources of numerical error are present.

### Spatial discretization

The central finite-difference approximation has leading error

\[
O(\Delta x^2).
\]

Reducing \(\Delta x\) should therefore reduce errors quadratically when the solution is sufficiently smooth and other errors are negligible.

### Finite computational domain

Systems defined analytically on

\[
-\infty<x<\infty
\]

must be truncated to a finite numerical interval.

The domain must be large enough that the wavefunction is negligible at the boundaries.

### Discontinuous potentials

Square wells and rectangular barriers contain abrupt discontinuities.

Their representation on a discrete grid can introduce additional errors associated with the precise grid locations assigned to the discontinuity.

### Floating-point error

Finite-precision arithmetic introduces small roundoff errors, particularly in long calculations or quantities obtained from subtracting nearly equal values.

---

## 13. Relative and Absolute Error

When an analytical reference value \(Q\_{\text{exact}}\) is known, the absolute error is

\[
\epsilon*{\text{abs}}
=
\left|
Q*{\text{numerical}}

- Q\_{\text{exact}}
  \right|.
  \]

For nonzero reference values, the relative error is

\[
\epsilon*{\text{rel}}
=
\frac{
\left|
Q*{\text{numerical}}

- Q*{\text{exact}}
  \right|
  }{
  |Q*{\text{exact}}|
  }.
  \]

These measures are used for eigenvalue validation and convergence studies.

---

## 14. Convergence Analysis

A numerical result should approach the continuum solution as

\[
\Delta x\rightarrow0.
\]

For the second-order finite-difference method, a sufficiently smooth problem is expected to exhibit

\[
\epsilon
\propto
(\Delta x)^2.
\]

Taking logarithms,

\[
\log\epsilon
=
p\log\Delta x

- C,
  \]

where \(p\) is the observed convergence order.

A linear fit of

\[
\log\epsilon
\]

against

\[
\log\Delta x
\]

therefore provides an estimate of \(p\).

For the infinite square well energy calculation, the expected asymptotic value is approximately

\[
p\approx2.
\]

The project evaluates convergence using increasingly fine grids rather than relying on a single resolution.

---

## 15. Analytical Validation

Numerical correctness is tested against several known results.

### Infinite square well

\[
E_n
=
\frac{
n^2\pi^2\hbar^2
}{
2mL^2
}.
\]

### Harmonic oscillator

\[
E_n
=
\hbar\omega
\left(
n+\frac12
\right).
\]

### Finite square well

Semi-analytical bound-state energies are obtained from the even and odd transcendental matching conditions.

### Free Gaussian wavepacket

The numerical propagation is compared with analytical center motion and spreading.

### Rectangular barrier

Numerical time-dependent transmission is compared with stationary scattering theory after accounting for the finite momentum distribution of the incident packet.

These independent checks reduce the likelihood that agreement in one experiment results from a compensating implementation error.

---

## 16. Numerical Validation Philosophy

A successful numerical calculation requires more than producing a visually plausible plot.

The project therefore checks combinations of:

- normalization,
- orthogonality,
- Hermiticity,
- analytical eigenvalues,
- parity,
- uncertainty relations,
- convergence order,
- probability conservation,
- stationary scattering theory,
- time-dependent scattering probabilities.

Agreement across physically independent diagnostics provides stronger evidence of numerical correctness than any individual test.

---

## 17. Limitations

The current finite-difference formulation is intentionally straightforward and physically transparent.

It is not necessarily the most efficient method for every quantum-mechanical problem.

Limitations include:

- second-order spatial accuracy,
- uniform grids,
- finite computational domains,
- simple Dirichlet boundaries,
- possible reflections from domain boundaries,
- grid sensitivity near discontinuous potentials,
- increasing computational cost at very fine spatial resolution.

Possible future extensions include higher-order finite differences, nonuniform grids, absorbing boundary conditions, spectral methods, and alternative propagation algorithms.
