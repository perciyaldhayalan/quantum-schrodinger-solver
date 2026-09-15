import numpy as np
import pytest

from schrodinger.analysis.errors import (
    relative_error,
)
from schrodinger.grid import Grid1D
from schrodinger.stationary.analytic import (
    infinite_well_energy,
    infinite_well_wavefunction,
)
from schrodinger.stationary.solver import (
    solve_stationary,
)


def test_exact_ground_state_energy() -> None:
    energy = infinite_well_energy(
        quantum_number=1,
        length=1.0,
        hbar=1.0,
        mass=1.0,
    )

    assert energy == pytest.approx(
        np.pi**2 / 2.0,
    )


def test_exact_energy_scales_with_n_squared() -> None:
    ground = infinite_well_energy(
        quantum_number=1,
        length=1.0,
    )

    second = infinite_well_energy(
        quantum_number=2,
        length=1.0,
    )

    third = infinite_well_energy(
        quantum_number=3,
        length=1.0,
    )

    assert second / ground == pytest.approx(
        4.0
    )

    assert third / ground == pytest.approx(
        9.0
    )


def test_exact_wavefunction_boundaries() -> None:
    x = np.linspace(
        0.0,
        1.0,
        101,
        dtype=np.float64,
    )

    wavefunction = infinite_well_wavefunction(
        x=x,
        quantum_number=1,
        left=0.0,
        right=1.0,
    )

    assert wavefunction[0] == pytest.approx(
        0.0,
        abs=1e-14,
    )

    assert wavefunction[-1] == pytest.approx(
        0.0,
        abs=1e-14,
    )


def test_exact_wavefunction_normalization() -> None:
    x = np.linspace(
        0.0,
        1.0,
        10001,
        dtype=np.float64,
    )

    dx = float(
        x[1] - x[0]
    )

    wavefunction = infinite_well_wavefunction(
        x=x,
        quantum_number=3,
        left=0.0,
        right=1.0,
    )

    norm = float(
        np.sum(
            np.abs(wavefunction) ** 2
        )
        * dx
    )

    assert norm == pytest.approx(
        1.0,
        abs=1e-10,
    )


@pytest.mark.parametrize(
    "quantum_number",
    [
        1,
        2,
        3,
        4,
    ],
)
def test_numerical_infinite_well_energies(
    quantum_number: int,
) -> None:
    grid = Grid1D(
        0.0,
        1.0,
        1001,
    )

    potential = np.zeros(
        grid.interior_size,
        dtype=np.float64,
    )

    solutions = solve_stationary(
        grid=grid,
        potential=potential,
        states=4,
        hbar=1.0,
        mass=1.0,
    )

    numerical = solutions[
        quantum_number - 1
    ].energy

    exact = infinite_well_energy(
        quantum_number=quantum_number,
        length=grid.length,
        hbar=1.0,
        mass=1.0,
    )

    error = relative_error(
        numerical=numerical,
        exact=exact,
    )

    assert error < 1e-4


def test_ground_state_wavefunction_matches_exact() -> None:
    grid = Grid1D(
        0.0,
        1.0,
        1001,
    )

    potential = np.zeros(
        grid.interior_size,
        dtype=np.float64,
    )

    numerical_state = solve_stationary(
        grid=grid,
        potential=potential,
        states=1,
    )[0]

    exact = infinite_well_wavefunction(
        x=grid.values,
        quantum_number=1,
        left=0.0,
        right=1.0,
    )

    overlap = float(
        np.sum(
            numerical_state.wavefunction
            * exact
        )
        * grid.dx
    )

    assert abs(overlap) == pytest.approx(
        1.0,
        abs=1e-5,
    )