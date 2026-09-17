# Quantum Tunnelling Study

## 1. Research Question

The tunnelling component of this project investigates the question:

> How does the transmission probability of a finite-width quantum wavepacket depend on the width and height of a rectangular potential barrier, and how closely does direct time-dependent propagation agree with stationary scattering theory?

The study combines:

- analytical rectangular-barrier transmission,
- Gaussian momentum distributions,
- Crank-Nicolson TDSE propagation,
- asymptotic reflection and transmission measurements,
- systematic barrier-parameter scans.

The objective is to treat quantum tunnelling quantitatively rather than only visualize a wavepacket crossing a barrier.

---

## 2. Physical System

The scattering potential is

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

The barrier width is

\[
L=x_R-x_L.
\]

For the centered barriers used in the parameter study,

\[
x_L=-\frac{L}{2},
\qquad
x_R=\frac{L}{2}.
\]

The incident particle is represented by a Gaussian wavepacket initially positioned to the left of the barrier and travelling toward positive \(x\).

---

## 3. Incident Gaussian Wavepacket

The initial state is

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

Its mean position is

\[
\langle x\rangle=x_0,
\]

and its mean momentum is

\[
\langle p\rangle=\hbar k_0.
\]

For this Gaussian convention,

\[
\Delta x=\sigma
\]

and

\[
\Delta p=\frac{\hbar}{2\sigma}.
\]

Therefore,

