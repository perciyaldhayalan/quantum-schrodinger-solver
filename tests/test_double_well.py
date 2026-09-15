import numpy as np
import pytest

from schrodinger.grid import Grid1D
from schrodinger.potentials import (
    double_well,
)
from schrodinger.stationary.double_well import (
    analyze_double_well,
    classify_parity,
    energy_splitting,
    parity_overlap,
)
from schrodinger.stationary.solver import (
    solve_stationary,
)


@pytest.fixture
def double_well_system():
    grid = Grid1D(
        -5.0,
        5.0,
        2001,
    )

    potential = double_well(
        x=grid.interior,
        a=1.0,
        b=1.5,
    )

    states = solve_stationary(
        grid=grid,
        potential=potential,
        states=6,
        hbar=1.0,
        mass=1.0,
    )

    return grid, states


def test_energy_splitting_is_positive(
    double_well_system,
) -> None:
    _, states = double_well_system

    splitting = energy_splitting(
        ground_state=states[0],
        first_excited_state=states[1],
    )

    assert splitting > 0.0


def test_ground_state_is_even(
    double_well_system,
) -> None:
    grid, states = double_well_system

    parity = classify_parity(
        wavefunction=states[0].wavefunction,
        grid=grid,
    )

    assert parity == "even"


def test_first_excited_state_is_odd(
    double_well_system,
) -> None:
    grid, states = double_well_system

    parity = classify_parity(
        wavefunction=states[1].wavefunction,
        grid=grid,
    )

    assert parity == "odd"


def test_ground_parity_overlap_is_positive(
    double_well_system,
) -> None:
    grid, states = double_well_system

    overlap = parity_overlap(
        wavefunction=states[0].wavefunction,
        grid=grid,
    )

    assert overlap == pytest.approx(
        1.0,
        abs=1e-4,
    )


def test_first_excited_parity_overlap_is_negative(
    double_well_system,
) -> None:
    grid, states = double_well_system

    overlap = parity_overlap(
        wavefunction=states[1].wavefunction,
        grid=grid,
    )

    assert overlap == pytest.approx(
        -1.0,
        abs=1e-4,
    )


def test_double_well_analysis(
    double_well_system,
) -> None:
    grid, states = double_well_system

    result = analyze_double_well(
        states=states,
        grid=grid,
    )

    assert (
        result.first_excited_energy
        > result.ground_energy
    )

    assert result.energy_splitting > 0.0
    assert result.ground_parity == "even"
    assert result.first_excited_parity == "odd"


def test_symmetric_probability_density(
    double_well_system,
) -> None:
    _, states = double_well_system

    ground_density = (
        np.abs(states[0].wavefunction) ** 2
    )

    first_density = (
        np.abs(states[1].wavefunction) ** 2
    )

    np.testing.assert_allclose(
        ground_density,
        ground_density[::-1],
        rtol=1e-5,
        atol=1e-5,
    )

    np.testing.assert_allclose(
        first_density,
        first_density[::-1],
        rtol=1e-5,
        atol=1e-5,
    )