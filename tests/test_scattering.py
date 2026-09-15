import numpy as np
import pytest
from numpy.typing import NDArray

from schrodinger.grid import Grid1D
from schrodinger.time_dependent.scattering import (
    rectangular_barrier_on_interior,
    region_probability,
    scattering_probabilities,
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


def test_rectangular_barrier_shape(
    grid: Grid1D,
) -> None:
    potential = rectangular_barrier_on_interior(
        grid=grid,
        barrier_left=-0.5,
        barrier_right=0.5,
        barrier_height=5.0,
    )

    assert potential.shape == (
        grid.interior_size,
    )


def test_rectangular_barrier_height(
    grid: Grid1D,
) -> None:
    potential = rectangular_barrier_on_interior(
        grid=grid,
        barrier_left=-0.5,
        barrier_right=0.5,
        barrier_height=5.0,
    )

    assert np.max(
        potential
    ) == pytest.approx(
        5.0
    )

    assert np.min(
        potential
    ) == pytest.approx(
        0.0
    )


def test_rectangular_barrier_location(
    grid: Grid1D,
) -> None:
    potential = rectangular_barrier_on_interior(
        grid=grid,
        barrier_left=-0.5,
        barrier_right=0.5,
        barrier_height=5.0,
    )

    inside = (
        (grid.interior >= -0.5)
        & (grid.interior <= 0.5)
    )

    outside = ~inside

    assert np.all(
        potential[inside] == 5.0
    )

    assert np.all(
        potential[outside] == 0.0
    )


def test_initial_packet_is_left_of_barrier(
    grid: Grid1D,
    wavepacket: ArrayComplex,
) -> None:
    probabilities = scattering_probabilities(
        wavefunction=wavepacket,
        grid=grid,
        barrier_left=-0.5,
        barrier_right=0.5,
    )

    assert probabilities.left > 0.999

    assert probabilities.barrier < 1e-8

    assert probabilities.right < 1e-8


def test_scattering_probabilities_sum_to_norm(
    grid: Grid1D,
    wavepacket: ArrayComplex,
) -> None:
    probabilities = scattering_probabilities(
        wavefunction=wavepacket,
        grid=grid,
        barrier_left=-0.5,
        barrier_right=0.5,
    )

    assert probabilities.total == pytest.approx(
        1.0,
        abs=1e-10,
    )


def test_region_probability_for_full_grid(
    grid: Grid1D,
    wavepacket: ArrayComplex,
) -> None:
    mask = np.ones(
        grid.size,
        dtype=np.bool_,
    )

    probability = region_probability(
        wavefunction=wavepacket,
        grid=grid,
        mask=mask,
    )

    assert probability == pytest.approx(
        1.0,
        abs=1e-10,
    )


def test_zero_height_barrier_is_free_space(
    grid: Grid1D,
) -> None:
    potential = rectangular_barrier_on_interior(
        grid=grid,
        barrier_left=-0.5,
        barrier_right=0.5,
        barrier_height=0.0,
    )

    assert np.all(
        potential == 0.0
    )


def test_negative_barrier_height_rejected(
    grid: Grid1D,
) -> None:
    with pytest.raises(ValueError):
        rectangular_barrier_on_interior(
            grid=grid,
            barrier_left=-0.5,
            barrier_right=0.5,
            barrier_height=-1.0,
        )


def test_invalid_barrier_order_rejected(
    grid: Grid1D,
) -> None:
    with pytest.raises(ValueError):
        rectangular_barrier_on_interior(
            grid=grid,
            barrier_left=1.0,
            barrier_right=-1.0,
            barrier_height=5.0,
        )


def test_barrier_outside_grid_rejected(
    grid: Grid1D,
) -> None:
    with pytest.raises(ValueError):
        rectangular_barrier_on_interior(
            grid=grid,
            barrier_left=-40.0,
            barrier_right=0.5,
            barrier_height=5.0,
        )


def test_invalid_mask_size_rejected(
    grid: Grid1D,
    wavepacket: ArrayComplex,
) -> None:
    mask = np.ones(
        100,
        dtype=np.bool_,
    )

    with pytest.raises(ValueError):
        region_probability(
            wavefunction=wavepacket,
            grid=grid,
            mask=mask,
        )