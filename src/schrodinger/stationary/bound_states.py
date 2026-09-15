from dataclasses import dataclass

import numpy as np

from schrodinger.grid import Grid1D
from schrodinger.stationary.states import (
    StationaryState,
)


@dataclass(frozen=True, slots=True)
class BoundStateResult:
    states: tuple[StationaryState, ...]
    continuum_threshold: float

    @property
    def count(self) -> int:
        return len(self.states)

    @property
    def energies(self) -> np.ndarray:
        return np.asarray(
            [
                state.energy
                for state in self.states
            ],
            dtype=np.float64,
        )


def extract_bound_states(
    states: list[StationaryState],
    continuum_threshold: float = 0.0,
) -> BoundStateResult:
    if not np.isfinite(continuum_threshold):
        raise ValueError(
            "continuum_threshold must be finite."
        )

    bound = tuple(
        state
        for state in states
        if state.energy < continuum_threshold
    )

    return BoundStateResult(
        states=bound,
        continuum_threshold=continuum_threshold,
    )


def exterior_probability(
    state: StationaryState,
    grid: Grid1D,
    left: float,
    right: float,
) -> float:
    if not np.isfinite(left):
        raise ValueError(
            "left must be finite."
        )

    if not np.isfinite(right):
        raise ValueError(
            "right must be finite."
        )

    if left >= right:
        raise ValueError(
            "left must be smaller than right."
        )

    if state.wavefunction.size != grid.size:
        raise ValueError(
            "wavefunction size must match grid size."
        )

    density = (
        np.abs(state.wavefunction) ** 2
    )

    outside = (
        (grid.values < left)
        | (grid.values > right)
    )

    probability = (
        np.sum(density[outside])
        * grid.dx
    )

    return float(probability)


def interior_probability(
    state: StationaryState,
    grid: Grid1D,
    left: float,
    right: float,
) -> float:
    if not np.isfinite(left):
        raise ValueError(
            "left must be finite."
        )

    if not np.isfinite(right):
        raise ValueError(
            "right must be finite."
        )

    if left >= right:
        raise ValueError(
            "left must be smaller than right."
        )

    if state.wavefunction.size != grid.size:
        raise ValueError(
            "wavefunction size must match grid size."
        )

    density = (
        np.abs(state.wavefunction) ** 2
    )

    inside = (
        (grid.values >= left)
        & (grid.values <= right)
    )

    probability = (
        np.sum(density[inside])
        * grid.dx
    )

    return float(probability)