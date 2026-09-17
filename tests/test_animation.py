from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pytest

matplotlib.use("Agg")

from schrodinger.grid import Grid1D
from schrodinger.time_dependent.crank_nicolson import (
    CrankNicolsonPropagator,
)
from schrodinger.time_dependent.propagation import (
    PropagationSnapshot,
    propagate_with_snapshots,
)
from schrodinger.time_dependent.scattering import (
    rectangular_barrier_on_interior,
)
from schrodinger.time_dependent.wavepacket import (
    gaussian_wavepacket,
)
from schrodinger.visualization.animation import (
    create_tunnelling_animation,
    save_animation_gif,
)


@pytest.fixture
def grid() -> Grid1D:
    return Grid1D(
        -15.0,
        15.0,
        1001,
    )


@pytest.fixture
def snapshots(
    grid: Grid1D,
) -> list[PropagationSnapshot]:
    wavefunction = gaussian_wavepacket(
        grid=grid,
        center=-5.0,
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

    return propagate_with_snapshots(
        propagator=propagator,
        wavefunction=wavefunction,
        steps=20,
        snapshot_interval=5,
    )


def test_animation_created(
    grid: Grid1D,
    snapshots: list[PropagationSnapshot],
) -> None:
    figure, animation = (
        create_tunnelling_animation(
            grid=grid,
            snapshots=snapshots,
            barrier_left=-0.5,
            barrier_right=0.5,
            barrier_height=5.0,
        )
    )

    assert animation is not None

    assert len(
        figure.axes
    ) == 1

    plt.close(
        figure
    )


def test_animation_gif_saved(
    grid: Grid1D,
    snapshots: list[PropagationSnapshot],
    tmp_path: Path,
) -> None:
    figure, animation = (
        create_tunnelling_animation(
            grid=grid,
            snapshots=snapshots,
            barrier_left=-0.5,
            barrier_right=0.5,
            barrier_height=5.0,
        )
    )

    output = (
        tmp_path
        / "test_tunnelling.gif"
    )

    save_animation_gif(
        animation=animation,
        path=output,
        fps=10,
        dpi=80,
    )

    assert output.exists()

    assert output.stat().st_size > 0

    plt.close(
        figure
    )


def test_empty_snapshots_rejected(
    grid: Grid1D,
) -> None:
    with pytest.raises(
        ValueError,
        match="snapshots must not be empty",
    ):
        create_tunnelling_animation(
            grid=grid,
            snapshots=[],
            barrier_left=-0.5,
            barrier_right=0.5,
            barrier_height=5.0,
        )


def test_invalid_barrier_rejected(
    grid: Grid1D,
    snapshots: list[PropagationSnapshot],
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "barrier_left must be smaller "
            "than barrier_right"
        ),
    ):
        create_tunnelling_animation(
            grid=grid,
            snapshots=snapshots,
            barrier_left=1.0,
            barrier_right=-1.0,
            barrier_height=5.0,
        )


def test_negative_height_rejected(
    grid: Grid1D,
    snapshots: list[PropagationSnapshot],
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "barrier_height must be "
            "non-negative"
        ),
    ):
        create_tunnelling_animation(
            grid=grid,
            snapshots=snapshots,
            barrier_left=-0.5,
            barrier_right=0.5,
            barrier_height=-1.0,
        )


def test_invalid_interval_rejected(
    grid: Grid1D,
    snapshots: list[PropagationSnapshot],
) -> None:
    with pytest.raises(
        ValueError,
        match="interval must be positive",
    ):
        create_tunnelling_animation(
            grid=grid,
            snapshots=snapshots,
            barrier_left=-0.5,
            barrier_right=0.5,
            barrier_height=5.0,
            interval=0,
        )


def test_boolean_interval_rejected(
    grid: Grid1D,
    snapshots: list[PropagationSnapshot],
) -> None:
    with pytest.raises(
        TypeError,
        match="interval must be an integer",
    ):
        create_tunnelling_animation(
            grid=grid,
            snapshots=snapshots,
            barrier_left=-0.5,
            barrier_right=0.5,
            barrier_height=5.0,
            interval=True,
        )


def test_invalid_fps_rejected(
    grid: Grid1D,
    snapshots: list[PropagationSnapshot],
    tmp_path: Path,
) -> None:
    figure, animation = (
        create_tunnelling_animation(
            grid=grid,
            snapshots=snapshots,
            barrier_left=-0.5,
            barrier_right=0.5,
            barrier_height=5.0,
        )
    )

    try:
        with pytest.raises(
            ValueError,
            match="fps must be positive",
        ):
            save_animation_gif(
                animation=animation,
                path=(
                    tmp_path
                    / "invalid.gif"
                ),
                fps=0,
            )
    finally:
        plt.close(
            figure
        )


def test_boolean_fps_rejected(
    grid: Grid1D,
    snapshots: list[PropagationSnapshot],
    tmp_path: Path,
) -> None:
    figure, animation = (
        create_tunnelling_animation(
            grid=grid,
            snapshots=snapshots,
            barrier_left=-0.5,
            barrier_right=0.5,
            barrier_height=5.0,
        )
    )

    try:
        with pytest.raises(
            TypeError,
            match="fps must be an integer",
        ):
            save_animation_gif(
                animation=animation,
                path=(
                    tmp_path
                    / "invalid.gif"
                ),
                fps=True,
            )
    finally:
        plt.close(
            figure
        )


def test_invalid_dpi_rejected(
    grid: Grid1D,
    snapshots: list[PropagationSnapshot],
    tmp_path: Path,
) -> None:
    figure, animation = (
        create_tunnelling_animation(
            grid=grid,
            snapshots=snapshots,
            barrier_left=-0.5,
            barrier_right=0.5,
            barrier_height=5.0,
        )
    )

    try:
        with pytest.raises(
            ValueError,
            match="dpi must be positive",
        ):
            save_animation_gif(
                animation=animation,
                path=(
                    tmp_path
                    / "invalid.gif"
                ),
                dpi=0,
            )
    finally:
        plt.close(
            figure
        )


def test_boolean_dpi_rejected(
    grid: Grid1D,
    snapshots: list[PropagationSnapshot],
    tmp_path: Path,
) -> None:
    figure, animation = (
        create_tunnelling_animation(
            grid=grid,
            snapshots=snapshots,
            barrier_left=-0.5,
            barrier_right=0.5,
            barrier_height=5.0,
        )
    )

    try:
        with pytest.raises(
            TypeError,
            match="dpi must be an integer",
        ):
            save_animation_gif(
                animation=animation,
                path=(
                    tmp_path
                    / "invalid.gif"
                ),
                dpi=True,
            )
    finally:
        plt.close(
            figure
        )