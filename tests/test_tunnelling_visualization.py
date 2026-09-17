import matplotlib
import matplotlib.pyplot as plt
import pytest

matplotlib.use("Agg")

from schrodinger.grid import Grid1D
from schrodinger.time_dependent.crank_nicolson import (
    CrankNicolsonPropagator,
)
from schrodinger.time_dependent.propagation import (
    propagate_with_snapshots,
)
from schrodinger.time_dependent.scattering import (
    rectangular_barrier_on_interior,
)
from schrodinger.time_dependent.wavepacket import (
    gaussian_wavepacket,
)
from schrodinger.visualization.tunnelling import (
    plot_scattering_probabilities,
    plot_tunnelling_snapshots,
)


@pytest.fixture
def simulation() -> tuple[
    Grid1D,
    list,
]:
    grid = Grid1D(
        -15.0,
        15.0,
        1001,
    )

    wavefunction = gaussian_wavepacket(
        grid=grid,
        center=-6.0,
        sigma=1.5,
        wave_number=2.0,
    )

    potential = rectangular_barrier_on_interior(
        grid=grid,
        barrier_left=-0.5,
        barrier_right=0.5,
        barrier_height=5.0,
    )

    propagator = CrankNicolsonPropagator(
        grid=grid,
        potential=potential,
        dt=0.002,
    )

    snapshots = propagate_with_snapshots(
        propagator=propagator,
        wavefunction=wavefunction,
        steps=500,
        snapshot_interval=250,
    )

    return grid, snapshots


def test_tunnelling_snapshot_plot_created(
    simulation: tuple[
        Grid1D,
        list,
    ],
) -> None:
    grid, snapshots = simulation

    figure = plot_tunnelling_snapshots(
        grid=grid,
        snapshots=snapshots,
        barrier_left=-0.5,
        barrier_right=0.5,
        barrier_height=5.0,
    )

    assert len(
        figure.axes
    ) == 1

    plt.close(
        figure
    )


def test_scattering_probability_plot_created(
    simulation: tuple[
        Grid1D,
        list,
    ],
) -> None:
    grid, snapshots = simulation

    figure = plot_scattering_probabilities(
        grid=grid,
        snapshots=snapshots,
        barrier_left=-0.5,
        barrier_right=0.5,
    )

    assert len(
        figure.axes
    ) == 1

    plt.close(
        figure
    )


def test_empty_snapshot_plot_rejected(
    simulation: tuple[
        Grid1D,
        list,
    ],
) -> None:
    grid, _ = simulation

    with pytest.raises(ValueError):
        plot_tunnelling_snapshots(
            grid=grid,
            snapshots=[],
            barrier_left=-0.5,
            barrier_right=0.5,
            barrier_height=5.0,
        )


def test_empty_probability_plot_rejected(
    simulation: tuple[
        Grid1D,
        list,
    ],
) -> None:
    grid, _ = simulation

    with pytest.raises(ValueError):
        plot_scattering_probabilities(
            grid=grid,
            snapshots=[],
            barrier_left=-0.5,
            barrier_right=0.5,
        )


def test_negative_barrier_height_rejected(
    simulation: tuple[
        Grid1D,
        list,
    ],
) -> None:
    grid, snapshots = simulation

    with pytest.raises(ValueError):
        plot_tunnelling_snapshots(
            grid=grid,
            snapshots=snapshots,
            barrier_left=-0.5,
            barrier_right=0.5,
            barrier_height=-1.0,
        )