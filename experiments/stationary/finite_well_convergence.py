
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
    reference = finite_well_reference_states(
        half_width=1.0,
        depth=10.0,
        mass=1.0,
        hbar=1.0,
    )

    point_counts = (
        1001,
        2001,
        4001,
        8001,
    )

    print(
        "Finite Square Well Grid Convergence"
    )
    print(
        "-----------------------------------"
    )

    for points in point_counts:
        grid = Grid1D(
            -10.0,
            10.0,
            points,
        )

        potential = finite_square_well(
            x=grid.interior,
            left=-1.0,
            right=1.0,
            depth=10.0,
        )

        numerical = solve_stationary(
            grid=grid,
            potential=potential,
            states=6,
            hbar=1.0,
            mass=1.0,
        )

        bound = extract_bound_states(
            states=numerical,
        )

        if bound.count != len(reference):
            raise RuntimeError(
                "Bound-state count mismatch."
            )

        print()
        print(
            f"N = {points}, dx = {grid.dx:.8f}"
        )

        print(
            f"{'n':>3} "
            f"{'Numerical':>14} "
            f"{'Reference':>14} "
            f"{'Abs Error':>14} "
            f"{'Rel Error':>14}"
        )

        for numerical_state, reference_state in zip(
            bound.states,
            reference,
            strict=True,
        ):
            absolute = abs(
                numerical_state.energy
                - reference_state.energy
            )

            relative = (
                absolute
                / abs(reference_state.energy)
            )

            print(
                f"{reference_state.index:>3d} "
                f"{numerical_state.energy:>14.8f} "
                f"{reference_state.energy:>14.8f} "
                f"{absolute:>14.6e} "
                f"{relative:>14.6e}"
            )


if __name__ == "__main__":
    main()