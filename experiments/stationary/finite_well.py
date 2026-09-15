from schrodinger.grid import Grid1D
from schrodinger.potentials import (
    finite_square_well,
)
from schrodinger.stationary.bound_states import (
    exterior_probability,
    extract_bound_states,
    interior_probability,
)
from schrodinger.stationary.solver import (
    solve_stationary,
)


def main() -> None:
    grid = Grid1D(
        -10.0,
        10.0,
        2001,
    )

    left = -1.0
    right = 1.0
    depth = 10.0
    hbar = 1.0
    mass = 1.0

    potential = finite_square_well(
        x=grid.interior,
        left=left,
        right=right,
        depth=depth,
    )

    solutions = solve_stationary(
        grid=grid,
        potential=potential,
        states=10,
        hbar=hbar,
        mass=mass,
    )

    bound = extract_bound_states(
        states=solutions,
        continuum_threshold=0.0,
    )

    print(
        "Finite Square Well Bound States"
    )
    print(
        "--------------------------------"
    )

    print(
        f"Well range: [{left}, {right}]"
    )
    print(
        f"Well depth: {depth}"
    )
    print(
        f"Bound states found: {bound.count}"
    )
    print()

    print(
        f"{'n':>3} "
        f"{'Energy':>14} "
        f"{'P_inside':>14} "
        f"{'P_outside':>14} "
        f"{'Total':>14}"
    )

    for state in bound.states:
        inside = interior_probability(
            state=state,
            grid=grid,
            left=left,
            right=right,
        )

        outside = exterior_probability(
            state=state,
            grid=grid,
            left=left,
            right=right,
        )

        total = inside + outside

        print(
            f"{state.index:>3d} "
            f"{state.energy:>14.8f} "
            f"{inside:>14.8f} "
            f"{outside:>14.8f} "
            f"{total:>14.8f}"
        )


if __name__ == "__main__":
    main()