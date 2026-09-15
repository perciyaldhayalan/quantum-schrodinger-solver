import numpy as np
import pytest

from schrodinger.grid import Grid1D
from schrodinger.potentials import (
    finite_square_well,
)
from schrodinger.stationary.bound_states import (
    extract_bound_states,
)
from schrodinger.stationary.finite_well_analytic import (
    finite_well_reference_states,
    finite_well_strength,
)
from schrodinger.stationary.solver import (
    solve_stationary,
)


def test_finite_well_strength() -> None:
    result = finite_well_strength(
        half_width=1.0,
        depth=10.0,
        mass=1.0,
        hbar=1.0,
    )

    assert result == pytest.approx(
        np.sqrt(20.0)
    )


def test_reference_states_exist() -> None:
    states = finite_well_reference_states(
        half_width=1.0,
        depth=10.0,
    )

    assert len(states) > 0


def test_reference_energies_are_bound() -> None:
    states = finite_well_reference_states(
        half_width=1.0,
        depth=10.0,
    )

    for state in states:
        assert -10.0 < state.energy < 0.0


def test_reference_states_alternate_parity() -> None:
    states = finite_well_reference_states(
        half_width=1.0,
        depth=10.0,
    )

    for index, state in enumerate(states):
        expected = (
            "even"
            if index % 2 == 0
            else "odd"
        )

        assert state.parity == expected


def test_reference_energies_are_sorted() -> None:
    states = finite_well_reference_states(
        half_width=1.0,
        depth=10.0,
    )

    energies = np.asarray(
        [
            state.energy
            for state in states
        ],
        dtype=np.float64,
    )

    assert np.all(
        np.diff(energies) > 0.0
    )


def test_numerical_bound_state_count_matches_reference() -> None:
    grid = Grid1D(
        -10.0,
        10.0,
        4001,
    )

    potential = finite_square_well(
        x=grid.interior,
        left=-1.0,
        right=1.0,
        depth=10.0,
    )

    numerical = solve_stationary(
        grid=grid,
        potential=potential,
        states=8,
        hbar=1.0,
        mass=1.0,
    )

    bound = extract_bound_states(
        states=numerical,
    )

    reference = finite_well_reference_states(
        half_width=1.0,
        depth=10.0,
        mass=1.0,
        hbar=1.0,
    )

    assert bound.count == len(reference)


def test_numerical_energies_are_consistent_with_reference() -> None:
    grid = Grid1D(
        -10.0,
        10.0,
        4001,
    )

    potential = finite_square_well(
        x=grid.interior,
        left=-1.0,
        right=1.0,
        depth=10.0,
    )

    numerical = solve_stationary(
        grid=grid,
        potential=potential,
        states=6,
        hbar=1.0,
        mass=1.0,
    )

    bound = extract_bound_states(
        states=numerical,
    )

    reference = finite_well_reference_states(
        half_width=1.0,
        depth=10.0,
        mass=1.0,
        hbar=1.0,
    )

    assert bound.count == len(reference)

    relative_errors = np.asarray(
        [
            abs(
                numerical_state.energy
                - reference_state.energy
            )
            / abs(reference_state.energy)
            for numerical_state, reference_state in zip(
                bound.states,
                reference,
                strict=True,
            )
        ],
        dtype=np.float64,
    )

    assert np.all(
        relative_errors < 1e-2
    )


def test_invalid_reference_parameters() -> None:
    with pytest.raises(ValueError):
        finite_well_reference_states(
            half_width=0.0,
            depth=10.0,
        )

    with pytest.raises(ValueError):
        finite_well_reference_states(
            half_width=1.0,
            depth=0.0,
        )

    with pytest.raises(ValueError):
        finite_well_reference_states(
            half_width=1.0,
            depth=10.0,
            mass=0.0,
        )

    with pytest.raises(ValueError):
        finite_well_reference_states(
            half_width=1.0,
            depth=10.0,
            hbar=0.0,
        )