import numpy as np
import pytest

from schrodinger.grid import Grid1D


def test_grid_creation() -> None:
    grid = Grid1D(-5.0, 5.0, 11)

    assert grid.x_min == -5.0
    assert grid.x_max == 5.0
    assert grid.points == 11
    assert grid.size == 11


def test_grid_values() -> None:
    grid = Grid1D(-2.0, 2.0, 5)

    expected = np.array(
        [-2.0, -1.0, 0.0, 1.0, 2.0],
        dtype=np.float64,
    )

    np.testing.assert_allclose(grid.values, expected)


def test_grid_spacing() -> None:
    grid = Grid1D(-5.0, 5.0, 11)

    assert grid.dx == pytest.approx(1.0)


def test_grid_spacing_formula() -> None:
    grid = Grid1D(-10.0, 10.0, 101)

    expected_dx = (
        grid.x_max - grid.x_min
    ) / (grid.points - 1)

    assert grid.dx == pytest.approx(expected_dx)


def test_grid_length() -> None:
    grid = Grid1D(-4.0, 6.0, 101)

    assert grid.length == pytest.approx(10.0)


def test_grid_boundaries() -> None:
    grid = Grid1D(-7.5, 3.5, 100)

    assert grid.left_boundary == pytest.approx(-7.5)
    assert grid.right_boundary == pytest.approx(3.5)


def test_grid_interior() -> None:
    grid = Grid1D(-2.0, 2.0, 5)

    expected = np.array(
        [-1.0, 0.0, 1.0],
        dtype=np.float64,
    )

    np.testing.assert_allclose(grid.interior, expected)


def test_grid_interior_size() -> None:
    grid = Grid1D(-5.0, 5.0, 101)

    assert grid.interior_size == 99


def test_grid_is_uniform() -> None:
    grid = Grid1D(-10.0, 10.0, 501)

    spacing = np.diff(grid.values)

    np.testing.assert_allclose(
        spacing,
        grid.dx,
        rtol=1e-12,
        atol=1e-12,
    )


def test_grid_rejects_equal_boundaries() -> None:
    with pytest.raises(
        ValueError,
        match="x_min must be smaller than x_max",
    ):
        Grid1D(5.0, 5.0, 100)


def test_grid_rejects_reversed_boundaries() -> None:
    with pytest.raises(
        ValueError,
        match="x_min must be smaller than x_max",
    ):
        Grid1D(5.0, -5.0, 100)


def test_grid_rejects_too_few_points() -> None:
    with pytest.raises(
        ValueError,
        match="points must be at least 3",
    ):
        Grid1D(-5.0, 5.0, 2)


def test_grid_rejects_non_integer_points() -> None:
    with pytest.raises(
        TypeError,
        match="points must be an integer",
    ):
        Grid1D(-5.0, 5.0, 100.5)


def test_grid_rejects_boolean_points() -> None:
    with pytest.raises(
        TypeError,
        match="points must be an integer",
    ):
        Grid1D(-5.0, 5.0, True)


def test_grid_rejects_non_finite_minimum() -> None:
    with pytest.raises(
        ValueError,
        match="x_min must be finite",
    ):
        Grid1D(float("-inf"), 5.0, 100)


def test_grid_rejects_non_finite_maximum() -> None:
    with pytest.raises(
        ValueError,
        match="x_max must be finite",
    ):
        Grid1D(-5.0, float("inf"), 100)