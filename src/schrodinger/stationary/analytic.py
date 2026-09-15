import numpy as np
from numpy.typing import NDArray

ArrayFloat = NDArray[np.float64]


def infinite_well_energy(
    quantum_number: int,
    length: float,
    hbar: float = 1.0,
    mass: float = 1.0,
) -> float:
    if isinstance(quantum_number, bool) or not isinstance(
        quantum_number,
        int,
    ):
        raise TypeError(
            "quantum_number must be an integer."
        )

    if quantum_number <= 0:
        raise ValueError(
            "quantum_number must be positive."
        )

    if not np.isfinite(length):
        raise ValueError(
            "length must be finite."
        )

    if length <= 0.0:
        raise ValueError(
            "length must be positive."
        )

    if not np.isfinite(hbar):
        raise ValueError(
            "hbar must be finite."
        )

    if hbar <= 0.0:
        raise ValueError(
            "hbar must be positive."
        )

    if not np.isfinite(mass):
        raise ValueError(
            "mass must be finite."
        )

    if mass <= 0.0:
        raise ValueError(
            "mass must be positive."
        )

    numerator = (
        quantum_number**2
        * np.pi**2
        * hbar**2
    )

    denominator = (
        2.0
        * mass
        * length**2
    )

    return float(
        numerator / denominator
    )


def infinite_well_wavefunction(
    x: ArrayFloat,
    quantum_number: int,
    left: float,
    right: float,
) -> ArrayFloat:
    if x.ndim != 1:
        raise ValueError(
            "x must be one-dimensional."
        )

    if x.size == 0:
        raise ValueError(
            "x must not be empty."
        )

    if not np.all(np.isfinite(x)):
        raise ValueError(
            "x values must be finite."
        )

    if isinstance(quantum_number, bool) or not isinstance(
        quantum_number,
        int,
    ):
        raise TypeError(
            "quantum_number must be an integer."
        )

    if quantum_number <= 0:
        raise ValueError(
            "quantum_number must be positive."
        )

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

    length = right - left

    wavefunction = np.zeros_like(
        x,
        dtype=np.float64,
    )

    inside = (
        (x >= left)
        & (x <= right)
    )

    shifted_x = (
        x[inside] - left
    )

    wavefunction[inside] = (
        np.sqrt(2.0 / length)
        * np.sin(
            quantum_number
            * np.pi
            * shifted_x
            / length
        )
    )

    return wavefunction


def harmonic_oscillator_energy(
    quantum_number: int,
    omega: float = 1.0,
    hbar: float = 1.0,
) -> float:
    if isinstance(quantum_number, bool) or not isinstance(
        quantum_number,
        int,
    ):
        raise TypeError(
            "quantum_number must be an integer."
        )

    if quantum_number < 0:
        raise ValueError(
            "quantum_number must be non-negative."
        )

    if not np.isfinite(omega):
        raise ValueError(
            "omega must be finite."
        )

    if omega <= 0.0:
        raise ValueError(
            "omega must be positive."
        )

    if not np.isfinite(hbar):
        raise ValueError(
            "hbar must be finite."
        )

    if hbar <= 0.0:
        raise ValueError(
            "hbar must be positive."
        )

    return float(
        hbar
        * omega
        * (quantum_number + 0.5)
    )