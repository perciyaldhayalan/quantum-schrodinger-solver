from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

ArrayFloat = NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class StationaryState:
    index: int
    energy: float
    wavefunction: ArrayFloat

    def __post_init__(self) -> None:
        if self.index < 0:
            raise ValueError(
                "state index must be non-negative."
            )

        if not np.isfinite(self.energy):
            raise ValueError(
                "state energy must be finite."
            )

        if self.wavefunction.ndim != 1:
            raise ValueError(
                "wavefunction must be one-dimensional."
            )

        if self.wavefunction.size < 3:
            raise ValueError(
                "wavefunction must contain at least 3 points."
            )

        if not np.all(
            np.isfinite(self.wavefunction)
        ):
            raise ValueError(
                "wavefunction values must be finite."
            )