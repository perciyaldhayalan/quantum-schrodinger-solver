from schrodinger.analysis.errors import (
    absolute_error,
    relative_error,
)
from schrodinger.grid import Grid1D
from schrodinger.potentials import (
    finite_square_well,
)
from schrodinger.stationary.bound_states import (
    extract_bound_states,
)
from schrodinger.stationary.finite_well_analytic import (
    finite_well_reference_states,
)
from schrodinger.stationary.solver import (
    solve_stationary,
)


def main() -> None:
    grid = Grid1D(
        -10.0,
        10.0,
        4001,
    )

    half_width = 1.0
    depth = 10.0
    mass = 1.0
    hbar = 1.0

    potential = finite_square_well(
        x=grid.interior,
        left=-half_width,
        right=half_width,
        depth=depth,
    )

    numerical_states = solve_stationary(
        grid=grid,
        potential=potential,
        states=8,
        mass=mass,
        hbar=hbar,
    )

    bound_states = extract_bound_states(
        states=numerical_states,
    )

    reference_states = finite_well_reference_states(
        half_width=half_width,
        depth=depth,
        mass=mass,
        hbar=hbar,
    )

    if bound_states.count != len(
        reference_states
    ):
        raise RuntimeError(
            "Numerical and reference bound-state "
            "counts do not agree."
        )

    print(
        "Finite Square Well Validation"
    )
    print(
        "--------------------------------"
    )

    print(
        f"{'n':>3} "
        f"{'Parity':>8} "
        f"{'Numerical':>14} "
        f"{'Reference':>14} "
        f"{'Abs Error':>14} "
        f"{'Rel Error':>14}"
    )

    for numerical, reference in zip(
        bound_states.states,
        reference_states,
        strict=True,
    ):
        abs_error = absolute_error(
            numerical.energy,
            reference.energy,
        )

        rel_error = relative_error(
            numerical.energy,
            reference.energy,
        )

        print(
            f"{reference.index:>3d} "
            f"{reference.parity:>8} "
            f"{numerical.energy:>14.8f} "
            f"{reference.energy:>14.8f} "
            f"{abs_error:>14.6e} "
            f"{rel_error:>14.6e}"
        )


if __name__ == "__main__":
    main()