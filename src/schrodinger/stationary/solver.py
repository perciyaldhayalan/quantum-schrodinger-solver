import numpy as np
from numpy.typing import NDArray
from scipy.sparse.linalg import eigsh

from schrodinger.analysis.normalization import (
    normalize_wavefunction,
)
from schrodinger.grid import Grid1D
from schrodinger.hamiltonian import build_hamiltonian
from schrodinger.stationary.states import StationaryState

ArrayFloat = NDArray[np.float64]


def solve_stationary(
    grid: Grid1D,
    potential: ArrayFloat,
    states: int = 6,
    hbar: float = 1.0,
    mass: float = 1.0,
) -> list[StationaryState]:
    if isinstance(states, bool) or not isinstance(
        states,
        int,
    ):
        raise TypeError("states must be an integer.")

    if states <= 0:
        raise ValueError("states must be positive.")

    if states >= grid.interior_size:
        raise ValueError(
            "states must be smaller than the number "
            "of interior grid points."
        )

    hamiltonian = build_hamiltonian(
        grid=grid,
        potential=potential,
        hbar=hbar,
        mass=mass,
    )

    eigenvalues, eigenvectors = eigsh(
        hamiltonian,
        k=states,
        which="SA",
    )

    order = np.argsort(eigenvalues)

    sorted_energies = eigenvalues[order]
    sorted_vectors = eigenvectors[:, order]

    solutions: list[StationaryState] = []

    for state_index in range(states):
        interior_wavefunction = np.asarray(
            sorted_vectors[:, state_index],
            dtype=np.float64,
        )

        full_wavefunction = np.zeros(
            grid.size,
            dtype=np.float64,
        )

        full_wavefunction[1:-1] = (
            interior_wavefunction
        )

        normalized = normalize_wavefunction(
            wavefunction=full_wavefunction,
            dx=grid.dx,
        )

        normalized_real = np.asarray(
            normalized,
            dtype=np.float64,
        )

        state = StationaryState(
            index=state_index,
            energy=float(
                sorted_energies[state_index]
            ),
            wavefunction=normalized_real,
        )

        solutions.append(state)

    return solutions