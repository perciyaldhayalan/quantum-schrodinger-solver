import numpy as np
import pytest

from schrodinger.potentials import (
    double_well,
    finite_square_well,
    harmonic_oscillator,
    infinite_square_well,
    rectangular_barrier,
)


def test_infinite_square_well() -> None:
    x = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])

    potential = infinite_square_well(
        x=x,
        left=-1.0,
        right=1.0,
    )

    assert np.isinf(potential[0])
    assert potential[1] == pytest.approx(0.0)
    assert potential[2] == pytest.approx(0.0)
    assert potential[3] == pytest.approx(0.0)
    assert np.isinf(potential[4])


def test_finite_square_well() -> None:
    x = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])

    potential = finite_square_well(
        x=x,
        left=-1.0,
        right=1.0,
        depth=5.0,
    )

    expected = np.array(
        [0.0, -5.0, -5.0, -5.0, 0.0],
    )

    np.testing.assert_allclose(
        potential,
        expected,
    )


def test_harmonic_oscillator() -> None:
    x = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])

    potential = harmonic_oscillator(
        x=x,
        omega=1.0,
        mass=1.0,
    )

    expected = np.array(
        [2.0, 0.5, 0.0, 0.5, 2.0],
    )

    np.testing.assert_allclose(
        potential,
        expected,
    )


def test_harmonic_oscillator_center() -> None:
    x = np.array([0.0, 1.0, 2.0])

    potential = harmonic_oscillator(
        x=x,
        omega=1.0,
        mass=1.0,
        center=1.0,
    )

    expected = np.array(
        [0.5, 0.0, 0.5],
    )

    np.testing.assert_allclose(
        potential,
        expected,
    )


def test_double_well() -> None:
    x = np.array(
        [-1.0, 0.0, 1.0],
    )

    potential = double_well(
        x=x,
        a=1.0,
        b=1.0,
    )

    expected = np.array(
        [0.0, 1.0, 0.0],
    )

    np.testing.assert_allclose(
        potential,
        expected,
    )


def test_double_well_is_symmetric() -> None:
    x = np.linspace(
        -5.0,
        5.0,
        101,
    )

    potential = double_well(
        x=x,
        a=1.0,
        b=2.0,
    )

    np.testing.assert_allclose(
        potential,
        potential[::-1],
        rtol=1e-12,
        atol=1e-12,
    )


def test_rectangular_barrier() -> None:
    x = np.array(
        [-2.0, -1.0, 0.0, 1.0, 2.0],
    )

    potential = rectangular_barrier(
        x=x,
        left=-1.0,
        right=1.0,
        height=10.0,
    )

    expected = np.array(
        [0.0, 10.0, 10.0, 10.0, 0.0],
    )

    np.testing.assert_allclose(
        potential,
        expected,
    )


def test_finite_well_requires_positive_depth() -> None:
    x = np.linspace(
        -1.0,
        1.0,
        5,
    )

    with pytest.raises(
        ValueError,
        match="depth must be positive",
    ):
        finite_square_well(
            x=x,
            left=-0.5,
            right=0.5,
            depth=0.0,
        )


def test_harmonic_oscillator_requires_positive_omega() -> None:
    x = np.linspace(
        -1.0,
        1.0,
        5,
    )

    with pytest.raises(
        ValueError,
        match="omega must be positive",
    ):
        harmonic_oscillator(
            x=x,
            omega=0.0,
        )


def test_harmonic_oscillator_requires_positive_mass() -> None:
    x = np.linspace(
        -1.0,
        1.0,
        5,
    )

    with pytest.raises(
        ValueError,
        match="mass must be positive",
    ):
        harmonic_oscillator(
            x=x,
            mass=0.0,
        )


def test_double_well_requires_positive_a() -> None:
    x = np.linspace(
        -1.0,
        1.0,
        5,
    )

    with pytest.raises(
        ValueError,
        match="a must be positive",
    ):
        double_well(
            x=x,
            a=0.0,
        )


def test_double_well_requires_positive_b() -> None:
    x = np.linspace(
        -1.0,
        1.0,
        5,
    )

    with pytest.raises(
        ValueError,
        match="b must be positive",
    ):
        double_well(
            x=x,
            b=0.0,
        )


def test_barrier_requires_positive_height() -> None:
    x = np.linspace(
        -1.0,
        1.0,
        5,
    )

    with pytest.raises(
        ValueError,
        match="height must be positive",
    ):
        rectangular_barrier(
            x=x,
            left=-0.5,
            right=0.5,
            height=0.0,
        )


@pytest.mark.parametrize(
    ("left", "right"),
    [
        (1.0, 1.0),
        (2.0, -2.0),
    ],
)
def test_infinite_well_rejects_invalid_bounds(
    left: float,
    right: float,
) -> None:
    x = np.linspace(
        -5.0,
        5.0,
        101,
    )

    with pytest.raises(
        ValueError,
        match="left must be smaller than right",
    ):
        infinite_square_well(
            x=x,
            left=left,
            right=right,
        )


@pytest.mark.parametrize(
    ("left", "right"),
    [
        (1.0, 1.0),
        (2.0, -2.0),
    ],
)
def test_finite_well_rejects_invalid_bounds(
    left: float,
    right: float,
) -> None:
    x = np.linspace(
        -5.0,
        5.0,
        101,
    )

    with pytest.raises(
        ValueError,
        match="left must be smaller than right",
    ):
        finite_square_well(
            x=x,
            left=left,
            right=right,
            depth=5.0,
        )


@pytest.mark.parametrize(
    ("left", "right"),
    [
        (1.0, 1.0),
        (2.0, -2.0),
    ],
)
def test_barrier_rejects_invalid_bounds(
    left: float,
    right: float,
) -> None:
    x = np.linspace(
        -5.0,
        5.0,
        101,
    )

    with pytest.raises(
        ValueError,
        match="left must be smaller than right",
    ):
        rectangular_barrier(
            x=x,
            left=left,
            right=right,
            height=10.0,
        )