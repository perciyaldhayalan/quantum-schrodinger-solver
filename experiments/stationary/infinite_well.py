import numpy as np

from schrodinger.analysis.errors import (
    relative_error,
)
from schrodinger.grid import Grid1D
from schrodinger.stationary.analytic import (
    infinite_well_energy,
)
from schrodinger.stationary.solver import (
    solve_stationary,
)


def main() -> None:
    grid = Grid1D(
        0.0,
        1.0,
        1001,
    )

    hbar = 1.0
    mass = 1.0
    number_of_states = 5

    potential = np.zeros(
        grid.interior_size,
        dtype=np.float64,
    )

    solutions = solve_stationary(
        grid=grid,
        potential=potential,
        states=number_of_states,
        hbar=hbar,
        mass=mass,
    )

    print(
        "Infinite Square Well Validation"
    )
    print(
        "--------------------------------"
    )
    print(
        f"{'n':>3} "
        f"{'Numerical':>16} "
        f"{'Exact':>16} "
        f"{'Relative Error':>18}"
    )

    for quantum_number, state in enumerate(
        solutions,
        start=1,
    ):
        exact = infinite_well_energy(
            quantum_number=quantum_number,
            length=grid.length,
            hbar=hbar,
            mass=mass,
        )

        error = relative_error(
            numerical=state.energy,
            exact=exact,
        )

        print(
            f"{quantum_number:>3d} "
            f"{state.energy:>16.10f} "
            f"{exact:>16.10f} "
            f"{error:>18.6e}"
        )


if __name__ == "__main__":
    main()