from collections.abc import Iterable
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.artist import Artist
from matplotlib.figure import Figure

from schrodinger.grid import Grid1D
from schrodinger.time_dependent.propagation import (
    PropagationSnapshot,
)
from schrodinger.time_dependent.scattering import (
    scattering_probabilities,
)


def create_tunnelling_animation(
    grid: Grid1D,
    snapshots: list[PropagationSnapshot],
    barrier_left: float,
    barrier_right: float,
    barrier_height: float,
    interval: int = 50,
) -> tuple[Figure, FuncAnimation]:
    _validate_animation_inputs(
        snapshots=snapshots,
        barrier_left=barrier_left,
        barrier_right=barrier_right,
        barrier_height=barrier_height,
        interval=interval,
    )

    maximum_density = max(
        float(
            np.max(
                np.abs(
                    snapshot.wavefunction
                )
                ** 2
            )
        )
        for snapshot in snapshots
    )

    y_max = (
        maximum_density
        * 1.2
    )

    figure, axis = plt.subplots(
        figsize=(11.0, 6.5)
    )

    density_line, = axis.plot(
        [],
        [],
        linewidth=2.0,
        label=r"$|\psi(x,t)|^2$",
    )

    barrier_display_height = (
        maximum_density
        * 0.9
    )

    axis.fill_between(
        [
            barrier_left,
            barrier_right,
        ],
        [
            0.0,
            0.0,
        ],
        [
            barrier_display_height,
            barrier_display_height,
        ],
        alpha=0.25,
        label=(
            f"Barrier V0="
            f"{barrier_height:.2f}"
        ),
    )

    axis.axvline(
        barrier_left,
        linestyle="--",
        linewidth=1.0,
        alpha=0.6,
    )

    axis.axvline(
        barrier_right,
        linestyle="--",
        linewidth=1.0,
        alpha=0.6,
    )

    time_text = axis.text(
        0.02,
        0.95,
        "",
        transform=axis.transAxes,
        va="top",
    )

    probability_text = axis.text(
        0.02,
        0.87,
        "",
        transform=axis.transAxes,
        va="top",
    )

    axis.set_xlim(
        grid.x_min,
        grid.x_max,
    )

    axis.set_ylim(
        0.0,
        y_max,
    )

    axis.set_xlabel(
        "Position x"
    )

    axis.set_ylabel(
        r"$|\psi(x,t)|^2$"
    )

    axis.set_title(
        "Quantum Tunnelling of a Gaussian Wavepacket"
    )

    axis.legend(
        loc="upper right"
    )

    axis.grid(
        alpha=0.2
    )

    figure.tight_layout()

    def initialize() -> Iterable[Artist]:
        density_line.set_data(
            [],
            [],
        )

        time_text.set_text(
            ""
        )

        probability_text.set_text(
            ""
        )

        return (
            density_line,
            time_text,
            probability_text,
        )

    def update(
        frame: int,
    ) -> Iterable[Artist]:
        snapshot = snapshots[
            frame
        ]

        density = (
            np.abs(
                snapshot.wavefunction
            )
            ** 2
        )

        density_line.set_data(
            grid.values,
            density,
        )

        probabilities = (
            scattering_probabilities(
                wavefunction=(
                    snapshot.wavefunction
                ),
                grid=grid,
                barrier_left=barrier_left,
                barrier_right=barrier_right,
            )
        )

        time_text.set_text(
            f"t = {snapshot.time:.3f}"
        )

        probability_text.set_text(
            
                f"PL = {probabilities.left:.3f}   "
                f"PB = {probabilities.barrier:.3f}   "
                f"PR = {probabilities.right:.3f}"
            
        )

        return (
            density_line,
            time_text,
            probability_text,
        )

    animation = FuncAnimation(
        figure,
        update,
        frames=len(
            snapshots
        ),
        init_func=initialize,
        interval=interval,
        blit=False,
        repeat=True,
    )

    return (
        figure,
        animation,
    )


def save_animation_gif(
    animation: FuncAnimation,
    path: str | Path,
    fps: int = 20,
    dpi: int = 120,
) -> None:
    if isinstance(
        fps,
        bool,
    ):
        raise TypeError(
            "fps must be an integer."
        )

    if not isinstance(
        fps,
        (int, np.integer),
    ):
        raise TypeError(
            "fps must be an integer."
        )

    if fps <= 0:
        raise ValueError(
            "fps must be positive."
        )

    if isinstance(
        dpi,
        bool,
    ):
        raise TypeError(
            "dpi must be an integer."
        )

    if not isinstance(
        dpi,
        (int, np.integer),
    ):
        raise TypeError(
            "dpi must be an integer."
        )

    if dpi <= 0:
        raise ValueError(
            "dpi must be positive."
        )

    output_path = Path(
        path
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    writer = PillowWriter(
        fps=int(
            fps
        )
    )

    animation.save(
        output_path,
        writer=writer,
        dpi=int(
            dpi
        ),
    )


def _validate_animation_inputs(
    snapshots: list[PropagationSnapshot],
    barrier_left: float,
    barrier_right: float,
    barrier_height: float,
    interval: int,
) -> None:
    if len(
        snapshots
    ) == 0:
        raise ValueError(
            "snapshots must not be empty."
        )

    if not np.isfinite(
        barrier_left
    ):
        raise ValueError(
            "barrier_left must be finite."
        )

    if not np.isfinite(
        barrier_right
    ):
        raise ValueError(
            "barrier_right must be finite."
        )

    if (
        barrier_left
        >= barrier_right
    ):
        raise ValueError(
            "barrier_left must be smaller "
            "than barrier_right."
        )

    if not np.isfinite(
        barrier_height
    ):
        raise ValueError(
            "barrier_height must be finite."
        )

    if barrier_height < 0.0:
        raise ValueError(
            "barrier_height must be non-negative."
        )

    if isinstance(
        interval,
        bool,
    ):
        raise TypeError(
            "interval must be an integer."
        )

    if not isinstance(
        interval,
        (int, np.integer),
    ):
        raise TypeError(
            "interval must be an integer."
        )

    if interval <= 0:
        raise ValueError(
            "interval must be positive."
        )