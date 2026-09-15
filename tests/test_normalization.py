import numpy as np
import pytest

from schrodinger.analysis.normalization import (
    normalize_wavefunction,
    probability_norm,
)


def test_probability_norm() -> None:
    wavefunction = np.ones(
        4,
        dtype=np.float64,
    )

    norm = probability_norm(
        wavefunction=wavefunction,
        dx=0.25,
    )

    assert norm == pytest.approx(1.0)


def test_normalize_wavefunction() -> None:
    wavefunction = np.array(
        [1.0, 1.0, 1.0, 1.0],
        dtype=np.float64,
    )

    normalized = normalize_wavefunction(
        wavefunction=wavefunction,
        dx=0.5,
    )

    norm = probability_norm(
        wavefunction=normalized,
        dx=0.5,
    )

    assert norm == pytest.approx(
        1.0,
        abs=1e-12,
    )


def test_complex_wavefunction_norm() -> None:
    wavefunction = np.array(
        [
            1.0 + 1.0j,
            1.0 - 1.0j,
        ],
        dtype=np.complex128,
    )

    norm = probability_norm(
        wavefunction=wavefunction,
        dx=0.25,
    )

    assert norm == pytest.approx(1.0)


def test_normalization_preserves_complex_dtype() -> None:
    wavefunction = np.array(
        [
            1.0 + 1.0j,
            2.0 - 1.0j,
        ],
        dtype=np.complex128,
    )

    normalized = normalize_wavefunction(
        wavefunction=wavefunction,
        dx=0.1,
    )

    assert np.iscomplexobj(normalized)


def test_probability_norm_rejects_zero_dx() -> None:
    wavefunction = np.ones(
        5,
        dtype=np.float64,
    )

    with pytest.raises(
        ValueError,
        match="dx must be positive",
    ):
        probability_norm(
            wavefunction=wavefunction,
            dx=0.0,
        )


def test_probability_norm_rejects_negative_dx() -> None:
    wavefunction = np.ones(
        5,
        dtype=np.float64,
    )

    with pytest.raises(
        ValueError,
        match="dx must be positive",
    ):
        probability_norm(
            wavefunction=wavefunction,
            dx=-0.1,
        )


def test_probability_norm_rejects_non_finite_dx() -> None:
    wavefunction = np.ones(
        5,
        dtype=np.float64,
    )

    with pytest.raises(
        ValueError,
        match="dx must be finite",
    ):
        probability_norm(
            wavefunction=wavefunction,
            dx=np.inf,
        )


def test_normalization_rejects_zero_wavefunction() -> None:
    wavefunction = np.zeros(
        5,
        dtype=np.float64,
    )

    with pytest.raises(
        ValueError,
        match="wavefunction norm must be positive",
    ):
        normalize_wavefunction(
            wavefunction=wavefunction,
            dx=0.1,
        )