from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from schrodinger.grid import Grid1D
from schrodinger.stationary.states import (
    StationaryState,
)

ArrayFloat = NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class DoubleWellAnalysis:
    ground_energy: float
    first_excited_energy: float
    energy_splitting: float
    ground_parity: str
    first_excited_parity: str


def energy_splitting(
    ground_state: StationaryState,
    first_excited_state: StationaryState,
) -> float:
    splitting = (
        first_excited_state.energy
        - ground_state.energy
    )

    if splitting <= 0.0:
        raise ValueError(
            "first excited energy must be greater "
            "than ground-state energy."
        )

    return float(splitting)


def parity_overlap(
    wavefunction: ArrayFloat,
    grid: Grid1D,
) -> float:
    if wavefunction.ndim != 1:
        raise ValueError(
            "wavefunction must be one-dimensional."
        )

    if wavefunction.size != grid.size:
        raise ValueError(
            "wavefunction size must match grid size."
        )

    if not np.all(
        np.isfinite(wavefunction)
    ):
        raise ValueError(
            "wavefunction values must be finite."
        )

    reflected = wavefunction[::-1]

    overlap = (
        np.vdot(
            wavefunction,
            reflected,
        )
        * grid.dx
    )

    return float(
        np.real(overlap)
    )


def classify_parity(
    wavefunction: ArrayFloat,
    grid: Grid1D,
    tolerance: float = 1e-3,
) -> str:
    if not np.isfinite(tolerance):
        raise ValueError(
            "tolerance must be finite."
        )

    if tolerance <= 0.0:
        raise ValueError(
            "tolerance must be positive."
        )

    overlap = parity_overlap(
        wavefunction=wavefunction,
        grid=grid,
    )

    if abs(overlap - 1.0) <= tolerance:
        return "even"

    if abs(overlap + 1.0) <= tolerance:
        return "odd"

    return "mixed"


def analyze_double_well(
    states: list[StationaryState],
    grid: Grid1D,
) -> DoubleWellAnalysis:
    if len(states) < 2:
        raise ValueError(
            "at least two stationary states are required."
        )

    ground = states[0]
    first_excited = states[1]

    splitting = energy_splitting(
        ground_state=ground,
        first_excited_state=first_excited,
    )

    return DoubleWellAnalysis(
        ground_energy=ground.energy,
        first_excited_energy=(
            first_excited.energy
        ),
        energy_splitting=splitting,
        ground_parity=classify_parity(
            wavefunction=ground.wavefunction,
            grid=grid,
        ),
        first_excited_parity=classify_parity(
            wavefunction=(
                first_excited.wavefunction
            ),
            grid=grid,
        ),
    )