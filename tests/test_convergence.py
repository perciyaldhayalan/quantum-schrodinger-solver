import numpy as np
import pytest

from schrodinger.analysis.convergence import (
    estimate_convergence_order,
    infinite_well_convergence,
)


def test_estimate_second_order_convergence() -> None:
    spacings = np.array(
        [
            0.1,
            0.05,
            0.025,
            0.0125,
        ],
        dtype=np.float64,
    )

    errors = spacings**2

    order = estimate_convergence_order(
        grid_spacings=spacings,
        errors=errors,
    )

    assert order == pytest.approx(
        2.0,
        abs=1e-12,
    )


def test_infinite_well_error_decreases() -> None:
    point_counts = np.array(
        [
            100,
            200,
            400,
            800,
        ],
        dtype=np.int64,
    )

    result = infinite_well_convergence(
        point_counts=point_counts,
    )

    differences = np.diff(
        result.absolute_errors
    )

    assert np.all(
        differences < 0.0
    )


def test_infinite_well_relative_error_decreases() -> None:
    point_counts = np.array(
        [
            100,
            200,
            400,
            800,
        ],
        dtype=np.int64,
    )

    result = infinite_well_convergence(
        point_counts=point_counts,
    )

    differences = np.diff(
        result.relative_errors
    )

    assert np.all(
        differences < 0.0
    )


def test_infinite_well_has_second_order_convergence() -> None:
    point_counts = np.array(
        [
            100,
            200,
            400,
            800,
            1600,
        ],
        dtype=np.int64,
    )

    result = infinite_well_convergence(
        point_counts=point_counts,
    )

    assert result.observed_order == pytest.approx(
        2.0,
        abs=0.05,
    )


def test_numerical_energy_approaches_exact_energy() -> None:
    point_counts = np.array(
        [
            100,
            200,
            400,
            800,
        ],
        dtype=np.int64,
    )

    result = infinite_well_convergence(
        point_counts=point_counts,
    )

    initial_error = abs(
        result.numerical_energies[0]
        - result.exact_energy
    )

    final_error = abs(
        result.numerical_energies[-1]
        - result.exact_energy
    )

    assert final_error < initial_error


def test_convergence_result_shapes() -> None:
    point_counts = np.array(
        [
            100,
            200,
            400,
        ],
        dtype=np.int64,
    )

    result = infinite_well_convergence(
        point_counts=point_counts,
    )

    expected_shape = (
        point_counts.size,
    )

    assert result.grid_points.shape == expected_shape
    assert result.grid_spacings.shape == expected_shape
    assert (
        result.numerical_energies.shape
        == expected_shape
    )
    assert (
        result.absolute_errors.shape
        == expected_shape
    )
    assert (
        result.relative_errors.shape
        == expected_shape
    )


def test_rejects_single_convergence_point() -> None:
    spacings = np.array(
        [0.1],
        dtype=np.float64,
    )

    errors = np.array(
        [0.01],
        dtype=np.float64,
    )

    with pytest.raises(
        ValueError,
        match="at least two data points",
    ):
        estimate_convergence_order(
            grid_spacings=spacings,
            errors=errors,
        )


def test_rejects_non_positive_errors() -> None:
    spacings = np.array(
        [
            0.1,
            0.05,
        ],
        dtype=np.float64,
    )

    errors = np.array(
        [
            0.01,
            0.0,
        ],
        dtype=np.float64,
    )

    with pytest.raises(
        ValueError,
        match="errors must be positive",
    ):
        estimate_convergence_order(
            grid_spacings=spacings,
            errors=errors,
        )


def test_rejects_invalid_grid_sizes() -> None:
    point_counts = np.array(
        [
            2,
            100,
        ],
        dtype=np.int64,
    )

    with pytest.raises(
        ValueError,
        match="at least 3 points",
    ):
        infinite_well_convergence(
            point_counts=point_counts,
        )