import numpy as np
from numpy.typing import NDArray

ArrayFloat = NDArray[np.float64]
ArrayComplex = NDArray[np.complex128]


def probability_norm(
    wavefunction: ArrayFloat | ArrayComplex,
    dx: float,
) -> float:
    if wavefunction.ndim != 1:
        raise ValueError(
            "wavefunction must be one-dimensional."
        )

    if wavefunction.size == 0:
        raise ValueError(
            "wavefunction must not be empty."
        )

    if not np.all(np.isfinite(wavefunction)):
        raise ValueError(
            "wavefunction values must be finite."
        )

    if not np.isfinite(dx):
        raise ValueError("dx must be finite.")

    if dx <= 0.0:
        raise ValueError("dx must be positive.")

    probability_density = np.abs(
        wavefunction
    ) ** 2

    return float(
        np.sum(probability_density) * dx
    )


def normalize_wavefunction(
    wavefunction: ArrayFloat | ArrayComplex,
    dx: float,
) -> ArrayFloat | ArrayComplex:
    norm = probability_norm(
        wavefunction=wavefunction,
        dx=dx,
    )

    if norm <= 0.0:
        raise ValueError(
            "wavefunction norm must be positive."
        )

    scale = np.sqrt(norm)

    if np.iscomplexobj(wavefunction):
        normalized_complex = np.asarray(
            wavefunction / scale,
            dtype=np.complex128,
        )

        return normalized_complex

    normalized_real = np.asarray(
        wavefunction / scale,
        dtype=np.float64,
    )

    return normalized_real