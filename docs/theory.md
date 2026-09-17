# Quantum-Mechanical Theory

## 1. Overview

This project studies the numerical solution of the one-dimensional Schrödinger equation for bound states, wavepacket dynamics, and quantum tunnelling.

The central objective is to connect numerical solutions directly with the underlying quantum mechanics. Stationary eigenvalue calculations are validated against systems with known analytical solutions, while time-dependent simulations are checked through probability conservation, wavepacket dynamics, and comparison with stationary scattering theory.

Unless otherwise specified, the numerical experiments use natural units,

\[
\hbar = 1,
\qquad
m = 1,
\]

which simplify the equations while preserving their physical structure.

---

## 2. Quantum State and Wavefunction

The state of a one-dimensional quantum particle is represented in position space by a wavefunction

\[
\psi(x,t).
\]

The corresponding probability density is

\[
\rho(x,t)
=
|\psi(x,t)|^2
=
\psi^\*(x,t)\psi(x,t).
\]

For a normalized state,

\[
\int\_{-\infty}^{\infty}
|\psi(x,t)|^2\,dx
=

1.  \]

This normalization condition expresses conservation of total probability.

For numerical calculations on a finite domain,

\[
x*{\min}\leq x\leq x*{\max},
\]

the corresponding condition becomes

\[
\int*{x*{\min}}^{x\_{\max}}
|\psi(x,t)|^2\,dx
\approx
1,
\]

provided that negligible probability reaches the computational boundaries.

---

## 3. Time-Independent Schrödinger Equation

For a particle of mass \(m\) moving in a time-independent potential \(V(x)\), stationary states satisfy

\[
\hat{H}\psi_n(x)
=
E_n\psi_n(x),
\]

where the Hamiltonian operator is

\[
\hat{H}
=
-\frac{\hbar^2}{2m}
\frac{d^2}{dx^2}

- V(x).
  \]

Therefore,

\[
-\frac{\hbar^2}{2m}
\frac{d^2\psi_n}{dx^2}

- # V(x)\psi_n
  E_n\psi_n.
  \]

The quantities \(E_n\) are the allowed energy eigenvalues and \(\psi_n(x)\) are the corresponding eigenfunctions.

For bound systems the energies form a discrete spectrum,

\[
E_0<E_1<E_2<\cdots.
\]

The eigenstates of a Hermitian Hamiltonian can be chosen orthonormal:

\[
\int
\psi*m^\*(x)\psi_n(x)\,dx
=
\delta*{mn}.
\]

---

## 4. Hamiltonian and Hermiticity

The Hamiltonian represents the total energy,

\[
\hat{H}
=
\hat{T}

- \hat{V},
  \]

where

\[
\hat{T}
=
-\frac{\hbar^2}{2m}
\frac{d^2}{dx^2}
\]

is the kinetic-energy operator and

\[
\hat{V}
=
V(x)
\]

is the potential-energy operator.

Physical observables correspond to Hermitian operators. Consequently,

\[
\hat{H}^{\dagger}
=
\hat{H},
\]

and its eigenvalues are real.

Hermiticity also provides an important numerical diagnostic. The discretized Hamiltonian should remain Hermitian to numerical precision.

---

## 5. Expectation Values

For an observable represented by an operator \(\hat{A}\), its expectation value is

\[
\langle A\rangle
=
\int
\psi^\*(x)
\hat{A}
\psi(x)\,dx.
\]

The position expectation value is

\[
\langle x\rangle
=
\int
x|\psi(x)|^2\,dx,
\]

while

\[
\langle x^2\rangle
=
\int
x^2|\psi(x)|^2\,dx.
\]

The position uncertainty is

\[
\Delta x
=
\sqrt{
\langle x^2\rangle

- \langle x\rangle^2
  }.
  \]

  ***

## 6. Momentum Operator

In the position representation,

\[
\hat{p}
=
-i\hbar
\frac{d}{dx}.
\]

Therefore,

\[
\langle p\rangle
=
\int
\psi^\*
\left(
-i\hbar
\frac{d}{dx}
\right)
\psi\,dx.
\]

The squared momentum operator is

\[
\hat{p}^2
=
-\hbar^2
\frac{d^2}{dx^2}.
\]

Thus,

\[
\langle p^2\rangle
=
\int
\psi^\*
\left(
-\hbar^2
\frac{d^2}{dx^2}
\right)
\psi\,dx.
\]

The momentum uncertainty is

\[
\Delta p
=
\sqrt{
\langle p^2\rangle

- \langle p\rangle^2
  }.
  \]

  ***

## 7. Heisenberg Uncertainty Relation

Position and momentum satisfy

\[
\Delta x\Delta p
\geq
\frac{\hbar}{2}.
\]

This relation is not caused by numerical uncertainty. It is a fundamental property of quantum states arising from the noncommutativity of position and momentum,

\[
[\hat{x},\hat{p}]
=
i\hbar.
\]

The Gaussian wavepacket used in this project approaches the minimum-uncertainty limit,

\[
\Delta x\Delta p
=
\frac{\hbar}{2},
\]

for its analytical initial state.

Finite-difference approximations introduce small numerical deviations from the exact value.

