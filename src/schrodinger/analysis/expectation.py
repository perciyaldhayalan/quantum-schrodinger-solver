import numpy as np
from numpy.typing import NDArray

ArrayFloat = NDArray[np.float64]
ArrayComplex = NDArray[np.complex128]
Wavefunction = ArrayFloat | ArrayComplex


def expectation_value(
    wavefunction: Wavefunction,
    operator_wavefunction: Wavefunction,
    dx: float,
) -> complex:
    if wavefunction.ndim != 1:
        raise ValueError(
            "wavefunction must be one-dimensional."
        )

    if operator_wavefunction.ndim != 1:
        raise ValueError(
            "operator_wavefunction must be one-dimensional."
        )

    if wavefunction.shape != operator_wavefunction.shape:
        raise ValueError(
            "wavefunction and operator_wavefunction "
            "must have the same shape."
        )

    if wavefunction.size == 0:
        raise ValueError(
            "wavefunction must not be empty."
        )

    if not np.all(np.isfinite(wavefunction)):
        raise ValueError(
            "wavefunction values must be finite."
        )

    if not np.all(
        np.isfinite(operator_wavefunction)
    ):
        raise ValueError(
            "operator_wavefunction values must be finite."
        )

    if not np.isfinite(dx):
        raise ValueError(
            "dx must be finite."
        )

    if dx <= 0.0:
        raise ValueError(
            "dx must be positive."
        )

    value = (
        np.vdot(
            wavefunction,
            operator_wavefunction,
        )
        * dx
    )

    return complex(value)


def real_expectation_value(
    wavefunction: Wavefunction,
    operator_wavefunction: Wavefunction,
    dx: float,
    tolerance: float = 1e-10,
) -> float:
    if not np.isfinite(tolerance):
        raise ValueError(
            "tolerance must be finite."
        )

    if tolerance < 0.0:
        raise ValueError(
            "tolerance must be non-negative."
        )

    value = expectation_value(
        wavefunction=wavefunction,
        operator_wavefunction=operator_wavefunction,
        dx=dx,
    )

    if abs(value.imag) > tolerance:
        raise ValueError(
            "expectation value has a significant "
            "imaginary component."
        )

    return float(value.real)