import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pytest

matplotlib.use("Agg")

from schrodinger.visualization.tunnelling_analysis import (
    plot_log_transmission_vs_width,
    plot_transmission_comparison,
    plot_transmission_vs_height,
    plot_transmission_vs_width,
)


@pytest.fixture
def width_data() -> tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
]:
    widths = np.asarray(
        [
            0.5,
            0.75,
            1.0,
            1.25,
            1.5,
        ],
        dtype=np.float64,
    )

    tdse = np.asarray(
        [
            0.20,
            0.12,
            0.07,
            0.04,
            0.02,
        ],
        dtype=np.float64,
    )

    stationary = np.asarray(
        [
            0.19,
            0.11,
            0.065,
            0.037,
            0.018,
        ],
        dtype=np.float64,
    )

    return (
        widths,
        tdse,
        stationary,
    )


def test_width_plot_created(
    width_data: tuple[
        np.ndarray,
        np.ndarray,
        np.ndarray,
    ],
) -> None:
    widths, tdse, stationary = width_data

    figure = plot_transmission_vs_width(
        widths=widths,
        tdse_transmissions=tdse,
        stationary_transmissions=stationary,
    )

    assert len(
        figure.axes
    ) == 1

    plt.close(
        figure
    )


def test_height_plot_created(
    width_data: tuple[
        np.ndarray,
        np.ndarray,
        np.ndarray,
    ],
) -> None:
    heights, tdse, stationary = width_data

    figure = plot_transmission_vs_height(
        heights=heights,
        tdse_transmissions=tdse,
        stationary_transmissions=stationary,
    )

    assert len(
        figure.axes
    ) == 1

    plt.close(
        figure
    )


def test_comparison_plot_created(
    width_data: tuple[
        np.ndarray,
        np.ndarray,
        np.ndarray,
    ],
) -> None:
    _, tdse, stationary = width_data

    figure = plot_transmission_comparison(
        stationary_transmissions=stationary,
        tdse_transmissions=tdse,
    )

    assert len(
        figure.axes
    ) == 1

    plt.close(
        figure
    )


def test_log_width_plot_created(
    width_data: tuple[
        np.ndarray,
        np.ndarray,
        np.ndarray,
    ],
) -> None:
    widths, tdse, _ = width_data

    figure = plot_log_transmission_vs_width(
        widths=widths,
        transmissions=tdse,
    )

    assert len(
        figure.axes
    ) == 1

    plt.close(
        figure
    )


def test_mismatched_arrays_rejected() -> None:
    with pytest.raises(ValueError):
        plot_transmission_vs_width(
            widths=np.asarray(
                [
                    0.5,
                    1.0,
                ],
                dtype=np.float64,
            ),
            tdse_transmissions=np.asarray(
                [0.1],
                dtype=np.float64,
            ),
            stationary_transmissions=np.asarray(
                [
                    0.1,
                    0.05,
                ],
                dtype=np.float64,
            ),
        )


def test_negative_transmission_rejected() -> None:
    with pytest.raises(ValueError):
        plot_transmission_vs_width(
            widths=np.asarray(
                [1.0],
                dtype=np.float64,
            ),
            tdse_transmissions=np.asarray(
                [-0.1],
                dtype=np.float64,
            ),
            stationary_transmissions=np.asarray(
                [0.1],
                dtype=np.float64,
            ),
        )


def test_zero_transmission_rejected_for_log_plot() -> None:
    with pytest.raises(ValueError):
        plot_log_transmission_vs_width(
            widths=np.asarray(
                [
                    0.5,
                    1.0,
                ],
                dtype=np.float64,
            ),
            transmissions=np.asarray(
                [
                    0.1,
                    0.0,
                ],
                dtype=np.float64,
            ),
        )