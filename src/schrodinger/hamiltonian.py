import numpy as np
from numpy.typing import NDArray
from scipy.sparse import csr_matrix

from schrodinger.grid import Grid1D

ArrayFloat = NDArray[np.float64]


def kinetic_energy_operator(
    grid: Grid1D,
    hbar: float = 1.0,
    mass: float = 1.0,
) -> csr_matrix:
    if not np.isfinite(hbar):
        raise ValueError("hbar must be finite.")

    if hbar <= 0.0:
        raise ValueError("hbar must be positive.")

    if not np.isfinite(mass):
        raise ValueError("mass must be finite.")

    if mass <= 0.0:
        raise ValueError("mass must be positive.")

    size = grid.interior_size
    coefficient = hbar**2 / (2.0 * mass * grid.dx**2)

    main_indices = np.arange(
        size,
        dtype=np.int64,
    )

    off_indices = np.arange(
        size - 1,
        dtype=np.int64,
    )

    rows = np.concatenate(
        (
            main_indices,
            off_indices,
            off_indices + 1,
        )
    )

    columns = np.concatenate(
        (
            main_indices,
            off_indices + 1,
            off_indices,
        )
    )

    data = np.concatenate(
        (
            np.full(
                size,
                2.0 * coefficient,
                dtype=np.float64,
            ),
            np.full(
                size - 1,
                -coefficient,
                dtype=np.float64,
            ),
            np.full(
                size - 1,
                -coefficient,
                dtype=np.float64,
            ),
        )
    )

    operator = csr_matrix(
        (data, (rows, columns)),
        shape=(size, size),
        dtype=np.float64,
    )

    return operator


def potential_energy_operator(
    potential: ArrayFloat,
) -> csr_matrix:
    if potential.ndim != 1:
        raise ValueError("potential must be one-dimensional.")

    if potential.size == 0:
        raise ValueError("potential must not be empty.")

    if not np.all(np.isfinite(potential)):
        raise ValueError("potential values must be finite.")

    size = potential.size

    indices = np.arange(
        size,
        dtype=np.int64,
    )

    operator = csr_matrix(
        (
            potential,
            (indices, indices),
        ),
        shape=(size, size),
        dtype=np.float64,
    )

    return operator


def build_hamiltonian(
    grid: Grid1D,
    potential: ArrayFloat,
    hbar: float = 1.0,
    mass: float = 1.0,
) -> csr_matrix:
    if potential.ndim != 1:
        raise ValueError("potential must be one-dimensional.")

    if potential.size != grid.interior_size:
        raise ValueError(
            "potential size must match the number of interior grid points."
        )

    kinetic = kinetic_energy_operator(
        grid=grid,
        hbar=hbar,
        mass=mass,
    )

    potential_operator = potential_energy_operator(
        potential=potential,
    )

    return csr_matrix(
        kinetic + potential_operator
    )


def is_hermitian(
    matrix: csr_matrix,
    tolerance: float = 1e-12,
) -> bool:
    if not np.isfinite(tolerance):
        raise ValueError("tolerance must be finite.")

    if tolerance < 0.0:
        raise ValueError("tolerance must be non-negative.")

    difference = matrix - matrix.getH()

    if difference.nnz == 0:
        return True

    maximum_difference = float(
        np.max(
            np.abs(difference.data)
        )
    )

    return maximum_difference <= tolerance