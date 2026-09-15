import numpy as np
import pytest

from schrodinger.analysis.expectation import (
    expectation_value,
    real_expectation_value,
)


def test_identity_expectation_for_normalized_state() -> None:
    wavefunction = np.array(
        [
            0.0,
            1.0,
            1.0,
            0.0,
        ],
        dtype=np.float64,
    )

    dx = 0.5

    value = expectation_value(
        wavefunction=wavefunction,
        operator_wavefunction=wavefunction,
        dx=dx,
    )

    assert value.real == pytest.approx(
        1.0
    )

    assert value.imag == pytest.approx(
        0.0
    )


def test_complex_expectation_value() -> None:
    wavefunction = np.array(
        [
            1.0 + 0.0j,
            0.0 + 1.0j,
        ],
        dtype=np.complex128,
    )

    operated = wavefunction.copy()

    value = expectation_value(
        wavefunction=wavefunction,
        operator_wavefunction=operated,
        dx=0.5,
    )

    assert value.real == pytest.approx(
        1.0
    )


def test_real_expectation_value() -> None:
    wavefunction = np.array(
        [
            0.0,
            1.0,
            1.0,
            0.0,
        ],
        dtype=np.float64,
    )

    value = real_expectation_value(
        wavefunction=wavefunction,
        operator_wavefunction=wavefunction,
        dx=0.5,
    )

    assert value == pytest.approx(
        1.0
    )


def test_expectation_rejects_shape_mismatch() -> None:
    first = np.ones(
        5,
        dtype=np.float64,
    )

    second = np.ones(
        6,
        dtype=np.float64,
    )

    with pytest.raises(
        ValueError,
        match="same shape",
    ):
        expectation_value(
            wavefunction=first,
            operator_wavefunction=second,
            dx=0.1,
        )


def test_expectation_rejects_zero_dx() -> None:
    wavefunction = np.ones(
        5,
        dtype=np.float64,
    )

    with pytest.raises(
        ValueError,
        match="dx must be positive",
    ):
        expectation_value(
            wavefunction=wavefunction,
            operator_wavefunction=wavefunction,
            dx=0.0,
        )