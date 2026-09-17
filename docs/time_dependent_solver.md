# Time-Dependent Schrödinger Solver

## 1. Overview

The time-dependent component of this project solves

\[
i\hbar
\frac{\partial\psi(x,t)}{\partial t}
=
\hat{H}\psi(x,t)
\]

for one-dimensional quantum systems.

The primary numerical propagator is the Crank-Nicolson method.

This method is particularly useful for quantum dynamics because it treats the Hamiltonian implicitly and preserves the norm for a time-independent Hermitian Hamiltonian up to numerical solution and floating-point error.

The implementation is used for:

- free Gaussian wavepacket propagation,
- wavepacket spreading,
- rectangular-barrier scattering,
- reflection,
- transmission,
- quantum tunnelling,
- parameter-dependent tunnelling studies.

---

## 2. Semi-Discrete Schrödinger Equation

After spatial finite-difference discretization, the wavefunction becomes a vector

\[
\boldsymbol{\psi}(t).
\]

The TDSE becomes

\[
i\hbar
\frac{d\boldsymbol{\psi}}{dt}
=
H\boldsymbol{\psi},
\]

where \(H\) is the sparse finite-difference Hamiltonian.

For a time-independent Hamiltonian, the exact evolution over one time step is

\[
\boldsymbol{\psi}(t+\Delta t)
=
e^{-iH\Delta t/\hbar}
\boldsymbol{\psi}(t).
\]

Directly evaluating the matrix exponential at every step is unnecessary for the systems considered here.

---

## 3. Crank-Nicolson Discretization

The Crank-Nicolson method averages the Hamiltonian action between the current and next time levels.

Starting from

\[
i\hbar
\frac{
\boldsymbol{\psi}^{n+1}

- \boldsymbol{\psi}^{n}
  }{
  \Delta t
  }
  =
  \frac12
  H
  \left(
  \boldsymbol{\psi}^{n+1}

* \boldsymbol{\psi}^{n}
  \right),
  \]

multiply by

\[
\frac{\Delta t}{i\hbar}.
\]

Rearranging gives

\[
\left(
I

- \frac{
  i\Delta t
  }{
  2\hbar
  }
  H
  \right)
  \boldsymbol{\psi}^{n+1}
  =
  \left(
  I

* \frac{
  i\Delta t
  }{
  2\hbar
  }
  H
  \right)
  \boldsymbol{\psi}^{n}.
  \]

Define

\[
A
=
I

- \frac{
  i\Delta t
  }{
  2\hbar
  }
  H
  \]

and

\[
B
=
I

- \frac{
  i\Delta t
  }{
  2\hbar
  }
  H.
  \]

Then each time step satisfies

\[
A\boldsymbol{\psi}^{n+1}
=
B\boldsymbol{\psi}^{n}.
\]

Therefore,

\[
\boldsymbol{\psi}^{n+1}
=
A^{-1}
B\boldsymbol{\psi}^{n}.
\]

The implementation does not explicitly form \(A^{-1}\). Instead, it solves the sparse linear system.

---

## 4. Crank-Nicolson Evolution Operator

The numerical one-step evolution operator is

\[
U\_{\text{CN}}
=
\left(
I+
\frac{i\Delta tH}{2\hbar}
\right)^{-1}
\left(
I-
\frac{i\Delta tH}{2\hbar}
\right).
\]

This is the Cayley transform of the Hamiltonian.

For Hermitian \(H\),

\[
H^\dagger=H.
\]

The corresponding Crank-Nicolson evolution operator is unitary in exact arithmetic,

\[
U*{\text{CN}}^\dagger
U*{\text{CN}}
=
I.
\]

Therefore,

\[
\|\boldsymbol{\psi}^{n+1}\|
=
\|\boldsymbol{\psi}^{n}\|.
\]

This makes probability conservation a particularly strong validation criterion for the propagator.

---

## 5. Probability Conservation

The total probability is

\[
P(t)
=
\int
|\psi(x,t)|^2\,dx.
\]

For unitary evolution,

\[
P(t)
=
P(0).
\]

The numerical calculation evaluates

