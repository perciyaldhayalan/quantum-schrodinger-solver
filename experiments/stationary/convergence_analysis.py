import numpy as np

from schrodinger.analysis.convergence import (
    infinite_well_convergence,
)


def main() -> None:
    point_counts = np.array(
        [
            100,
            200,
            400,
            800,
            1600,
            3200,
        ],
        dtype=np.int64,
    )

    result = infinite_well_convergence(
        point_counts=point_counts,
        quantum_number=1,
        length=1.0,
        hbar=1.0,
        mass=1.0,
    )

    print(
        "Infinite Square Well Grid Convergence"
    )
    print(
        "-------------------------------------"
    )

    print(
        f"{'N':>6} "
        f"{'dx':>14} "
        f"{'Energy':>16} "
        f"{'Abs Error':>16} "
        f"{'Rel Error':>16}"
    )

    for index in range(
        result.grid_points.size
    ):
        print(
            f"{result.grid_points[index]:>6d} "
            f"{result.grid_spacings[index]:>14.6e} "
            f"{result.numerical_energies[index]:>16.10f} "
            f"{result.absolute_errors[index]:>16.6e} "
            f"{result.relative_errors[index]:>16.6e}"
        )

    print()
    print(
        f"Exact energy: "
        f"{result.exact_energy:.12f}"
    )

    print(
        f"Observed convergence order: "
        f"{result.observed_order:.6f}"
    )


if __name__ == "__main__":
    main()