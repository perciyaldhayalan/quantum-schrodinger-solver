import numpy as np
import pytest

from schrodinger.grid import Grid1D
from schrodinger.potentials import (
    finite_square_well,
)
from schrodinger.stationary.bound_states import (
    exterior_probability,
    extract_bound_states,
    interior_probability,
)
from schrodinger.stationary.solver import (
    solve_stationary,
)


@pytest.fixture
def finite_well_system() -> tuple[
    Grid1D,
    list,
]:
    grid = Grid1D(
        -10.0,
        10.0,
        2001,
    )

    potential = finite_square_well(
        x=grid.interior,
        left=-1.0,
        right=1.0,
        depth=10.0,
    )

    states = solve_stationary(
        grid=grid,
        potential=potential,
        states=8,
        hbar=1.0,
        mass=1.0,
    )

    return grid, states


def test_finite_well_has_bound_states(
    finite_well_system: tuple[
        Grid1D,
        list,
    ],
) -> None:
    _, states = finite_well_system

    bound = extract_bound_states(
        states=states,
    )

    assert bound.count > 0


def test_bound_state_energies_are_negative(
    finite_well_system: tuple[
        Grid1D,
        list,
    ],
) -> None:
    _, states = finite_well_system

    bound = extract_bound_states(
        states=states,
    )

    assert np.all(
        bound.energies < 0.0
    )


def test_bound_state_energies_are_above_well_bottom(
    finite_well_system: tuple[
        Grid1D,
        list,
    ],
) -> None:
    _, states = finite_well_system

    bound = extract_bound_states(
        states=states,
    )

    assert np.all(
        bound.energies > -10.0
    )


def test_ground_state_penetrates_outside_well(
    finite_well_system: tuple[
        Grid1D,
        list,
    ],
) -> None:
    grid, states = finite_well_system

    bound = extract_bound_states(
        states=states,
    )

    ground_state = bound.states[0]

    probability = exterior_probability(
        state=ground_state,
        grid=grid,
        left=-1.0,
        right=1.0,
    )

    assert probability > 0.0
    assert probability < 1.0


def test_probability_is_mostly_inside_well(
    finite_well_system: tuple[
        Grid1D,
        list,
    ],
) -> None:
    grid, states = finite_well_system

    bound = extract_bound_states(
        states=states,
    )

    ground_state = bound.states[0]

    inside = interior_probability(
        state=ground_state,
        grid=grid,
        left=-1.0,
        right=1.0,
    )

    outside = exterior_probability(
        state=ground_state,
        grid=grid,
        left=-1.0,
        right=1.0,
    )

    assert inside > outside


def test_inside_and_outside_probability_sum_to_one(
    finite_well_system: tuple[
        Grid1D,
        list,
    ],
) -> None:
    grid, states = finite_well_system

    bound = extract_bound_states(
        states=states,
    )

    ground_state = bound.states[0]

    inside = interior_probability(
        state=ground_state,
        grid=grid,
        left=-1.0,
        right=1.0,
    )

    outside = exterior_probability(
        state=ground_state,
        grid=grid,
        left=-1.0,
        right=1.0,
    )

    assert inside + outside == pytest.approx(
        1.0,
        abs=2e-3,
    )


def test_ground_state_is_even(
    finite_well_system: tuple[
        Grid1D,
        list,
    ],
) -> None:
    _, states = finite_well_system

    bound = extract_bound_states(
        states=states,
    )

    wavefunction = (
        bound.states[0].wavefunction
    )

    np.testing.assert_allclose(
        wavefunction,
        wavefunction[::-1],
        rtol=1e-6,
        atol=1e-6,
    )


def test_first_excited_bound_state_is_odd(
    finite_well_system: tuple[
        Grid1D,
        list,
    ],
) -> None:
    _, states = finite_well_system

    bound = extract_bound_states(
        states=states,
    )

    assert bound.count >= 2

    wavefunction = (
        bound.states[1].wavefunction
    )

    np.testing.assert_allclose(
        wavefunction,
        -wavefunction[::-1],
        rtol=1e-6,
        atol=1e-6,
    )