import numpy as np
import pytest

from schrodinger.analysis.double_well_splitting import (
    double_well_splitting_scan,
)
from schrodinger.grid import Grid1D


@pytest.fixture
def grid() -> Grid1D:
    return Grid1D(
        -5.0,
        5.0,
        1601,
    )


def test_splitting_scan_returns_expected_shape(
    grid: Grid1D,
) -> None:
    coefficients = np.asarray(
        [0.5, 1.0, 2.0, 3.0],
        dtype=np.float64,
    )

    result = double_well_splitting_scan(
        grid=grid,
        coefficients=coefficients,
        b=1.5,
    )

    assert result.coefficients.shape == (4,)
    assert result.barrier_heights.shape == (4,)
    assert result.ground_energies.shape == (4,)
    assert result.first_excited_energies.shape == (4,)
    assert result.energy_splittings.shape == (4,)


def test_barrier_height_increases(
    grid: Grid1D,
) -> None:
    coefficients = np.asarray(
        [0.5, 1.0, 2.0, 3.0],
        dtype=np.float64,
    )

    result = double_well_splitting_scan(
        grid=grid,
        coefficients=coefficients,
        b=1.5,
    )

    assert np.all(
        np.diff(result.barrier_heights) > 0.0
    )


def test_all_energy_splittings_are_positive(
    grid: Grid1D,
) -> None:
    coefficients = np.asarray(
        [0.5, 1.0, 2.0, 3.0],
        dtype=np.float64,
    )

    result = double_well_splitting_scan(
        grid=grid,
        coefficients=coefficients,
        b=1.5,
    )

    assert np.all(
        result.energy_splittings > 0.0
    )


def test_splitting_decreases_with_barrier(
    grid: Grid1D,
) -> None:
    coefficients = np.asarray(
        [0.5, 1.0, 2.0, 3.0],
        dtype=np.float64,
    )

    result = double_well_splitting_scan(
        grid=grid,
        coefficients=coefficients,
        b=1.5,
    )

    assert np.all(
        np.diff(
            result.energy_splittings
        )
        < 0.0
    )


def test_first_excited_energy_above_ground(
    grid: Grid1D,
) -> None:
    coefficients = np.asarray(
        [0.5, 1.0, 2.0, 3.0],
        dtype=np.float64,
    )

    result = double_well_splitting_scan(
        grid=grid,
        coefficients=coefficients,
        b=1.5,
    )

    assert np.all(
        result.first_excited_energies
        > result.ground_energies
    )


def test_invalid_coefficients_rejected(
    grid: Grid1D,
) -> None:
    with pytest.raises(ValueError):
        double_well_splitting_scan(
            grid=grid,
            coefficients=np.asarray(
                [1.0],
                dtype=np.float64,
            ),
            b=1.5,
        )

    with pytest.raises(ValueError):
        double_well_splitting_scan(
            grid=grid,
            coefficients=np.asarray(
                [1.0, -2.0],
                dtype=np.float64,
            ),
            b=1.5,
        )

    with pytest.raises(ValueError):
        double_well_splitting_scan(
            grid=grid,
            coefficients=np.asarray(
                [2.0, 1.0],
                dtype=np.float64,
            ),
            b=1.5,
        )


def test_invalid_physical_parameters_rejected(
    grid: Grid1D,
) -> None:
    coefficients = np.asarray(
        [1.0, 2.0],
        dtype=np.float64,
    )

    with pytest.raises(ValueError):
        double_well_splitting_scan(
            grid=grid,
            coefficients=coefficients,
            b=0.0,
        )

    with pytest.raises(ValueError):
        double_well_splitting_scan(
            grid=grid,
            coefficients=coefficients,
            b=1.5,
            mass=0.0,
        )

    with pytest.raises(ValueError):
        double_well_splitting_scan(
            grid=grid,
            coefficients=coefficients,
            b=1.5,
            hbar=0.0,
        )