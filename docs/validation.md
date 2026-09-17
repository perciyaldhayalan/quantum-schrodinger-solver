# Numerical Validation

## 1. Validation Strategy

A numerical Schrödinger solver should not be considered correct simply because its wavefunctions or animations appear physically reasonable.

This project validates the implementation using several independent tests:

1. comparison with exact analytical spectra,
2. comparison with analytical eigenfunctions,
3. normalization and orthogonality,
4. Hamiltonian Hermiticity,
5. parity of symmetric-system eigenstates,
6. finite-difference convergence,
7. expectation values and uncertainty relations,
8. semi-analytical finite-well calculations,
9. free-wavepacket analytical dynamics,
10. probability conservation during time propagation,
11. stationary versus time-dependent tunnelling calculations.

These tests examine different parts of the numerical implementation and reduce the possibility that an apparently correct result is produced by compensating numerical errors.

---

## 2. Infinite Square Well

The infinite square well provides the primary stationary-state benchmark.

For a well of width \(L\),

\[
E_n
=
\frac{
n^2\pi^2\hbar^2
}{
2mL^2
},
\qquad
n=1,2,\ldots
\]

and

\[
\psi_n(x)
=
\sqrt{\frac{2}{L}}
\sin
\left(
\frac{n\pi x}{L}
\right).
\]

The numerical solver is tested against both quantities.

### Energy validation

For each computed state,

\[
\epsilon*{\mathrm{rel}}
=
\frac{
|E*{\mathrm{num}}-E*{\mathrm{exact}}|
}{
|E*{\mathrm{exact}}|
}.
\]

The low-energy numerical eigenvalues should approach the analytical values as the spatial grid is refined.

The spectrum must also reproduce the characteristic scaling

\[
E_n\propto n^2.
\]

### Wavefunction validation

Because the overall sign of an eigenvector is arbitrary, direct signed point-by-point comparison is not used as the primary wavefunction test.

Instead, the numerical and analytical states can be compared through their overlap,

\[
\mathcal{O}\_n
=
\left|
\langle
\psi_n^{\mathrm{exact}}
|
\psi_n^{\mathrm{num}}
\rangle
\right|.
\]

A well-resolved numerical state should produce

\[
\mathcal{O}\_n\approx1.
\]

The boundary conditions are independently checked:

\[
\psi(x*{\min})
=
\psi(x*{\max})
= 0.
\]

---

## 3. Spatial Convergence

The central finite-difference approximation to the second derivative is

\[
\psi''(x*i)
=
\frac{
\psi*{i+1}

- 2\psi_i

* \psi\_{i-1}
  }{
  \Delta x^2
  }
* O(\Delta x^2).
  \]

Therefore, for sufficiently smooth solutions, the leading spatial discretization error is expected to scale as

\[
\epsilon
\propto
(\Delta x)^2.
\]

The infinite-well ground-state energy is evaluated on progressively finer grids.

The convergence experiment uses grid sizes

\[
N=
100,\,
200,\,
400,\,
800,\,
1600,\, 3200.
\]

For every resolution,

\[
\Delta x
=
\frac{
x*{\max}-x*{\min}
}{
N-1
}
\]

and the relative ground-state energy error is calculated.

The observed convergence order is estimated from

\[
\log\epsilon
=
p\log\Delta x+C.
\]

A slope near

\[
p=2
\]

is consistent with the expected second-order finite-difference discretization.

The convergence calculation is implemented in

```text
src/schrodinger/analysis/convergence.py
```
