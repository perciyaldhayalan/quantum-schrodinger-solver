from dataclasses import dataclass, field
from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy.sparse import csc_matrix, eye
from scipy.sparse.linalg import splu

from schrodinger.grid import Grid1D
from schrodinger.hamiltonian import build_hamiltonian

ArrayFloat = NDArray[np.float64]
ArrayComplex = NDArray[np.complex128]


@dataclass(slots=True)
class CrankNicolsonPropagator:
    grid: Grid1D
    potential: ArrayFloat
    dt: float
    mass: float = 1.0
    hbar: float = 1.0
    _left_matrix: Any = field(
        init=False,
        repr=False,
    )
    _right_matrix: Any = field(
        init=False,
        repr=False,
    )
    _left_solver: Any = field(
        init=False,
        repr=False,
    )

    def __post_init__(self) -> None:
        self._validate_parameters()

        hamiltonian = build_hamiltonian(
            grid=self.grid,
            potential=self.potential,
            mass=self.mass,
            hbar=self.hbar,
        )

        hamiltonian_complex = csc_matrix(
            hamiltonian,
            dtype=np.complex128,
        )

        identity = eye(
            self.grid.interior_size,
            dtype=np.complex128,
            format="csc",
        )

        coefficient = (
            1j
            * self.dt
            / (
                2.0
                * self.hbar
            )
        )

        self._left_matrix = csc_matrix(
            identity
            + coefficient
            * hamiltonian_complex
        )

        self._right_matrix = csc_matrix(
            identity
            - coefficient
            * hamiltonian_complex
        )

        self._left_solver = splu(
            self._left_matrix
        )

    def step(
        self,
        wavefunction: ArrayComplex,
    ) -> ArrayComplex:
        self._validate_wavefunction(
            wavefunction=wavefunction
        )

        interior = np.asarray(
            wavefunction[1:-1],
            dtype=np.complex128,
        )

        right_hand_side = (
            self._right_matrix
            @ interior
        )

        next_interior = (
            self._left_solver.solve(
                right_hand_side
            )
        )

        next_wavefunction = np.zeros(
            self.grid.size,
            dtype=np.complex128,
        )

        next_wavefunction[1:-1] = (
            next_interior
        )

        return next_wavefunction

    def propagate(
        self,
        wavefunction: ArrayComplex,
        steps: int,
    ) -> ArrayComplex:
        self._validate_wavefunction(
            wavefunction=wavefunction
        )

        if isinstance(steps, bool):
            raise TypeError(
                "steps must be an integer."
            )

        if not isinstance(
            steps,
            (int, np.integer),
        ):
            raise TypeError(
                "steps must be an integer."
            )

        if steps < 0:
            raise ValueError(
                "steps must be non-negative."
            )

        state = np.asarray(
            wavefunction,
            dtype=np.complex128,
        ).copy()

        for _ in range(int(steps)):
            state = self.step(
                wavefunction=state
            )

        return state

    def _validate_parameters(self) -> None:
        if self.potential.ndim != 1:
            raise ValueError(
                "potential must be "
                "one-dimensional."
            )

        if (
            self.potential.size
            != self.grid.interior_size
        ):
            raise ValueError(
                "potential size must match "
                "grid interior size."
            )

        if not np.all(
            np.isfinite(self.potential)
        ):
            raise ValueError(
                "potential values must be finite."
            )

        if not np.isfinite(self.dt):
            raise ValueError(
                "dt must be finite."
            )

        if self.dt <= 0.0:
            raise ValueError(
                "dt must be positive."
            )

        if not np.isfinite(self.mass):
            raise ValueError(
                "mass must be finite."
            )

        if self.mass <= 0.0:
            raise ValueError(
                "mass must be positive."
            )

        if not np.isfinite(self.hbar):
            raise ValueError(
                "hbar must be finite."
            )

        if self.hbar <= 0.0:
            raise ValueError(
                "hbar must be positive."
            )

    def _validate_wavefunction(
        self,
        wavefunction: ArrayComplex,
    ) -> None:
        if wavefunction.ndim != 1:
            raise ValueError(
                "wavefunction must be "
                "one-dimensional."
            )

        if (
            wavefunction.size
            != self.grid.size
        ):
            raise ValueError(
                "wavefunction size must "
                "match grid size."
            )

        if not np.all(
            np.isfinite(wavefunction)
        ):
            raise ValueError(
                "wavefunction values "
                "must be finite."
            )