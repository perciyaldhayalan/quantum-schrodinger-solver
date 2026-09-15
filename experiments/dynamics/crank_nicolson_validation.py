import numpy as np

from schrodinger.analysis.normalization import (
    probability_norm,
)
from schrodinger.grid import Grid1D
from schrodinger.time_dependent.crank_nicolson import (
    CrankNicolsonPropagator,
)
from schrodinger.time_dependent.wavepacket import (
    gaussian_wavepacket,
)


def main() -> None:
    grid = Grid1D(
        -30.0,
        30.0,
        3001,
    )

    potential = np.zeros(
        grid.interior_size,
        dtype=np.float64,
    )

    wavefunction = gaussian_wavepacket(
        grid=grid,
        center=-10.0,
        sigma=1.5,
        wave_number=2.0,
    )

    dt = 0.001
    steps = 500

    propagator = CrankNicolsonPropagator(
        grid=grid,
        potential=potential,
        dt=dt,
        mass=1.0,
        hbar=1.0,
    )

    initial_norm = probability_norm(
        wavefunction=wavefunction,
        dx=grid.dx,
    )

    final_state = propagator.propagate(
        wavefunction=wavefunction,
        steps=steps,
    )

    final_norm = probability_norm(
        wavefunction=final_state,
        dx=grid.dx,
    )

    norm_drift = abs(
        final_norm
        - initial_norm
    )

    print(
        "Crank-Nicolson Validation"
    )
    print(
        "--------------------------------"
    )

    print(
        f"Grid points: {grid.size}"
    )

    print(
        f"dx: {grid.dx:.8f}"
    )

    print(
        f"dt: {dt:.8f}"
    )

    print(
        f"Steps: {steps}"
    )

    print(
        f"Final time: "
        f"{dt * steps:.8f}"
    )

    print()

    print(
        f"Initial norm: "
        f"{initial_norm:.12f}"
    )

    print(
        f"Final norm:   "
        f"{final_norm:.12f}"
    )

    print(
        f"Norm drift:   "
        f"{norm_drift:.3e}"
    )

    if norm_drift > 1e-9:
        raise RuntimeError(
            "Crank-Nicolson probability "
            "conservation check failed."
        )


if __name__ == "__main__":
    main()