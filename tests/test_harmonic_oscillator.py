import numpy as np
import pytest

from schrodinger.analysis.errors import (
    relative_error,
)
from schrodinger.grid import Grid1D
from schrodinger.potentials import (
    harmonic_oscillator,
)
from schrodinger.stationary.analytic import (
    harmonic_oscillator_energy,
)
from schrodinger.stationary.solver import (
    solve_stationary,
)


def test_exact_ground_state_energy() -> None:
    energy = harmonic_oscillator_energy(
        quantum_number=0,
        omega=1.0,
        hbar=1.0,
    )

    assert energy == pytest.approx(0.5)


@pytest.mark.parametrize(
    ("quantum_number", "expected"),
    [
        (0, 0.5),
        (1, 1.5),
        (2, 2.5),
        (3, 3.5),
        (4, 4.5),
    ],
)
def test_exact_harmonic_oscillator_energies(
    quantum_number: int,
    expected: float,
) -> None:
    energy = harmonic_oscillator_energy(
        quantum_number=quantum_number,
    )

    assert energy == pytest.approx(
        expected
    )


@pytest.mark.parametrize(
    "quantum_number",
    [
        0,
        1,
        2,
        3,
        4,
    ],
)
def test_numerical_harmonic_oscillator_energies(
    quantum_number: int,
) -> None:
    grid = Grid1D(
        -8.0,
        8.0,
        1201,
    )

    potential = harmonic_oscillator(
        x=grid.interior,
        omega=1.0,
        mass=1.0,
        center=0.0,
    )

    solutions = solve_stationary(
        grid=grid,
        potential=potential,
        states=5,
        hbar=1.0,
        mass=1.0,
    )

    numerical = solutions[
        quantum_number
    ].energy

    exact = harmonic_oscillator_energy(
        quantum_number=quantum_number,
        omega=1.0,
        hbar=1.0,
    )

    error = relative_error(
        numerical=numerical,
        exact=exact,
    )

    assert error < 1e-4


def test_energy_spacing_is_hbar_omega() -> None:
    grid = Grid1D(
        -8.0,
        8.0,
        1201,
    )

    potential = harmonic_oscillator(
        x=grid.interior,
        omega=1.0,
        mass=1.0,
    )

    solutions = solve_stationary(
        grid=grid,
        potential=potential,
        states=5,
    )

    energies = np.array(
        [
            state.energy
            for state in solutions
        ],
        dtype=np.float64,
    )

    spacings = np.diff(energies)

    np.testing.assert_allclose(
        spacings,
        np.ones(4),
        rtol=1e-4,
        atol=1e-4,
    )


def test_ground_state_is_even() -> None:
    grid = Grid1D(
        -8.0,
        8.0,
        1201,
    )

    potential = harmonic_oscillator(
        x=grid.interior,
    )

    ground_state = solve_stationary(
        grid=grid,
        potential=potential,
        states=1,
    )[0]

    np.testing.assert_allclose(
        ground_state.wavefunction,
        ground_state.wavefunction[::-1],
        rtol=1e-7,
        atol=1e-7,
    )


def test_first_excited_state_has_odd_parity() -> None:
    grid = Grid1D(
        -8.0,
        8.0,
        1201,
    )

    potential = harmonic_oscillator(
        x=grid.interior,
    )

    first_excited = solve_stationary(
        grid=grid,
        potential=potential,
        states=2,
    )[1]

    np.testing.assert_allclose(
        first_excited.wavefunction,
        -first_excited.wavefunction[::-1],
        rtol=1e-7,
        atol=1e-7,
    )


def test_rejects_negative_quantum_number() -> None:
    with pytest.raises(
        ValueError,
        match="quantum_number must be non-negative",
    ):
        harmonic_oscillator_energy(
            quantum_number=-1,
        )


def test_rejects_boolean_quantum_number() -> None:
    with pytest.raises(
        TypeError,
        match="quantum_number must be an integer",
    ):
        harmonic_oscillator_energy(
            quantum_number=True,
        )


def test_rejects_non_positive_omega() -> None:
    with pytest.raises(
        ValueError,
        match="omega must be positive",
    ):
        harmonic_oscillator_energy(
            quantum_number=0,
            omega=0.0,
        )