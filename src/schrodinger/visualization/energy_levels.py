import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

ArrayFloat = NDArray[np.float64]


def plot_energy_levels(
    energies: ArrayFloat,
    title: str = "Quantum Energy Levels",
) -> Figure:
    if energies.ndim != 1:
        raise ValueError(
            "energies must be one-dimensional."
        )

    if energies.size == 0:
        raise ValueError(
            "energies must not be empty."
        )

    if not np.all(
        np.isfinite(energies)
    ):
        raise ValueError(
            "energies must be finite."
        )

    figure, axis = plt.subplots(
        figsize=(7.0, 6.0)
    )

    for index, energy in enumerate(
        energies
    ):
        axis.hlines(
            y=energy,
            xmin=0.0,
            xmax=1.0,
            linewidth=2.0,
        )

        axis.text(
            1.05,
            energy,
            (
                f"n={index + 1}  "
                f"E={energy:.6f}"
            ),
            va="center",
        )

    axis.set_xlim(
        -0.1,
        1.8,
    )

    axis.set_xticks(
        []
    )

    axis.set_ylabel(
        "Energy"
    )

    axis.set_title(
        title
    )

    axis.grid(
        axis="y",
        alpha=0.2,
    )

    figure.tight_layout()

    return figure