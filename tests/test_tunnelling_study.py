import numpy as np
import pytest

from schrodinger.analysis.tunnelling_study import (
    run_tunnelling_study,
)
from schrodinger.grid import Grid1D
from schrodinger.time_dependent.wavepacket import (
    gaussian_wavepacket,
)


def test_width_scan_reduces_transmission() -> None:
    grid = Grid1D(
        -25.0,
        25.0,
        2001,
    )

    wavefunction = gaussian_wavepacket(
        grid=grid,
        center=-8.0,
        sigma=1.5,
        wave_number=2.0,
    )

    widths = np.asarray(
        [
            0.5,
            1.0,
        ],
        dtype=np.float64,
    )

    heights = np.full(
        widths.shape,
        5.0,
        dtype=np.float64,
    )

    result = run_tunnelling_study(
        grid=grid,
        initial_wavefunction=wavefunction,
        barrier_heights=heights,
        barrier_widths=widths,
        dt=0.002,
        steps=4000,
        separation_tolerance=2e-2,
    )

    assert (
        result.tdse_transmissions[1]
        < result.tdse_transmissions[0]
    )

    assert (
        result.stationary_transmissions[1]
        < result.stationary_transmissions[0]
    )


def test_height_scan_reduces_transmission() -> None:
    grid = Grid1D(
        -25.0,
        25.0,
        2001,
    )

    wavefunction = gaussian_wavepacket(
        grid=grid,
        center=-8.0,
        sigma=1.5,
        wave_number=2.0,
    )

    heights = np.asarray(
        [
            4.0,
            6.0,
        ],
        dtype=np.float64,
    )

    widths = np.full(
        heights.shape,
        1.0,
        dtype=np.float64,
    )

    result = run_tunnelling_study(
        grid=grid,
        initial_wavefunction=wavefunction,
        barrier_heights=heights,
        barrier_widths=widths,
        dt=0.002,
        steps=4000,
        separation_tolerance=2e-2,
    )

    assert (
        result.tdse_transmissions[1]
        < result.tdse_transmissions[0]
    )

    assert (
        result.stationary_transmissions[1]
        < result.stationary_transmissions[0]
    )


def test_tunnelling_transmission_is_nonzero() -> None:
    grid = Grid1D(
        -25.0,
        25.0,
        2001,
    )

    wavefunction = gaussian_wavepacket(
        grid=grid,
        center=-8.0,
        sigma=1.5,
        wave_number=2.0,
    )

    result = run_tunnelling_study(
        grid=grid,
        initial_wavefunction=wavefunction,
        barrier_heights=np.asarray(
            [5.0],
            dtype=np.float64,
        ),
        barrier_widths=np.asarray(
            [1.0],
            dtype=np.float64,
        ),
        dt=0.002,
        steps=4000,
        separation_tolerance=2e-2,
    )

    assert (
        result.tdse_transmissions[0]
        > 0.0
    )

    assert (
        result.stationary_transmissions[0]
        > 0.0
    )


def test_probability_is_conserved() -> None:
    grid = Grid1D(
        -25.0,
        25.0,
        2001,
    )

    wavefunction = gaussian_wavepacket(
        grid=grid,
        center=-8.0,
        sigma=1.5,
        wave_number=2.0,
    )

    result = run_tunnelling_study(
        grid=grid,
        initial_wavefunction=wavefunction,
        barrier_heights=np.asarray(
            [5.0],
            dtype=np.float64,
        ),
        barrier_widths=np.asarray(
            [1.0],
            dtype=np.float64,
        ),
        dt=0.002,
        steps=4000,
        separation_tolerance=2e-2,
    )

    assert (
        result.total_probabilities[0]
        == pytest.approx(
            1.0,
            abs=1e-8,
        )
    )


def test_agreement_error_is_nonnegative() -> None:
    grid = Grid1D(
        -25.0,
        25.0,
        2001,
    )

    wavefunction = gaussian_wavepacket(
        grid=grid,
        center=-8.0,
        sigma=1.5,
        wave_number=2.0,
    )

    result = run_tunnelling_study(
        grid=grid,
        initial_wavefunction=wavefunction,
        barrier_heights=np.asarray(
            [5.0],
            dtype=np.float64,
        ),
        barrier_widths=np.asarray(
            [1.0],
            dtype=np.float64,
        ),
        dt=0.002,
        steps=4000,
        separation_tolerance=2e-2,
    )

    assert (
        result.agreement_errors[0]
        >= 0.0
    )


def test_mismatched_parameter_sizes_rejected() -> None:
    grid = Grid1D(
        -10.0,
        10.0,
        501,
    )

    wavefunction = gaussian_wavepacket(
        grid=grid,
        center=-5.0,
        sigma=1.0,
        wave_number=2.0,
    )

    with pytest.raises(ValueError):
        run_tunnelling_study(
            grid=grid,
            initial_wavefunction=wavefunction,
            barrier_heights=np.asarray(
                [
                    4.0,
                    5.0,
                ],
                dtype=np.float64,
            ),
            barrier_widths=np.asarray(
                [1.0],
                dtype=np.float64,
            ),
            dt=0.01,
            steps=10,
        )


def test_negative_barrier_height_rejected() -> None:
    grid = Grid1D(
        -10.0,
        10.0,
        501,
    )

    wavefunction = gaussian_wavepacket(
        grid=grid,
        center=-5.0,
        sigma=1.0,
        wave_number=2.0,
    )

    with pytest.raises(ValueError):
        run_tunnelling_study(
            grid=grid,
            initial_wavefunction=wavefunction,
            barrier_heights=np.asarray(
                [-1.0],
                dtype=np.float64,
            ),
            barrier_widths=np.asarray(
                [1.0],
                dtype=np.float64,
            ),
            dt=0.01,
            steps=10,
        )


def test_zero_barrier_width_rejected() -> None:
    grid = Grid1D(
        -10.0,
        10.0,
        501,
    )

    wavefunction = gaussian_wavepacket(
        grid=grid,
        center=-5.0,
        sigma=1.0,
        wave_number=2.0,
    )

    with pytest.raises(ValueError):
        run_tunnelling_study(
            grid=grid,
            initial_wavefunction=wavefunction,
            barrier_heights=np.asarray(
                [5.0],
                dtype=np.float64,
            ),
            barrier_widths=np.asarray(
                [0.0],
                dtype=np.float64,
            ),
            dt=0.01,
            steps=10,
        )