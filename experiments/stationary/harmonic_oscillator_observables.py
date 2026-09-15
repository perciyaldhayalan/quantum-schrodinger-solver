import numpy as np

from schrodinger.analysis.diagnostics import (
    satisfies_heisenberg,
)
from schrodinger.grid import Grid1D
from schrodinger.potentials import (
    harmonic_oscillator,
)
from schrodinger.stationary.observables import (
    calculate_observables,
)
from schrodinger.stationary.solver import (
    solve_stationary,
)


def main() -> None:
    grid = Grid1D(
        -8.0,
        8.0,
        1601,
    )

    hbar = 1.0
    mass = 1.0
    omega = 1.0
    numerical_tolerance = 1e-5

    potential = harmonic_oscillator(
        x=grid.interior,
        omega=omega,
        mass=mass,
    )

    solutions = solve_stationary(
        grid=grid,
        potential=potential,
        states=4,
        hbar=hbar,
        mass=mass,
    )

    print(
        "Harmonic Oscillator Observables"
    )
    print(
        "--------------------------------"
    )

    print(
        f"{'n':>3} "
        f"{'<x>':>12} "
        f"{'<p>':>12} "
        f"{'Delta x':>12} "
        f"{'Delta p':>12} "
        f"{'DxDp':>12} "
        f"{'Heisenberg':>12}"
    )

    for state in solutions:
        observables = calculate_observables(
            wavefunction=state.wavefunction,
            grid=grid,
            hbar=hbar,
        )

        valid = satisfies_heisenberg(
            delta_x=(
                observables.position_uncertainty
            ),
            delta_p=(
                observables.momentum_uncertainty
            ),
            hbar=hbar,
            tolerance=numerical_tolerance,
        )

        status = (
            "PASS"
            if valid
            else "FAIL"
        )

        print(
            f"{state.index:>3d} "
            f"{observables.position:>12.6e} "
            f"{observables.momentum:>12.6e} "
            f"{observables.position_uncertainty:>12.6f} "
            f"{observables.momentum_uncertainty:>12.6f} "
            f"{observables.uncertainty_product:>12.6f} "
            f"{status:>12}"
        )

        if not valid:
            raise RuntimeError(
                "Heisenberg uncertainty relation "
                "failed outside numerical tolerance."
            )


if __name__ == "__main__":
    main()