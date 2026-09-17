import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

from schrodinger.grid import Grid1D
from schrodinger.stationary.states import (
    StationaryState,
)

ArrayFloat = NDArray[np.float64]


def plot_stationary_states(
    grid: Grid1D,
    potential: ArrayFloat,
    states: list[StationaryState],
    title: str = "Stationary Quantum States",
    wavefunction_scale: float = 0.5,
) -> Figure:
    if potential.ndim != 1:
        raise ValueError(
            "potential must be one-dimensional."
        )

    if potential.size != grid.size:
        raise ValueError(
            "potential size must match grid size."
        )

    if not np.all(
        np.isfinite(potential)
    ):
        raise ValueError(
            "potential values must be finite."
        )

    if len(states) == 0:
        raise ValueError(
            "states must not be empty."
        )

    if not np.isfinite(
        wavefunction_scale
    ):
        raise ValueError(
            "wavefunction_scale must be finite."
        )

    if wavefunction_scale <= 0.0:
        raise ValueError(
            "wavefunction_scale must be positive."
        )

    figure, axis = plt.subplots(
        figsize=(10.0, 6.5)
    )

    axis.plot(
        grid.values,
        potential,
        linewidth=2.0,
        label="V(x)",
    )

    for state in states:
        wavefunction = np.real(
            state.wavefunction
        )

        amplitude = float(
            np.max(
                np.abs(wavefunction)
            )
        )

        if amplitude == 0.0:
            scaled_wavefunction = wavefunction
        else:
            scaled_wavefunction = (
                wavefunction
                / amplitude
                * wavefunction_scale
            )

        shifted_wavefunction = (
            state.energy
            + scaled_wavefunction
        )

        axis.plot(
            grid.values,
            shifted_wavefunction,
            linewidth=1.5,
            label=(
                f"n={state.index + 1}, "
                f"E={state.energy:.4f}"
            ),
        )

        axis.axhline(
            state.energy,
            linewidth=0.8,
            linestyle="--",
            alpha=0.5,
        )

    axis.set_xlabel(
        "Position x"
    )

    axis.set_ylabel(
        "Energy / shifted wavefunction"
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