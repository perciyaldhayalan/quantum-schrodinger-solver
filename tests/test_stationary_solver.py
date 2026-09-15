import numpy as np
import pytest

from schrodinger.analysis.normalization import (
    probability_norm,
)
from schrodinger.grid import Grid1D
from schrodinger.stationary.solver import (
    solve_stationary,
)


def test_solver_returns_requested_number_of_states() -> None:
    grid = Grid1D(
        -5.0,
        5.0,
        201,
    )

    potential = np.zeros(
        grid.interior_size,
        dtype=np.float64,
    )

    solutions = solve_stationary(
        grid=grid,
        potential=potential,
        states=4,
    )

    assert len(solutions) == 4


def test_solver_sorts_energies() -> None:
    grid = Grid1D(
        -5.0,
        5.0,
        201,
    )

    potential = np.zeros(
        grid.interior_size,
        dtype=np.float64,
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
        ]
    )

    assert np.all(
        np.diff(energies) > 0.0
    )


def test_solver_normalizes_wavefunctions() -> None:
    grid = Grid1D(
        -5.0,
        5.0,
        201,
    )

    potential = np.zeros(
        grid.interior_size,
        dtype=np.float64,
    )

    solutions = solve_stationary(
        grid=grid,
        potential=potential,
        states=4,
    )

    for state in solutions:
        norm = probability_norm(
            wavefunction=state.wavefunction,
            dx=grid.dx,
        )

        assert norm == pytest.approx(
            1.0,
            abs=1e-10,
        )


def test_solver_applies_dirichlet_boundaries() -> None:
    grid = Grid1D(
        -5.0,
        5.0,
        201,
    )

    potential = np.zeros(
        grid.interior_size,
        dtype=np.float64,
    )

    solutions = solve_stationary(
        grid=grid,
        potential=potential,
        states=4,
    )

    for state in solutions:
        assert state.wavefunction[0] == pytest.approx(
            0.0
        )

        assert state.wavefunction[-1] == pytest.approx(
            0.0
        )


def test_solver_state_indices() -> None:
    grid = Grid1D(
        -5.0,
        5.0,
        201,
    )

    potential = np.zeros(
        grid.interior_size,
        dtype=np.float64,
    )

    solutions = solve_stationary(
        grid=grid,
        potential=potential,
        states=4,
    )

    indices = [
        state.index
        for state in solutions
    ]

    assert indices == [
        0,
        1,
        2,
        3,
    ]


def test_solver_rejects_zero_states() -> None:
    grid = Grid1D(
        -1.0,
        1.0,
        21,
    )

    potential = np.zeros(
        grid.interior_size,
        dtype=np.float64,
    )

    with pytest.raises(
        ValueError,
        match="states must be positive",
    ):
        solve_stationary(
            grid=grid,
            potential=potential,
            states=0,
        )


def test_solver_rejects_boolean_states() -> None:
    grid = Grid1D(
        -1.0,
        1.0,
        21,
    )

    potential = np.zeros(
        grid.interior_size,
        dtype=np.float64,
    )

    with pytest.raises(
        TypeError,
        match="states must be an integer",
    ):
        solve_stationary(
            grid=grid,
            potential=potential,
            states=True,
        )


def test_solver_rejects_too_many_states() -> None:
    grid = Grid1D(
        -1.0,
        1.0,
        5,
    )

    potential = np.zeros(
        grid.interior_size,
        dtype=np.float64,
    )

    with pytest.raises(
        ValueError,
        match="states must be smaller",
    ):
        solve_stationary(
            grid=grid,
            potential=potential,
            states=3,
        )