---

## 8. Infinite Square Well

For an infinite square well of width \(L\),

\[
V(x)
=
\begin{cases}
0,
&
0<x<L,
\\
\infty,
&
\text{otherwise}.
\end{cases}
\]

The wavefunction must vanish at the boundaries,

\[
\psi(0)
=
\psi(L)
= 0.
\]

The normalized eigenfunctions are

\[
\psi_n(x)
=
\sqrt{\frac{2}{L}}
\sin
\left(
\frac{n\pi x}{L}
\right),
\]

with

\[
n=1,2,3,\ldots.
\]

The exact energies are

\[
E_n
=
\frac{
n^2\pi^2\hbar^2
}{
2mL^2
}.
\]

Therefore,

\[
E_n\propto n^2.
\]

Because the exact solution is known, the infinite well provides a direct validation benchmark for the numerical eigensolver and finite-difference discretization.

---

## 9. Harmonic Oscillator

The harmonic oscillator potential is

\[
V(x)
=
\frac{1}{2}
m\omega^2x^2.
\]

Its exact energy spectrum is

\[
E_n
=
\hbar\omega
\left(
n+\frac{1}{2}
\right),
\]

where

\[
n=0,1,2,\ldots.
\]

Adjacent energy levels therefore satisfy

\[
E\_{n+1}-E_n
=
\hbar\omega.
\]

The ground state is even under spatial inversion,

\[
\psi_0(-x)
=
\psi_0(x),
\]

while the first excited state is odd,

\[
\psi_1(-x)
=
-\psi_1(x).
\]

For the ground state,

\[
\Delta x
=
\sqrt{
\frac{\hbar}{2m\omega}
},
\]

and

\[
\Delta p
=
\sqrt{
\frac{m\hbar\omega}{2}
}.
\]

Consequently,

\[
\Delta x\Delta p
=
\frac{\hbar}{2}.
\]

These analytical properties provide multiple independent checks of the numerical implementation.

---

## 10. Finite Square Well

A symmetric finite attractive well can be written as

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

where

\[
V_0>0.
\]

Bound states satisfy

\[
-V_0<E<0.
\]

Unlike the infinite well, the wavefunction does not vanish at the edges of the well. Instead, it penetrates into the classically forbidden exterior region and decays exponentially.

Inside the well,

\[
k
=
\frac{
\sqrt{2m(E+V_0)}
}{
\hbar
},
\]

while outside,

\[
\kappa
=
\frac{
\sqrt{-2mE}
}{
\hbar
}.
\]

For even states,

\[
k\tan(ka)
=
\kappa,
\]

and for odd states,

\[
-k\cot(ka)
=
\kappa.
\]

These transcendental equations provide semi-analytical reference energies for validation of the numerical finite-well solver.

---

## 11. Symmetric Double Well

The quartic double-well potential used in this project is

\[
V(x)
=
a(x^2-b^2)^2.
\]

Its minima occur at

\[
x=\pm b,
\]

and the central barrier has height

\[
V(0)
=
ab^4.
\]

Classically, sufficiently low-energy particles remain localized in one of the two wells.

Quantum mechanically, the wavefunction can penetrate the central barrier. The two lowest stationary states are approximately symmetric and antisymmetric combinations of states localized in the individual wells.

The corresponding energy splitting is

\[
\Delta E
=
E_1-E_0.
\]

Increasing the barrier within this family of potentials suppresses tunnelling and generally decreases the low-state energy splitting.

When the coefficient \(a\) is varied at fixed \(b\), both the central barrier and the local curvature of the wells change. Therefore, such a scan should be interpreted as a study within the quartic double-well family rather than as variation of an isolated barrier parameter.

---

## 12. Time-Dependent Schrödinger Equation

Quantum dynamics are governed by

\[
i\hbar
\frac{\partial\psi(x,t)}{\partial t}
=
\hat{H}\psi(x,t).
\]

For a time-independent Hamiltonian,

\[
i\hbar
\frac{\partial\psi}{\partial t}
=
\left[
-\frac{\hbar^2}{2m}
\frac{\partial^2}{\partial x^2}

- V(x)
  \right]
  \psi.
  \]

The formal solution is

\[
\psi(t)
=
e^{-i\hat{H}t/\hbar}
\psi(0).
\]

Because the exact exponential of a large discretized Hamiltonian is generally inconvenient to evaluate directly, numerical propagation methods are used.

This project uses the Crank-Nicolson method as its primary real-space time propagator.

---

## 13. Gaussian Wavepacket

The initial travelling state used in the time-dependent simulations is

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

Its initial position expectation value is

\[
\langle x\rangle
=
x_0,
\]

and its mean momentum is

\[
\langle p\rangle
=
\hbar k_0.
\]

For this convention,

\[
\Delta x
=
\sigma
\]

and

\[
\Delta p
=
\frac{\hbar}{2\sigma}.
\]

Therefore,

\[
\Delta x\Delta p
=
\frac{\hbar}{2}.
\]

The mean kinetic energy contains contributions from both the mean momentum and the finite momentum spread:

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

## 14. Free-Particle Wavepacket Motion

