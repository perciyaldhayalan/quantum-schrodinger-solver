import numpy as np
import pytest

from schrodinger.analysis.errors import (
    absolute_error,
    relative_error,
    relative_errors,
)


def test_absolute_error() -> None:
    error = absolute_error(
        numerical=9.8,
        exact=10.0,
    )

    assert error == pytest.approx(0.2)


def test_relative_error() -> None:
    error = relative_error(
        numerical=9.0,
        exact=10.0,
    )

    assert error == pytest.approx(0.1)


def test_relative_errors_array() -> None:
    numerical = np.array(
        [9.0, 18.0, 27.0],
        dtype=np.float64,
    )

    exact = np.array(
        [10.0, 20.0, 30.0],
        dtype=np.float64,
    )

    errors = relative_errors(
        numerical=numerical,
        exact=exact,
    )

    expected = np.array(
        [0.1, 0.1, 0.1],
        dtype=np.float64,
    )

    np.testing.assert_allclose(
        errors,
        expected,
    )


def test_relative_error_rejects_zero_exact() -> None:
    with pytest.raises(
        ValueError,
        match="exact value must be non-zero",
    ):
        relative_error(
            numerical=1.0,
            exact=0.0,
        )


def test_relative_errors_reject_shape_mismatch() -> None:
    numerical = np.array(
        [1.0, 2.0],
        dtype=np.float64,
    )

    exact = np.array(
        [1.0, 2.0, 3.0],
        dtype=np.float64,
    )

    with pytest.raises(
        ValueError,
        match="same shape",
    ):
        relative_errors(
            numerical=numerical,
            exact=exact,
        )