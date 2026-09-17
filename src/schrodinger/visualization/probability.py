from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

from schrodinger.grid import Grid1D

ArrayFloat = NDArray[np.float64]
ArrayComplex = NDArray[np.complex128]
Wavefunction = ArrayFloat | ArrayComplex


def probability_density(
    wavefunction: Wavefunction,
) -> ArrayFloat:
    if wavefunction.ndim != 1:
        raise ValueError(
            "wavefunction must be one-dimensional."
        )

    if wavefunction.size == 0:
        raise ValueError(
            "wavefunction must not be empty."
        )

    if not np.all(
        np.isfinite(wavefunction)
    ):
        raise ValueError(
            "wavefunction values must be finite."
        )

    return np.asarray(
        np.abs(wavefunction) ** 2,
        dtype=np.float64,
    )


def plot_probability_density(
    grid: Grid1D,
    wavefunction: Wavefunction,
    title: str = "Probability Density",
) -> Figure:
    if wavefunction.size != grid.size:
        raise ValueError(
            "wavefunction size must match grid size."
        )

    density = probability_density(
        wavefunction=wavefunction
    )

    figure, axis = plt.subplots(
        figsize=(9.0, 5.5)
    )

    axis.plot(
        grid.values,
        density,
        linewidth=2.0,
    )

    axis.set_xlabel(
        "Position x"
    )

    axis.set_ylabel(
        r"$|\psi(x)|^2$"
    )

    axis.set_title(
        title
    )

    axis.grid(
        alpha=0.25
    )

    figure.tight_layout()

    return figure


def save_figure(
    figure: Figure,
    path: str | Path,
    dpi: int = 200,
) -> None:
    if isinstance(dpi, bool):
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

    output_path = Path(path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    figure.savefig(
        output_path,
        dpi=int(dpi),
        bbox_inches="tight",
    )