\[
\Delta x\Delta p=\frac{\hbar}{2}.
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

The principal tunnelling experiments select barriers whose heights exceed the packet's mean kinetic energy.

---

## 4. Meaning of Sub-Barrier Tunnelling

For a classical particle with a definite energy,

\[
E<V_0
\]

implies zero transmission through the barrier.

Quantum mechanics predicts a different result.

For a stationary quantum state with

\[
E<V_0,
\]

the wavefunction penetrates into the classically forbidden region and can emerge on the opposite side with nonzero probability.

A Gaussian wavepacket introduces an additional consideration because it does not contain a single momentum or energy.

Instead, it contains a distribution of momentum components.

Therefore,

\[
\langle T\rangle<V_0
\]

does not imply that every spectral component satisfies

\[
E<V_0.
\]

The packet can contain a small high-energy tail.

For this reason, the simulations are described as having **sub-barrier mean energy** rather than claiming that every spectral component lies below the barrier.

This distinction is important when comparing time-dependent propagation with stationary scattering theory.

---

## 5. Stationary Tunnelling Theory

For a monochromatic component with

\[
E<V_0,
\]

define the decay constant

\[
\kappa
=
\frac{
\sqrt{2m(V_0-E)}
}{
\hbar
}.
\]

Inside the classically forbidden barrier, the stationary wavefunction contains exponentially decaying components of the form

\[
\psi(x)\sim e^{-\kappa x}.
\]

For a rectangular barrier of width \(L\), the exact stationary transmission coefficient is

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

This expression gives

\[
T>0
\]

even when

\[
E<V_0.
\]

This nonzero sub-barrier transmission is the central stationary signature of quantum tunnelling.

---

## 6. Strong-Barrier Approximation

For a sufficiently wide or high barrier,

\[
\kappa L\gg1.
\]

In this regime,

\[
\sinh(\kappa L)
\]

grows approximately exponentially.

The dominant transmission dependence becomes

\[
T\propto e^{-2\kappa L}.
\]

Taking the logarithm gives

\[
\ln T
\approx
-2\kappa L+C.
\]

Therefore, an approximately linear relationship between

\[
\ln T
\]

and barrier width is expected in an appropriate deep-tunnelling regime.

The project generates a logarithmic transmission-versus-width plot to investigate this behavior numerically.

---

## 7. Above-Barrier Scattering

The Gaussian packet contains a range of energies, so the stationary calculation must also handle components satisfying

\[
E>V_0.
\]

For these components, define

\[
q
=
\frac{
\sqrt{2m(E-V_0)}
}{
\hbar
}.
\]

The transmission coefficient becomes

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

Even above the barrier, transmission need not equal unity because quantum waves can reflect at potential discontinuities.

The implementation therefore supports both the sub-barrier and above-barrier regimes.

---

## 8. Threshold Energy

At

\[
E=V_0,
\]

the usual sub-barrier and above-barrier formulas contain expressions that require taking a limit.

The implementation uses the corresponding threshold expression,

\[
T(E=V_0)
=
\left[
1+
\frac{
mV_0L^2
}{
2\hbar^2
}
\right]^{-1}.
\]

Handling this case separately avoids numerical singularities near the barrier threshold.

---

## 9. Time-Dependent Schrödinger Equation

The wavepacket evolves according to

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

The project propagates this equation using the Crank-Nicolson method.

For one time step,

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

The sparse left-hand matrix is factorized once and reused throughout the propagation when the Hamiltonian is time independent.

No artificial wavefunction renormalization is performed after each time step.

---

## 10. Probability Conservation

For unitary quantum evolution,

\[
\int
|\psi(x,t)|^2dx
=
1
\]

for all times if the initial state is normalized.

The numerical equivalent is

\[
P\_{\text{total}}(t)
\approx
\sum_i
|\psi_i(t)|^2
\Delta x.
\]

Probability conservation is monitored directly during propagation.

The wavefunction is intentionally not renormalized at every step because doing so could conceal numerical errors in the propagator.

---

## 11. Spatial Probability Regions

During scattering, the computational domain is divided into three regions.

The probability to the left of the barrier is

\[
P*L(t)
=
\int*{x<x_L}
|\psi(x,t)|^2dx.
\]

The probability inside the barrier is

\[
P*B(t)
=
\int*{x_L\leq x\leq x_R}
|\psi(x,t)|^2dx.
\]

The probability to the right of the barrier is

\[
P*R(t)
=
\int*{x>x_R}
|\psi(x,t)|^2dx.
\]

The total probability satisfies

\[
P_L+P_B+P_R
\approx

1.  \]

These quantities allow the scattering process to be followed continuously in time.

---

## 12. Before the Collision

Initially, the Gaussian packet is positioned well to the left of the barrier.

Therefore,

\[
P_L\approx1,
\]

while

\[
P_B\approx0
\]

and

\[
P_R\approx0.
\]

The packet then travels toward positive \(x\) with mean momentum

\[
\langle p\rangle=\hbar k_0.
\]

---

## 13. Barrier Interaction

When the packet reaches the barrier, part of its probability density enters the barrier region.

During this stage,

\[
P_B>0.
\]

The wavefunction also develops reflected and transmitted components.

However, during the interaction it is not yet appropriate to identify

\[
P_L
\]

and

\[
P_R
\]

as the final reflection and transmission probabilities because the wavefunction is still interacting with the barrier.

---

## 14. Asymptotic Scattering

After sufficient propagation time, the reflected and transmitted packets move away from the barrier.

The probability remaining inside the barrier becomes small:

\[
P_B\rightarrow0.
\]

The asymptotic reflection probability can then be identified as

\[
R\approx P_L,
\]

and the transmission probability as

\[
T\approx P_R.
\]

Probability conservation requires

\[
R+T\approx1.
\]

The implementation uses a barrier-probability tolerance to determine whether the packet has sufficiently separated from the interaction region.

A small value of \(P_B\) alone is not sufficient to prove that scattering has occurred, because \(P_B\) is also small before the incident packet reaches the barrier.

The simulation time and initial packet position therefore provide the additional physical context needed when extracting asymptotic scattering probabilities.

---

## 15. Momentum-Space Distribution

A Gaussian wavepacket is not monochromatic.

Its momentum-space wavefunction is obtained using a discrete Fourier transform.

The momentum probability distribution is denoted by

\[
P(p).
\]

Each momentum component corresponds to kinetic energy

\[
E(p)
=
\frac{p^2}{2m}.
\]

Consequently, each component experiences a different stationary barrier transmission coefficient,

\[
T[E(p)].
\]

This is why the complete momentum distribution must be considered when comparing the finite-width packet with stationary scattering theory.

---

## 16. Positive-Momentum Components

The initial packet is constructed to travel toward positive \(x\).

The incoming part of the momentum distribution therefore corresponds primarily to

\[
p>0.
\]

The packet-averaged stationary prediction is calculated using these positive-momentum components.

This avoids including components travelling away from the barrier in the incoming transmission reference.

---

## 17. Packet-Averaged Stationary Transmission

The stationary prediction appropriate for the Gaussian packet is

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

The denominator normalizes the positive-momentum portion of the distribution.

This quantity is more physically appropriate than simply calculating

\[
T(\langle E\rangle).
\]

Evaluating the transmission coefficient only at the mean energy would ignore the finite energy spread of the wavepacket.

---

## 18. Independent Transmission Calculations

Transmission is therefore calculated using two independent approaches.

### Time-dependent calculation

After asymptotic separation,

\[
T*{\text{TDSE}}
=
P_R(t*{\text{final}}).
\]

### Stationary calculation

The packet-weighted theoretical prediction is

\[
T*{\text{stationary}}
=
T*{\text{packet}}.
\]

The disagreement is measured using

\[
\Delta T
=
\left|
T\_{\text{TDSE}}

- T\_{\text{stationary}}
  \right|.
  \]

Agreement between these independently implemented approaches provides an important validation of the scattering calculation.

---

## 19. Barrier-Width Study

The first systematic tunnelling study varies barrier width while holding barrier height fixed.

The configured widths are

\[
L=
0.50,\,
0.75,\,
1.00,\,
1.25,\,
1.50.
\]

The fixed barrier height is

\[
V_0=5
\]

in the natural-unit experiment.

The expected physical trend is

\[
L\uparrow
\quad\Rightarrow\quad
T\downarrow.
\]

A wider classically forbidden region produces stronger attenuation of the wavefunction.

Both

\[
T\_{\text{TDSE}}
\]

and

\[
T\_{\text{stationary}}
\]

are evaluated for every width.

The resulting figure is generated at

```text
results/figures/tunnelling/transmission_vs_width.png
```

---

## 20. Logarithmic Width Analysis

The same width-dependent transmission results are also analyzed using

\[
\ln T.
\]

For deep tunnelling,

\[
T\propto e^{-2\kappa L},
\]

so

\[
\ln T
\]

should become approximately linear in \(L\).

The generated figure is

```text
results/figures/tunnelling/log_transmission_vs_width.png
```

A linear fit is included as a numerical diagnostic.

The fitted slope should not be interpreted as exactly

\[
-2\kappa
\]

for one fixed energy because the Gaussian packet contains a distribution of energies.

Furthermore, the exact rectangular-barrier expression is not purely exponential over every barrier regime.

---

## 21. Barrier-Height Study

The second systematic study keeps the barrier width fixed while varying the barrier height.

The configured heights are

\[
V_0=
3,\,
4,\,
5,\,
6,\, 7.
\]

The fixed width is

\[
L=1.
\]

The expected trend is

\[
V_0\uparrow
\quad\Rightarrow\quad
T\downarrow.
\]

For a monochromatic sub-barrier component,

\[
\kappa
=
\frac{
\sqrt{2m(V_0-E)}
}{
\hbar
}.
\]

Increasing \(V_0\) therefore increases \(\kappa\), causing the wavefunction to decay more strongly inside the barrier.

The generated result is

```text
results/figures/tunnelling/transmission_vs_height.png
```

---

## 22. TDSE Versus Stationary Theory

The width and height scans provide multiple pairs of

\[
T\_{\text{stationary}}
\]

and

\[
T\_{\text{TDSE}}.
\]

These values are displayed against the reference relationship

\[
T*{\text{TDSE}}
=
T*{\text{stationary}}.
\]

The generated comparison figure is

```text
results/figures/validation/tdse_vs_stationary_transmission.png
```

Points close to the diagonal indicate agreement between the stationary scattering calculation and direct TDSE propagation.

This comparison is one of the strongest quantitative validation results in the project because the two transmission estimates are obtained through substantially different numerical procedures.

---

## 23. Tunnelling Snapshots

The time-dependent probability density is visualized at selected stages of the scattering process.

The generated figure is

```text
results/figures/dynamics/tunnelling_snapshots.png
```

The snapshots illustrate the progression

\[
\text{incident packet}
\rightarrow
\text{barrier interaction}
\rightarrow
\text{reflected + transmitted packets}.
\]

The barrier is displayed spatially on the same figure.

Because potential energy and probability density have different physical units, the displayed barrier height is rescaled for visualization.

The actual value of \(V_0\) remains identified in the figure.

---

## 24. Regional Probability Evolution

The quantities

\[
P_L(t),
\qquad
P_B(t),
\qquad
P_R(t)
\]

are plotted throughout the simulation.

The generated figure is

```text
results/figures/tunnelling/scattering_probabilities.png
```

This visualization shows how probability moves between the incident, interaction, reflected, and transmitted regions.

It also provides a visual check that the probability is redistributed rather than created or destroyed.

---

## 25. Quantum Tunnelling Animation

The complete scattering process is exported as an animation:

```text
results/animations/tunnelling/quantum_tunnelling.gif
```

The animation displays the evolving probability density

\[
|\psi(x,t)|^2
\]

together with the barrier and the regional probabilities.

The animation provides an intuitive representation of the tunnelling process, but it is not used as the sole evidence for tunnelling.

The quantitative conclusions are based on the calculated reflection and transmission probabilities and their comparison with stationary scattering theory.

---

## 26. Discrete Barrier Representation

The analytical rectangular barrier has exactly defined boundaries.

On the numerical grid, the barrier is represented at grid points satisfying

\[
x_L\leq x_i\leq x_R.
\]

As a result, the effective discrete barrier width can differ slightly from the requested continuous width.

The discrepancy is of order

\[
\Delta x.
\]

This effect can contribute to differences between the continuous stationary transmission formula and the finite-grid TDSE result.

Increasing spatial resolution reduces this representation error.

---

## 27. Spatial Resolution

The TDSE calculation uses a second-order finite-difference Hamiltonian.

The spatial truncation error for sufficiently smooth wavefunctions is therefore approximately

\[
O(\Delta x^2).
\]

The discontinuous rectangular barrier can introduce additional grid sensitivity near its boundaries.

Consequently, agreement with continuous stationary theory should be interpreted within the spatial resolution of the simulation.

---

## 28. Time-Step Resolution

Crank-Nicolson is second-order accurate in time.

Therefore, temporal discretization error decreases approximately as

\[
O(\Delta t^2)
\]

in the appropriate convergence regime.

Although Crank-Nicolson preserves norm for a Hermitian time-independent Hamiltonian in exact arithmetic, probability conservation alone does not guarantee that the chosen time step resolves the wavefunction phase accurately.

Both spatial and temporal resolution matter when evaluating scattering accuracy.

---

## 29. Boundary Effects

The real-space solver uses Dirichlet boundaries.

These boundaries behave as numerical reflecting walls.

If the transmitted or reflected packet reaches a computational boundary, it can reflect back toward the barrier and contaminate the scattering measurement.

The simulations therefore use a sufficiently large domain and stop before significant boundary reflection occurs.

Future versions could use absorbing boundary conditions or complex absorbing potentials.

---

## 30. Sources of TDSE-Theory Difference

Residual disagreement between

\[
T\_{\text{TDSE}}
\]

and

\[
T\_{\text{stationary}}
\]

can result from several sources:

- finite spatial resolution,
- finite time-step resolution,
- discrete representation of the barrier width,
- finite computational boundaries,
- incomplete asymptotic separation,
- momentum-space discretization,
- finite momentum resolution,
- numerical quadrature,
- floating-point arithmetic.

Therefore, the two calculations are expected to agree within numerical accuracy rather than produce exactly identical values.

---

## 31. Interpretation of the Width Scan

The width scan tests one of the defining characteristics of quantum tunnelling.

As the barrier becomes wider,

\[
L\uparrow,
\]

the wavefunction must penetrate through a larger classically forbidden region.

The transmission probability therefore decreases:

\[
T\downarrow.
\]

In an appropriate deep-tunnelling regime, the suppression approaches an exponential dependence.

This provides a quantitative connection between the numerical simulation and the analytical form of evanescent-wave decay.

---

## 32. Interpretation of the Height Scan

Increasing barrier height increases the difference

\[
V_0-E
\]

for sub-barrier components.

Therefore,

\[
\kappa
=
\frac{
\sqrt{2m(V_0-E)}
}{
\hbar
}
\]

increases.

The characteristic penetration length

\[
\frac{1}{\kappa}
\]

decreases.

Consequently, increasing barrier height suppresses transmission.

The TDSE and stationary calculations are both expected to reproduce this behavior.

---

## 33. Main Physical Conclusions

The tunnelling study is designed to establish several related results.

First, quantum mechanics permits

\[
T>0
\]

for incident components whose energy lies below the barrier.

Second, increasing barrier width suppresses transmission:

\[
L\uparrow
\quad\Rightarrow\quad
T\downarrow.
\]

Third, increasing barrier height suppresses transmission:

\[
V_0\uparrow
\quad\Rightarrow\quad
T\downarrow.
\]

Fourth, the tunnelling probability can exhibit approximately exponential dependence on barrier width in an appropriate regime.

Fifth, the time-dependent transmission probability can be quantitatively compared with stationary scattering theory when the finite momentum distribution of the incident packet is taken into account.

These results demonstrate quantum tunnelling as both a visual wave phenomenon and a quantitatively testable scattering process.

---

## 34. Reproducing the Tunnelling Study

The quantitative tunnelling parameter study is implemented in

```text
experiments/dynamics/tunnelling_parameter_study.py
```

The tunnelling visualization experiment is implemented in

```text
experiments/dynamics/generate_tunnelling_figures.py
```

The quantitative analysis figures are generated by

```text
experiments/dynamics/generate_tunnelling_analysis_figures.py
```

The animation is generated by

```text
experiments/dynamics/generate_tunnelling_animation.py
```

The complete scientific visualization pipeline can be run using

```bash
python scripts/generate_all_figures.py
```

The automated test suite can be run using

```bash
pytest -v
```

Static checks can be performed with

```bash
ruff check src tests experiments scripts
```

and

```bash
mypy src
```

---

## 35. Reproducibility Principle

The figures and animation stored in the repository are outputs of the numerical implementation.

They are not intended to be manually edited representations of expected quantum behavior.

A user should be able to reproduce the results from the source code and experiment configuration.

This allows the scientific claims to be inspected through:

\[
\text{source code}
\rightarrow
\text{numerical experiment}
\rightarrow
\text{result}
\rightarrow
\text{validation}.
\]

---

## 36. Possible Extensions

The current rectangular-barrier study provides a foundation for more advanced quantum-scattering experiments.

Possible extensions include:

- transmission convergence with respect to \(\Delta x\),
- transmission convergence with respect to \(\Delta t\),
- narrower momentum distributions approaching monochromatic scattering,
- Gaussian barriers,
- asymmetric barriers,
- potential steps,
- multiple barriers,
- double-barrier resonant tunnelling,
- periodic potentials,
- complex absorbing potentials,
- absorbing boundary layers,
- explicitly time-dependent barriers,
- split-operator Fourier propagation,
- two-dimensional tunnelling.

A particularly useful future extension would be resonant tunnelling through a double-barrier system, where transmission can become strongly enhanced at specific energies.
