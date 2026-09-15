from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from schrodinger.grid import Grid1D

ArrayComplex = NDArray[np.complex128]


@dataclass(frozen=True, slots=True)
class ScatteringProbabilities:
    left: float
    barrier: float
    right: float
    total: float


def region_probability(
    wavefunction: ArrayComplex,
    grid: Grid1D,
    mask: NDArray[np.bool_],
) -> float:
    _validate_wavefunction(
        wavefunction=wavefunction,
        grid=grid,
    )

    if mask.ndim != 1:
        raise ValueError(
            "mask must be one-dimensional."
        )

    if mask.size != grid.size:
        raise ValueError(
            "mask size must match grid size."
        )

    density = (
        np.abs(wavefunction) ** 2
    )

    return float(
        np.sum(
            density[mask]
        )
        * grid.dx
    )


def scattering_probabilities(
    wavefunction: ArrayComplex,
    grid: Grid1D,
    barrier_left: float,
    barrier_right: float,
) -> ScatteringProbabilities:
    _validate_barrier(
        grid=grid,
        barrier_left=barrier_left,
        barrier_right=barrier_right,
    )

    left_mask = (
        grid.values
        < barrier_left
    )

    barrier_mask = (
        (grid.values >= barrier_left)
        & (grid.values <= barrier_right)
    )

    right_mask = (
        grid.values
        > barrier_right
    )

    left_probability = region_probability(
        wavefunction=wavefunction,
        grid=grid,
        mask=left_mask,
    )

    barrier_probability = region_probability(
        wavefunction=wavefunction,
        grid=grid,
        mask=barrier_mask,
    )

    right_probability = region_probability(
        wavefunction=wavefunction,
        grid=grid,
        mask=right_mask,
    )

    total = (
        left_probability
        + barrier_probability
        + right_probability
    )

    return ScatteringProbabilities(
        left=left_probability,
        barrier=barrier_probability,
        right=right_probability,
        total=total,
    )


def rectangular_barrier_on_interior(
    grid: Grid1D,
    barrier_left: float,
    barrier_right: float,
    barrier_height: float,
) -> NDArray[np.float64]:
    _validate_barrier(
        grid=grid,
        barrier_left=barrier_left,
        barrier_right=barrier_right,
    )

    if not np.isfinite(barrier_height):
        raise ValueError(
            "barrier_height must be finite."
        )

    if barrier_height < 0.0:
        raise ValueError(
            "barrier_height must be non-negative."
        )

    interior = grid.interior

    potential = np.where(
        (interior >= barrier_left)
        & (interior <= barrier_right),
        barrier_height,
        0.0,
    )

    return np.asarray(
        potential,
        dtype=np.float64,
    )


def _validate_wavefunction(
    wavefunction: ArrayComplex,
    grid: Grid1D,
) -> None:
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


def _validate_barrier(
    grid: Grid1D,
    barrier_left: float,
    barrier_right: float,
) -> None:
    if not np.isfinite(barrier_left):
        raise ValueError(
            "barrier_left must be finite."
        )

    if not np.isfinite(barrier_right):
        raise ValueError(
            "barrier_right must be finite."
        )

    if barrier_left >= barrier_right:
        raise ValueError(
            "barrier_left must be smaller "
            "than barrier_right."
        )

    if (
        barrier_left <= grid.x_min
        or barrier_right >= grid.x_max
    ):
        raise ValueError(
            "barrier must lie inside the grid."
        )