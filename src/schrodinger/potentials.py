import numpy as np
from numpy.typing import NDArray

ArrayFloat = NDArray[np.float64]


def infinite_square_well(
    x: ArrayFloat,
    left: float,
    right: float,
) -> ArrayFloat:
    if not np.isfinite(left):
        raise ValueError("left must be finite.")

    if not np.isfinite(right):
        raise ValueError("right must be finite.")

    if left >= right:
        raise ValueError("left must be smaller than right.")

    potential = np.full_like(x, np.inf, dtype=np.float64)

    inside = (x >= left) & (x <= right)

    potential[inside] = 0.0

    return potential


def finite_square_well(
    x: ArrayFloat,
    left: float,
    right: float,
    depth: float,
) -> ArrayFloat:
    if not np.isfinite(left):
        raise ValueError("left must be finite.")

    if not np.isfinite(right):
        raise ValueError("right must be finite.")

    if left >= right:
        raise ValueError("left must be smaller than right.")

    if not np.isfinite(depth):
        raise ValueError("depth must be finite.")

    if depth <= 0.0:
        raise ValueError("depth must be positive.")

    potential = np.zeros_like(x, dtype=np.float64)

    inside = (x >= left) & (x <= right)

    potential[inside] = -depth

    return potential


def harmonic_oscillator(
    x: ArrayFloat,
    omega: float = 1.0,
    mass: float = 1.0,
    center: float = 0.0,
) -> ArrayFloat:
    if not np.isfinite(omega):
        raise ValueError("omega must be finite.")

    if omega <= 0.0:
        raise ValueError("omega must be positive.")

    if not np.isfinite(mass):
        raise ValueError("mass must be finite.")

    if mass <= 0.0:
        raise ValueError("mass must be positive.")

    if not np.isfinite(center):
        raise ValueError("center must be finite.")

    displacement = x - center

    return 0.5 * mass * omega**2 * displacement**2


def double_well(
    x: ArrayFloat,
    a: float = 1.0,
    b: float = 1.0,
) -> ArrayFloat:
    if not np.isfinite(a):
        raise ValueError("a must be finite.")

    if a <= 0.0:
        raise ValueError("a must be positive.")

    if not np.isfinite(b):
        raise ValueError("b must be finite.")

    if b <= 0.0:
        raise ValueError("b must be positive.")

    return a * (x**2 - b**2) ** 2


def rectangular_barrier(
    x: ArrayFloat,
    left: float,
    right: float,
    height: float,
) -> ArrayFloat:
    if not np.isfinite(left):
        raise ValueError("left must be finite.")

    if not np.isfinite(right):
        raise ValueError("right must be finite.")

    if left >= right:
        raise ValueError("left must be smaller than right.")

    if not np.isfinite(height):
        raise ValueError("height must be finite.")

    if height <= 0.0:
        raise ValueError("height must be positive.")

    potential = np.zeros_like(x, dtype=np.float64)

    inside = (x >= left) & (x <= right)

    potential[inside] = height

    return potential