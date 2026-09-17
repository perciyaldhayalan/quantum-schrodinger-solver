import numpy as np
import pytest
from numpy.typing import NDArray

from schrodinger.grid import Grid1D
from schrodinger.time_dependent.momentum_space import (
    momentum_distribution,
)
from schrodinger.time_dependent.scattering import (
    extract_asymptotic_scattering,
)
from schrodinger.time_dependent.tunnelling_validation import (
    packet_averaged_transmission,
)
from schrodinger.time_dependent.wavepacket import (
    gaussian_wavepacket,
)

ArrayComplex = NDArray[np.complex128]


@pytest.fixture
def grid() -> Grid1D:
    return Grid1D(
        -30.0,
        30.0,
        3001,
    )


@pytest.fixture
def wavepacket(
    grid: Grid1D,
) -> ArrayComplex:
    return gaussian_wavepacket(
        grid=grid,
        center=-10.0,
        sigma=1.5,
        wave_number=2.0,
    )


def test_momentum_distribution_is_normalized(
    grid: Grid1D,
    wavepacket: ArrayComplex,
) -> None:
    distribution = momentum_distribution(
        wavefunction=wavepacket,
        grid=grid,
    )

    norm = (
        np.sum(
            distribution.probability_density
        )
        * distribution.dp
    )

    assert norm == pytest.approx(
        1.0,
        abs=1e-10,
    )


def test_momentum_distribution_peaks_near_expected_value(
    grid: Grid1D,
    wavepacket: ArrayComplex,
) -> None:
    distribution = momentum_distribution(
        wavefunction=wavepacket,
        grid=grid,
    )

    peak_index = int(
        np.argmax(
            distribution.probability_density
        )
    )

    peak_momentum = (
        distribution.momentum[
            peak_index
        ]
    )

    assert peak_momentum == pytest.approx(
        2.0,
        abs=0.12,
    )


def test_incident_packet_is_mostly_positive_momentum(
    grid: Grid1D,
    wavepacket: ArrayComplex,
) -> None:
    prediction = packet_averaged_transmission(
        wavefunction=wavepacket,
        grid=grid,
        barrier_height=5.0,
        barrier_width=1.0,
    )

    assert (
        prediction.positive_momentum_probability
        > 0.999
    )


def test_sub_barrier_packet_has_nonzero_transmission(
    grid: Grid1D,
    wavepacket: ArrayComplex,
) -> None:
    prediction = packet_averaged_transmission(
        wavefunction=wavepacket,
        grid=grid,
        barrier_height=5.0,
        barrier_width=1.0,
    )

    assert prediction.transmission > 0.0

    assert prediction.transmission < 1.0


def test_wider_barrier_reduces_packet_transmission(
    grid: Grid1D,
    wavepacket: ArrayComplex,
) -> None:
    narrow = packet_averaged_transmission(
        wavefunction=wavepacket,
        grid=grid,
        barrier_height=5.0,
        barrier_width=0.5,
    )

    wide = packet_averaged_transmission(
        wavefunction=wavepacket,
        grid=grid,
        barrier_height=5.0,
        barrier_width=1.5,
    )

    assert (
        wide.transmission
        < narrow.transmission
    )


def test_higher_barrier_reduces_packet_transmission(
    grid: Grid1D,
    wavepacket: ArrayComplex,
) -> None:
    low = packet_averaged_transmission(
        wavefunction=wavepacket,
        grid=grid,
        barrier_height=3.0,
        barrier_width=1.0,
    )

    high = packet_averaged_transmission(
        wavefunction=wavepacket,
        grid=grid,
        barrier_height=7.0,
        barrier_width=1.0,
    )

    assert (
        high.transmission
        < low.transmission
    )


def test_initial_packet_is_not_asymptotically_separated(
    grid: Grid1D,
    wavepacket: ArrayComplex,
) -> None:
    result = extract_asymptotic_scattering(
        wavefunction=wavepacket,
        grid=grid,
        barrier_left=-0.5,
        barrier_right=0.5,
        separation_tolerance=1e-3,
    )

    assert result.separated


def test_initial_probability_is_almost_all_reflection_region(
    grid: Grid1D,
    wavepacket: ArrayComplex,
) -> None:
    result = extract_asymptotic_scattering(
        wavefunction=wavepacket,
        grid=grid,
        barrier_left=-0.5,
        barrier_right=0.5,
    )

    assert result.reflection > 0.999

    assert result.transmission < 1e-8


def test_asymptotic_total_probability_is_normalized(
    grid: Grid1D,
    wavepacket: ArrayComplex,
) -> None:
    result = extract_asymptotic_scattering(
        wavefunction=wavepacket,
        grid=grid,
        barrier_left=-0.5,
        barrier_right=0.5,
    )

    assert (
        result.total_probability
        == pytest.approx(
            1.0,
            abs=1e-10,
        )
    )


def test_invalid_barrier_width_rejected(
    grid: Grid1D,
    wavepacket: ArrayComplex,
) -> None:
    with pytest.raises(ValueError):
        packet_averaged_transmission(
            wavefunction=wavepacket,
            grid=grid,
            barrier_height=5.0,
            barrier_width=0.0,
        )


def test_invalid_separation_tolerance_rejected(
    grid: Grid1D,
    wavepacket: ArrayComplex,
) -> None:
    with pytest.raises(ValueError):
        extract_asymptotic_scattering(
            wavefunction=wavepacket,
            grid=grid,
            barrier_left=-0.5,
            barrier_right=0.5,
            separation_tolerance=0.0,
        )