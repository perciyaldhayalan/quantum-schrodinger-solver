import numpy as np
import pytest
from numpy.typing import NDArray

from schrodinger.grid import Grid1D
from schrodinger.time_dependent.wavepacket import (
    analyze_wavepacket,
    gaussian_probability_density,
    gaussian_wavepacket,
    mean_kinetic_energy,
)

ArrayComplex = NDArray[np.complex128]


@pytest.fixture
def grid() -> Grid1D:
    return Grid1D(
        -30.0,
        30.0,
        6001,
    )


@pytest.fixture
def wavepacket(
    grid: Grid1D,
) -> ArrayComplex:
    return gaussian_wavepacket(
        grid=grid,
        center=-8.0,
        sigma=1.5,
        wave_number=2.0,
    )


def test_gaussian_wavepacket_shape(
    grid: Grid1D,
) -> None:
    wavefunction = gaussian_wavepacket(
        grid=grid,
        center=-8.0,
        sigma=1.5,
        wave_number=2.0,
    )

    assert wavefunction.shape == (
        grid.size,
    )

    assert np.iscomplexobj(
        wavefunction
    )


def test_gaussian_wavepacket_is_normalized(
    grid: Grid1D,
    wavepacket: ArrayComplex,
) -> None:
    result = analyze_wavepacket(
        wavefunction=wavepacket,
        grid=grid,
    )

    assert result.norm == pytest.approx(
        1.0,
        abs=1e-10,
    )


def test_probability_density_is_non_negative(
    wavepacket: ArrayComplex,
) -> None:
    density = gaussian_probability_density(
        wavefunction=wavepacket,
    )

    assert np.all(
        density >= 0.0
    )


def test_position_expectation_matches_center(
    grid: Grid1D,
    wavepacket: ArrayComplex,
) -> None:
    result = analyze_wavepacket(
        wavefunction=wavepacket,
        grid=grid,
    )

    assert result.position == pytest.approx(
        -8.0,
        abs=1e-4,
    )


def test_momentum_expectation_matches_hbar_k(
    grid: Grid1D,
    wavepacket: ArrayComplex,
) -> None:
    result = analyze_wavepacket(
        wavefunction=wavepacket,
        grid=grid,
        hbar=1.0,
    )

    assert result.momentum == pytest.approx(
        2.0,
        rel=2e-4,
    )


def test_position_uncertainty_matches_sigma(
    grid: Grid1D,
    wavepacket: ArrayComplex,
) -> None:
    result = analyze_wavepacket(
        wavefunction=wavepacket,
        grid=grid,
    )

    assert (
        result.position_uncertainty
        == pytest.approx(
            1.5,
            rel=1e-4,
        )
    )


def test_momentum_uncertainty_matches_gaussian_result(
    grid: Grid1D,
    wavepacket: ArrayComplex,
) -> None:
    result = analyze_wavepacket(
        wavefunction=wavepacket,
        grid=grid,
        hbar=1.0,
    )

    expected = (
        1.0
        / (
            2.0
            * 1.5
        )
    )

    assert (
        result.momentum_uncertainty
        == pytest.approx(
            expected,
            rel=3e-3,
        )
    )


def test_minimum_uncertainty_product(
    grid: Grid1D,
    wavepacket: ArrayComplex,
) -> None:
    result = analyze_wavepacket(
        wavefunction=wavepacket,
        grid=grid,
        hbar=1.0,
    )

    assert (
        result.uncertainty_product
        == pytest.approx(
            0.5,
            rel=3e-3,
        )
    )


def test_mean_kinetic_energy_matches_analytic_value(
    grid: Grid1D,
    wavepacket: ArrayComplex,
) -> None:
    result = analyze_wavepacket(
        wavefunction=wavepacket,
        grid=grid,
        mass=1.0,
        hbar=1.0,
    )

    sigma = 1.5
    wave_number = 2.0

    expected_p_squared = (
        wave_number**2
        + 1.0
        / (
            4.0
            * sigma**2
        )
    )

    expected_energy = (
        expected_p_squared
        / 2.0
    )

    assert (
        result.mean_kinetic_energy
        == pytest.approx(
            expected_energy,
            rel=5e-4,
        )
    )


def test_invalid_sigma_rejected(
    grid: Grid1D,
) -> None:
    with pytest.raises(ValueError):
        gaussian_wavepacket(
            grid=grid,
            center=0.0,
            sigma=0.0,
            wave_number=1.0,
        )


def test_center_outside_grid_rejected(
    grid: Grid1D,
) -> None:
    with pytest.raises(ValueError):
        gaussian_wavepacket(
            grid=grid,
            center=40.0,
            sigma=1.0,
            wave_number=1.0,
        )


def test_invalid_mass_rejected() -> None:
    with pytest.raises(ValueError):
        mean_kinetic_energy(
            momentum=1.0,
            momentum_squared=2.0,
            mass=0.0,
        )