\[
P_n
\approx
\sum_i
|\psi_i^n|^2
\Delta x.
\]

A well-resolved Crank-Nicolson simulation should maintain

\[
P_n\approx1
\]

for a normalized initial state.

The implementation does not renormalize the wavefunction after every time step.

Artificial renormalization would conceal errors in the propagation algorithm.

Instead, norm conservation is measured directly.

---

## 6. Sparse Linear Solution

At every time step,

\[
A\boldsymbol{\psi}^{n+1}
=
B\boldsymbol{\psi}^{n}
\]

must be solved.

For a time-independent potential, the Hamiltonian does not change with time.

Therefore, the matrix

\[
A
=
I+
\frac{i\Delta tH}{2\hbar}
\]

also remains unchanged.

The implementation factorizes \(A\) once during propagator initialization.

The stored factorization is then reused for every subsequent time step.

This avoids repeatedly factorizing the same sparse matrix and substantially reduces the computational cost of long simulations.

---

## 7. Boundary Conditions

The real-space TDSE solver uses Dirichlet boundaries,

\[
\psi(x*{\min},t)
=
\psi(x*{\max},t)
= 0.
\]

The propagated numerical vector corresponds to the interior points.

After propagation, the full wavefunction representation restores zero values at both boundaries.

These boundaries behave as hard numerical walls.

Therefore, a propagating wavepacket can eventually reflect from them.

Simulation domains and final times must be selected so that boundary reflections do not contaminate the physical process being studied.

---

## 8. Gaussian Initial State

The primary incident state is

\[
\psi(x,0)
=
\frac{1}{
(2\pi\sigma^2)^{1/4}
}
\exp
\left[
-\frac{
(x-x_0)^2
}{
4\sigma^2
}

- ik_0x
  \right].
  \]

Its probability density is

\[
|\psi(x,0)|^2
=
\frac{1}{
\sqrt{2\pi\sigma^2}
}
\exp
\left[
-\frac{
(x-x_0)^2
}{
2\sigma^2
}
\right].
\]

Therefore,

\[
\langle x\rangle=x_0
\]

and

\[
\Delta x=\sigma.
\]

The mean momentum is

\[
\langle p\rangle
=
\hbar k_0,
\]

with

\[
\Delta p
=
\frac{\hbar}{2\sigma}.
\]

---

## 9. Mean Kinetic Energy

Because the Gaussian packet has finite momentum width, its mean kinetic energy is not simply

\[
\frac{
(\hbar k_0)^2
}{
2m
}.
\]

Instead,

\[
\langle p^2\rangle
=
(\hbar k_0)^2

- \left(
  \frac{\hbar}{2\sigma}
  \right)^2.
  \]

Therefore,

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

This distinction matters when describing an incident packet as being below a tunnelling barrier.

---

## 10. Free-Particle Validation

For

\[
V(x)=0,
\]

the packet center evolves as

\[
x_c(t)
=
x_0

- \frac{
  \hbar k_0
  }{
  m
  }t.
  \]

Its mean momentum remains constant,

\[
\langle p\rangle
=
\hbar k_0.
\]

The Gaussian width evolves according to

\[
\sigma_x(t)
=
\sigma
\sqrt{
1+
\left(
\frac{
\hbar t
}{
2m\sigma^2
}
\right)^2
}.
\]

These exact results provide a direct time-dependent validation of the numerical propagator.

A correct simulation must reproduce both translational motion and quantum dispersion.

---

## 11. Rectangular-Barrier Scattering

The time-dependent tunnelling experiment uses

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
\text{otherwise}.
\end{cases}
\]

The incident Gaussian begins sufficiently far to the left of the barrier and travels toward positive \(x\).

During the interaction, the packet develops reflected and transmitted components.

The spatial probability is divided into three regions:

\[
P*L(t)
=
\int*{x<x_L}
|\psi(x,t)|^2\,dx,
\]

\[
P*B(t)
=
\int*{x_L\leq x\leq x_R}
|\psi(x,t)|^2\,dx,
\]

and

\[
P*R(t)
=
\int*{x>x_R}
|\psi(x,t)|^2\,dx.
\]

Probability conservation requires

