
from schrodinger.analysis.errors import (
    relative_error,
)
from schrodinger.grid import Grid1D
from schrodinger.potentials import (
    harmonic_oscillator,
)
from schrodinger.stationary.analytic import (
    harmonic_oscillator_energy,
)
from schrodinger.stationary.solver import (
    solve_stationary,
)


def main() -> None:
    grid = Grid1D(
        -8.0,
        8.0,
        1201,
    )

    hbar = 1.0
    mass = 1.0
    omega = 1.0
    number_of_states = 6

    potential = harmonic_oscillator(
        x=grid.interior,
        omega=omega,
        mass=mass,
    )

    solutions = solve_stationary(
        grid=grid,
        potential=potential,
        states=number_of_states,
        hbar=hbar,
        mass=mass,
    )

    print(
        "Quantum Harmonic Oscillator Validation"
    )
    print(
        "--------------------------------------"
    )
    print(
        f"{'n':>3} "
        f"{'Numerical':>16} "
        f"{'Exact':>16} "
        f"{'Relative Error':>18}"
    )

    for quantum_number, state in enumerate(
        solutions
    ):
        exact = harmonic_oscillator_energy(
            quantum_number=quantum_number,
            omega=omega,
            hbar=hbar,
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