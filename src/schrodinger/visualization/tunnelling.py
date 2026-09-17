import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from schrodinger.grid import Grid1D
from schrodinger.time_dependent.propagation import (
    PropagationSnapshot,
)
from schrodinger.time_dependent.scattering import (
    scattering_probabilities,
)


def plot_tunnelling_snapshots(
    grid: Grid1D,
    snapshots: list[PropagationSnapshot],
    barrier_left: float,
    barrier_right: float,
    barrier_height: float,
    title: str = "Quantum Wavepacket Tunnelling",
) -> Figure:
    if len(snapshots) == 0:
        raise ValueError(
            "snapshots must not be empty."
        )

    if not np.isfinite(barrier_height):
        raise ValueError(
            "barrier_height must be finite."
        )

    if barrier_height < 0.0:
        raise ValueError(
            "barrier_height must be non-negative."
        )

    figure, axis = plt.subplots(
        figsize=(11.0, 6.5)
    )

    maximum_density = 0.0

    for snapshot in snapshots:
        density = np.abs(
            snapshot.wavefunction
        ) ** 2

        maximum_density = max(
            maximum_density,
            float(np.max(density)),
        )

        axis.plot(
            grid.values,
            density,
            linewidth=1.8,
            label=f"t={snapshot.time:.2f}",
        )

    if maximum_density > 0.0:
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
            alpha=0.2,
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

    axis.set_xlabel(
        "Position x"
    )

    axis.set_ylabel(
        r"$|\psi(x,t)|^2$"
    )

    axis.set_title(
        title
    )

    axis.legend()

    axis.grid(
        alpha=0.2
    )

    figure.tight_layout()

    return figure


def plot_scattering_probabilities(
    grid: Grid1D,
    snapshots: list[PropagationSnapshot],
    barrier_left: float,
    barrier_right: float,
    title: str = "Scattering Probability Evolution",
) -> Figure:
    if len(snapshots) == 0:
        raise ValueError(
            "snapshots must not be empty."
        )

    times: list[float] = []
    left_probabilities: list[float] = []
    barrier_probabilities: list[float] = []
    right_probabilities: list[float] = []
    total_probabilities: list[float] = []

    for snapshot in snapshots:
        probabilities = (
            scattering_probabilities(
                wavefunction=snapshot.wavefunction,
                grid=grid,
                barrier_left=barrier_left,
                barrier_right=barrier_right,
            )
        )

        times.append(
            snapshot.time
        )

        left_probabilities.append(
            probabilities.left
        )

        barrier_probabilities.append(
            probabilities.barrier
        )

        right_probabilities.append(
            probabilities.right
        )

        total_probabilities.append(
            probabilities.total
        )

    figure, axis = plt.subplots(
        figsize=(10.0, 6.0)
    )

    axis.plot(
        times,
        left_probabilities,
        linewidth=2.0,
        label=r"$P_L(t)$",
    )

    axis.plot(
        times,
        barrier_probabilities,
        linewidth=2.0,
        label=r"$P_B(t)$",
    )

    axis.plot(
        times,
        right_probabilities,
        linewidth=2.0,
        label=r"$P_R(t)$",
    )

    axis.plot(
        times,
        total_probabilities,
        linewidth=1.2,
        linestyle="--",
        label="Total",
    )

    axis.set_xlabel(
        "Time"
    )

    axis.set_ylabel(
        "Probability"
    )

    axis.set_ylim(
        -0.02,
        1.05,
    )

    axis.set_title(
        title
    )

    axis.legend()

    axis.grid(
        alpha=0.2
    )

    figure.tight_layout()

    return figure