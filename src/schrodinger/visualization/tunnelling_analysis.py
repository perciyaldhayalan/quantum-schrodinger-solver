import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

ArrayFloat = NDArray[np.float64]


def plot_transmission_vs_width(
    widths: ArrayFloat,
    tdse_transmissions: ArrayFloat,
    stationary_transmissions: ArrayFloat,
    title: str = "Transmission vs Barrier Width",
) -> Figure:
    _validate_scan_data(
        parameters=widths,
        tdse_transmissions=tdse_transmissions,
        stationary_transmissions=stationary_transmissions,
    )

    figure, axis = plt.subplots(
        figsize=(9.0, 5.8)
    )

    axis.plot(
        widths,
        tdse_transmissions,
        marker="o",
        linewidth=2.0,
        label="TDSE",
    )

    axis.plot(
        widths,
        stationary_transmissions,
        marker="s",
        linewidth=2.0,
        linestyle="--",
        label="Stationary prediction",
    )

    axis.set_xlabel(
        "Barrier width L"
    )

    axis.set_ylabel(
        "Transmission probability T"
    )

    axis.set_title(
        title
    )

    axis.set_ylim(
        bottom=0.0
    )

    axis.legend()

    axis.grid(
        alpha=0.25
    )

    figure.tight_layout()

    return figure


def plot_transmission_vs_height(
    heights: ArrayFloat,
    tdse_transmissions: ArrayFloat,
    stationary_transmissions: ArrayFloat,
    title: str = "Transmission vs Barrier Height",
) -> Figure:
    _validate_scan_data(
        parameters=heights,
        tdse_transmissions=tdse_transmissions,
        stationary_transmissions=stationary_transmissions,
    )

    figure, axis = plt.subplots(
        figsize=(9.0, 5.8)
    )

    axis.plot(
        heights,
        tdse_transmissions,
        marker="o",
        linewidth=2.0,
        label="TDSE",
    )

    axis.plot(
        heights,
        stationary_transmissions,
        marker="s",
        linewidth=2.0,
        linestyle="--",
        label="Stationary prediction",
    )

    axis.set_xlabel(
        "Barrier height V0"
    )

    axis.set_ylabel(
        "Transmission probability T"
    )

    axis.set_title(
        title
    )

    axis.set_ylim(
        bottom=0.0
    )

    axis.legend()

    axis.grid(
        alpha=0.25
    )

    figure.tight_layout()

    return figure


def plot_transmission_comparison(
    stationary_transmissions: ArrayFloat,
    tdse_transmissions: ArrayFloat,
    title: str = "TDSE vs Stationary Transmission",
) -> Figure:
    _validate_comparison_data(
        stationary_transmissions=stationary_transmissions,
        tdse_transmissions=tdse_transmissions,
    )

    minimum = float(
        min(
            np.min(stationary_transmissions),
            np.min(tdse_transmissions),
        )
    )

    maximum = float(
        max(
            np.max(stationary_transmissions),
            np.max(tdse_transmissions),
        )
    )

    padding = max(
        0.02 * (maximum - minimum),
        1e-4,
    )

    lower = max(
        0.0,
        minimum - padding,
    )

    upper = (
        maximum
        + padding
    )

    figure, axis = plt.subplots(
        figsize=(7.0, 6.5)
    )

    axis.scatter(
        stationary_transmissions,
        tdse_transmissions,
        s=55.0,
        label="Simulation points",
    )

    axis.plot(
        [
            lower,
            upper,
        ],
        [
            lower,
            upper,
        ],
        linestyle="--",
        linewidth=1.5,
        label="Perfect agreement",
    )

    axis.set_xlim(
        lower,
        upper,
    )

    axis.set_ylim(
        lower,
        upper,
    )

    axis.set_xlabel(
        "Stationary packet-averaged T"
    )

    axis.set_ylabel(
        "TDSE T"
    )

    axis.set_title(
        title
    )

    axis.legend()

    axis.grid(
        alpha=0.25
    )

    figure.tight_layout()

    return figure


