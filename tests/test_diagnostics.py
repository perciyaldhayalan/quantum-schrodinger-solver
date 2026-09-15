import numpy as np
import pytest

from schrodinger.analysis.diagnostics import (
    orthogonality_matrix,
    satisfies_heisenberg,
    state_overlap,
)
from schrodinger.grid import Grid1D
from schrodinger.potentials import (
    harmonic_oscillator,
)
from schrodinger.stationary.solver import (
    solve_stationary,
)


def test_state_overlap_for_orthogonal_vectors() -> None:
    first = np.array(
        [
            1.0,
            0.0,
        ],
        dtype=np.float64,
    )

    second = np.array(
        [
            0.0,
            1.0,
        ],
        dtype=np.float64,
    )

    overlap = state_overlap(
        first=first,
        second=second,
        dx=1.0,
    )

    assert overlap == pytest.approx(
        0.0
    )


def test_stationary_states_are_orthonormal() -> None:
    grid = Grid1D(
        -8.0,
        8.0,
        1201,
    )

    potential = harmonic_oscillator(
        x=grid.interior,
    )

    solutions = solve_stationary(
        grid=grid,
        potential=potential,
        states=4,
    )

    wavefunctions = np.stack(
        [
            state.wavefunction
            for state in solutions
        ]
    )

    matrix = orthogonality_matrix(
        wavefunctions=wavefunctions,
        grid=grid,
    )

    expected = np.eye(
        4,
        dtype=np.complex128,
    )

    np.testing.assert_allclose(
        matrix,
        expected,
        rtol=1e-9,
        atol=1e-9,
    )


def test_heisenberg_equality() -> None:
    delta = 1.0 / np.sqrt(2.0)

    assert satisfies_heisenberg(
        delta_x=delta,
        delta_p=delta,
        hbar=1.0,
    )


def test_heisenberg_larger_product() -> None:
    assert satisfies_heisenberg(
        delta_x=1.0,
        delta_p=1.0,
        hbar=1.0,
    )


def test_heisenberg_violation() -> None:
    assert not satisfies_heisenberg(
        delta_x=0.1,
        delta_p=0.1,
        hbar=1.0,
    )