\[
P_L+P_B+P_R
\approx1.
\]

---

## 12. Interaction and Asymptotic Regimes

During collision with the barrier,

\[
P_B
\]

can be significant.

It is therefore incorrect to identify

\[
P_L
\]

and

\[
P_R
\]

immediately as the final reflection and transmission coefficients.

The asymptotic interpretation is made only after the reflected and transmitted packets have moved away from the barrier and

\[
P_B
\]

has become sufficiently small.

Then,

\[
R\approx P_L
\]

and

\[
T\approx P_R.
\]

The numerical analysis includes a barrier-probability tolerance to identify this separated regime.

---

## 13. Stationary Rectangular-Barrier Reference

For a monochromatic component with energy

\[
E<V_0,
\]

define

\[
\kappa
=
\frac{
\sqrt{
2m(V_0-E)
}
}{
\hbar
}.
\]

The exact stationary transmission coefficient is

\[
T(E)
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

For

\[
E>V_0,
\]

define

\[
q
=
\frac{
\sqrt{
2m(E-V_0)
}
}{
\hbar
}.
\]

Then,

\[
T(E)
=
\left[
1+
\frac{
V_0^2
\sin^2(qL)
}{
4E(E-V_0)
}
\right]^{-1}.
\]

The threshold

\[
E=V_0
\]

is treated using the corresponding limiting expression.

---

## 14. Momentum-Space Representation

The incident Gaussian contains a distribution of wave numbers.

A discrete Fourier transform is used to obtain its momentum-space representation.

For momentum

\[
p=\hbar k,
\]

the momentum probability density describes the relative weight of different incident energy components.

Each component has energy

\[
E(p)
=
\frac{p^2}{2m}.
\]

This distribution is essential for quantitative comparison between a finite-width wavepacket and stationary scattering theory.

---

## 15. Packet-Averaged Transmission

A Gaussian wavepacket is not monochromatic.

Therefore, its TDSE transmission probability should not generally be compared only with the stationary coefficient evaluated at its mean energy.

Instead, the project evaluates a positive-momentum-weighted stationary prediction,

\[
T*{\text{packet}}
=
\frac{
\int*{p>0}
P(p)
T[E(p)]\,dp
}{
\int\_{p>0}
P(p)\,dp
}.
\]

The denominator accounts for the probability contained in the incoming positive-momentum portion of the packet.

This provides a more physically meaningful stationary reference for the time-dependent calculation.

---

## 16. Quantitative Tunnelling Validation

The tunnelling study compares

\[
T\_{\text{TDSE}}
\]

obtained from asymptotic wavepacket propagation with

\[
T\_{\text{packet}}
\]

obtained from the momentum-averaged stationary calculation.

The comparison tests whether two independent formulations of the same scattering physics agree:

1. direct real-space time evolution,
2. stationary transmission weighted over the packet's momentum spectrum.

Agreement provides stronger validation than comparing the TDSE result only with qualitative expectations.

---

## 17. Barrier-Width Dependence

For sub-barrier energy,

\[
E<V_0,
\]

the wavefunction decays inside the barrier approximately as

\[
e^{-\kappa x}.
\]

In the strong-barrier limit, transmission behaves approximately as

\[
T
\propto
e^{-2\kappa L}.
\]

Therefore,

\[
\ln T
\approx
-2\kappa L+C.
\]

The numerical parameter study tests the expected suppression of transmission as barrier width increases.

Because the incident packet contains a range of energies, a fitted slope from the wavepacket calculation should not be interpreted as exactly equal to a single monochromatic value of

\[
-2\kappa.
\]

---

## 18. Barrier-Height Dependence

At fixed width, increasing \(V_0\) increases the classically forbidden energy difference

\[
V_0-E.
\]

For a monochromatic sub-barrier component,

\[
\kappa
=
\frac{
\sqrt{
2m(V_0-E)
}
}{
\hbar
}
\]

therefore increases.

The wavefunction decays more rapidly inside the barrier and transmission decreases.

The project verifies this trend using both TDSE propagation and packet-averaged stationary theory.

---

## 19. Time-Step Accuracy

Crank-Nicolson is second-order accurate in time.

Its local discretization is based on averaging the Hamiltonian between adjacent time levels.

For sufficiently smooth evolution, reducing

\[
\Delta t
\]

reduces temporal discretization error.

Although Crank-Nicolson is norm-preserving for a Hermitian time-independent Hamiltonian in exact arithmetic, norm conservation alone does not guarantee that a chosen time step resolves the dynamics accurately.

A simulation can preserve probability while still having phase or dispersion errors if the temporal or spatial resolution is inadequate.

---

## 20. Spatial Accuracy

The propagator uses the same second-order spatial Hamiltonian as the stationary solver.

Therefore, spatial discretization introduces an error of approximately

\[
O(\Delta x^2)
\]

for sufficiently smooth wavefunctions and potentials.

Discontinuous barriers can introduce additional grid-representation effects.

Both

\[
\Delta x
\]

and

\[
\Delta t
\]

must therefore be considered when assessing time-dependent accuracy.

---

## 21. Boundary Reflections

Dirichlet boundaries are not absorbing.

If a reflected or transmitted packet reaches a computational boundary, it can reflect back into the simulation.

Such a reflection is numerical rather than part of the intended barrier-scattering experiment.

The tunnelling experiments therefore use:

- sufficiently large spatial domains,
- initial packets positioned away from the boundaries,
- final times chosen before significant boundary contamination.

Future extensions could introduce absorbing boundary layers or complex absorbing potentials.

---

## 22. Why the Wavefunction Is Not Renormalized

After each numerical step it would be possible to replace

\[
\psi
\rightarrow
\frac{\psi}{
\sqrt{
\int|\psi|^2dx
}
}.
\]

This project intentionally avoids that procedure during propagation.

Crank-Nicolson should conserve probability naturally for the systems considered.

Renormalizing at every step could hide:

- implementation errors,
- incorrect matrix construction,
- unstable numerical behavior,
- accumulated solver error.

The norm is therefore treated as a diagnostic rather than forcibly corrected.

---

## 23. Numerical Diagnostics

The time-dependent solver is evaluated using several independent diagnostics:

- total probability conservation,
- zero Dirichlet boundary values,
- free-particle center motion,
- Gaussian wavepacket spreading,
- mean momentum behavior,
- reflected probability,
- transmitted probability,
- barrier-region probability,
- asymptotic separation,
- comparison with stationary scattering theory.

These checks test both mathematical correctness and physical behavior.

---

## 24. Computational Workflow

A typical time-dependent simulation follows the sequence

\[
\text{grid}
\rightarrow
\text{potential}
\rightarrow
\text{initial wavepacket}
\rightarrow
\text{Hamiltonian}
\rightarrow
\text{Crank-Nicolson propagator}
\rightarrow
\text{time evolution}
\rightarrow
\text{diagnostics}
\rightarrow
\text{physical analysis}.
\]

Snapshots are stored at selected intervals rather than necessarily retaining every propagated time step.

This supports analysis and visualization while controlling memory usage.

---

## 25. Limitations

The current time-dependent solver is designed for transparent one-dimensional computational experiments rather than large-scale production simulations.

Current limitations include:

- one spatial dimension,
- time-independent external potentials,
- uniform spatial grids,
- second-order finite differences,
- Dirichlet boundaries,
- no absorbing boundary conditions,
- no adaptive time stepping,
- no nonlinear interactions,
- no explicitly time-dependent Hamiltonians.

A split-operator Fourier module is reserved in the project architecture as a possible future propagation method.

Other extensions could include higher-order finite differences, complex absorbing potentials, time-dependent external fields, and multidimensional propagation.

---

## 26. Summary

The Crank-Nicolson solver provides a direct numerical realization of unitary quantum evolution on a finite spatial grid.

Its validity is assessed through more than visual inspection.

The implementation connects:

\[
\text{TDSE propagation}
\]

with

\[
\text{probability conservation},
\]

\[
\text{analytical free-particle dynamics},
\]

and

\[
\text{stationary scattering theory}.
\]

This combination allows the tunnelling simulations to be treated as quantitative computational-physics experiments rather than purely illustrative animations.
