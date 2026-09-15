from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from schrodinger.grid import Grid1D
from schrodinger.potentials import double_well
from schrodinger.stationary.double_well import (
    energy_splitting,
)
from schrodinger.stationary.solver import (
    solve_stationary,
)

ArrayFloat = NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class SplittingScanResult:
    coefficients: ArrayFloat
    barrier_heights: ArrayFloat
    ground_energies: ArrayFloat
    first_excited_energies: ArrayFloat
    energy_splittings: ArrayFloat


def double_well_splitting_scan(
    grid: Grid1D,
    coefficients: ArrayFloat,
    b: float,
    mass: float = 1.0,
    hbar: float = 1.0,
) -> SplittingScanResult:
    if coefficients.ndim != 1:
        raise ValueError(
            "coefficients must be one-dimensional."
        )

    if coefficients.size < 2:
        raise ValueError(
            "at least two coefficients are required."
        )

    if not np.all(np.isfinite(coefficients)):
        raise ValueError(
            "coefficients must be finite."
        )

    if np.any(coefficients <= 0.0):
        raise ValueError(
            "coefficients must be positive."
        )

    if not np.all(np.diff(coefficients) > 0.0):
        raise ValueError(
            "coefficients must be strictly increasing."
        )

    if not np.isfinite(b) or b <= 0.0:
        raise ValueError(
            "b must be finite and positive."
        )

    if not np.isfinite(mass) or mass <= 0.0:
        raise ValueError(
            "mass must be finite and positive."
        )

    if not np.isfinite(hbar) or hbar <= 0.0:
        raise ValueError(
            "hbar must be finite and positive."
        )

    barrier_heights: list[float] = []
    ground_energies: list[float] = []
    first_excited_energies: list[float] = []
    splittings: list[float] = []

    for coefficient in coefficients:
        a = float(coefficient)

        potential = double_well(
            x=grid.interior,
            a=a,
            b=b,
        )

        states = solve_stationary(
            grid=grid,
            potential=potential,
            states=2,
            mass=mass,
            hbar=hbar,
        )

        splitting = energy_splitting(
            ground_state=states[0],
            first_excited_state=states[1],
        )

        barrier_heights.append(
            a * b**4
        )

        ground_energies.append(
            states[0].energy
        )

        first_excited_energies.append(
            states[1].energy
        )

        splittings.append(
            splitting
        )

    return SplittingScanResult(
        coefficients=np.asarray(
            coefficients,
            dtype=np.float64,
        ),
        barrier_heights=np.asarray(
            barrier_heights,
            dtype=np.float64,
        ),
        ground_energies=np.asarray(
            ground_energies,
            dtype=np.float64,
        ),
        first_excited_energies=np.asarray(
            first_excited_energies,
            dtype=np.float64,
        ),
        energy_splittings=np.asarray(
            splittings,
            dtype=np.float64,
        ),
    )