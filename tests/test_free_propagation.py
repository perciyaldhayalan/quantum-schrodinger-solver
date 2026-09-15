import numpy as np
import pytest
from numpy.typing import NDArray

from schrodinger.grid import Grid1D
from schrodinger.time_dependent.crank_nicolson import (
    CrankNicolsonPropagator,
)
from schrodinger.time_dependent.propagation import (
    free_particle_expected_momentum,
    free_particle_expected_position,
    free_particle_expected_width,
    propagate_with_snapshots,
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


@pytest.fixture
def propagator(
    grid: Grid1D,
) -> CrankNicolsonPropagator:
    potential = np.zeros(
        grid.interior_size,
        dtype=np.float64,
    )

    return CrankNicolsonPropagator(
        grid=grid,
        potential=potential,
        dt=0.001,
        mass=1.0,
        hbar=1.0,
    )


def test_expected_free_particle_position() -> None:
    result = free_particle_expected_position(
        initial_position=-10.0,
        wave_number=2.0,
        time=1.0,
        mass=1.0,
        hbar=1.0,
    )

    assert result == pytest.approx(
        -8.0
    )


def test_expected_free_particle_momentum() -> None:
    result = free_particle_expected_momentum(
        wave_number=2.0,
        hbar=1.0,
    )

    assert result == pytest.approx(
        2.0
    )


def test_expected_free_particle_width_at_zero_time() -> None:
    result = free_particle_expected_width(
        initial_sigma=1.5,
        time=0.0,
        mass=1.0,
        hbar=1.0,
    )

    assert result == pytest.approx(
        1.5
    )


def test_expected_free_particle_width_increases() -> None:
    initial = free_particle_expected_width(
        initial_sigma=1.5,
        time=0.0,
    )

    later = free_particle_expected_width(
        initial_sigma=1.5,
        time=1.0,
    )

    assert later > initial


def test_numerical_position_matches_analytic(
    propagator: CrankNicolsonPropagator,
    wavepacket: ArrayComplex,
) -> None:
    steps = 1000

    snapshots = propagate_with_snapshots(
        propagator=propagator,
        wavefunction=wavepacket,
        steps=steps,
        snapshot_interval=steps,
    )

    final = snapshots[-1]

    expected = free_particle_expected_position(
        initial_position=-10.0,
        wave_number=2.0,
        time=final.time,
        mass=1.0,
        hbar=1.0,
    )

    assert final.position == pytest.approx(
        expected,
        abs=2e-3,
    )


def test_numerical_momentum_is_conserved(
    propagator: CrankNicolsonPropagator,
    wavepacket: ArrayComplex,
) -> None:
    steps = 1000

    snapshots = propagate_with_snapshots(
        propagator=propagator,
        wavefunction=wavepacket,
        steps=steps,
        snapshot_interval=steps,
    )

    initial = snapshots[0]
    final = snapshots[-1]

    assert final.momentum == pytest.approx(
        initial.momentum,
        abs=1e-8,
    )


def test_numerical_width_matches_analytic(
    propagator: CrankNicolsonPropagator,
    wavepacket: ArrayComplex,
) -> None:
    steps = 1000

    snapshots = propagate_with_snapshots(
        propagator=propagator,
        wavefunction=wavepacket,
        steps=steps,
        snapshot_interval=steps,
    )

    final = snapshots[-1]

    expected = free_particle_expected_width(
        initial_sigma=1.5,
        time=final.time,
        mass=1.0,
        hbar=1.0,
    )

    assert (
        final.position_uncertainty
        == pytest.approx(
            expected,
            rel=2e-3,
        )
    )


def test_norm_remains_constant(
    propagator: CrankNicolsonPropagator,
    wavepacket: ArrayComplex,
) -> None:
    snapshots = propagate_with_snapshots(
        propagator=propagator,
        wavefunction=wavepacket,
        steps=1000,
        snapshot_interval=100,
    )

    norms = np.asarray(
        [
            snapshot.norm
            for snapshot in snapshots
        ],
        dtype=np.float64,
    )

    assert np.max(
        np.abs(
            norms - norms[0]
        )
    ) < 1e-9


def test_snapshot_times_are_correct(
    propagator: CrankNicolsonPropagator,
    wavepacket: ArrayComplex,
) -> None:
    snapshots = propagate_with_snapshots(
        propagator=propagator,
        wavefunction=wavepacket,
        steps=1000,
        snapshot_interval=250,
    )

    times = [
        snapshot.time
        for snapshot in snapshots
    ]

    assert times == pytest.approx(
        [
            0.0,
            0.25,
            0.50,
            0.75,
            1.00,
        ]
    )


def test_final_snapshot_included_for_non_divisible_interval(
    propagator: CrankNicolsonPropagator,
    wavepacket: ArrayComplex,
) -> None:
    snapshots = propagate_with_snapshots(
        propagator=propagator,
        wavefunction=wavepacket,
        steps=1050,
        snapshot_interval=250,
    )

    assert snapshots[-1].step == 1050

    assert snapshots[-1].time == pytest.approx(
        1.05
    )


def test_negative_time_rejected() -> None:
    with pytest.raises(ValueError):
        free_particle_expected_position(
            initial_position=0.0,
            wave_number=1.0,
            time=-1.0,
        )


def test_invalid_snapshot_interval_rejected(
    propagator: CrankNicolsonPropagator,
    wavepacket: ArrayComplex,
) -> None:
    with pytest.raises(ValueError):
        propagate_with_snapshots(
            propagator=propagator,
            wavefunction=wavepacket,
            steps=100,
            snapshot_interval=0,
        )