def plot_log_transmission_vs_width(
    widths: ArrayFloat,
    transmissions: ArrayFloat,
    title: str = (
        "Exponential Suppression "
        "of Quantum Tunnelling"
    ),
) -> Figure:
    if widths.ndim != 1:
        raise ValueError(
            "widths must be one-dimensional."
        )

    if transmissions.ndim != 1:
        raise ValueError(
            "transmissions must be one-dimensional."
        )

    if widths.size == 0:
        raise ValueError(
            "widths must not be empty."
        )

    if widths.size != transmissions.size:
        raise ValueError(
            "widths and transmissions "
            "must have the same size."
        )

    if not np.all(
        np.isfinite(widths)
    ):
        raise ValueError(
            "widths must be finite."
        )

    if not np.all(
        np.isfinite(transmissions)
    ):
        raise ValueError(
            "transmissions must be finite."
        )

    if np.any(
        widths <= 0.0
    ):
        raise ValueError(
            "widths must be positive."
        )

    if np.any(
        transmissions <= 0.0
    ):
        raise ValueError(
            "transmissions must be positive "
            "for logarithmic plotting."
        )

    log_transmissions = np.log(
        transmissions
    )

    coefficients = np.polyfit(
        widths,
        log_transmissions,
        deg=1,
    )

    fitted_log_transmissions = np.polyval(
        coefficients,
        widths,
    )

    figure, axis = plt.subplots(
        figsize=(9.0, 5.8)
    )

    axis.plot(
        widths,
        log_transmissions,
        marker="o",
        linewidth=2.0,
        label=r"TDSE $\ln T$",
    )

    axis.plot(
        widths,
        fitted_log_transmissions,
        linestyle="--",
        linewidth=1.8,
        label=(
            "Linear fit: "
            f"slope={coefficients[0]:.3f}"
        ),
    )

    axis.set_xlabel(
        "Barrier width L"
    )

    axis.set_ylabel(
        r"$\ln T$"
    )

    axis.set_title(
        title
    )

    axis.legend()

    axis.grid(
        alpha=0.25
    )

    figure.tight_layout()

    return figure


def _validate_scan_data(
    parameters: ArrayFloat,
    tdse_transmissions: ArrayFloat,
    stationary_transmissions: ArrayFloat,
) -> None:
    if parameters.ndim != 1:
        raise ValueError(
            "parameters must be one-dimensional."
        )

    if tdse_transmissions.ndim != 1:
        raise ValueError(
            "tdse_transmissions must be "
            "one-dimensional."
        )

    if stationary_transmissions.ndim != 1:
        raise ValueError(
            "stationary_transmissions must be "
            "one-dimensional."
        )

    if parameters.size == 0:
        raise ValueError(
            "scan data must not be empty."
        )

    if (
        parameters.size
        != tdse_transmissions.size
        or parameters.size
        != stationary_transmissions.size
    ):
        raise ValueError(
            "all scan arrays must have "
            "the same size."
        )

    if not np.all(
        np.isfinite(parameters)
    ):
        raise ValueError(
            "parameters must be finite."
        )

    if not np.all(
        np.isfinite(tdse_transmissions)
    ):
        raise ValueError(
            "tdse_transmissions must be finite."
        )

    if not np.all(
        np.isfinite(stationary_transmissions)
    ):
        raise ValueError(
            "stationary_transmissions must be finite."
        )

    if np.any(
        tdse_transmissions < 0.0
    ) or np.any(
        tdse_transmissions > 1.0
    ):
        raise ValueError(
            "TDSE transmissions must lie "
            "between zero and one."
        )

    if np.any(
        stationary_transmissions < 0.0
    ) or np.any(
        stationary_transmissions > 1.0
    ):
        raise ValueError(
            "stationary transmissions must lie "
            "between zero and one."
        )


def _validate_comparison_data(
    stationary_transmissions: ArrayFloat,
    tdse_transmissions: ArrayFloat,
) -> None:
    dummy_parameters = np.arange(
        tdse_transmissions.size,
        dtype=np.float64,
    )

    _validate_scan_data(
        parameters=dummy_parameters,
        tdse_transmissions=tdse_transmissions,
        stationary_transmissions=stationary_transmissions,
    )