import numpy as np
import pytest

from schrodinger.grid import Grid1D
from schrodinger.potentials import (
    harmonic_oscillator,
)
from schrodinger.stationary.observables import (
    calculate_observables,
    position_expectation,
    uncertainty,
)
from schrodinger.stationary.solver import (
    solve_stationary,
)


@pytest.fixture
def oscillator_ground_state() -> tuple[
    Grid1D,
    np.ndarray,
]:
    grid = Grid1D(
        -8.0,
        8.0,
        1601,
    )

    potential = harmonic_oscillator(
        x=grid.interior,
        omega=1.0,
        mass=1.0,
    )

    state = solve_stationary(
        grid=grid,
        potential=potential,
        states=1,
        hbar=1.0,
        mass=1.0,
    )[0]

    return (
        grid,
        state.wavefunction,
    )


def test_ground_state_position_expectation(
    oscillator_ground_state: tuple[
        Grid1D,
        np.ndarray,
    ],
) -> None:
    grid, wavefunction = (
        oscillator_ground_state
    )

    value = position_expectation(
        wavefunction=wavefunction,
        grid=grid,
    )

    assert value == pytest.approx(
        0.0,
        abs=1e-10,
    )


def test_ground_state_position_uncertainty(
    oscillator_ground_state: tuple[
        Grid1D,
        np.ndarray,
    ],
) -> None:
    grid, wavefunction = (
        oscillator_ground_state
    )

    result = calculate_observables(
        wavefunction=wavefunction,
        grid=grid,
        hbar=1.0,
    )

    expected = 1.0 / np.sqrt(2.0)

    assert result.position_uncertainty == pytest.approx(
        expected,
        rel=1e-4,
    )


def test_ground_state_momentum_expectation(
    oscillator_ground_state: tuple[
        Grid1D,
        np.ndarray,
    ],
) -> None:
    grid, wavefunction = (
        oscillator_ground_state
    )

    result = calculate_observables(
        wavefunction=wavefunction,
        grid=grid,
        hbar=1.0,
    )

    assert result.momentum == pytest.approx(
        0.0,
        abs=1e-10,
    )


def test_ground_state_momentum_uncertainty(
    oscillator_ground_state: tuple[
        Grid1D,
        np.ndarray,
    ],
) -> None:
    grid, wavefunction = (
        oscillator_ground_state
    )

    result = calculate_observables(
        wavefunction=wavefunction,
        grid=grid,
        hbar=1.0,
    )

    expected = 1.0 / np.sqrt(2.0)

    assert result.momentum_uncertainty == pytest.approx(
        expected,
        rel=1e-4,
    )


def test_ground_state_minimum_uncertainty(
    oscillator_ground_state: tuple[
        Grid1D,
        np.ndarray,
    ],
) -> None:
    grid, wavefunction = (
        oscillator_ground_state
    )

    result = calculate_observables(
        wavefunction=wavefunction,
        grid=grid,
        hbar=1.0,
    )

    assert result.uncertainty_product == pytest.approx(
        0.5,
        rel=1e-4,
    )


def test_uncertainty() -> None:
    result = uncertainty(
        first_moment=2.0,
        second_moment=5.0,
    )

    assert result == pytest.approx(
        1.0
    )


def test_uncertainty_rejects_negative_variance() -> None:
    with pytest.raises(
        ValueError,
        match="variance must not be negative",
    ):
        uncertainty(
            first_moment=2.0,
            second_moment=3.0,
        )