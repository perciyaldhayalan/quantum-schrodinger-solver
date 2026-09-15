import numpy as np
from numpy.typing import NDArray

ArrayFloat = NDArray[np.float64]


def absolute_error(
    numerical: float,
    exact: float,
) -> float:
    if not np.isfinite(numerical):
        raise ValueError("numerical value must be finite.")

    if not np.isfinite(exact):
        raise ValueError("exact value must be finite.")

    return abs(numerical - exact)


def relative_error(
    numerical: float,
    exact: float,
) -> float:
    if not np.isfinite(numerical):
        raise ValueError("numerical value must be finite.")

    if not np.isfinite(exact):
        raise ValueError("exact value must be finite.")

    if exact == 0.0:
        raise ValueError(
            "exact value must be non-zero "
            "for relative error."
        )

    return abs(
        (numerical - exact) / exact
    )


def relative_errors(
    numerical: ArrayFloat,
    exact: ArrayFloat,
) -> ArrayFloat:
    if numerical.ndim != 1:
        raise ValueError(
            "numerical values must be one-dimensional."
        )

    if exact.ndim != 1:
        raise ValueError(
            "exact values must be one-dimensional."
        )

    if numerical.shape != exact.shape:
        raise ValueError(
            "numerical and exact values must have "
            "the same shape."
        )

    if not np.all(np.isfinite(numerical)):
        raise ValueError(
            "numerical values must be finite."
        )

    if not np.all(np.isfinite(exact)):
        raise ValueError(
            "exact values must be finite."
        )

    if np.any(exact == 0.0):
        raise ValueError(
            "exact values must be non-zero "
            "for relative error."
        )

    result = np.abs(
        (numerical - exact) / exact
    )

    return np.asarray(
        result,
        dtype=np.float64,
    )