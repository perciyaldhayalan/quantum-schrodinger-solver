from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from schrodinger.analysis.expectation import (
    expectation_value,
    real_expectation_value,
)
from schrodinger.grid import Grid1D

ArrayFloat = NDArray[np.float64]
ArrayComplex = NDArray[np.complex128]
Wavefunction = ArrayFloat | ArrayComplex


@dataclass(frozen=True, slots=True)
class ObservableResult:
    position: float
    position_squared: float
    momentum: float
    momentum_squared: float
    position_uncertainty: float
    momentum_uncertainty: float
    uncertainty_product: float


def validate_wavefunction_grid(
    wavefunction: Wavefunction,
    grid: Grid1D,
) -> None:
    if wavefunction.ndim != 1:
        raise ValueError(
            "wavefunction must be one-dimensional."
        )

    if wavefunction.size != grid.size:
        raise ValueError(
            "wavefunction size must match grid size."
        )

    if not np.all(np.isfinite(wavefunction)):
        raise ValueError(
            "wavefunction values must be finite."
        )


def position_expectation(
    wavefunction: Wavefunction,
    grid: Grid1D,
) -> float:
    validate_wavefunction_grid(
        wavefunction=wavefunction,
        grid=grid,
    )

    operator_wavefunction = (
        grid.values * wavefunction
    )

    return real_expectation_value(
        wavefunction=wavefunction,
        operator_wavefunction=operator_wavefunction,
        dx=grid.dx,
    )


def position_squared_expectation(
    wavefunction: Wavefunction,
    grid: Grid1D,
) -> float:
    validate_wavefunction_grid(
        wavefunction=wavefunction,
        grid=grid,
    )

    operator_wavefunction = (
        grid.values**2
        * wavefunction
    )

    return real_expectation_value(
        wavefunction=wavefunction,
        operator_wavefunction=operator_wavefunction,
        dx=grid.dx,
    )


def momentum_operator(
    wavefunction: Wavefunction,
    grid: Grid1D,
    hbar: float = 1.0,
) -> ArrayComplex:
    validate_wavefunction_grid(
        wavefunction=wavefunction,
        grid=grid,
    )

    if not np.isfinite(hbar):
        raise ValueError(
            "hbar must be finite."
        )

    if hbar <= 0.0:
        raise ValueError(
            "hbar must be positive."
        )

    derivative = np.zeros(
        grid.size,
        dtype=np.complex128,
    )

    derivative[1:-1] = (
        wavefunction[2:]
        - wavefunction[:-2]
    ) / (2.0 * grid.dx)

    result = (
        -1j
        * hbar
        * derivative
    )

    return np.asarray(
        result,
        dtype=np.complex128,
    )


def momentum_squared_operator(
    wavefunction: Wavefunction,
    grid: Grid1D,
    hbar: float = 1.0,
) -> ArrayComplex:
    validate_wavefunction_grid(
        wavefunction=wavefunction,
        grid=grid,
    )

    if not np.isfinite(hbar):
        raise ValueError(
            "hbar must be finite."
        )

    if hbar <= 0.0:
        raise ValueError(
            "hbar must be positive."
        )

    second_derivative = np.zeros(
        grid.size,
        dtype=np.complex128,
    )

    second_derivative[1:-1] = (
        wavefunction[2:]
        - 2.0 * wavefunction[1:-1]
        + wavefunction[:-2]
    ) / grid.dx**2

    result = (
        -hbar**2
        * second_derivative
    )

    return np.asarray(
        result,
        dtype=np.complex128,
    )


def momentum_expectation(
    wavefunction: Wavefunction,
    grid: Grid1D,
    hbar: float = 1.0,
) -> float:
    operated = momentum_operator(
        wavefunction=wavefunction,
        grid=grid,
        hbar=hbar,
    )

    value = expectation_value(
        wavefunction=wavefunction,
        operator_wavefunction=operated,
        dx=grid.dx,
    )

    if abs(value.imag) > 1e-8:
        raise ValueError(
            "momentum expectation has a significant "
            "imaginary component."
        )

    return float(value.real)


def momentum_squared_expectation(
    wavefunction: Wavefunction,
    grid: Grid1D,
    hbar: float = 1.0,
) -> float:
    operated = momentum_squared_operator(
        wavefunction=wavefunction,
        grid=grid,
        hbar=hbar,
    )

    value = expectation_value(
        wavefunction=wavefunction,
        operator_wavefunction=operated,
        dx=grid.dx,
    )

    if abs(value.imag) > 1e-8:
        raise ValueError(
            "momentum-squared expectation has a "
            "significant imaginary component."
        )

    return float(value.real)


def uncertainty(
    first_moment: float,
    second_moment: float,
) -> float:
    if not np.isfinite(first_moment):
        raise ValueError(
            "first_moment must be finite."
        )

    if not np.isfinite(second_moment):
        raise ValueError(
            "second_moment must be finite."
        )

    variance = (
        second_moment
        - first_moment**2
    )

    if variance < -1e-12:
        raise ValueError(
            "variance must not be negative."
        )

    variance = max(
        variance,
        0.0,
    )

    return float(
        np.sqrt(variance)
    )


def calculate_observables(
    wavefunction: Wavefunction,
    grid: Grid1D,
    hbar: float = 1.0,
) -> ObservableResult:
    x_mean = position_expectation(
        wavefunction=wavefunction,
        grid=grid,
    )

    x_squared_mean = (
        position_squared_expectation(
            wavefunction=wavefunction,
            grid=grid,
        )
    )

    p_mean = momentum_expectation(
        wavefunction=wavefunction,
        grid=grid,
        hbar=hbar,
    )

    p_squared_mean = (
        momentum_squared_expectation(
            wavefunction=wavefunction,
            grid=grid,
            hbar=hbar,
        )
    )

    delta_x = uncertainty(
        first_moment=x_mean,
        second_moment=x_squared_mean,
    )

    delta_p = uncertainty(
        first_moment=p_mean,
        second_moment=p_squared_mean,
    )

    return ObservableResult(
        position=x_mean,
        position_squared=x_squared_mean,
        momentum=p_mean,
        momentum_squared=p_squared_mean,
        position_uncertainty=delta_x,
        momentum_uncertainty=delta_p,
        uncertainty_product=(
            delta_x * delta_p
        ),
    )