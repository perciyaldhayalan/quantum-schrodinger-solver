from schrodinger.grid import Grid1D
from schrodinger.potentials import (
    double_well,
)
from schrodinger.stationary.double_well import (
    analyze_double_well,
)
from schrodinger.stationary.solver import (
    solve_stationary,
)


def main() -> None:
    grid = Grid1D(
        -5.0,
        5.0,
        2001,
    )

    a = 1.0
    b = 1.5
    hbar = 1.0
    mass = 1.0

    potential = double_well(
        x=grid.interior,
        a=a,
        b=b,
    )

    states = solve_stationary(
        grid=grid,
        potential=potential,
        states=6,
        hbar=hbar,
        mass=mass,
    )

    result = analyze_double_well(
        states=states,
        grid=grid,
    )

    barrier_height = (
        a * b**4
    )

    print(
        "Symmetric Double Well"
    )
    print(
        "--------------------------------"
    )

    print(
        f"a: {a}"
    )
    print(
        f"b: {b}"
    )
    print(
        f"Barrier height: {barrier_height:.8f}"
    )
    print()

    print(
        f"Ground energy: "
        f"{result.ground_energy:.8f}"
    )

    print(
        f"First excited energy: "
        f"{result.first_excited_energy:.8f}"
    )

    print(
        f"Energy splitting: "
        f"{result.energy_splitting:.8e}"
    )

    print(
        f"Ground parity: "
        f"{result.ground_parity}"
    )

    print(
        f"First excited parity: "
        f"{result.first_excited_parity}"
    )

    print()
    print(
        f"{'n':>3} "
        f"{'Energy':>16}"
    )

    for state in states:
        print(
            f"{state.index:>3d} "
            f"{state.energy:>16.8f}"
        )


if __name__ == "__main__":
    main()