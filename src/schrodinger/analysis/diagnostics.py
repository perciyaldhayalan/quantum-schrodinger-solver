import numpy as np
from numpy.typing import NDArray

from schrodinger.grid import Grid1D

ArrayFloat = NDArray[np.float64]
ArrayComplex = NDArray[np.complex128]
Wavefunction = ArrayFloat | ArrayComplex


def state_overlap(
    first: Wavefunction,
    second: Wavefunction,
    dx: float,
) -> complex:
    if first.ndim != 1 or second.ndim != 1:
        raise ValueError(
            "wavefunctions must be one-dimensional."
        )

    if first.shape != second.shape:
        raise ValueError(
            "wavefunctions must have the same shape."
        )

    if not np.isfinite(dx):
        raise ValueError(
            "dx must be finite."
        )

    if dx <= 0.0:
        raise ValueError(
            "dx must be positive."
        )

    value = np.vdot(
        first,
        second,
    ) * dx

    return complex(value)


def orthogonality_matrix(
    wavefunctions: ArrayFloat,
    grid: Grid1D,
) -> ArrayComplex:
    if wavefunctions.ndim != 2:
        raise ValueError(
            "wavefunctions must be two-dimensional."
        )

    if wavefunctions.shape[1] != grid.size:
        raise ValueError(
            "wavefunction size must match grid size."
        )

    if not np.all(np.isfinite(wavefunctions)):
        raise ValueError(
            "wavefunction values must be finite."
        )

    number_of_states = (
        wavefunctions.shape[0]
    )

    matrix = np.empty(
        (
            number_of_states,
            number_of_states,
        ),
        dtype=np.complex128,
    )

    for row in range(number_of_states):
        for column in range(number_of_states):
            matrix[row, column] = state_overlap(
                first=wavefunctions[row],
                second=wavefunctions[column],
                dx=grid.dx,
            )

    return matrix


def satisfies_heisenberg(
    delta_x: float,
    delta_p: float,
    hbar: float = 1.0,
    tolerance: float = 1e-10,
) -> bool:
    if not np.isfinite(delta_x):
        raise ValueError(
            "delta_x must be finite."
        )

    if not np.isfinite(delta_p):
        raise ValueError(
            "delta_p must be finite."
        )

    if delta_x < 0.0 or delta_p < 0.0:
        raise ValueError(
            "uncertainties must be non-negative."
        )

    if not np.isfinite(hbar):
        raise ValueError(
            "hbar must be finite."
        )

    if hbar <= 0.0:
        raise ValueError(
            "hbar must be positive."
        )

    if not np.isfinite(tolerance):
        raise ValueError(
            "tolerance must be finite."
        )

    if tolerance < 0.0:
        raise ValueError(
            "tolerance must be non-negative."
        )

    product = delta_x * delta_p
    lower_bound = hbar / 2.0

    return (
        product + tolerance
        >= lower_bound
    )