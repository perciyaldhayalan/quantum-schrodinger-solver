# Potential-Energy Models

## 1. Overview

The potential-energy function \(V(x)\) defines the physical system described by the Schrödinger equation,

\[
\hat{H}
=
-\frac{\hbar^2}{2m}
\frac{d^2}{dx^2}

- V(x).
  \]

This project implements several one-dimensional potentials chosen to exercise different aspects of quantum mechanics and numerical computation.

The models include confined systems, analytically solvable reference systems, finite bound-state problems, coupled wells, and scattering barriers.

---

## 2. Infinite Square Well

The ideal infinite square well is

\[
V(x)
=
\begin{cases}
0,
&
x*{\min}<x<x*{\max},
\\
\infty,
&
\text{outside the well}.
\end{cases}
\]

Its width is

\[
L
=
x*{\max}-x*{\min}.
\]

The infinite exterior potential is not inserted directly into the numerical Hamiltonian.

Instead, confinement is represented through Dirichlet boundary conditions,

\[
\psi(x*{\min})
=
\psi(x*{\max})
= 0.
\]

The numerical Hamiltonian is therefore constructed only on the interior grid points, where

\[
V(x)=0.
\]

This avoids placing infinite floating-point values into the sparse Hamiltonian matrix.

### Physical purpose

The infinite well is primarily used for:

- validating numerical eigenvalues,
- validating eigenfunctions,
- testing normalization,
- testing boundary conditions,
- measuring finite-difference convergence.

Its exact spectrum makes it one of the strongest baseline tests in the project.

---

## 3. Finite Square Well

The symmetric finite square well is represented as

\[
V(x)
=
\begin{cases}
-V_0,
&
|x|\leq a,
\\
0,
&
|x|>a,
\end{cases}
\]

where \(V_0>0\).

The total width of the attractive region is

\[
L=2a.
\]

Bound states satisfy

\[
-V_0<E<0.
\]

Unlike the infinite well, finite-well eigenstates penetrate into the exterior classically forbidden region.

The exterior probability is therefore nonzero:

\[
P*{\text{outside}}
=
\int*{|x|>a}
|\psi(x)|^2\,dx

> 0.  \]

### Physical purpose

The finite well is used to study:

- finite confinement,
- exponentially decaying wavefunctions,
- bound-state counting,
- even and odd parity,
- semi-analytical transcendental equations,
- sensitivity to discontinuous potentials.

Because the potential is discontinuous, its numerical convergence behavior can differ from that of smooth potentials.

---

## 4. Harmonic Oscillator

The harmonic oscillator potential is

\[
V(x)
=
\frac{1}{2}
m\omega^2x^2.
\]

It is smooth, symmetric, and exactly solvable.

The energy spectrum is

\[
E_n
=
\hbar\omega
\left(
n+\frac{1}{2}
\right).
\]

### Physical purpose

The harmonic oscillator provides validation of:

- low-energy eigenvalues,
- equal energy spacing,
- wavefunction parity,
- expectation values,
- position uncertainty,
- momentum uncertainty,
- the Heisenberg uncertainty relation.

It is particularly useful because it tests the solver using a smooth potential rather than the discontinuous boundaries of square-well systems.

---

## 5. Quartic Double Well

The symmetric double-well potential is

\[
V(x)
=
a(x^2-b^2)^2,
\]

with

\[
a>0,
\qquad
b>0.
\]

The minima occur at

\[
x=\pm b.
\]

At these locations,

\[
V(\pm b)=0.
\]

The central barrier is located at

\[
x=0
\]

with height

\[
V(0)
=
ab^4.
\]

The potential is symmetric:

\[
V(-x)
=
V(x).
\]

Therefore, stationary eigenstates can be classified by parity.

### Low-energy states

The two lowest states are typically an even ground state and an odd first excited state.

Their energy difference,

\[
\Delta E
=
E_1-E_0,
\]

provides a measure of tunnelling-induced coupling between the two wells.

### Parameter interpretation

At fixed \(b\), increasing \(a\) increases the central barrier:

\[
V(0)=ab^4.
\]

However, it also changes the curvature near the minima,