For a free particle,

\[
V(x)=0,
\]

the center of the Gaussian packet moves according to

\[
x_c(t)
=
x_0

- \frac{\hbar k_0}{m}t.
  \]

Its mean momentum remains constant,

\[
\langle p\rangle
=
\hbar k_0.
\]

The packet spreads with time according to

\[
\sigma_x(t)
=
\sigma
\sqrt{
1+
\left(
\frac{\hbar t}{
2m\sigma^2
}
\right)^2
}.
\]

These relations provide analytical validation of the time-dependent numerical propagator.

---

## 15. Quantum Tunnelling

Consider a rectangular barrier,

\[
V(x)
=
\begin{cases}
V_0,
&
|x|\leq L/2,
\\
0,
&
\text{otherwise}.
\end{cases}
\]

For a classical particle with

\[
E<V_0,
\]

transmission through the barrier is forbidden.

Quantum mechanics predicts a nonzero probability of transmission.

Inside the classically forbidden barrier region,

\[
\kappa
=
\frac{
\sqrt{2m(V_0-E)}
}{
\hbar
}.
\]

The wavefunction contains exponentially decaying components,

\[
\psi(x)
\sim
e^{-\kappa x}.
\]

For a rectangular barrier with \(E<V_0\), the exact stationary transmission coefficient is

\[
T
=
\left[
1+
\frac{
V_0^2
\sinh^2(\kappa L)
}{
4E(V_0-E)
}
\right]^{-1}.
\]

For sufficiently strong barriers, the dominant dependence is approximately

\[
T
\propto
e^{-2\kappa L}.
\]

Consequently,

\[
\ln T
\]

is approximately linear in barrier width in the deep-tunnelling regime.

---

## 16. Reflection and Transmission in Wavepacket Scattering

For a localized wavepacket interacting with a barrier, the spatial probability can be separated into left, barrier, and right regions:

\[
P*L
=
\int*{\text{left}}
|\psi(x,t)|^2\,dx,
\]

\[
P*B
=
\int*{\text{barrier}}
|\psi(x,t)|^2\,dx,
\]

and

\[
P*R
=
\int*{\text{right}}
|\psi(x,t)|^2\,dx.
\]

Probability conservation requires

\[
P_L+P_B+P_R
\approx

1.  \]

After the reflected and transmitted packets have separated spatially from the barrier,

\[
P_B\rightarrow 0.
\]

The asymptotic reflection and transmission probabilities can then be identified as

\[
R
\approx
P_L
\]

and

\[
T
\approx
P_R.
\]

Thus,

\[
R+T
\approx

1.  \]

---

## 17. Finite Momentum Width of the Incident Packet

A Gaussian wavepacket is not a single-energy stationary state.

Instead, it contains a distribution of momentum components,

\[
\tilde{\psi}(k).
\]

Each momentum component corresponds to a different energy and therefore experiences a different stationary transmission coefficient.

For this reason, comparing a time-dependent wavepacket transmission probability only with

\[
T(\langle E\rangle)
\]

is generally incomplete.

A more appropriate reference is a momentum-distribution-weighted stationary prediction,

\[
T*{\text{packet}}
=
\frac{
\int*{k>0}
P(k)T[E(k)]\,dk
}{
\int\_{k>0}
P(k)\,dk
}.
\]

This packet-averaged prediction is used when comparing stationary scattering theory with the full time-dependent simulation.

---

## 18. Interpretation of Sub-Barrier Wavepacket Tunnelling

When the mean kinetic energy satisfies

\[
\langle T\rangle<V_0,
\]

the incident packet is described as having sub-barrier mean energy.

However, a Gaussian packet has finite momentum width. It can therefore contain a small high-energy spectral tail with

\[
E>V_0.
\]

Consequently, the time-dependent transmission probability contains contributions from the full incident momentum distribution.

The momentum-averaged stationary calculation is used to account for this effect when quantitatively validating the tunnelling simulation.

---

## 19. Numerical Versus Physical Effects

Several effects observed in numerical simulations must be distinguished from physical quantum phenomena.

Physical effects include:

- wavepacket spreading,
- interference,
- tunnelling,
- reflection,
- bound-state penetration,
- parity,
- energy splitting,
- uncertainty.

Numerical effects include:

- finite spatial resolution,
- finite time step,
- finite computational boundaries,
- discretization error,
- representation of discontinuous potentials,
- accumulated floating-point error,
- boundary reflections when the simulation is run too long.

Validation and convergence studies are therefore essential for distinguishing physical conclusions from numerical artifacts.

---

## 20. Scope of the Model

The present solver considers one-dimensional, non-relativistic quantum mechanics.

The principal assumptions are:

- a single quantum particle,
- one spatial dimension,
- non-relativistic dynamics,
- prescribed external potentials,
- no particle-particle interactions,
- no spin degrees of freedom,
- no electromagnetic gauge fields,
- finite numerical domains,
- Dirichlet boundary conditions for the real-space solver.

Despite these simplifications, the model captures several fundamental quantum phenomena and provides a useful platform for studying eigenvalue problems, wavepacket dynamics, scattering, and tunnelling.
