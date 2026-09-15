import numpy as np

from schrodinger.analysis.double_well_splitting import (
    double_well_splitting_scan,
)
from schrodinger.grid import Grid1D


def main() -> None:
    grid = Grid1D(
        -5.0,
        5.0,
        2001,
    )

    coefficients = np.asarray(
        [
            0.25,
            0.50,
            0.75,
            1.00,
            1.50,
            2.00,
            3.00,
            4.00,
        ],
        dtype=np.float64,
    )

    b = 1.5

    result = double_well_splitting_scan(
        grid=grid,
        coefficients=coefficients,
        b=b,
        mass=1.0,
        hbar=1.0,
    )

    print(
        "Double-Well Tunnelling Splitting"
    )
    print(
        "--------------------------------"
    )

    print(
        f"{'a':>8} "
        f"{'Barrier':>12} "
        f"{'E0':>14} "
        f"{'E1':>14} "
        f"{'Delta E':>14}"
    )

    for index in range(
        result.coefficients.size
    ):
        print(
            f"{result.coefficients[index]:>8.3f} "
            f"{result.barrier_heights[index]:>12.6f} "
            f"{result.ground_energies[index]:>14.8f} "
            f"{result.first_excited_energies[index]:>14.8f} "
            f"{result.energy_splittings[index]:>14.8e}"
        )

    if not np.all(
        np.diff(
            result.energy_splittings
        )
        < 0.0
    ):
        raise RuntimeError(
            "Energy splitting did not decrease "
            "monotonically with barrier height."
        )


if __name__ == "__main__":
    main()