\[
V''(\pm b)
=
8ab^2.
\]

Therefore, varying \(a\) does not change only the barrier height. It modifies the complete quartic potential.

The resulting splitting scan should consequently be interpreted as a parameter study within this particular double-well family.

---

## 6. Rectangular Barrier

A rectangular scattering barrier is represented by

\[
V(x)
=
\begin{cases}
V_0,
&
x_L\leq x\leq x_R,
\\
0,
&
\text{otherwise},
\end{cases}
\]

where

\[
V_0\geq0.
\]

The barrier width is

\[
L
=
x_R-x_L.
\]

For a centered barrier,

\[
x_L=-\frac{L}{2},
\qquad
x_R=\frac{L}{2}.
\]

### Sub-barrier regime

When

\[
E<V_0,
\]

the classical particle cannot cross the barrier.

The quantum wavefunction instead decays inside it with decay constant

\[
\kappa
=
\frac{
\sqrt{2m(V_0-E)}
}{
\hbar
}.
\]

The resulting transmission coefficient is nonzero.

### Above-barrier regime

When

\[
E>V_0,
\]

the wavefunction is oscillatory inside the barrier.

The internal wave number is

\[
q
=
\frac{
\sqrt{2m(E-V_0)}
}{
\hbar
}.
\]

Interference between waves reflected from the two barrier interfaces produces energy-dependent transmission.

### Physical purpose

The rectangular barrier is used for:

- stationary transmission calculations,
- quantum tunnelling,
- reflection and transmission analysis,
- barrier-width studies,
- barrier-height studies,
- time-dependent wavepacket scattering,
- comparison between stationary and TDSE calculations.

---

## 7. Discontinuous Potentials on a Finite Grid

Square wells and rectangular barriers contain abrupt discontinuities.

On a spatial grid, the barrier or well is represented only at discrete coordinates.

For example, a barrier may be assigned using the condition

\[
x_L\leq x_i\leq x_R.
\]

The effective discrete representation can therefore differ from the requested continuous width by an amount of order

\[
\Delta x.
\]

This effect becomes relevant when comparing high-accuracy numerical transmission results with exact continuous-barrier formulas.

Increasing spatial resolution reduces this representation error.

---

## 8. Potential Symmetry

Several potentials in this project satisfy

\[
V(-x)=V(x).
\]

For a symmetric one-dimensional Hamiltonian, the stationary eigenfunctions may be chosen to have definite parity.

Even states satisfy

\[
\psi(-x)=\psi(x),
\]

while odd states satisfy

\[
\psi(-x)=-\psi(x).
\]

Parity therefore provides an additional numerical validation criterion for:

- the harmonic oscillator,
- symmetric finite wells,
- symmetric double wells.

---

## 9. Natural Units

Most computational experiments use

\[
\hbar=1,
\qquad
m=1.
\]

Under these units, the stationary Schrödinger equation becomes

\[
-\frac{1}{2}
\frac{d^2\psi}{dx^2}

- # V(x)\psi
  E\psi.
  \]

The time-dependent equation becomes

\[
i
\frac{\partial\psi}{\partial t}
=
\left[
-\frac{1}{2}
\frac{\partial^2}{\partial x^2}

- V(x)
  \right]
  \psi.
  \]

Natural units simplify numerical experiments without changing the underlying mathematical relationships.

Explicit \(m\) and \(\hbar\) parameters remain part of the solver so that the numerical formulation is not fundamentally restricted to this convention.

---

## 10. Summary

The potential models serve different scientific roles.

| Potential            | Main Physical Problem     | Primary Validation                   |
| -------------------- | ------------------------- | ------------------------------------ |
| Infinite square well | Ideal confinement         | Exact eigenvalues and eigenfunctions |
| Finite square well   | Finite confinement        | Semi-analytical bound-state energies |
| Harmonic oscillator  | Smooth bound system       | Exact spectrum and uncertainty       |
| Double well          | Coupled localized states  | Parity and energy splitting          |
| Rectangular barrier  | Scattering and tunnelling | Analytical transmission coefficient  |

Together, these models provide a progression from exactly solvable bound-state systems to genuinely time-dependent scattering problems.
